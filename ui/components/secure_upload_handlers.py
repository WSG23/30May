# ui/components/secure_upload_handlers.py
"""
Secure upload handlers with comprehensive validation - FIXED UNBOUND VARIABLES
"""

import base64
import pandas as pd
import io
from typing import Dict, Any, Optional, Tuple, Union
from dash import callback, Input, Output, State, ctx

from utils.secure_validator import SecureFileValidator
from utils.validators import CSVValidator
from utils.logging_config import get_logger

# Initialize loggers at module level
logger = get_logger(__name__)
security_logger = get_logger('security')

# Import security monitor if available
try:
    from utils.security_monitor import security_monitor
    SECURITY_MONITOR_AVAILABLE = True
    logger.info("Security monitor available")
except ImportError:
    logger.warning("SecurityMonitor module not found. Upload attempts will not be monitored.")
    
    # Create a dummy security monitor to prevent errors
    class DummySecurityMonitor:
        def log_upload_attempt(self, 
                              filename: str, 
                              file_size: int, 
                              source_ip: str = 'unknown', 
                              validation_result: Optional[Dict[str, Any]] = None) -> None:
            logger.info(f"Security monitoring not available - logging upload: {filename}")
    
    security_monitor = DummySecurityMonitor()
    SECURITY_MONITOR_AVAILABLE = False


class SecureUploadHandlers:
    """Enhanced upload handlers with security validation"""

    def __init__(self, app, component, icons: Dict[str, str]):
        self.app = app
        self.component = component
        self.icons = icons
        self.secure_validator = SecureFileValidator()
        self.csv_validator = CSVValidator()

        logger.info("SecureUploadHandlers initialized with security validation")

    def register_callbacks(self) -> None:
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
        def handle_secure_upload(contents: Optional[str], 
                                filename: Optional[str]) -> Tuple[str, str, Optional[Dict[str, Any]], Dict[str, str], Dict[str, str]]:
            """Handle file upload with comprehensive security validation"""

            if contents is None or filename is None:
                return ("", self.icons['default'], None,
                       {'display': 'block'}, {'display': 'none'})

            # Get client IP (in production, this would come from request headers)
            client_ip = 'unknown'
            
            # Initialize variables to prevent unbound variable errors
            file_content: bytes = b''
            content_string: str = ''
            file_size: int = 0

            try:
                # Log security event
                security_logger.info(f"File upload attempt: {filename}")
                logger.info(f"Processing upload: {filename}")

                # Decode file content
                content_type, content_string = contents.split(',')
                file_content = base64.b64decode(content_string)
                file_size = len(file_content)

                logger.info(f"File decoded: {file_size} bytes")

                # Step 1: Secure validation
                security_result: Dict[str, Any] = self.secure_validator.validate_upload(
                    file_content, filename
                )

                # Log upload attempt with security monitor
                # Ensure we pass a proper dictionary, never None
                security_monitor.log_upload_attempt(
                    filename=filename,
                    file_size=file_size,
                    source_ip=client_ip,
                    validation_result=security_result  # Always a Dict, never None
                )

                if not security_result.get('valid', False):
                    error_msg = "🛡️ Security validation failed:\n" + "\n".join(
                        security_result.get('errors', ['Unknown security error'])
                    )
                    logger.warning(f"Security validation failed for {filename}: {security_result.get('errors', [])}")

                    # Log security incident
                    security_logger.warning(
                        "File upload blocked - security validation failed",
                        extra={
                            'filename': filename,
                            'errors': security_result.get('errors', []),
                            'file_size': file_size,
                            'source_ip': client_ip
                        }
                    )

                    return (
                        error_msg,
                        self.icons['fail'],
                        None,
                        {'display': 'block'},
                        {'display': 'none'}
                    )

                # Log warnings if any
                warnings = security_result.get('warnings', [])
                if warnings:
                    logger.info(f"Upload warnings for {filename}: {warnings}")

                # Step 2: Load and validate CSV structure
                csv_file = io.StringIO(file_content.decode('utf-8'))

                try:
                    df = pd.read_csv(csv_file, dtype=str)
                    self.csv_validator.validate_csv_structure(df)
                    logger.info(f"CSV structure validated: {df.shape}")
                except Exception as e:
                    error_msg = f"📊 CSV structure validation failed: {str(e)}"
                    logger.warning(f"CSV validation failed for {filename}: {str(e)}")
                    return (
                        error_msg,
                        self.icons['fail'],
                        None,
                        {'display': 'block'},
                        {'display': 'none'}
                    )

                # Step 3: Store validated data
                file_info = security_result.get('file_info', {})
                csv_store_data: Dict[str, Any] = {
                    'content': content_string,
                    'filename': filename,
                    'columns': df.columns.tolist(),
                    'shape': list(df.shape),  # Convert to list for JSON serialization
                    'file_info': file_info
                }

                # Success message with file info
                success_msg = (
                    f"✅ {filename} uploaded successfully!\n"
                    f"🛡️ Security validation: PASSED\n"
                    f"📊 {file_info.get('row_count', 0):,} rows, "
                    f"{file_info.get('column_count', 0)} columns\n"
                    f"📁 {file_info.get('size_bytes', 0):,} bytes\n"
                    f"🔒 Hash: {file_info.get('file_hash', 'N/A')}"
                )

                # Add warnings to success message if any
                if warnings:
                    success_msg += f"\n⚠️ Warnings: {'; '.join(warnings)}"

                # Log successful upload
                logger.info(f"File uploaded successfully: {filename}")
                security_logger.info(
                    "File upload successful",
                    extra={
                        'filename': filename,
                        'file_hash': file_info.get('file_hash', ''),
                        'row_count': file_info.get('row_count', 0),
                        'column_count': file_info.get('column_count', 0),
                        'size_bytes': file_info.get('size_bytes', 0),
                        'source_ip': client_ip
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
                error_msg = f"💥 Upload processing failed: {str(e)}"
                logger.error(f"Upload error for {filename}: {str(e)}")

                # Log security incident for unexpected errors with proper type
                # Use the file_size we calculated (or 0 if not calculated yet)
                error_validation_result: Dict[str, Any] = {
                    'valid': False,
                    'errors': [f'Processing error: {str(e)}'],
                    'warnings': [],
                    'file_info': {}
                }

                # Use the file_size variable which is always defined
                security_monitor.log_upload_attempt(
                    filename=filename,
                    file_size=file_size,  # This is always defined now
                    source_ip=client_ip,
                    validation_result=error_validation_result
                )

                # Log security incident for unexpected errors
                security_logger.error(
                    "Upload processing error",
                    extra={
                        'filename': filename,
                        'error': str(e),
                        'source_ip': client_ip,
                        'file_size': file_size
                    }
                )

                return (
                    error_msg,
                    self.icons['fail'],
                    None,
                    {'display': 'block'},
                    {'display': 'none'}
                )


def create_secure_upload_handlers(app, upload_component, icons: Dict[str, str]) -> SecureUploadHandlers:
    """Factory function to create secure upload handlers"""
    logger.info("Creating secure upload handlers")
    return SecureUploadHandlers(app, upload_component, icons)