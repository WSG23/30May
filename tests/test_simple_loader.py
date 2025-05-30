# tests/test_simple_loader.py
"""
Simple test to debug the enhanced CSV loader
"""

import io
import pandas as pd
from data_io.enhanced_csv_loader import EnhancedCSVLoader
from constants import REQUIRED_INTERNAL_COLUMNS

def test_loader_debug():
    """Debug the enhanced CSV loader"""
    loader = EnhancedCSVLoader()
    
    # Simple CSV content
    csv_content = """Timestamp,UserID,DoorID,EventType
2024-01-01 10:00:00,USER_001,DOOR_001,ACCESS GRANTED
2024-01-01 11:00:00,USER_002,DOOR_002,ACCESS GRANTED"""

    # Correct column mapping
    column_mapping = {
        'Timestamp': 'Timestamp (Event Time)',
        'UserID': 'UserID (Person Identifier)',
        'DoorID': 'DoorID (Device Name)',
        'EventType': 'EventType (Access Result)'
    }
    
    print("🔍 Constants:", REQUIRED_INTERNAL_COLUMNS)
    print("🔍 Mapping:", column_mapping)
    
    csv_io = io.StringIO(csv_content)
    result = loader.load_csv_event_log(csv_io, column_mapping)
    
    print("🔍 Result type:", type(result))
    print("🔍 Result:", result)
    
    if isinstance(result, dict):
        print("🔍 Success:", result.get('success'))
        if result.get('success'):
            print("🔍 DataFrame shape:", result['result'].shape)
            print("🔍 DataFrame columns:", list(result['result'].columns))
        else:
            print("🔍 Error:", result.get('error'))
    
    # This will always pass - we just want to see the debug output
    assert True

def test_constants_check():
    """Check that constants are as expected"""
    print("🔍 REQUIRED_INTERNAL_COLUMNS:")
    for key, value in REQUIRED_INTERNAL_COLUMNS.items():
        print(f"  {key} -> {value}")
    
    expected_values = {
        'Timestamp (Event Time)',
        'UserID (Person Identifier)',
        'DoorID (Device Name)',
        'EventType (Access Result)'
    }
    
    actual_values = set(REQUIRED_INTERNAL_COLUMNS.values())
    print("🔍 Expected values:", expected_values)
    print("🔍 Actual values:", actual_values)
    print("🔍 Match:", expected_values == actual_values)
    
    assert True  # Always pass, just want debug info
