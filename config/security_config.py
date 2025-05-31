# config/security_config.py
"""
Security configuration and monitoring
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
import os

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    
    # File upload security
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_mime_types: List[str] = field(default_factory=lambda: [
        'text/csv', 'text/plain', 'application/csv'
    ])
    
    # Rate limiting
    upload_rate_limit: int = 10  # uploads per minute per IP
    processing_timeout: int = 300  # 5 minutes
    
    # Security monitoring
    enable_security_logging: bool = True
    alert_on_suspicious_patterns: bool = True
    quarantine_suspicious_files: bool = True
    
    # Content security
    max_pattern_checks: int = 1000  # Limit regex checks for performance
    suspicious_threshold: float = 0.1  # 10% suspicious content triggers alert
    
    # Audit settings
    log_all_uploads: bool = True
    log_file_hashes: bool = True
    retain_security_logs_days: int = 90

# utils/security_validator.py
"""
Security monitoring and alerting
"""

import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass

from utils.logging_config import get_logger

logger = get_logger(__name__)
security_logger = get_logger('security')

@dataclass
class SecurityEvent:
    """Security event data structure"""
    timestamp: datetime
    event_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    details: Dict[str, Any]
    source_ip: str = 'unknown'
    user_id: str = 'anonymous'

class SecurityMonitor:
    """Real-time security monitoring system"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.events = deque(maxlen=10000)  # Keep last 10k events
        self.rate_limits = defaultdict(lambda: deque(maxlen=100))
        self.suspicious_ips = set()
        self.lock = threading.Lock()
        
        # Alert thresholds
        self.alert_thresholds = {
            'failed_uploads_per_minute': 5,
            'suspicious_patterns_per_hour': 3,
            'large_files_per_hour': 10
        }
    
    def log_upload_attempt(self, filename: str, file_size: int, 
                          source_ip: str = 'unknown', 
                          validation_result: Dict[str, Any] = None):
        """Log file upload attempt"""
        
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type='file_upload',
            severity='low',
            details={
                'filename': filename,
                'file_size': file_size,
                'validation_result': validation_result
            },
            source_ip=source_ip
        )
        
        # Check for suspicious activity
        if validation_result and not validation_result.get('valid', False):
            event.severity = 'medium'
            errors = validation_result.get('errors', [])
            
            # Escalate severity for specific threats
            if any('suspicious pattern' in error.lower() for error in errors):
                event.severity = 'high'
                self._mark_suspicious_ip(source_ip)
            
        self._add_event(event)
        self._check_rate_limits(source_ip)
        
        # Log to security logger
        security_logger.info(
            f"Upload attempt: {filename}",
            extra={
                'file_size': file_size,
                'source_ip': source_ip,
                'severity': event.severity,
                'validation_result': validation_result
            }
        )
    
    def log_processing_error(self, filename: str, error: str, 
                           source_ip: str = 'unknown'):
        """Log data processing error"""
        
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type='processing_error',
            severity='medium',
            details={
                'filename': filename,
                'error': error
            },
            source_ip=source_ip
        )
        
        self._add_event(event)
        
        security_logger.warning(
            f"Processing error: {filename} - {error}",
            extra={'source_ip': source_ip}
        )
    
    def _add_event(self, event: SecurityEvent):
        """Add event to monitoring queue"""
        with self.lock:
            self.events.append(event)
            
        # Check for alert conditions
        self._check_alert_conditions()
    
    def _mark_suspicious_ip(self, ip: str):
        """Mark IP as suspicious"""
        with self.lock:
            self.suspicious_ips.add(ip)
        
        security_logger.warning(
            f"IP marked as suspicious: {ip}",
            extra={'suspicious_ip': ip}
        )
    
    def _check_rate_limits(self, source_ip: str):
        """Check if IP is exceeding rate limits"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old entries
        self.rate_limits[source_ip] = deque(
            [t for t in self.rate_limits[source_ip] if t > minute_ago],
            maxlen=100
        )
        
        # Add current request
        self.rate_limits[source_ip].append(now)
        
        # Check if rate limit exceeded
        if len(self.rate_limits[source_ip]) > self.config.upload_rate_limit:
            self._mark_suspicious_ip(source_ip)
            
            security_logger.warning(
                f"Rate limit exceeded for IP: {source_ip}",
                extra={
                    'source_ip': source_ip,
                    'requests_per_minute': len(self.rate_limits[source_ip])
                }
            )
    
    def _check_alert_conditions(self):
        """Check for conditions that should trigger alerts"""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)
        
        recent_events = [e for e in self.events if e.timestamp > hour_ago]
        
        # Count events by type
        event_counts = defaultdict(int)
        for event in recent_events:
            event_counts[event.event_type] += 1
            if event.severity in ['high', 'critical']:
                event_counts['high_severity'] += 1
        
        # Check thresholds and alert
        for alert_type, threshold in self.alert_thresholds.items():
            if event_counts.get(alert_type, 0) >= threshold:
                self._send_alert(alert_type, event_counts[alert_type], threshold)
    
    def _send_alert(self, alert_type: str, count: int, threshold: int):
        """Send security alert"""
        security_logger.critical(
            f"SECURITY ALERT: {alert_type}",
            extra={
                'alert_type': alert_type,
                'count': count,
                'threshold': threshold,
                'recent_events': len(self.events)
            }
        )
        
        # Here you could integrate with external alerting systems
        # like email, Slack, PagerDuty, etc.
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security monitoring summary"""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        recent_events = [e for e in self.events if e.timestamp > hour_ago]
        daily_events = [e for e in self.events if e.timestamp > day_ago]
        
        return {
            'timestamp': now.isoformat(),
            'events_last_hour': len(recent_events),
            'events_last_24h': len(daily_events),
            'suspicious_ips_count': len(self.suspicious_ips),
            'suspicious_ips': list(self.suspicious_ips),
            'recent_high_severity': len([e for e in recent_events if e.severity in ['high', 'critical']]),
            'event_types_summary': self._get_event_type_summary(daily_events),
            'status': self._get_overall_security_status(recent_events)
        }
    
    def _get_event_type_summary(self, events: List[SecurityEvent]) -> Dict[str, int]:
        """Get summary of event types"""
        summary = defaultdict(int)
        for event in events:
            summary[event.event_type] += 1
        return dict(summary)
    
    def _get_overall_security_status(self, recent_events: List[SecurityEvent]) -> str:
        """Determine overall security status"""
        if not recent_events:
            return 'normal'
        
        high_severity_count = len([e for e in recent_events if e.severity in ['high', 'critical']])
        
        if high_severity_count >= 3:
            return 'critical'
        elif high_severity_count >= 1:
            return 'elevated'
        elif len(recent_events) > 50:  # High activity
            return 'active'
        else:
            return 'normal'

# Global security monitor instance
from config.security_config import SecurityConfig
security_validator = SecurityMonitor(SecurityConfig())

# Integration with monitoring system
def setup_security_validatoring():
    """Setup security monitoring integration"""
    
    # Add security health check
    from utils.monitoring import health_checker
    
    def security_health_check():
        from utils.monitoring import HealthCheckResult
        
        summary = security_validator.get_security_summary()
        status = summary['status']
        
        if status == 'critical':
            return HealthCheckResult(
                name='security',
                status='unhealthy',
                message=f"Critical security status: {summary['recent_high_severity']} high-severity events",
                response_time_ms=0,
                timestamp=datetime.utcnow(),
                details=summary
            )
        elif status == 'elevated':
            return HealthCheckResult(
                name='security',
                status='degraded',
                message=f"Elevated security status: monitoring {summary['events_last_hour']} events",
                response_time_ms=0,
                timestamp=datetime.utcnow(),
                details=summary
            )
        else:
            return HealthCheckResult(
                name='security',
                status='healthy',
                message=f"Security status normal: {summary['events_last_hour']} events last hour",
                response_time_ms=0,
                timestamp=datetime.utcnow(),
                details=summary
            )
    
    health_checker.register_check('security', security_health_check)
    logger.info("Security monitoring health check registered")

# Export for use in other modules
__all__ = ['security_validator', 'SecurityMonitor', 'SecurityEvent', 'setup_security_validatoring']