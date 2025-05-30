# test_actual.py - Test the actual directory structure
"""
Test imports for the ACTUAL directory structure
"""

def test_actual_imports():
    """Test all imports for actual structure"""
    
   logger.info("🧪 Testing imports for ACTUAL directory structure...")
   logger.info("📁 Constants should be in: utils/constants.py")
   logger.info("📁 Services should be in: services/")
   logger.info()
    
    # Test 1: Utils constants
    try:
        from utils.constants import REQUIRED_INTERNAL_COLUMNS, DEFAULT_ICONS, FILE_LIMITS
       logger.info('✅ utils.constants import works')
       logger.info(f'✅ Found {len(REQUIRED_INTERNAL_COLUMNS)} required columns')
       logger.info(f'✅ Found {len(DEFAULT_ICONS)} default icons')
    except ImportError as e:
       logger.info(f'❌ utils.constants import failed: {e}')
        return False
    
    # Test 2: Services - Onion model
    try:
        from services.onion_model import run_onion_model_processing
       logger.info('✅ services.onion_model import works')
    except ImportError as e:
       logger.info(f'❌ services.onion_model import failed: {e}')
       logger.info("   Check: import statement in services/onion_model.py")
        return False
    
    # Test 3: Services - Cytoscape prep
    try:
        from services.cytoscape_prep import prepare_cytoscape_elements
       logger.info('✅ services.cytoscape_prep import works')
    except ImportError as e:
       logger.info(f'❌ services.cytoscape_prep import failed: {e}')
        return False
    
    # Test 4: Services - File utils
    try:
        from services.file_utils import decode_uploaded_csv
       logger.info('✅ services.file_utils import works')
    except ImportError as e:
       logger.info(f'❌ services.file_utils import failed: {e}')
        return False
    
    # Test 5: UI Components
    try:
        from ui.components.upload import create_enhanced_upload_component
       logger.info('✅ ui.components.upload import works')
    except ImportError as e:
       logger.info(f'❌ ui.components.upload import failed: {e}')
        return False
    
    # Test 6: UI Components - Mapping
    try:
        from ui.components.mapping import create_mapping_component
       logger.info('✅ ui.components.mapping import works')
    except ImportError as e:
       logger.info(f'❌ ui.components.mapping import failed: {e}')
        return False
    
   logger.info()
   logger.info("🎉 ALL imports working for actual directory structure!")
   logger.info("✅ Ready to run: python app.py")
    return True

if __name__ == "__main__":
    success = test_actual_imports()
    if not success:
       logger.info("\n❌ Some imports failed.")
       logger.info("🔧 Run the import fix script first:")
       logger.info("   chmod +x fix_imports_actual.sh")
       logger.info("   ./fix_imports_actual.sh")
        exit(1)
    else:
       logger.info("\n🚀 All good! Try running your app now.")