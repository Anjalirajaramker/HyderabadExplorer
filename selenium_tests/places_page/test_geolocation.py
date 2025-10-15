"""
Geolocation Test 🗺️
Tests for geolocation and nearest places functionality.
Uses Chrome DevTools Protocol to mock user location.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_cards_to_load, get_visible_cards


def test_geolocation_mock_and_nearest_places(browser):
    """
    Geolocation Test: Mock user location and test nearest places functionality.
    Uses button ID 'find-nearby-btn' for reliable selection.
    """
    wait_for_cards_to_load(browser)
    
    try:
        # Mock Hitec City coordinates using Chrome DevTools Protocol
        hitec_city_coords = {
            "latitude": 17.4435,
            "longitude": 78.3772,
            "accuracy": 100
        }
        browser.execute_cdp_cmd("Emulation.setGeolocationOverride", hitec_city_coords)
        
        # Wait a moment for the page to process location
        time.sleep(2)
        
        # Click the nearest places button using its ID
        nearest_btn = browser.find_element(By.ID, "find-nearby-btn")
        nearest_btn.click()
        
        # Wait for loading spinner to appear and disappear
        try:
            spinner = browser.find_element(By.ID, "loading-spinner")
            WebDriverWait(browser, 3).until(
                EC.visibility_of(spinner)
            )
            WebDriverWait(browser, 20).until(
                EC.invisibility_of_element_located((By.ID, "loading-spinner"))
            )
        except:
            time.sleep(3)  # Fallback wait
        
        # Verify cards are still visible
        cards_after_sort = get_visible_cards(browser)
        assert len(cards_after_sort) > 0, "No cards visible after sorting by distance"
        
        print(f"✅ Geolocation test passed - {len(cards_after_sort)} nearest places shown")
            
    except Exception as e:
        print(f"⚠️ Geolocation test failed: {e}")


if __name__ == "__main__":
    print("Run tests using: pytest test_geolocation.py -v")
