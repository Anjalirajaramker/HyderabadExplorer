"""
Cuisine Filter Tests for Food Places Page 🍽️
Tests for filtering food places by cuisine type (Biryani, Street Food, etc.)
"""

from selenium.webdriver.common.by import By
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import (
    wait_for_food_cards_to_load, 
    get_visible_food_cards,
    click_cuisine_filter_checkbox,
    get_clear_filters_button
)


def test_filter_by_biryani(food_browser):
    """
    Cuisine Filter Test 1: Verify filtering by 'Biryani & Hyderabadi' cuisine works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get initial count
    initial_cards = get_visible_food_cards(food_browser)
    initial_count = len(initial_cards)
    
    # Click Biryani filter
    click_cuisine_filter_checkbox(food_browser, "Biryani & Hyderabadi")
    time.sleep(1)
    
    # Get filtered cards
    filtered_cards = get_visible_food_cards(food_browser)
    filtered_count = len(filtered_cards)
    
    # Verify filter worked
    assert filtered_count > 0, "No cards visible after Biryani filter"
    assert filtered_count <= initial_count, "Filtered count should be less than or equal to initial"
    
    # Verify all visible cards have restaurant info
    for card in filtered_cards:
        place_type = card.find_element(By.CLASS_NAME, "place-type").text
        assert len(place_type) > 0, "Place type should not be empty"
    
    print(f"✅ Biryani & Hyderabadi filter test passed - {filtered_count}/{initial_count} places shown")


def test_filter_by_street_food(food_browser):
    """
    Cuisine Filter Test 2: Verify filtering by 'Street Food - Quick Bites' cuisine works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Click Street Food filter
    click_cuisine_filter_checkbox(food_browser, "Street Food - Quick Bites")
    time.sleep(1)
    
    # Get filtered cards
    filtered_cards = get_visible_food_cards(food_browser)
    
    assert len(filtered_cards) > 0, "No cards visible after Street Food filter"
    
    # Verify all visible cards have place type
    for card in filtered_cards:
        place_type = card.find_element(By.CLASS_NAME, "place-type").text
        assert len(place_type) > 0
    
    print(f"✅ Street Food - Quick Bites filter test passed - {len(filtered_cards)} places shown")


def test_filter_by_cafe(food_browser):
    """
    Cuisine Filter Test 3: Verify filtering by 'Cafes & Bakeries' cuisine works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Click Cafe filter
    click_cuisine_filter_checkbox(food_browser, "Cafes & Bakeries")
    time.sleep(1)
    
    # Get filtered cards
    filtered_cards = get_visible_food_cards(food_browser)
    
    assert len(filtered_cards) > 0, "No cards visible after Cafe filter"
    
    print(f"✅ Cafes & Bakeries filter test passed - {len(filtered_cards)} places shown")


def test_clear_cuisine_filters(food_browser):
    """
    Cuisine Filter Test 4: Verify clear filters button resets cuisine filters.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get initial count
    initial_cards = get_visible_food_cards(food_browser)
    initial_count = len(initial_cards)
    
    # Apply Biryani filter
    click_cuisine_filter_checkbox(food_browser, "Biryani & Hyderabadi")
    time.sleep(1)
    
    # Verify filter is active
    filtered_cards = get_visible_food_cards(food_browser)
    assert len(filtered_cards) < initial_count
    
    # Click clear filters
    clear_btn = get_clear_filters_button(food_browser)
    clear_btn.click()
    time.sleep(1)
    
    # Verify all cards are back
    final_cards = get_visible_food_cards(food_browser)
    assert len(final_cards) == initial_count, "Clear filters didn't restore all cards"
    
    print(f"✅ Clear cuisine filters test passed - Restored {len(final_cards)} places")


if __name__ == "__main__":
    print("Run tests using: pytest test_food_suites/test_cuisine_filters.py -v")
