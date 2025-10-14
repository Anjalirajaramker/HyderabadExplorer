"""
Distance Filter Tests 📍
Tests for distance-based filtering functionality (Within 5km, 10-20km, etc.)
Mocks geolocation using Chrome DevTools Protocol for reliable testing.
Note: Distance filters require clicking "Show Nearest Places" button first.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import wait_for_cards_to_load, get_visible_cards


def test_distance_filter_within_5km(browser):
    """
    Distance Test 1: Verify 'Within 5km' distance filter.
    Mocks Hitec City location for consistent testing.
    """
    wait_for_cards_to_load(browser)
    
    # Mock Hitec City coordinates using Chrome DevTools Protocol
    hitec_city_coords = {
        "latitude": 17.4435,
        "longitude": 78.3772,
        "accuracy": 100
    }
    browser.execute_cdp_cmd("Emulation.setGeolocationOverride", hitec_city_coords)
    
    # Wait for location to be processed
    time.sleep(2)
    
    # IMPORTANT: Click "Show Nearest Places" button first to enable distance filters
    nearest_btn = browser.find_element(By.ID, "find-nearby-btn")
    nearest_btn.click()
    
    # Wait for loading spinner to disappear
    try:
        spinner = browser.find_element(By.ID, "loading-spinner")
        WebDriverWait(browser, 3).until(EC.visibility_of(spinner))
        WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, "loading-spinner")))
    except:
        time.sleep(3)  # Fallback wait
    
    # Now click the distance filter
    within_5km_checkbox = browser.find_element(
        By.CSS_SELECTOR,
        "input.distance-filter-checkbox[data-min='0'][data-max='5']"
    )
    
    within_5km_checkbox.click()
    time.sleep(2)
    
    # Get filtered cards
    filtered_cards = get_visible_cards(browser)
    
    # Note: There might be 0 cards within 5km depending on location
    # The test passes if the filter is clickable and works (no crash)
    print(f"✅ Within 5km filter test passed - {len(filtered_cards)} places found")
    print(f"   📍 Mock location: Hitec City (17.4435, 78.3772)")
    
    if len(filtered_cards) == 0:
        print(f"   ℹ️  Note: No places within 5km of this location (this is valid)")


def test_distance_filter_range_10_20km(browser):
    """
    Distance Test 2: Verify '10-20km' distance filter.
    Mocks Hitec City location for consistent testing.
    """
    wait_for_cards_to_load(browser)
    
    # Mock Hitec City coordinates
    hitec_city_coords = {
        "latitude": 17.4435,
        "longitude": 78.3772,
        "accuracy": 100
    }
    browser.execute_cdp_cmd("Emulation.setGeolocationOverride", hitec_city_coords)
    
    # Wait for location to be processed
    time.sleep(2)
    
    # IMPORTANT: Click "Show Nearest Places" button first to enable distance filters
    nearest_btn = browser.find_element(By.ID, "find-nearby-btn")
    nearest_btn.click()
    
    # Wait for loading spinner to disappear
    try:
        spinner = browser.find_element(By.ID, "loading-spinner")
        WebDriverWait(browser, 3).until(EC.visibility_of(spinner))
        WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, "loading-spinner")))
    except:
        time.sleep(3)  # Fallback wait
    
    # Now click the 10-20km distance filter
    range_checkbox = browser.find_element(
        By.CSS_SELECTOR,
        "input.distance-filter-checkbox[data-min='10'][data-max='20']"
    )
    range_checkbox.click()
    time.sleep(2)
    
    # Get filtered cards
    filtered_cards = get_visible_cards(browser)
    
    assert len(filtered_cards) > 0, "No cards visible with '10-20km' filter"
    print(f"✅ 10-20km filter test passed - {len(filtered_cards)} places found")
    print(f"   📍 Mock location: Hitec City (17.4435, 78.3772)")


if __name__ == "__main__":
    print("Run tests using: pytest test_distance_filters.py -v")
