import pytest
from analysis import extract_number, clean_price

def test_extract_number():
    assert extract_number("3 Bed") == 3.0
    assert extract_number("2.5 Baths") == 2.5
    assert extract_number("Studio") is None
    assert extract_number(None) is None
    assert extract_number("No info") is None

def test_clean_price():
    assert clean_price("€350,000") == 350000.0
    assert clean_price("AMV: 1400000") == 1400000.0
    assert clean_price("€1,200,000") == 1200000.0
    assert clean_price(None) is None
    assert clean_price("No price") is None
