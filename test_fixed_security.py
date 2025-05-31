#!/usr/bin/env python3
# test_fixed_security.py
"""
Test script to verify all security fixes are working
"""

import sys
import os
import ast

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_syntax_validity():
    """Test that all Python files have valid syntax"""
    print("🔍 Testing Python syntax validity...")
    
    files_to_check = [
        'utils/secure_validator.py',
        'ui/components/secure_upload_handlers.py',
        'utils/security_monitor.py',
        'app.py'
    ]
    
    all_valid = True
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file to check syntax
            ast.parse(content)
            print(f"✅ {file_path} - syntax is valid")
            
        except SyntaxError as e:
            print(f"❌ {file_path} - syntax error at line {e.lineno}: {e.msg}")
            if e.text:
                print(f"   Problem line: {e.text.strip()}")
            all_valid = False
        except Exception as e:
            print(f"❌ {file_path} - error: {e}")
            all_valid = False
    
    return all_valid

def test_imports():
    """Test that all modules can be imported"""
    print("\n🔍 Testing module imports...")
    
    tests = [
        ('utils.secure_validator', 'SecureFileValidator'),
        ('ui.components.secure_upload_handlers', 'create_secure_upload_handlers'),
        ('utils.security_monitor', 'security_monitor'),
        ('utils.constants', 'FILE_LIMITS'),
        ('utils.logging_config', 'get_logger'),
    ]
    
    all_passed = True
    
    for module_name, item_name in tests:
        try:
            module = __import__(module_name, fromlist=[item_name])
            getattr(module, item_name)
            print(f"✅ {module_name}.{item_name} imports successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {e}")
            all_passed = False
        except AttributeError as e:
            print(f"❌ {module_name} missing {item_name}: {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ Error with {module_name}.{item_name}: {e}")
            all_passed = False
    
    return all_passed

def test_security_validator():
    """Test SecureFileValidator functionality"""
    print("\n🔍 Testing SecureFileValidator...")
    
    try:
        from utils.secure_validator import SecureFileValidator
        
        validator = SecureFileValidator()
        print("✅ SecureFileValidator instantiated successfully")
        
        # Test with valid CSV
        valid_csv = b"Name,Age,Department\nJohn,25,IT\nJane,30,HR"
        result = validator.validate_upload(valid_csv, "test.csv")
        
        if result['valid']:
            print("✅ Valid CSV validation passed")
            print(f"   File info: {result['file_info']}")
        else:
            print(f"❌ Valid CSV validation failed: {result['errors']}")
            return False
        
        # Test malicious content detection
        malicious_csv = b"Name,Script\nJohn,<script>alert('xss')</script>"
        result = validator.validate_upload(malicious_csv, "malicious.csv")
        
        if not result['valid']:
            print("✅ Malicious content correctly detected")
            print(f"   Threats: {result['errors']}")
        else:
            print("❌ Failed to detect malicious content!")
            return False
        
        # Test file extension validation
        result = validator.validate_upload(valid_csv, "test.txt")
        if not result['valid']:
            print("✅ File extension validation working")
        else:
            print("❌ File extension validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ SecureFileValidator test failed: {e}")
        return False

def test_security_monitor():
    """Test SecurityMonitor functionality"""
    print("\n🔍 Testing SecurityMonitor...")
    
    try:
        from utils.security_monitor import security_monitor
        
        # Test logging upload attempt
        security_monitor.log_upload_attempt(
            filename="test.csv",
            file_size=1024,
            source_ip="127.0.0.1",
            validation_result={'valid': True}
        )
        print("✅ SecurityMonitor.log_upload_attempt works")
        
        # Test getting security summary
        summary = security_monitor.get_security_summary()
        if isinstance(summary, dict) and 'timestamp' in summary:
            print("✅ SecurityMonitor.get_security_summary works")
            print(f"   Events last hour: {summary['events_last_hour']}")
        else:
            print("❌ SecurityMonitor.get_security_summary failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ SecurityMonitor test failed: {e}")
        return False

def test_upload_handlers():
    """Test SecureUploadHandlers can be created"""
    print("\n🔍 Testing SecureUploadHandlers...")
    
    try:
        from ui.components.secure_upload_handlers import create_secure_upload_handlers
        
        # Create mock objects
        class MockApp:
            def callback(self, *args, **kwargs):
                def decorator(func):
                    return func
                return decorator
        
        mock_app = MockApp()
        mock_component = {}
        mock_icons = {
            'default': 'icon1',
            'success': 'icon2',
            'fail': 'icon3'
        }
        
        handlers = create_secure_upload_handlers(mock_app, mock_component, mock_icons)
        print("✅ SecureUploadHandlers created successfully")
        
        # Test that it has the register_callbacks method
        if hasattr(handlers, 'register_callbacks'):
            print("✅ SecureUploadHandlers.register_callbacks method exists")
        else:
            print("❌ SecureUploadHandlers missing register_callbacks method")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ SecureUploadHandlers test failed: {e}")
        return False

def test_app_imports():
    """Test that app.py can import all dependencies"""
    print("\n🔍 Testing app.py imports...")
    
    try:
        # Test key imports from app.py
        from ui.components.upload import create_enhanced_upload_component
        print("✅ create_enhanced_upload_component imports")
        
        from ui.components.secure_upload_handlers import create_secure_upload_handlers
        print("✅ create_secure_upload_handlers imports")
        
        from utils.constants import DEFAULT_ICONS
        print("✅ DEFAULT_ICONS imports")
        
        from utils.logging_config import setup_application_logging, get_logger
        print("✅ Logging config imports")
        
        return True
        
    except Exception as e:
        print(f"❌ App imports test failed: {e}")
        return False

def create_test_files():
    """Create test CSV files for manual testing"""
    print("\n📁 Creating test files...")
    
    # Valid CSV file
    valid_csv = """Timestamp,UserID,DoorID,EventType
2024-01-15 09:00:00,USER001,MAIN_ENTRANCE,ACCESS GRANTED
2024-01-15 09:01:00,USER001,SECURE_AREA_1,ACCESS GRANTED
2024-01-15 09:02:00,USER002,MAIN_ENTRANCE,ACCESS GRANTED"""
    
    with open("test_valid_data.csv", "w", encoding='utf-8') as f:
        f.write(valid_csv)
    print("✅ Created test_valid_data.csv")
    
    # CSV with suspicious content
    suspicious_csv = """Timestamp,UserID,DoorID,EventType
2024-01-15 09:00:00,USER001,MAIN_ENTRANCE,ACCESS GRANTED
2024-01-15 09:01:00,HACKER,SECURE_AREA,<script>alert('xss')</script>
2024-01-15 09:02:00,USER002,MAIN_ENTRANCE,ACCESS GRANTED"""
    
    with open("test_malicious_data.csv", "w", encoding='utf-8') as f:
        f.write(suspicious_csv)
    print("✅ Created test_malicious_data.csv (should be blocked)")

def main():
    """Run all tests"""
    print("🔐 Testing Fixed Secure Upload System")
    print("=" * 50)
    
    all_passed = True
    
    # Core tests
    all_passed &= test_syntax_validity()
    all_passed &= test_imports()
    all_passed &= test_security_validator()
    all_passed &= test_security_monitor()
    all_passed &= test_upload_handlers()
    all_passed &= test_app_imports()
    
    # Create test files
    create_test_files()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Security system is working correctly!")
        print("\n📋 Next steps:")
        print("1. Start your app: python app.py")
        print("2. Test upload with test_valid_data.csv (should work)")
        print("3. Test upload with test_malicious_data.csv (should be blocked)")
        print("4. Check logs/ directory for security logs")
        print("\n🔐 Your secure upload system is ready!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\n🔧 Issues found:")
        print("1. Check the error messages above")
        print("2. Make sure all files are in correct locations")
        print("3. Verify all imports are working")
        print("4. Fix any syntax errors")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)