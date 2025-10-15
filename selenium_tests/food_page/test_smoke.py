"""
Smoke Tests for Food Places Page 🔥
Basic tests to verify the page loads correctly and essential elements are present.
"""

from selenium.webdriver.common.by import By
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_food_cards_to_load, get_visible_food_cards


def test_food_page_title(food_browser):
    """
    Smoke Test 1: Verify the page title contains 'City Quest'.
    """
    assert "City Quest" in food_browser.title
    print("✅ Food page title test passed")


def test_food_cards_are_loaded(food_browser):
    """
    Smoke Test 2: Verify that food place cards are loaded and visible.
    """
    wait_for_food_cards_to_load(food_browser)
    
    food_cards = get_visible_food_cards(food_browser)
    assert len(food_cards) > 0, "No food cards found on the page"
    
    print(f"✅ Food cards loaded test passed - Found {len(food_cards)} food places")


def test_header_elements_present(food_browser):
    """
    Smoke Test 3: Verify header elements are present (logo, navigation).
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Check for logo
    logo = food_browser.find_element(By.CLASS_NAME, "logo")
    assert logo.is_displayed()
    
    # Check for navigation
    nav = food_browser.find_element(By.CLASS_NAME, "main-nav")
    assert nav.is_displayed()
    
    # Check for nav buttons
    nav_buttons = nav.find_elements(By.CLASS_NAME, "nav-btn")
    assert len(nav_buttons) >= 3  # Home, Tourist Places, Food Places
    
    print("✅ Header elements test passed")


def test_filter_sections_present(food_browser):
    """
    Smoke Test 4: Verify filter sections are visible.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Check for cuisine filter section
    cuisine_filter = food_browser.find_element(By.ID, "cuisine-filter-options")
    assert cuisine_filter.is_displayed()
    
    # Check for budget filter section
    budget_filter = food_browser.find_element(By.ID, "budget-filter-options")
    assert budget_filter.is_displayed()
    
    print("✅ Filter sections test passed")


if __name__ == "__main__":
    print("Run tests using: pytest test_food_suites/test_smoke.py -v")
