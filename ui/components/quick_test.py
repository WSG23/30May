# quick_test.py
print("Testing imports...")

try:
    from config import REQUIRED_INTERNAL_COLUMNS
    print("✅ Config import works")
    print(f"Found {len(REQUIRED_INTERNAL_COLUMNS)} columns")
except Exception as e:
    print(f"❌ Config failed: {e}")

try:
    from services.onion_model import run_onion_model_processing
    print("✅ Onion model import works")
except Exception as e:
    print(f"❌ Onion model failed: {e}")

try:
    from ui.components.upload import create_enhanced_upload_component
    print("✅ Upload component works")
except Exception as e:
    print(f"❌ Upload component failed: {e}")

print("Test complete!")