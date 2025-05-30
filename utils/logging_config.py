# utils/logging_config.py
"""
Comprehensive logging configuration - FIXED VERSION
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import json
import traceback
from pathlib import Path

from config.app_config import get_config

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'process_id': os.getpid(),
            'thread_id': record.thread,
        }
        
        # Add exception information if present - FIXED with null checks
        if record.exc_info and record.exc_info[0] is not None:
            exc_type, exc_value, exc_traceback = record.exc_info
            log_entry['exception'] = {
                'type': exc_type.__name__ if exc_type else 'Unknown',
                'message': str(exc_value) if exc_value else 'No message',
                'traceback': traceback.format_exception(*record.exc_info) if all(record.exc_info) else []
            }
        
        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 
                          'processName', 'process', 'message', 'exc_info', 'exc_text', 'stack_info']:
                log_entry['extra'] = log_entry.get('extra', {})
                log_entry['extra'][key] = value
        
        return json.dumps(log_entry, default=str)

class ApplicationLogger:
    """Centralized application logging setup"""
    
    def __init__(self, app_name: str = "yosai_intel"):
        self.app_name = app_name
        try:
            self.config = get_config()
        except Exception:
            # Fallback configuration if config loading fails
            self.config = self._get_fallback_config()
        self.loggers: Dict[str, logging.Logger] = {}
    
    def _get_fallback_config(self):
        """Fallback configuration when main config fails"""
        class FallbackConfig:
            log_level = 'INFO'
            debug = False
            log_file = None
        
        return FallbackConfig()
        
    def setup_logging(self) -> None:
        """Setup comprehensive logging configuration"""
        try:
            # Create logs directory
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Configure root logger
            root_logger = logging.getLogger()
            
            # Safe log level setting
            try:
                log_level = getattr(logging, self.config.log_level.upper())
            except (AttributeError, ValueError):
                log_level = logging.INFO
            
            root_logger.setLevel(log_level)
            
            # Clear existing handlers
            root_logger.handlers.clear()
            
            # Console handler
            console_handler = self._create_console_handler()
            root_logger.addHandler(console_handler)
            
            # File handlers
            if getattr(self.config, 'log_file', None) or True:  # Always create file logs
                try:
                    file_handler = self._create_file_handler()
                    root_logger.addHandler(file_handler)
                    
                    error_handler = self._create_error_file_handler()
                    root_logger.addHandler(error_handler)
                except Exception as e:
                    # If file handlers fail, log to console
                    print(f"Warning: Could not create file handlers: {e}")
            
            # Performance logger
            self._setup_performance_logger()
            
            # Security logger
            self._setup_security_logger()
            
            # Application startup log
            logger = logging.getLogger(__name__)
            logger.info(f"Logging initialized for {self.app_name}")
            logger.info(f"Log level: {getattr(self.config, 'log_level', 'INFO')}")
            logger.info(f"Debug mode: {getattr(self.config, 'debug', False)}")
            
        except Exception as e:
            # Fallback to basic console logging
            print(f"Error setting up logging: {e}")
            logging.basicConfig(level=logging.INFO)
    
    def _create_console_handler(self) -> logging.Handler:
        """Create console handler with appropriate formatting"""
        handler = logging.StreamHandler(sys.stdout)
        
        debug_mode = getattr(self.config, 'debug', False)
        
        if debug_mode:
            # Detailed format for development
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
        else:
            # Simplified format for production
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
        
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO if not debug_mode else logging.DEBUG)
        
        return handler
    
    def _create_file_handler(self) -> logging.Handler:
        """Create rotating file handler for general logs"""
        filename = f"logs/{self.app_name}_{datetime.now().strftime('%Y%m%d')}.log"
        
        handler = logging.handlers.RotatingFileHandler(
            filename=filename,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        
        # Use JSON formatting for file logs
        handler.setFormatter(JSONFormatter())
        handler.setLevel(logging.DEBUG)
        
        return handler
    
    def _create_error_file_handler(self) -> logging.Handler:
        """Create separate handler for error logs"""
        filename = f"logs/{self.app_name}_errors_{datetime.now().strftime('%Y%m%d')}.log"
        
        handler = logging.handlers.RotatingFileHandler(
            filename=filename,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        
        handler.setFormatter(JSONFormatter())
        handler.setLevel(logging.ERROR)
        
        return handler
    
    def _setup_performance_logger(self) -> None:
        """Setup dedicated performance logger"""
        try:
            perf_logger = logging.getLogger('performance')
            perf_logger.setLevel(logging.INFO)
            
            # Performance log file
            perf_handler = logging.handlers.RotatingFileHandler(
                filename=f"logs/{self.app_name}_performance_{datetime.now().strftime('%Y%m%d')}.log",
                maxBytes=20 * 1024 * 1024,  # 20MB
                backupCount=5,
                encoding='utf-8'
            )
            
            perf_handler.setFormatter(JSONFormatter())
            perf_logger.addHandler(perf_handler)
            
            # Prevent propagation to root logger
            perf_logger.propagate = False
            
            self.loggers['performance'] = perf_logger
        except Exception as e:
            print(f"Warning: Could not setup performance logger: {e}")
    
    def _setup_security_logger(self) -> None:
        """Setup dedicated security logger"""
        try:
            sec_logger = logging.getLogger('security')
            sec_logger.setLevel(logging.INFO)
            
            # Security log file
            sec_handler = logging.handlers.RotatingFileHandler(
                filename=f"logs/{self.app_name}_security_{datetime.now().strftime('%Y%m%d')}.log",
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=10,
                encoding='utf-8'
            )
            
            sec_handler.setFormatter(JSONFormatter())
            sec_logger.addHandler(sec_handler)
            
            # Prevent propagation to root logger
            sec_logger.propagate = False
            
            self.loggers['security'] = sec_logger
        except Exception as e:
            print(f"Warning: Could not setup security logger: {e}")
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get logger instance"""
        return logging.getLogger(name)
    
    def get_performance_logger(self) -> logging.Logger:
        """Get performance logger"""
        return self.loggers.get('performance', logging.getLogger('performance'))
    
    def get_security_logger(self) -> logging.Logger:
        """Get security logger"""
        return self.loggers.get('security', logging.getLogger('security'))

# Global logger instance
app_logger = ApplicationLogger()

def setup_application_logging():
    """Setup application logging (call this at startup)"""
    app_logger.setup_logging()

def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return app_logger.get_logger(name)