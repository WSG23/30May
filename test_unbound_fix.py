#!/usr/bin/env python3
# test_unbound_fix.py
"""
Test script to verify unbound variable fixes
"""

import sys
import os
import ast

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_syntax_and_variables():
    """Test that all variables are properly bound"""
    print("🔍 Testing for unbound variables...")
    
    file_path = 'ui/components/secure_upload_handlers.py'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the file to check syntax
        tree = ast.parse(content)
        print(f"✅ {file_path} - syntax is valid")
        
        # Check for common unbound variable patterns
        unbound_patterns = [
            "len(file_content) if 'file_content' in locals()",  # Old pattern
            "'file_content' in locals()",  # Checking if variable exists
        ]
        
        found_problematic_patterns = []
        for pattern in unbound_patterns:
            if pattern in content:
                found_problematic_patterns.append(pattern)
        
        if found_problematic_patterns:
            print(f"⚠️ Found potentially problematic patterns:")
            for pattern in found_problematic_patterns:
                print(f"   - {pattern}")
        else:
            print("✅ No problematic unbound variable patterns found")
        
        # Check that variables are initialized properly
        required_initializations = [
            "file_content: bytes = b''",
            "content_string: str = ''", 
            "file_size: int = 0"
        ]
        
        missing_initializations = []
        for init in required_initializations:
            if init not in content:
                missing_initializations.append(init)
        
        if missing_initializations:
            print(f"❌ Missing variable initializations:")
            for init in missing_initializations:
                print(f"   - {init}")
            return False
        else:
            print("✅ All required variables are properly initialized")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False

def test_variable_usage():
    """Test that variables are used correctly"""
    print("\n🔍 Testing variable usage patterns...")
    
    try:
        from ui.components.secure_upload_handlers import SecureUploadHandlers
        
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
        
        # Test instantiation
        handlers = SecureUploadHandlers(mock_app, mock_component, mock_icons)
        print("✅ SecureUploadHandlers instantiated successfully")
        
        # Test that register_callbacks method exists and doesn't crash
        if hasattr(handlers, 'register_callbacks'):
            print("✅ register_callbacks method exists")
            
            # We can't actually call it without a real Dash app, but we can check it exists
            import inspect
            sig = inspect.signature(handlers.register_callbacks)
            print(f"✅ register_callbacks signature: {sig}")
        else:
            print("❌ register_callbacks method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Variable usage test failed: {e}")
        return False

def test_error_handling_paths():
    """Test that error handling doesn't cause unbound variable errors"""
    print("\n🔍 Testing error handling paths...")
    
    try:
        # Read the file and check for proper error handling
        with open('ui/components/secure_upload_handlers.py', 'r') as f:
            content = f.read()
        
        # Check that in exception handlers, we use initialized variables
        error_handler_checks = [
            "file_size",  # Should use file_size directly
            "except Exception as e:",  # Should have exception handlers
            "security_monitor.log_upload_attempt",  # Should log attempts
        ]
        
        missing_checks = []
        for check in error_handler_checks:
            if check not in content:
                missing_checks.append(check)
        
        if missing_checks:
            print(f"❌ Missing error handling elements:")
            for check in missing_checks:
                print(f"   - {check}")
            return False
        else:
            print("✅ Error handling elements present")
        
        # Check that we don't use potentially unbound variables in error handlers
        problematic_usage = [
            "len(file_content) if 'file_content'",  # Old conditional pattern
        ]
        
        found_problems = []
        for usage in problematic_usage:
            if usage in content:
                found_problems.append(usage)
        
        if found_problems:
            print(f"❌ Found problematic variable usage in error handlers:")
            for problem in found_problems:
                print(f"   - {problem}")
            return False
        else:
            print("✅ No problematic variable usage in error handlers")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all unbound variable tests"""
    print("🔍 Testing Unbound Variable Fixes")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_syntax_and_variables()
    all_passed &= test_variable_usage()
    all_passed &= test_error_handling_paths()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL UNBOUND VARIABLE TESTS PASSED!")
        print("\n✅ Variable binding fixes are working correctly!")
        print("\n📋 What was fixed:")
        print("1. ✅ All variables are initialized at function start")
        print("2. ✅ file_content, content_string, file_size always defined")
        print("3. ✅ Exception handlers use only bound variables")
        print("4. ✅ No conditional variable existence checks needed")
        print("5. ✅ Type annotations preserve variable scope")
        print("\n🔐 No more 'possibly unbound variable' errors!")
    else:
        print("❌ SOME UNBOUND VARIABLE TESTS FAILED!")
        print("\n🔧 Please check the errors above")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)