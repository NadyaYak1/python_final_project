"""import modules"""
import pytest
from playwright.sync_api import sync_playwright


# Define a pytest fixture to set up Playwright and browser instance
@pytest.fixture(scope="session")
def browser_launch():
    """Launching browser"""
    with sync_playwright() as playwright:
        browser_chrome = playwright.chromium.launch(headless=False)
        yield browser_chrome
        browser_chrome.close()


@pytest.fixture(scope="session")
def launch_page(browser_launch):
    """Launching page"""
    context = browser_launch.new_context()
    page = context.new_page()
    return page
