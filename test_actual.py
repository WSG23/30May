# test_actual.py - Test the actual directory structure
"""
Test imports for the ACTUAL directory structure
"""

def test_actual_imports():
    """Test all imports for actual structure"""
    
    print("🧪 Testing imports for ACTUAL directory structure...")
    print("📁 Constants should be in: utils/constants.py")
    print("📁 Services should be in: services/")
    print()
    
    # Test 1: Utils constants
    try:
        from utils.constants import REQUIRED_INTERNAL_COLUMNS, DEFAULT_ICONS, FILE_LIMITS
        print('✅ utils.constants import works')
        print(f'✅ Found {len(REQUIRED_INTERNAL_COLUMNS)} required columns')
        print(f'✅ Found {len(DEFAULT_ICONS)} default icons')
    except ImportError as e:
        print(f'❌ utils.constants import failed: {e}')
        return False
    
    # Test 2: Services - Onion model
    try:
        from services.onion_model import run_onion_model_processing
        print('✅ services.onion_model import works')
    except ImportError as e:
        print(f'❌ services.onion_model import failed: {e}')
        print("   Check: import statement in services/onion_model.py")
        return False
    
    # Test 3: Services - Cytoscape prep
    try:
        from services.cytoscape_prep import prepare_cytoscape_elements
        print('✅ services.cytoscape_prep import works')
    except ImportError as e:
        print(f'❌ services.cytoscape_prep import failed: {e}')
        return False
    
    # Test 4: Services - File utils
    try:
        from services.file_utils import decode_uploaded_csv
        print('✅ services.file_utils import works')
    except ImportError as e:
        print(f'❌ services.file_utils import failed: {e}')
        return False
    
    # Test 5: UI Components
    try:
        from ui.components.upload import create_enhanced_upload_component
        print('✅ ui.components.upload import works')
    except ImportError as e:
        print(f'❌ ui.components.upload import failed: {e}')
        return False
    
    # Test 6: UI Components - Mapping
    try:
        from ui.components.mapping import create_mapping_component
        print('✅ ui.components.mapping import works')
    except ImportError as e:
        print(f'❌ ui.components.mapping import failed: {e}')
        return False
    
    print()
    print("🎉 ALL imports working for actual directory structure!")
    print("✅ Ready to run: python app.py")
    return True

if __name__ == "__main__":
    success = test_actual_imports()
    if not success:
        print("\n❌ Some imports failed.")
        print("🔧 Run the import fix script first:")
        print("   chmod +x fix_imports_actual.sh")
        print("   ./fix_imports_actual.sh")
        exit(1)
    else:
        print("\n🚀 All good! Try running your app now.")