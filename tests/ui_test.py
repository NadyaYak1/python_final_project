
import time
import pytest
from logic.guide_page import GuidePage
from logic.page_start import StartingPage
from core.logger import get_logger

"""Logger initializing"""
logger = get_logger(__name__)
logger.info("Logging for UI is successfully initialized")
logger.info("Info message")
logger.debug("Debug message")


@pytest.mark.ui
def test_home_page(page):
    """Validation of starting page"""
    logger.debug("Starting log for test_home_page")
    home_page = StartingPage(page)
    home_page.navigate()
    assert home_page.result_textbox_elements.count() == 2
    home_page.get_try_it_result()
    time.sleep(2)
    assert home_page.result_textbox_elements.count() == 17
    logger.debug("The test_home_page is successfully completed")


@pytest.mark.parametrize(
    "number, expected_text",
    [
        ("1", "/posts/1/comments"),
        ("2", "/albums/1/photos"),
        ("3", "/users/1/albums"),
        ("4", "/users/1/todos"),
        ("5", "/users/1/posts")
    ],
)
@pytest.mark.ui
def test_names_of_nested_routes(page, number, expected_text):
    """Validation of available nested routes"""
    logger.debug(f"Starting log for test_home_page (input {number})")
    guide_page = GuidePage(page)
    guide_page.open_guide_page()
    assert guide_page.guide_header.inner_text() == "Guide"
    assert guide_page.get_list_item(number).inner_text() == expected_text
    logger.debug(f"The test_home_page (input {number}) is successfully completed")
