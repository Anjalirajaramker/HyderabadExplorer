"""
Smoke Tests 🔥
Basic tests to verify the page loads correctly and essential elements are present.
Run these first to ensure the application is functional.
"""

from selenium.webdriver.common.by import By
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_cards_to_load, get_visible_cards


def test_page_title(browser):
    """
    Smoke Test 1: Verify the title of the page contains 'City Quest'.
    """
    assert "City Quest" in browser.title, f"Expected 'City Quest' in title, got: {browser.title}"
    print("✅ Page title test passed")


def test_cards_are_loaded(browser):
    """
    Smoke Test 2: Verify that destination cards are loaded and visible.
    """
    wait_for_cards_to_load(browser)
    cards = browser.find_elements(By.CLASS_NAME, "destination-card")
    assert len(cards) > 0, "No destination cards found on the page"
    print(f"✅ Cards loaded test passed - Found {len(cards)} cards")


def test_header_elements_present(browser):
    """
    Smoke Test 3: Verify main header elements are present.
    """
    # Check logo
    logo = browser.find_element(By.CSS_SELECTOR, ".logo h1")
    assert "City Quest" in logo.text
    
    # Check navigation buttons
    nav_buttons = browser.find_elements(By.CLASS_NAME, "nav-btn")
    assert len(nav_buttons) == 3, "Expected 3 navigation buttons"
    
    print("✅ Header elements test passed")


def test_filter_sections_present(browser):
    """
    Smoke Test 4: Verify all filter sections are present.
    """
    # Check filter container
    filter_container = browser.find_element(By.ID, "filter-container")
    assert filter_container.is_displayed()
    
    # Check filter sections
    type_filter = browser.find_element(By.ID, "filter-options")
    budget_filter = browser.find_element(By.ID, "budget-filter-options")
    distance_filter = browser.find_element(By.ID, "distance-filter-options")
    
    assert type_filter.is_displayed()
    assert budget_filter.is_displayed()
    assert distance_filter.is_displayed()
    
    print("✅ Filter sections test passed")


if __name__ == "__main__":
    print("Run tests using: pytest test_smoke.py -v")
