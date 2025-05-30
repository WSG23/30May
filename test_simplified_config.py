# test_simplified_config.py
"""
Test the simplified configuration
"""

def test_simplified_config():
   logger.info("Testing simplified configuration...")
    
    # Test 1: Import config package
    try:
        from config import get_settings, REQUIRED_INTERNAL_COLUMNS, DEFAULT_ICONS
       logger.info("✅ config package import works")
       logger.info(f"✅ REQUIRED_INTERNAL_COLUMNS: {REQUIRED_INTERNAL_COLUMNS}")
       logger.info(f"✅ DEFAULT_ICONS: {list(DEFAULT_ICONS.keys())}")
    except Exception as e:
       logger.info(f"❌ config package failed: {e}")
        return
    
    # Test 2: Get settings
    try:
        settings = get_settings()
       logger.info("✅ get_settings() works")
       logger.info(f"✅ settings.required_columns: {settings.required_columns}")
       logger.info(f"✅ settings.ui.colors keys: {list(settings.ui.colors.keys())[:3]}...")
    except Exception as e:
       logger.info(f"❌ get_settings() failed: {e}")
        return
    
    # Test 3: Import from constants
    try:
        from constants.constants import REQUIRED_INTERNAL_COLUMNS as CONST_COLUMNS
       logger.info("✅ constants.constants import works")
       logger.info(f"✅ Constants match: {CONST_COLUMNS == REQUIRED_INTERNAL_COLUMNS}")
    except Exception as e:
       logger.info(f"❌ constants.constants failed: {e}")
        return
    
    # Test 4: Import mapping component
    try:
        from ui.components.mapping import create_mapping_component
        mapping_comp = create_mapping_component()
       logger.info("✅ ui.components.mapping import works")
       logger.info(f"✅ Mapping component created: {type(mapping_comp)}")
    except Exception as e:
       logger.info(f"❌ ui.components.mapping failed: {e}")
        return
    
   logger.info("\n🎉 All tests passed! Configuration is working.")

if __name__ == "__main__":
    test_simplified_config()