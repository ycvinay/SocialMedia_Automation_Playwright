"""
Authentication Fixtures.
Reusable fixtures for authenticated user sessions.
"""

import pytest
from pages.login_page import LoginPage
from constants.test_data import TestData
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def authenticated_user(page):
    """
    Fixture that provides an authenticated user session.
    Logs in the primary test user before the test.
    
    Args:
        page: Playwright page object
        
    Yields:
        Authenticated page object
    """
    logger.info("Setting up authenticated user session")
    
    # Login
    login_page = LoginPage(page)
    user = TestData.Users.PRIMARY_USER
    
    login_page.navigate()
    login_page.login(user['username'], user['password'])
    
    # Verify login success
    assert login_page.is_login_successful(), "Authentication fixture: Login failed"
    
    logger.info("Authenticated user session ready")
    
    yield page
    
    # Teardown (optional)
    logger.info("Tearing down authenticated user session")


@pytest.fixture(scope="function")
def authenticated_secondary_user(page):
    """
    Fixture that provides an authenticated secondary user session.
    Useful for testing friend interactions.
    
    Args:
        page: Playwright page object
        
    Yields:
        Authenticated page object
    """
    logger.info("Setting up authenticated secondary user session")
    
    # Login
    login_page = LoginPage(page)
    user = TestData.Users.SECONDARY_USER
    
    login_page.navigate()
    login_page.login(user['username'], user['password'])
    
    # Verify login success
    assert login_page.is_login_successful(), "Authentication fixture: Login failed"
    
    logger.info("Authenticated secondary user session ready")
    
    yield page
    
    # Teardown (optional)
    logger.info("Tearing down authenticated secondary user session")


@pytest.fixture(scope="function")
def user_credentials():
    """
    Fixture that provides test user credentials.
    
    Returns:
        Dictionary with user credentials
    """
    return TestData.Users.PRIMARY_USER


@pytest.fixture(scope="function")
def random_user():
    """
    Fixture that provides random user data.
    Useful for signup tests.
    
    Returns:
        Dictionary with random user data
    """
    return TestData.generate_random_user()
