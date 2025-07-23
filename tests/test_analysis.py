import pytest
from analysis import extract_number, clean_price #Import the two functions we want to test from your analysis.py module

#Tests if the extract_number() function correctly extracts numerical values from messy strings
def test_extract_number():
    assert extract_number("3 Bed") == 3.0 #checking if 3.0 is returned
    assert extract_number("2.5 Baths") == 2.5 #should return 2.5 as a float
    assert extract_number("Studio") is None #should return None
    assert extract_number(None) is None
    assert extract_number("No info") is None #no digit in string --> returns None

#Tests the clean_price() function to ensure it correctly cleans and converts price strings to float
#tests both valid inputs and invalid/missing data.
def test_clean_price():
    assert clean_price("€350,000") == 350000.0 #Checking if Euro sign is removed
    assert clean_price("AMV: 1400000") == 1400000.0 #Handles text to number
    assert clean_price("€1,200,000") == 1200000.0
    assert clean_price(None) is None #Return none for misisng input
    assert clean_price("No price") is None
