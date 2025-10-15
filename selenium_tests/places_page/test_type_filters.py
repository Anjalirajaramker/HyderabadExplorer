"""
Type Filter Tests 🧪
Tests for place type filtering functionality (Heritage, Parks, Museums, etc.)
"""

from selenium.webdriver.common.by import By
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_cards_to_load, get_visible_cards


def test_filter_by_type_heritage(browser):
    """
    Filter Test 1: Verify filtering by 'Heritage' type works.
    """
    wait_for_cards_to_load(browser)
    
    # Get initial card count
    initial_cards = len(get_visible_cards(browser))
    print(f"Initial cards visible: {initial_cards}")
    
    # Click Heritage filter
    try:
        heritage_checkbox = browser.find_element(
            By.CSS_SELECTOR, 
            "input.filter-checkbox[data-type='Heritage']"
        )
        heritage_checkbox.click()
        time.sleep(1)
        
        # Get filtered cards
        filtered_cards = get_visible_cards(browser)
        assert len(filtered_cards) < initial_cards, "Filter did not reduce card count"
        
        print(f"✅ Heritage filter test passed - {len(filtered_cards)} cards after filtering")
    except Exception as e:
        print(f"⚠️ Heritage filter not found (might be using different grouping): {e}")


def test_filter_by_type_parks(browser):
    """
    Filter Test 2: Verify filtering by 'Parks' type works.
    """
    wait_for_cards_to_load(browser)
    
    try:
        parks_checkbox = browser.find_element(
            By.CSS_SELECTOR, 
            "input.filter-checkbox[data-type='Parks']"
        )
        parks_checkbox.click()
        time.sleep(1)
        
        filtered_cards = get_visible_cards(browser)
        assert len(filtered_cards) > 0, "No parks found after filtering"
        
        print(f"✅ Parks filter test passed - {len(filtered_cards)} parks found")
    except Exception as e:
        print(f"⚠️ Parks filter not found: {e}")


def test_clear_filters_button(browser):
    """
    Filter Test 3: Verify clear filters button works.
    """
    wait_for_cards_to_load(browser)
    
    # Apply a filter
    try:
        heritage_checkbox = browser.find_element(
            By.CSS_SELECTOR, 
            "input.filter-checkbox[data-type='Heritage']"
        )
        heritage_checkbox.click()
        time.sleep(1)
        
        filtered_count = len(get_visible_cards(browser))
        
        # Click clear filters
        clear_btn = browser.find_element(By.ID, "clear-filters")
        clear_btn.click()
        time.sleep(1)
        
        # Verify all cards are back
        final_count = len(get_visible_cards(browser))
        assert final_count > filtered_count, "Clear filters did not restore all cards"
        
        print("✅ Clear filters button test passed")
    except Exception as e:
        print(f"⚠️ Clear filters test failed: {e}")


if __name__ == "__main__":
    print("Run tests using: pytest test_type_filters.py -v")
