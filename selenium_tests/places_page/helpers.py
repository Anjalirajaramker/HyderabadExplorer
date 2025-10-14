"""
Helper Functions for City Quest Tests
Shared utilities used across multiple test files

Note: Tests now use a local HTTP server (http://localhost:8888) 
instead of file:// protocol to properly load data.json files.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def find_card(browser, name):
    """
    Helper function to find a destination card by its name.
    Uses <h3> tag for card titles.
    """
    try:
        return browser.find_element(
            By.XPATH, 
            f"//div[contains(@class, 'destination-card')][.//h3[contains(text(), '{name}')]]"
        )
    except:
        return None


def wait_for_cards_to_load(browser, timeout=10):
    """Wait for destination cards to be loaded and visible."""
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "destination-card"))
    )


def get_visible_cards(browser):
    """Get all currently visible destination cards."""
    cards = browser.find_elements(By.CLASS_NAME, "destination-card")
    return [card for card in cards if card.is_displayed()]


def click_filter_checkbox(browser, filter_class, data_attribute, value):
    """
    Click a filter checkbox with specific data attribute.
    
    Args:
        filter_class: CSS class of checkbox (e.g., 'filter-checkbox')
        data_attribute: Data attribute name (e.g., 'type', 'min')
        value: Value to match
    """
    checkbox = browser.find_element(
        By.CSS_SELECTOR, 
        f"input.{filter_class}[data-{data_attribute}='{value}']"
    )
    checkbox.click()
    time.sleep(1)  # Allow filtering to complete
