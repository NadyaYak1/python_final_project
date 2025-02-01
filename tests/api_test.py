"""Import modules"""
import pytest
import requests
from jsonschema import validate
from unittest.mock import patch
from core.logger import get_logger

# Initialize the logger
logger = get_logger(__name__)
logger.info(" API logger initialized successfully!")
logger.info("This is an info message.")
logger.debug("This is a debug message.")


# URL for the API
URL = "https://jsonplaceholder.typicode.com"


# Fixtures for reusable setup
@pytest.fixture(scope="session")
def base_url():
    """Base URL for the API."""
    return URL


@pytest.fixture
def headers():
    """Providing common headers."""
    return {"Content-Type": "application/json"}


@pytest.fixture
def post_data():
    """Providing mock data for creating a post."""
    return {
        "title": "Test Title",
        "userId": "1"
    }


# JSON Schema Validation
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": ["string", "integer"]},
        "id": {"type": ["string", "integer"]},
        "title": {"type": "string"}
    },
    "required": ["userId", "id", "title"]
}


# Test fetching: GET
def test_fetch_post(base_url, headers):
    """Test fetching a post by ID."""
    logger.debug("Starting log for test_fetch_post")
    post_id = 1
    response = requests.get(f"{base_url}/posts/{post_id}", headers=headers)
    assert response.status_code == 200, "Expected status code 200"
    validate(instance=response.json(), schema=POST_SCHEMA)
    assert response.json()["id"] == post_id, "Fetched post ID does not match"
    logger.debug("Test test_fetch_post is successfully completed")


# Test creating: POST
def test_create_post(base_url, headers, post_data):
    """Test creating a new post."""
    logger.debug("Starting log for test_create_post")
    response = requests.post(f"{base_url}/posts", json=post_data, headers=headers)
    assert response.status_code == 201, "Expected status code 201 for post creation"
    created_post = response.json()
    assert created_post["title"] == post_data["title"], "Title does not match"
    assert created_post["userId"] == post_data["userId"], "UserId does not match"
    logger.debug("The test_create_post is successfully completed")


# Test updating: PUT
def test_update_post(base_url, headers, post_data):
    """Test updating an existing post."""
    logger.debug("Starting log for test_update_post")
    post_id = 1
    updated_post = post_data.copy()
    updated_post["title"] = "Updated Title"
    response = requests.put(f"{base_url}/posts/{post_id}", json=updated_post, headers=headers)
    assert response.status_code == 200, "Expected status code 200 for post update"
    assert response.json()["title"] == "Updated Title", "Title was not updated"
    logger.debug("The test_fetch_post is successfully completed")


# Test deleting: DELETE
def test_delete_post(base_url, headers):
    """Test deleting a post."""
    logger.debug("Starting log for test_delete_post")
    post_id = 1
    response = requests.delete(f"{base_url}/posts/{post_id}", headers=headers)
    assert response.status_code == 200, "Expected status code 200 for post deletion"
    logger.debug("The test_delete_post is successfully completed")


# Test fetching comments and filtering: GET
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_fetch_comments(base_url, headers, post_id):
    """Test fetching comments for a post."""
    logger.debug("Starting log for test_fetch_comments")
    response = requests.get(f"{base_url}/posts/{post_id}/comments", headers=headers)
    assert response.status_code == 200, "Expected status code 200"
    comments = response.json()
    assert all(comment["postId"] == post_id for comment in comments), "Comments do not match the post ID"
    logger.debug("The test_fetch_comments is successfully completed")


# Mock tests
# GET
def test_fetch_post_mock():
    """Test fetching a post with mocked response."""
    logger.debug("Starting log for test_fetch_post_mock")
    mock_response = {
        "userId": "1",
        "id": "1",
        "title": "Mocked Title"
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = requests.get(f"{URL}/posts/1")
        assert response.status_code == 200
        assert response.json() == mock_response
        logger.debug("The test_fetch_post_mock is successfully completed")


def test_create_post_mock(post_data):
    """Creating POST with mocked response"""
    logger.debug("Starting log for test_create_post_mock")
    mock_response = post_data.copy()
    mock_response["id"] = 101
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response

        response = requests.post(f"{URL}/posts", json=post_data)
        assert response.status_code == 201
        assert response.json() == mock_response
        logger.debug("The test_create_post_mock is successfully completed")


def test_timeout_handling():
    """Timeout respond"""
    logger.debug("Starting log for test_timeout_handling")
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        try:
            requests.get(f"{URL}/posts/1", timeout=1)
        except requests.exceptions.Timeout:
            assert True, "Timeout exception"
            logger.debug("The test_timeout_handling is successfully completed")


# Run all tests
if __name__ == "__main__":
    pytest.main()
