"""
Performance & Loading Tests ⚡
Tests for page load time and dynamic content generation.
"""

from selenium.webdriver.common.by import By
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import wait_for_cards_to_load


def test_page_loads_within_timeout(browser):
    """
    Performance Test: Verify page loads and cards render within reasonable time.
    """
    start_time = time.time()
    
    wait_for_cards_to_load(browser, timeout=15)
    
    load_time = time.time() - start_time
    
    assert load_time < 15, f"Page took too long to load: {load_time:.2f}s"
    
    print(f"✅ Page load test passed - Loaded in {load_time:.2f}s")


def test_filters_generate_dynamically(browser):
    """
    Dynamic Content Test: Verify filters are generated from data.json.
    """
    wait_for_cards_to_load(browser)
    
    # Check type filters
    type_checkboxes = browser.find_elements(By.CLASS_NAME, "filter-checkbox")
    assert len(type_checkboxes) > 0, "Type filters not generated"
    
    # Check budget filters
    budget_checkboxes = browser.find_elements(By.CLASS_NAME, "budget-filter-checkbox")
    assert len(budget_checkboxes) > 0, "Budget filters not generated"
    
    # Check distance filters
    distance_checkboxes = browser.find_elements(By.CLASS_NAME, "distance-filter-checkbox")
    assert len(distance_checkboxes) > 0, "Distance filters not generated"
    
    print(f"✅ Dynamic filters test passed")
    print(f"   - Type filters: {len(type_checkboxes)}")
    print(f"   - Budget filters: {len(budget_checkboxes)}")
    print(f"   - Distance filters: {len(distance_checkboxes)}")


if __name__ == "__main__":
    print("Run tests using: pytest test_performance.py -v")
