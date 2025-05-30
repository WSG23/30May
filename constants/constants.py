# yosai_intel_dashboard/constants.py
REQUIRED_INTERNAL_COLUMNS = {
    'Timestamp': 'Timestamp (Event Time)',
    'UserID': 'UserID (Person Identifier)',
    'DoorID': 'DoorID (Device Name)',
    'EventType': 'EventType (Access Result)'
}

# Debug print to verify constants
print(f"DEBUG: REQUIRED_INTERNAL_COLUMNS = {REQUIRED_INTERNAL_COLUMNS}")