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
    
def find_food_card(browser, name):
    """
    Finds a food card element based on the restaurant/place name.
    
    Args:
        browser: Selenium WebDriver instance
        name: Name of the food place to find
    
    Returns:
        WebElement: The food card element
    """
    return browser.find_element(
        By.XPATH, 
        f"//div[contains(@class, 'food-place-card')][.//h3[contains(text(), '{name}')]]"
    )


def wait_for_food_cards_to_load(browser, timeout=15):
    """
    Wait for food cards to be loaded on the page.
    
    Args:
        browser: Selenium WebDriver instance
        timeout: Maximum time to wait in seconds
    """
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "food-place-card"))
    )


def get_visible_food_cards(browser):
    """
    Get all visible food cards on the page.
    
    Args:
        browser: Selenium WebDriver instance
    
    Returns:
        list: List of visible food card WebElements
    """
    all_cards = browser.find_elements(By.CLASS_NAME, "food-place-card")
    return [card for card in all_cards if card.is_displayed()]


def click_cuisine_filter_checkbox(browser, cuisine_type):
    """
    Click a cuisine type filter checkbox.
    
    Args:
        browser: Selenium WebDriver instance
        cuisine_type: Type of cuisine (e.g., 'Biryani', 'Street Food')
    """
    checkbox = browser.find_element(
        By.CSS_SELECTOR,
        f"input.cuisine-checkbox[data-cuisine='{cuisine_type}']"
    )
    checkbox.click()


def click_budget_filter_checkbox(browser, budget_label):
    """
    Click a budget range filter checkbox.
    
    Args:
        browser: Selenium WebDriver instance
        budget_label: Budget label text (e.g., 'Budget Friendly (Under ₹200)')
    """
    # Find by label text since data attributes are min/max budget values
    checkboxes = browser.find_elements(By.CSS_SELECTOR, "input.budget-checkbox")
    for checkbox in checkboxes:
        parent_label = checkbox.find_element(By.XPATH, "..")
        if budget_label in parent_label.text:
            checkbox.click()
            time.sleep(0.5)  # Wait for filter to apply
            return
    raise Exception(f"Budget filter '{budget_label}' not found")


def get_clear_filters_button(browser):
    """
    Get the clear filters button element.
    
    Args:
        browser: Selenium WebDriver instance
    
    Returns:
        WebElement: The clear filters button
    """
    return browser.find_element(By.ID, "clear-filters")

