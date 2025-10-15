"""
UI/UX Tests 🎨
Tests for user interface elements, card structure, and navigation.
"""

from selenium.webdriver.common.by import By
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_cards_to_load, get_visible_cards


def test_card_structure_and_content(browser):
    """
    UI Test 1: Verify destination card has all required elements.
    """
    wait_for_cards_to_load(browser)
    
    cards = get_visible_cards(browser)
    first_card = cards[0]
    
    # Check for required elements
    assert first_card.find_element(By.CLASS_NAME, "destination-name")
    assert first_card.find_element(By.CLASS_NAME, "destination-info")
    assert first_card.find_element(By.CLASS_NAME, "place-type")
    assert first_card.find_element(By.CLASS_NAME, "entry-fee")
    assert first_card.find_element(By.CLASS_NAME, "description")
    
    print("✅ Card structure test passed - All elements present")


def test_responsive_grid_layout(browser):
    """
    UI Test 2: Verify cards are in a grid layout.
    """
    wait_for_cards_to_load(browser)
    
    destinations_container = browser.find_element(By.ID, "destinations-container")
    display_style = destinations_container.value_of_css_property("display")
    
    assert "grid" in display_style or "flex" in display_style, \
        f"Expected grid or flex layout, got: {display_style}"
    
    print("✅ Grid layout test passed")


def test_navigation_links_work(browser):
    """
    Navigation Test: Verify navigation links are clickable.
    """
    nav_links = browser.find_elements(By.CLASS_NAME, "nav-btn")
    
    assert len(nav_links) == 3, "Expected 3 navigation links"
    
    # Check that links have href attributes
    for link in nav_links:
        href = link.get_attribute("href")
        assert href is not None and len(href) > 0, "Navigation link missing href"
    
    print("✅ Navigation links test passed")


if __name__ == "__main__":
    print("Run tests using: pytest test_ui_ux.py -v")
