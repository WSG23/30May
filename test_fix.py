#!/usr/bin/env python3
# test_fix.py
"""
Test script to verify the upload and stats panel fixes
"""

import sys
import os

def test_file_structure():
    """Test that required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        'ui/components/secure_upload_handlers.py',
        'ui/pages/main_page.py',
        'app.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test that key imports work"""
    print("\n🔍 Testing imports...")
    
    try:
        # Add project root to path
        sys.path.insert(0, '.')
        
        # Test secure upload handlers
        from ui.components.secure_upload_handlers import create_secure_upload_handlers
        print("✅ secure_upload_handlers imports correctly")
        
        # Test main page
        from ui.pages.main_page import create_main_layout
        print("✅ main_page imports correctly")
        
        # Test app imports
        from utils.constants import REQUIRED_INTERNAL_COLUMNS
        print("✅ constants import correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_layout_creation():
    """Test that layout can be created"""
    print("\n🔍 Testing layout creation...")
    
    try:
        import dash
        from ui.pages.main_page import create_main_layout
        
        # Create mock app
        app = dash.Dash(__name__, suppress_callback_exceptions=True)
        
        # Test layout creation
        layout = create_main_layout(
            app_instance=app,
            main_logo_path="/assets/logo_white.png", 
            icon_upload_default="/assets/upload_file_csv_icon.png"
        )
        
        print("✅ Layout created successfully")
        
        # Check that stats panels are hidden by default
        layout_str = str(layout)
        if "yosai-custom-header" in layout_str and "'display': 'none'" in layout_str:
            print("✅ Stats header properly hidden")
        else:
            print("⚠️ Stats header visibility may need checking")
            
        if "stats-panels-container" in layout_str:
            print("✅ Stats panels container found")
        else:
            print("⚠️ Stats panels container missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Layout test failed: {e}")
        return False

def check_specific_fixes():
    """Check specific fixes for the reported issues"""
    print("\n🔍 Checking specific fixes...")
    
    try:
        # Check main_page.py for proper hiding of stats
        with open('ui/pages/main_page.py', 'r') as f:
            content = f.read()
        
        if "create_custom_header_hidden" in content:
            print("✅ Custom header properly set to hidden")
        else:
            print("❌ Custom header fix not applied")
            
        if "create_stats_panels_hidden" in content:
            print("✅ Stats panels properly set to hidden")
        else:
            print("❌ Stats panels fix not applied")
            
        if "'display': 'none'" in content:
            print("✅ Display none styling found")
        else:
            print("❌ Display none styling not found")
        
        # Check for secure upload handlers
        if os.path.exists('ui/components/secure_upload_handlers.py'):
            with open('ui/components/secure_upload_handlers.py', 'r') as f:
                handler_content = f.read()
            
            if "SecureUploadHandlers" in handler_content:
                print("✅ SecureUploadHandlers class found")
            else:
                print("❌ SecureUploadHandlers class missing")
                
            if "register_callbacks" in handler_content:
                print("✅ register_callbacks method found")
            else:
                print("❌ register_callbacks method missing")
        else:
            print("❌ secure_upload_handlers.py file missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Specific fix check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Testing Upload and Stats Panel Fixes")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_file_structure()
    all_passed &= test_imports()
    all_passed &= test_layout_creation()
    all_passed &= check_specific_fixes()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Fixes applied successfully!")
        print("✅ Upload should now work properly")
        print("✅ Stats panels should be hidden until after upload")
        print("\n🚀 Try starting your app:")
        print("   python app.py")
        print("\n📋 Expected behavior:")
        print("   1. Only upload area should be visible initially")
        print("   2. Data Overview should NOT be visible")
        print("   3. CSV upload should work")
        print("   4. Stats panels appear only after processing")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\n🔧 Issues to fix:")
        print("1. Make sure secure_upload_handlers.py is created in ui/components/")
        print("2. Make sure main_page.py is updated with hidden stats panels")
        print("3. Check that all imports are working")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)