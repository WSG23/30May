#!/usr/bin/env python3
# test_security_installation.py
"""
Test script to verify secure file validator installation
"""

import sys
import os
import tempfile

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from utils.secure_validator import SecureFileValidator
        print("✅ SecureFileValidator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import SecureFileValidator: {e}")
        return False
    
    try:
        from ui.components.secure_upload_handlers import create_secure_upload_handlers
        print("✅ Secure upload handlers imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import secure upload handlers: {e}")
        return False
    
    try:
        from utils.constants import FILE_LIMITS
        print("✅ Constants imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import constants: {e}")
        return False
    
    try:
        from utils.logging_config import get_logger
        print("✅ Logging config imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import logging config: {e}")
        return False
    
    return True

def test_dependencies():
    """Test external dependencies"""
    print("\n🔍 Testing dependencies...")
    
    try:
        import pandas as pd
        print("✅ pandas available")
    except ImportError:
        print("❌ pandas not available")
        return False
    
    try:
        import magic
        print("✅ python-magic available")
    except ImportError:
        print("⚠️ python-magic not available (MIME detection disabled)")
    
    try:
        import hashlib
        print("✅ hashlib available")
    except ImportError:
        print("❌ hashlib not available")
        return False
    
    return True

def test_validator_functionality():
    """Test validator functionality"""
    print("\n🔍 Testing validator functionality...")
    
    try:
        from utils.secure_validator import SecureFileValidator
        validator = SecureFileValidator()
        print("✅ Validator initialized successfully")
        
        # Test with sample CSV data
        sample_csv = b"Name,Age,Department\nJohn,25,IT\nJane,30,HR"
        result = validator.validate_upload(sample_csv, "test.csv")
        
        if result['valid']:
            print("✅ Sample CSV validation passed")
            print(f"   File info: {result['file_info']}")
        else:
            print(f"❌ Sample CSV validation failed: {result['errors']}")
            return False
        
        # Test malicious content detection
        malicious_csv = b"Name,Script\nJohn,<script>alert('xss')</script>"
        result = validator.validate_upload(malicious_csv, "malicious.csv")
        
        if not result['valid']:
            print("✅ Malicious content correctly detected and blocked")
        else:
            print("❌ Failed to detect malicious content!")
            return False
        
        # Test file extension validation
        result = validator.validate_upload(sample_csv, "test.txt")
        if not result['valid']:
            print("✅ File extension validation working")
        else:
            print("❌ File extension validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Validator functionality test failed: {e}")
        return False

def test_app_integration():
    """Test app integration"""
    print("\n🔍 Testing app integration...")
    
    try:
        # Test that app can be imported
        import app
        print("✅ Main app module imported successfully")
        
        # Test that secure handlers can be created
        from ui.components.secure_upload_handlers import create_secure_upload_handlers
        from ui.components.upload import create_enhanced_upload_component
        
        # Mock components for testing
        class MockApp:
            def callback(self, *args, **kwargs):
                def decorator(func):
                    return func
                return decorator
        
        mock_app = MockApp()
        upload_component = create_enhanced_upload_component("icon1", "icon2", "icon3")
        
        handlers = create_secure_upload_handlers(mock_app, upload_component, {
            'default': 'icon1',
            'success': 'icon2', 
            'fail': 'icon3'
        })
        
        print("✅ Secure handlers created successfully")
        return True
        
    except Exception as e:
        print(f"❌ App integration test failed: {e}")
        return False

def create_test_files():
    """Create test CSV files for manual testing"""
    print("\n📁 Creating test files...")
    
    # Valid CSV file
    valid_csv = """Name,Age,Department,Access_Level
John Doe,25,IT,2
Jane Smith,30,HR,1
Bob Wilson,35,Finance,3
Alice Johnson,28,IT,2
Charlie Brown,45,Management,3"""
    
    with open("test_valid_data.csv", "w") as f:
        f.write(valid_csv)
    print("✅ Created test_valid_data.csv")
    
    # CSV with suspicious content (for testing detection)
    suspicious_csv = """Name,Age,Note
John,25,Normal user
Hacker,99,<script>alert('xss')</script>
Jane,30,Regular employee"""
    
    with open("test_suspicious_data.csv", "w") as f:
        f.write(suspicious_csv)
    print("✅ Created test_suspicious_data.csv (should be blocked)")
    
    # Large CSV file (for size testing)
    large_csv_lines = ["Name,Age,Department"] + [f"User{i},{20+i%50},Dept{i%5}" for i in range(1000)]
    large_csv = "\n".join(large_csv_lines)
    
    with open("test_large_data.csv", "w") as f:
        f.write(large_csv)
    print("✅ Created test_large_data.csv (1000 rows)")

def main():
    """Run all installation tests"""
    print("🔐 Yōsai Intel Security Installation Test")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_dependencies()
    all_passed &= test_validator_functionality()
    all_passed &= test_app_integration()
    
    # Create test files
    create_test_files()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Security installation successful!")
        print("\n📋 Next steps:")
        print("1. Start your app: python app.py")
        print("2. Test upload with test_valid_data.csv (should work)")
        print("3. Test upload with test_suspicious_data.csv (should be blocked)")
        print("4. Check logs/ directory for security logs")
        print("\n🔐 Your application now has enhanced security!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\n🔧 Please check the errors above and:")
        print("1. Make sure all files are in the correct locations")
        print("2. Install missing dependencies: pip install python-magic python-magic-bin")
        print("3. Check file paths and imports")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)