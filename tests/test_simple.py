# tests/test_simple.py
def test_simple():
    """Basic test to verify pytest works"""
    assert 1 + 1 == 2

def test_fixtures_work(valid_column_mapping):
    """Test that our corrected fixtures work"""
    assert 'Timestamp' in valid_column_mapping
    assert valid_column_mapping['Timestamp'] == 'Timestamp (Event Time)'
    print("✅ Fixtures working correctly!")