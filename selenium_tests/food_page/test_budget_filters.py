"""
Budget Filter Tests for Food Places Page 💰
Tests for filtering food places by budget ranges (Under ₹200, ₹200-₹500, etc.)
"""

from selenium.webdriver.common.by import By
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from selenium_tests.helpers import (
    wait_for_food_cards_to_load, 
    get_visible_food_cards,
    click_budget_filter_checkbox,
    get_clear_filters_button
)


def test_filter_by_affordable_budget(food_browser):
    """
    Budget Filter Test 1: Verify filtering by 'Under ₹200' (Affordable) works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get initial count
    initial_cards = get_visible_food_cards(food_browser)
    initial_count = len(initial_cards)
    
    # Click 'Under ₹200' budget filter
    click_budget_filter_checkbox(food_browser, "Under ₹200")
    time.sleep(1)
    
    # Get filtered cards
    filtered_cards = get_visible_food_cards(food_browser)
    filtered_count = len(filtered_cards)
    
    # Verify filter worked
    assert filtered_count > 0, "No cards visible after 'Under ₹200' filter"
    assert filtered_count <= initial_count, "Filtered count should be less than or equal to initial"
    
    print(f"✅ Under ₹200 filter test passed - {filtered_count}/{initial_count} affordable places shown")


def test_filter_by_mid_range_budget(food_browser):
    """
    Budget Filter Test 2: Verify filtering by 'Moderate (₹200 - ₹400)' works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Click 'Moderate (₹200 - ₹400)' budget filter
    click_budget_filter_checkbox(food_browser, "Moderate (₹200 - ₹400)")
    time.sleep(1)
    
    # Get filtered cards
    filtered_cards = get_visible_food_cards(food_browser)
    
    assert len(filtered_cards) > 0, "No cards visible after 'Moderate (₹200 - ₹400)' filter"
    
    print(f"✅ Moderate (₹200 - ₹400) filter test passed - {len(filtered_cards)} mid-range places shown")


def test_filter_by_premium_budget(food_browser):
    """
    Budget Filter Test 3: Verify filtering by 'Premium (₹400 - ₹600)' works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Click 'Premium (₹400 - ₹600)' budget filter
    click_budget_filter_checkbox(food_browser, "Premium (₹400 - ₹600)")
    time.sleep(1)
    
    # Get filtered cards
    filtered_cards = get_visible_food_cards(food_browser)
    
    assert len(filtered_cards) > 0, "No cards visible after 'Premium (₹400 - ₹600)' filter"
    
    print(f"✅ Premium (₹400 - ₹600) filter test passed - {len(filtered_cards)} premium places shown")


def test_combined_cuisine_and_budget_filters(food_browser):
    """
    Budget Filter Test 4: Verify combining cuisine and budget filters works.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get initial count
    initial_count = len(get_visible_food_cards(food_browser))
    
    # Apply Biryani cuisine filter
    biryani_checkbox = food_browser.find_element(
        By.CSS_SELECTOR,
        "input.cuisine-checkbox[data-cuisine='Biryani & Hyderabadi']"
    )
    biryani_checkbox.click()
    time.sleep(1)
    
    cuisine_filtered = len(get_visible_food_cards(food_browser))
    
    # Apply Budget Friendly (Under ₹200) filter
    click_budget_filter_checkbox(food_browser, "Budget Friendly (Under ₹200)")
    time.sleep(1)
    
    # Get cards with both filters
    both_filtered = get_visible_food_cards(food_browser)
    both_count = len(both_filtered)
    
    # Verify both filters are active
    assert both_count > 0, "No cards with both filters applied"
    assert both_count <= cuisine_filtered, "Combined filter should show fewer or equal cards"
    assert both_count <= initial_count, "Combined filter should show fewer or equal cards than initial"
    
    print(f"✅ Combined filters test passed - {both_count} Biryani places under ₹200")


def test_clear_budget_filters(food_browser):
    """
    Budget Filter Test 5: Verify clear filters button resets budget filters.
    """
    wait_for_food_cards_to_load(food_browser)
    
    # Get initial count
    initial_count = len(get_visible_food_cards(food_browser))
    
    # Apply budget filter
    click_budget_filter_checkbox(food_browser, "Under ₹200")
    time.sleep(1)
    
    # Verify filter is active
    filtered_count = len(get_visible_food_cards(food_browser))
    assert filtered_count < initial_count, "Filter should reduce visible cards"
    
    # Click clear filters
    clear_btn = get_clear_filters_button(food_browser)
    clear_btn.click()
    time.sleep(1)
    
    # Verify all cards are back
    final_count = len(get_visible_food_cards(food_browser))
    assert final_count == initial_count, "Clear filters didn't restore all cards"
    
    print(f"✅ Clear budget filters test passed - Restored {final_count} places")


if __name__ == "__main__":
    print("Run tests using: pytest test_food_suites/test_budget_filters.py -v")
