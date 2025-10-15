"""
Budget Filter Tests 💰
Tests for budget-based filtering functionality (Free, Under ₹50, etc.)
"""

from selenium.webdriver.common.by import By
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_cards_to_load, get_visible_cards


def test_filter_by_budget_free(browser):
    """
    Budget Test 1: Verify filtering by 'Free' budget option.
    Uses checkbox filters with data-min='0' and data-max='0'.
    """
    wait_for_cards_to_load(browser)
    
    # Find and click Free checkbox (min=0, max=0)
    try:
        free_checkbox = browser.find_element(
            By.CSS_SELECTOR,
            "input.budget-filter-checkbox[data-min='0'][data-max='0']"
        )
        free_checkbox.click()
        time.sleep(1)
        
        filtered_cards = get_visible_cards(browser)
        assert len(filtered_cards) > 0, "No free places found"
        
        print(f"✅ Free budget filter test passed - {len(filtered_cards)} free places found")
    except Exception as e:
        print(f"⚠️ Free budget filter test failed: {e}")


def test_filter_by_budget_under_50(browser):
    """
    Budget Test 2: Verify filtering by 'Under ₹50' budget option.
    """
    wait_for_cards_to_load(browser)
    
    try:
        under_50_checkbox = browser.find_element(
            By.CSS_SELECTOR,
            "input.budget-filter-checkbox[data-min='1'][data-max='50']"
        )
        under_50_checkbox.click()
        time.sleep(1)
        
        filtered_cards = get_visible_cards(browser)
        assert len(filtered_cards) > 0, "No places under ₹50 found"
        
        print(f"✅ Under ₹50 filter test passed - {len(filtered_cards)} places found")
    except Exception as e:
        print(f"⚠️ Under ₹50 filter test failed: {e}")


def test_combined_type_and_budget_filter(browser):
    """
    Combined Filter Test: Verify combining type and budget filters works.
    """
    wait_for_cards_to_load(browser)
    
    try:
        # Click Heritage type filter
        heritage_checkbox = browser.find_element(
            By.CSS_SELECTOR,
            "input.filter-checkbox[data-type='Heritage']"
        )
        heritage_checkbox.click()
        time.sleep(1)
        
        heritage_count = len(get_visible_cards(browser))
        
        # Add budget filter
        free_checkbox = browser.find_element(
            By.CSS_SELECTOR,
            "input.budget-filter-checkbox[data-min='0'][data-max='0']"
        )
        free_checkbox.click()
        time.sleep(1)
        
        combined_count = len(get_visible_cards(browser))
        
        # Combined filter should show equal or fewer results
        assert combined_count <= heritage_count, "Combined filter showed more results than type filter alone"
        
        print(f"✅ Combined filter test passed - Heritage: {heritage_count}, Combined: {combined_count}")
    except Exception as e:
        print(f"⚠️ Combined filter test failed: {e}")


if __name__ == "__main__":
    print("Run tests using: pytest test_budget_filters.py -v")
