"""import module"""
from playwright.sync_api import Page


class StartingPage:
    """Class represents the starting page."""
    def __init__(self, page: Page):
        self.page = page
        self.run_script_button = page.locator("#run-button")
        self.result_textbox = page.locator("#result")
        self.result_textbox_elements = page.locator("#result .token")

    def navigate(self):
        """Navigation"""
        self.page.goto("https://jsonplaceholder.typicode.com/")

    def get_try_it_result(self):
        """Getting the result"""
        self.run_script_button.click()
