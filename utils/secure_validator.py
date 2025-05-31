# utils/secure_validator.py - Your existing code with minor improvements
"""
Secure file validation for uploads
"""

import pandas as pd
import hashlib
import tempfile
import os
from typing import Dict, List, Optional, Any
import re

from utils.constants import FILE_LIMITS  # Use your existing constants

class SecurityError(Exception):
    """Security-related validation error"""
    pass

class SecureFileValidator:
    """Secure file validation with comprehensive checks"""
    
    def __init__(self):
        self.max_file_size = FILE_LIMITS['max_file_size']
        self.max_rows = FILE_LIMITS['max_rows']
        self.allowed_extensions = FILE_LIMITS['allowed_extensions']
        
        # Try to import python-magic, fallback if not available
        try:
            import magic
            self.magic = magic.Magic(mime=True)
            self.magic_available = True
        except ImportError:
            self.magic = None
            self.magic_available = False
    
    def validate_upload(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Comprehensive file validation
        Returns validation result with details
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        try:
            # 1. File size validation
            if len(file_content) > self.max_file_size:
                result['errors'].append(
                    f"File too large: {len(file_content):,} bytes "
                    f"(max: {self.max_file_size:,})"
                )
                return result
            
            # 2. Extension validation
            if not any(filename.lower().endswith(ext) for ext in self.allowed_extensions):
                result['errors'].append(
                    f"Invalid file extension. Allowed: {', '.join(self.allowed_extensions)}"
                )
                return result
            
            # 3. MIME type validation (if python-magic is available)
            if self.magic_available and self.magic is not None:
                try:
                    detected_mime = self.magic.from_buffer(file_content)
                    allowed_mimes = ['text/csv', 'text/plain', 'application/csv']
                    if detected_mime not in allowed_mimes:
                        result['warnings'].append(
                            f"Detected MIME type: {detected_mime}. Expected CSV format."
                        )
                except Exception:
                    result['warnings'].append("Could not detect MIME type")
            
            # 4. Content structure validation
            csv_validation = self._validate_csv_structure(file_content)
            if not csv_validation['valid']:
                result['errors'].extend(csv_validation['errors'])
                return result
            
            # 5. Malicious pattern detection
            malware_check = self._check_malicious_patterns(file_content)
            if not malware_check['safe']:
                result['errors'].extend(malware_check['threats'])
                return result
            
            # Success
            result['valid'] = True
            result['file_info'] = {
                'size_bytes': len(file_content),
                'row_count': csv_validation.get('row_count', 0),
                'column_count': csv_validation.get('column_count', 0),
                'file_hash': hashlib.sha256(file_content).hexdigest()[:16]  # First 16 chars
            }
            
        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")
        
        return result
    
    def _validate_csv_structure(self, file_content: bytes) -> Dict[str, Any]:
        """Validate CSV file structure"""
        try:
            # Create temporary file for pandas
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            try:
                # Read CSV with limited preview (first 1000 rows)
                df_preview = pd.read_csv(tmp_file_path, nrows=1000, dtype=str)
                
                # Basic structure checks
                if df_preview.empty:
                    return {'valid': False, 'errors': ['CSV file is empty']}
                
                if len(df_preview.columns) == 0:
                    return {'valid': False, 'errors': ['CSV has no columns']}
                
                # Estimate total rows
                estimated_rows = self._estimate_csv_rows(tmp_file_path)
                if estimated_rows > self.max_rows:
                    return {
                        'valid': False, 
                        'errors': [f'Too many rows: ~{estimated_rows:,} (max: {self.max_rows:,})']
                    }
                
                return {
                    'valid': True,
                    'row_count': estimated_rows,
                    'column_count': len(df_preview.columns)
                }
                
            finally:
                # Clean up temp file
                try:
                    os.unlink(tmp_file_path)
                except OSError:
                    pass
                
        except Exception as e:
            return {'valid': False, 'errors': [f'CSV parsing error: {str(e)}']}
    
    def _estimate_csv_rows(self, file_path: str) -> int:
        """Estimate number of rows in CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Count lines in first chunk
                chunk_size = 1024 * 1024  # 1MB
                chunk = f.read(chunk_size)
                lines_in_chunk = chunk.count('\n')
                
                # Get file size
                f.seek(0, 2)  # Seek to end
                file_size = f.tell()
                
                if file_size <= chunk_size:
                    return max(lines_in_chunk - 1, 0)  # Subtract header
                
                # Estimate based on proportion
                estimated_lines = int((lines_in_chunk / chunk_size) * file_size)
                return max(estimated_lines - 1, 0)  # Subtract header
        except Exception:
            return 0
    
    def _check_malicious_patterns(self, file_content: bytes) -> Dict[str, Any]:
        """Check for malicious patterns in file content"""
        threats = []
        
        try:
            # Convert to string for pattern matching
            content_str = file_content.decode('utf-8', errors='ignore')
            
            # Check for suspicious patterns
            malicious_patterns = [
                r'<script[^>]*>',  # JavaScript
                r'javascript:',     # JavaScript URLs
                r'vbscript:',      # VBScript
                r'onload=',        # Event handlers
                r'onerror=',
                r'eval\(',         # Code execution
                r'exec\(',
                r'import\s+os',    # Python OS imports
                r'subprocess',
                r'__import__',
                r'<\?php',         # PHP tags
                r'<%.*%>',         # ASP/JSP tags
            ]
            
            for pattern in malicious_patterns:
                if re.search(pattern, content_str, re.IGNORECASE):
                    threats.append(f"Suspicious pattern detected: {pattern}")
            
            # Check for excessive special characters (potential binary data)
            if len(content_str) > 0:
                special_char_ratio = sum(1 for c in content_str if ord(c) < 32 and c not in '\r\n\t') / len(content_str)
                if special_char_ratio > 0.1:  # More than 10% special characters
                    threats.append("High ratio of special characters detected")
            
        except UnicodeDecodeError:
            threats.append("File contains invalid UTF-8 characters")
        
        return {
            'safe': len(threats) == 0,
            'threats': threats
        }


# Enhanced upload handler that integrates with your existing system
# ui/components/secure_upload_handlers.py

import base64
from dash import callback, Input, Output, State, ctx
from utils.secure_validator import SecureFileValidator
from utils.validators import CSVValidator
from services.csv_loader import load_csv_event_log
from utils.logging_config import get_logger

logger = get_logger(__name__)

class SecureUploadHandlers:
    """Enhanced upload handlers with security validation"""
    
    def __init__(self, app, component, icons):
        self.app = app
        self.component = component
        self.icons = icons
        self.secure_validator = SecureFileValidator()
        self.csv_validator = CSVValidator()
    
    def register_callbacks(self):
        """Register upload callbacks with security validation"""
        
        @self.app.callback(
            [
                Output('upload-status', 'children'),
                Output('upload-icon', 'src'),
                Output('csv-store', 'data'),
                Output('upload-section', 'style'),
                Output('mapping-section', 'style')
            ],
            [Input('upload-component', 'contents')],
            [State('upload-component', 'filename')]
        )
        def handle_secure_upload(contents, filename):
            """Handle file upload with comprehensive security validation"""
            
            if contents is None:
                return ("", self.icons['default'], None, 
                       {'display': 'block'}, {'display': 'none'})
            
            try:
                # Log security event
                security_logger = get_logger('security')
                security_logger.info(f"File upload attempt: {filename}")
                
                # Decode file content
                content_type, content_string = contents.split(',')
                file_content = base64.b64decode(content_string)
                
                # Step 1: Secure validation
                security_result = self.secure_validator.validate_upload(
                    file_content, filename
                )
                
                if not security_result['valid']:
                    error_msg = "Security validation failed:\n" + "\n".join(security_result['errors'])
                    logger.warning(f"Security validation failed for {filename}: {security_result['errors']}")
                    
                    # Log security incident
                    security_logger.warning(
                        "File upload blocked",
                        extra={
                            'filename': filename,
                            'errors': security_result['errors'],
                            'file_size': len(file_content)
                        }
                    )
                    
                    return (
                        f"❌ {error_msg}",
                        self.icons['fail'],
                        None,
                        {'display': 'block'},
                        {'display': 'none'}
                    )
                
                # Log warnings if any
                if security_result['warnings']:
                    logger.info(f"Upload warnings for {filename}: {security_result['warnings']}")
                
                # Step 2: Load and validate CSV structure
                import io
                csv_file = io.StringIO(file_content.decode('utf-8'))
                
                # Basic CSV validation using existing validator
                try:
                    df = pd.read_csv(csv_file, dtype=str)
                    self.csv_validator.validate_csv_structure(df)
                except Exception as e:
                    error_msg = f"CSV structure validation failed: {str(e)}"
                    logger.warning(f"CSV validation failed for {filename}: {str(e)}")
                    return (
                        f"❌ {error_msg}",
                        self.icons['fail'],
                        None,
                        {'display': 'block'},
                        {'display': 'none'}
                    )
                
                # Step 3: Store validated data
                csv_store_data = {
                    'content': content_string,
                    'filename': filename,
                    'columns': df.columns.tolist(),
                    'shape': df.shape,
                    'file_info': security_result['file_info']
                }
                
                # Success message with file info
                file_info = security_result['file_info']
                success_msg = (
                    f"✅ {filename} uploaded successfully!\n"
                    f"📊 {file_info['row_count']:,} rows, "
                    f"{file_info['column_count']} columns\n"
                    f"📁 {file_info['size_bytes']:,} bytes"
                )
                
                # Log successful upload
                logger.info(f"File uploaded successfully: {filename}")
                security_logger.info(
                    "File upload successful",
                    extra={
                        'filename': filename,
                        'file_hash': file_info['file_hash'],
                        'row_count': file_info['row_count'],
                        'column_count': file_info['column_count'],
                        'size_bytes': file_info['size_bytes']
                    }
                )
                
                return (
                    success_msg,
                    self.icons['success'],
                    csv_store_data,
                    {'display': 'none'},  # Hide upload section
                    {'display': 'block'}   # Show mapping section
                )
                
            except Exception as e:
                error_msg = f"Upload processing failed: {str(e)}"
                logger.error(f"Upload error for {filename}: {str(e)}")
                
                # Log security incident for unexpected errors
                security_logger.error(
                    "Upload processing error",
                    extra={
                        'filename': filename,
                        'error': str(e)
                    }
                )
                
                return (
                    f"❌ {error_msg}",
                    self.icons['fail'],
                    None,
                    {'display': 'block'},
                    {'display': 'none'}
                )


# Integration function for your existing app.py
def create_secure_upload_handlers(app, upload_component, icons):
    """Factory function to create secure upload handlers"""
    return SecureUploadHandlers(app, upload_component, icons)