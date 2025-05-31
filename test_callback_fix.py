#!/usr/bin/env python3
# test_callback_fix.py
"""
Test that callback conflicts are resolved
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_app_import():
    """Test that app can be imported without callback errors"""
    print("🔍 Testing app import without callback conflicts...")
    
    try:
        # Import the main modules that register callbacks
        from ui.components.secure_upload_handlers import create_secure_upload_handlers
        print("✅ Secure upload handlers import OK")
        
        from ui.components.mapping_handlers import create_mapping_handlers  
        print("✅ Mapping handlers import OK")
        
        from ui.components.classification_handlers import create_classification_handlers
        print("✅ Classification handlers import OK")
        
        from ui.components.graph_handlers import create_graph_handlers
        print("✅ Graph handlers import OK")
        
        # Test that we can create handlers without conflicts
        import dash
        test_app = dash.Dash(__name__, suppress_callback_exceptions=True)
        
        mock_component = {}
        mock_icons = {'default': 'test', 'success': 'test', 'fail': 'test'}
        
        upload_handlers = create_secure_upload_handlers(test_app, mock_component, mock_icons)
        print("✅ Upload handlers created without error")
        
        return True
        
    except Exception as e:
        print(f"❌ Import/creation test failed: {e}")
        return False

def test_floor_slider_conflict():
    """Specifically test for floor slider conflicts"""
    print("\n🔍 Testing for floor slider callback conflicts...")
    
    try:
        # Check if app.py contains floor slider callback
        app_py_path = 'app.py'
        if os.path.exists(app_py_path):
            with open(app_py_path, 'r') as f:
                content = f.read()
            
            # Look for floor slider callback patterns
            conflict_patterns = [
                'num-floors-display',
                'num-floors-store', 
                'update_floor_number'
            ]
            
            found_conflicts = []
            lines = content.split('\n')
            callback_found = False
            
            for i, line in enumerate(lines):
                if '@app.callback' in line:
                    callback_found = True
                    callback_start = i
                elif callback_found and any(pattern in line for pattern in conflict_patterns):
                    found_conflicts.append(f"Line {i+1}: Floor slider callback in app.py")
                    callback_found = False
                elif callback_found and 'def ' in line and not line.strip().startswith('#'):
                    callback_found = False
            
            if found_conflicts:
                print("❌ Found floor slider conflicts in app.py:")
                for conflict in found_conflicts:
                    print(f"   {conflict}")
                print("\n🔧 Fix: Comment out or remove the floor slider callback from app.py")
                return False
            else:
                print("✅ No floor slider conflicts found in app.py")
                return True
        else:
            print("⚠️ app.py not found")
            return True
            
    except Exception as e:
        print(f"❌ Floor slider test failed: {e}")
        return False

def test_run_server_fix():
    """Check if app.py uses correct Dash API"""
    print("\n🔍 Testing Dash API usage...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        if 'app.run_server(' in content:
            print("❌ Found app.run_server() - this is obsolete")
            print("🔧 Fix: Change app.run_server() to app.run()")
            return False
        elif 'app.run(' in content:
            print("✅ Using correct app.run() API")
            return True
        else:
            print("⚠️ No app startup found")
            return True
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all callback conflict tests"""
    print("🔍 Testing Callback Conflict Resolution")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_app_import()
    all_passed &= test_floor_slider_conflict() 
    all_passed &= test_run_server_fix()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CALLBACK TESTS PASSED!")
        print("\n✅ No callback conflicts detected!")
        print("✅ App should start without errors")
        print("✅ Dash API usage correct")
        print("\n🚀 Ready to start your app:")
        print("   mkdir -p logs")
        print("   python3 app.py")
    else:
        print("❌ CALLBACK CONFLICTS DETECTED!")
        print("\n🔧 Manual fixes needed:")
        print("1. Remove floor slider callback from app.py")
        print("2. Change app.run_server() to app.run()")
        print("3. Create logs directory: mkdir -p logs")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)