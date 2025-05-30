# test_simplified_config.py
"""
Test the simplified configuration
"""

def test_simplified_config():
    print("Testing simplified configuration...")
    
    # Test 1: Import config package
    try:
        from config import get_settings, REQUIRED_INTERNAL_COLUMNS, DEFAULT_ICONS
        print("✅ config package import works")
        print(f"✅ REQUIRED_INTERNAL_COLUMNS: {REQUIRED_INTERNAL_COLUMNS}")
        print(f"✅ DEFAULT_ICONS: {list(DEFAULT_ICONS.keys())}")
    except Exception as e:
        print(f"❌ config package failed: {e}")
        return
    
    # Test 2: Get settings
    try:
        settings = get_settings()
        print("✅ get_settings() works")
        print(f"✅ settings.required_columns: {settings.required_columns}")
        print(f"✅ settings.ui.colors keys: {list(settings.ui.colors.keys())[:3]}...")
    except Exception as e:
        print(f"❌ get_settings() failed: {e}")
        return
    
    # Test 3: Import from constants
    try:
        from constants.constants import REQUIRED_INTERNAL_COLUMNS as CONST_COLUMNS
        print("✅ constants.constants import works")
        print(f"✅ Constants match: {CONST_COLUMNS == REQUIRED_INTERNAL_COLUMNS}")
    except Exception as e:
        print(f"❌ constants.constants failed: {e}")
        return
    
    # Test 4: Import mapping component
    try:
        from ui.components.mapping import create_mapping_component
        mapping_comp = create_mapping_component()
        print("✅ ui.components.mapping import works")
        print(f"✅ Mapping component created: {type(mapping_comp)}")
    except Exception as e:
        print(f"❌ ui.components.mapping failed: {e}")
        return
    
    print("\n🎉 All tests passed! Configuration is working.")

if __name__ == "__main__":
    test_simplified_config()