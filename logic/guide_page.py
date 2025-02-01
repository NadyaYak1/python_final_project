"""import module"""
from playwright.sync_api import Page


class GuidePage:
    """Class represents the Guide page."""
    def __init__(self, page: Page):
        self.page = page
        self.guide_header = page.get_by_role("heading", name="Guide")
        self.routes_list = page.locator("//*[contains(text(),'available nested')]/following-sibling::ul")

    def open_guide_page(self):
        """Guide page"""
        self.page.goto("https://jsonplaceholder.typicode.com/")
        self.page.locator("text='Guide'").click()

    def get_list_item(self, number):
        """Get list of items"""
        return self.routes_list.locator(f"//li[{number}]")
