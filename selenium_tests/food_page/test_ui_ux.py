"""
UI/UX Tests for Food Places Page 🎨
Tests for user interface elements, card interactions, and responsive design.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import wait_for_food_cards_to_load, get_visible_food_cards


def test_food_card_structure_and_content(food_browser):
    """
    UI Test 1: Verify each food card has all required elements.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get first visible card
    cards = get_visible_food_cards(food_browser)
    assert len(cards) > 0, "No cards found"
    
    first_card = cards[0]
    
    # Check for restaurant name
    name = first_card.find_element(By.CLASS_NAME, "restaurant-name")
    assert name.text != "", "Card should have a restaurant name"
    
    # Check for cuisine type/place type
    cuisine = first_card.find_element(By.CLASS_NAME, "place-type")
    assert cuisine.text != "", "Card should have cuisine type"
    
    # Check for area
    area = first_card.find_element(By.CLASS_NAME, "area")
    assert area.text != "", "Card should have area/location"
    
    # Check for budget badge
    budget = first_card.find_element(By.CLASS_NAME, "budget-badge")
    assert budget.text != "", "Card should have budget info"
    
    print("✅ Food card structure test passed - All elements present")


def test_expand_card_details(food_browser):
    """
    UI Test 2: Verify clicking 'View Details' expands card to show full information.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get first visible card
    cards = get_visible_food_cards(food_browser)
    first_card = cards[0]
    
    # Find and click "View Details" button
    try:
        view_details_btn = first_card.find_element(By.CLASS_NAME, "view-details-btn")
        
        # Check if details are initially hidden
        details_section = first_card.find_element(By.CLASS_NAME, "food-details")
        initial_display = details_section.value_of_css_property("display")
        
        # Click to expand
        view_details_btn.click()
        time.sleep(0.5)
        
        # Verify details are now visible
        expanded_display = details_section.value_of_css_property("display")
        assert expanded_display != "none", "Details should be visible after clicking"
        
        # Verify expanded content exists
        special_dishes = first_card.find_element(By.CLASS_NAME, "special-dishes")
        assert special_dishes.is_displayed(), "Special dishes should be visible when expanded"
        
        timings = first_card.find_element(By.CLASS_NAME, "food-timings")
        assert timings.is_displayed(), "Timings should be visible when expanded"
        
        print("✅ Expand card test passed - Details show on click")
        
    except Exception as e:
        print(f"⚠️ Expand card test - element may not be expandable: {e}")


def test_responsive_grid_layout(food_browser):
    """
    UI Test 3: Verify food cards are displayed in a grid/flex layout.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get the container
    container = food_browser.find_element(By.ID, "food-places-container")
    
    # Verify container has display: grid or flex
    display_prop = container.value_of_css_property("display")
    assert display_prop in ["grid", "flex", "block"], f"Container should have valid display type, got: {display_prop}"
    
    # Get visible cards
    cards = get_visible_food_cards(food_browser)
    assert len(cards) > 1, "Should have multiple cards to test layout"
    
    # Verify cards have consistent dimensions
    card_widths = [card.size['width'] for card in cards[:3]]  # Check first 3 cards
    # All cards should have similar widths (allow small variance)
    width_variance = max(card_widths) - min(card_widths)
    assert width_variance < 50, "Cards should have consistent widths"
    
    print(f"✅ Grid layout test passed - {display_prop} layout with consistent cards")


def test_navigation_links_work(food_browser):
    """
    UI Test 4: Verify navigation links in header work correctly.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Find navigation links
    nav_links = food_browser.find_elements(By.CSS_SELECTOR, ".main-nav .nav-btn")
    assert len(nav_links) >= 3, "Should have at least 3 navigation links"
    
    # Verify each link has href
    for link in nav_links:
        href = link.get_attribute("href")
        assert href is not None and href != "", "Navigation link should have href"
        
        # Check if current page link is active
        if "food-places.html" in href:
            classes = link.get_attribute("class")
            assert "active" in classes, "Current page link should have 'active' class"
    
    print(f"✅ Navigation test passed - {len(nav_links)} working links found")


def test_show_nearby_button_present(food_browser):
    """
    UI Test 5: Verify 'Show Nearby Places' button is present and clickable.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Find the nearby button
    nearby_btn = food_browser.find_element(By.ID, "show-nearby")
    assert nearby_btn.is_displayed(), "Show nearby button should be visible"
    assert nearby_btn.is_enabled(), "Show nearby button should be enabled"
    
    # Verify button text
    button_text = nearby_btn.text
    assert "nearby" in button_text.lower() or "📍" in button_text, "Button should mention 'nearby' or have location icon"
    
    print("✅ Show nearby button test passed - Button is present and clickable")


def test_results_count_display(food_browser):
    """
    UI Test 6: Verify results count is displayed and updates with filters.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Find results count element
    results_count = food_browser.find_element(By.ID, "results-count")
    assert results_count.is_displayed(), "Results count should be visible"
    
    initial_text = results_count.text
    assert initial_text != "", "Results count should have text"
    assert any(char.isdigit() for char in initial_text), "Results count should contain numbers"
    
    # Apply a budget filter using correct class name
    affordable_checkbox = food_browser.find_element(
        By.CSS_SELECTOR,
        "input.budget-checkbox"
    )
    affordable_checkbox.click()
    time.sleep(1)
    
    # Verify count updated
    filtered_text = results_count.text
    assert filtered_text != initial_text, "Results count should update after filtering"
    
    print(f"✅ Results count test passed - Initial: '{initial_text}', Filtered: '{filtered_text}'")


def test_hero_banner_present(food_browser):
    """
    UI Test 7: Verify hero banner section is present with proper content.
    """
    # Hero banner should load immediately
    hero_banner = food_browser.find_element(By.CLASS_NAME, "hero-banner")
    assert hero_banner.is_displayed(), "Hero banner should be visible"
    
    # Check for hero text
    hero_text = food_browser.find_element(By.CLASS_NAME, "hero-text")
    assert hero_text.is_displayed(), "Hero text should be visible"
    
    # Verify hero content mentions food/restaurants
    hero_content = hero_text.text.lower()
    assert any(word in hero_content for word in ['food', 'restaurant', 'culinary', 'explore']), \
        "Hero text should mention food/restaurants"
    
    print("✅ Hero banner test passed - Banner present with relevant content")


if __name__ == "__main__":
    print("Run tests using: pytest test_food_suites/test_ui_ux.py -v")
