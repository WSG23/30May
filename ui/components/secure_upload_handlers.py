# ui/components/secure_upload_handlers.py
"""
Secure upload handlers with comprehensive validation
"""

import base64
import pandas as pd
import io
from dash import callback, Input, Output, State, ctx # Assuming dash is used here

from utils.secure_validator import SecureFileValidator
from utils.validators import CSVValidator
from utils.logging_config import get_logger

# Initialize loggers at module level
logger = get_logger(__name__)
security_logger = get_logger('security')

# Define security_validator (assuming it's intended to be a separate module/class)
# If security_validator is meant to be part of SecureUploadHandlers, it needs to be an attribute.
# For now, I'm assuming it's an external utility or part of the logging setup.
# If you don't have a security_validator module, you'll need to create one or adjust this line.
try:
    from utils.security_validator import SecurityMonitor # Assuming this exists
    security_validator = SecurityMonitor()
except ImportError:
    logger.warning("SecurityMonitor module not found. Upload attempts will not be monitored.")
    class DummySecurityMonitor: # Create a dummy if it doesn't exist to prevent errors
        def log_upload_attempt(self, *args, **kwargs):
            pass
    security_validator = DummySecurityMonitor()


class SecureUploadHandlers:
    """Enhanced upload handlers with security validation"""

    def __init__(self, app, component, icons):
        self.app = app
        self.component = component
        self.icons = icons
        self.secure_validator = SecureFileValidator()
        self.csv_validator = CSVValidator()

        logger.info("SecureUploadHandlers initialized with security validation")

    def register_secure_callbacks(self):
        # <--- THIS LINE (THE DOCSTRING AND EVERYTHING AFTER IT)
        #      NEEDS TO BE INDENTED 4 SPACES FROM THE 'def' LINE.
        #      IT WAS LIKELY MISALIGNED IN THE PREVIOUS PASTE.
        """Enhanced callback registration with security monitoring"""

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
        def handle_secure_upload_with_monitoring(contents, filename):
            """Handle file upload with comprehensive security and monitoring"""

            if contents is None:
                return ("", self.icons['default'], None,
                       {'display': 'block'}, {'display': 'none'})

            # Get client IP (in production, this would come from request headers)
            # For testing, a placeholder or a way to pass it would be needed.
            client_ip = 'unknown'

            try:
                # Log security event for monitoring
                security_logger.info(f"Processing upload: {filename} from IP: {client_ip}")
                logger.info(f"Processing upload: {filename}")

                # Decode file content
                content_type, content_string = contents.split(',')
                file_content = base64.b64decode(content_string)

                logger.info(f"File decoded: {len(file_content)} bytes")

                # Log upload attempt for monitoring (moved here to ensure decoding happens first)
                security_validator.log_upload_attempt(
                    filename=filename,
                    file_size=len(file_content),
                    source_ip=client_ip,
                    # Note: validation_result will be added after security check
                )

                # Step 1: Secure validation
                security_result = self.secure_validator.validate_upload(
                    file_content, filename
                )

                # Update log with security result
                security_validator.log_upload_attempt(
                    filename=filename,
                    file_size=len(file_content),
                    source_ip=client_ip,
                    validation_result=security_result # Now includes validation result
                )


                if not security_result['valid']:
                    error_msg = f"🛡️ セキュリティ検証失敗:\n" + "\n".join(security_result['errors'])
                    logger.warning(f"Security validation failed for {filename}: {security_result['errors']}")

                    # Log security incident
                    security_logger.warning(
                        "ファイルアップロードブロック - セキュリティ検証失敗",
                        extra={
                            'filename': filename,
                            'errors': security_result['errors'],
                            'file_size': len(file_content),
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
                if security_result['warnings']:
                    logger.info(f"Upload warnings for {filename}: {security_result['warnings']}")

                # Step 2: Load and validate CSV structure
                csv_file = io.StringIO(file_content.decode('utf-8'))

                try:
                    df = pd.read_csv(csv_file, dtype=str)
                    self.csv_validator.validate_csv_structure(df)
                    logger.info(f"CSV structure validated: {df.shape}")
                except Exception as e:
                    error_msg = f"📊 CSV構造検証失敗: {str(e)}"
                    logger.warning(f"CSV validation failed for {filename}: {str(e)}")
                    return (
                        error_msg,
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
                    f"✅ {filename} アップロード成功！\n"
                    f"🛡️ セキュリティ検証: 成功\n"
                    f"📊 {file_info['row_count']:,} 行, "
                    f"{file_info['column_count']} 列\n"
                    f"📁 {file_info['size_bytes']:,} バイト\n"
                    f"🔒 ハッシュ: {file_info['file_hash']}"
                )

                # Add warnings to success message if any
                if security_result['warnings']:
                    success_msg += f"\n⚠️ 警告: {'; '.join(security_result['warnings'])}"

                # Log successful upload
                logger.info(f"File uploaded successfully: {filename}")
                security_logger.info(
                    "ファイルアップロード成功",
                    extra={
                        'filename': filename,
                        'file_hash': file_info['file_hash'],
                        'row_count': file_info['row_count'],
                        'column_count': file_info['column_count'],
                        'size_bytes': file_info['size_bytes'],
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
                error_msg = f"💥 アップロード処理失敗: {str(e)}"
                logger.error(f"Upload error for {filename}: {str(e)}")

                # Log security incident for unexpected errors
                security_logger.error(
                    "アップロード処理エラー",
                    extra={
                        'filename': filename,
                        'error': str(e),
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

# Factory function for creating secure upload handlers
def create_secure_upload_handlers(app, upload_component, icons):
    """Factory function to create secure upload handlers"""
    logger.info("Creating secure upload handlers")
    return SecureUploadHandlers(app, upload_component, icons)