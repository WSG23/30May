# quick_test.py
print("Testing imports...")

try:
    from config import REQUIRED_INTERNAL_COLUMNS
   logger.info("✅ Config import works")
   logger.info(f"Found {len(REQUIRED_INTERNAL_COLUMNS)} columns")
except Exception as e:
   logger.info(f"❌ Config failed: {e}")

try:
    from services.onion_model import run_onion_model_processing
   logger.info("✅ Onion model import works")
except Exception as e:
   logger.info(f"❌ Onion model failed: {e}")

try:
    from ui.components.upload import create_enhanced_upload_component
   logger.info("✅ Upload component works")
except Exception as e:
   logger.info(f"❌ Upload component failed: {e}")

print("Test complete!")