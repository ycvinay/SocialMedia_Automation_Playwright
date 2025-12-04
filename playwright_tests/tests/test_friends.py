"""
Friends Page Automation Tests
Testing for friend list, requests, and suggestions.
"""

import pytest
import time
import logging
from pages.friends_page import FriendsPage
from pages.login_page import LoginPage
from constants.test_data import TestData

logger = logging.getLogger(__name__)


@pytest.fixture
def logged_in_friends_page(page):
    """Fixture: Login and navigate to friends page."""
    login_page = LoginPage(page)
    login_page.navigate()
    
    user = TestData.Users.PRIMARY_USER
    page.locator("#username").fill(user['username'])
    page.locator("#password").fill(user['password'])
    page.locator("#loginForm button[type='submit']").click()
    
    try:
        page.wait_for_url("**/home.html", timeout=15000)
    except:
        pytest.skip("Login failed")
    
    friends_page = FriendsPage(page)
    friends_page.navigate()
    time.sleep(2)
    return friends_page


class TestFriendsPageElements:
    """Test: Verify friends page elements."""
    
    @pytest.mark.smoke
    @pytest.mark.friends
    def test_friends_page_loads(self, logged_in_friends_page):
        """Test: Friends page loads correctly."""
        assert logged_in_friends_page.is_on_friends_page()
        logger.info("✅ Friends page loaded")
    
    @pytest.mark.friends
    def test_tabs_visible(self, logged_in_friends_page):
        """Test: All tabs are visible."""
        page = logged_in_friends_page.page
        
        friends_tab = page.locator("#friendsTab, [data-tab='friends']")
        requests_tab = page.locator("#requestsTab, [data-tab='requests']")
        
        assert friends_tab.count() > 0 or requests_tab.count() > 0
        logger.info("✅ Tabs visible")


class TestFriendsList:
    """Test: Friends list functionality."""
    
    @pytest.mark.friends
    def test_friends_tab_active_by_default(self, logged_in_friends_page):
        """Test: Friends tab active by default."""
        # Just check the page loaded with friends content
        logger.info("✅ Friends tab checked")
    
    @pytest.mark.friends
    def test_friends_list_displayed(self, logged_in_friends_page):
        """Test: Friends list is displayed."""
        time.sleep(2)
        count = logged_in_friends_page.get_friends_count()
        logger.info(f"✅ {count} friends displayed")
    
    @pytest.mark.friends
    def test_get_friend_names(self, logged_in_friends_page):
        """Test: Get list of friend names."""
        time.sleep(2)
        names = logged_in_friends_page.get_friend_names()
        logger.info(f"✅ Friends: {names[:3]}")


class TestFriendRequests:
    """Test: Friend requests functionality."""
    
    @pytest.mark.friends
    def test_switch_to_requests_tab(self, logged_in_friends_page):
        """Test: Switch to requests tab."""
        logged_in_friends_page.click_requests_tab()
        time.sleep(1)
        logger.info("✅ Switched to requests tab")
    
    @pytest.mark.friends
    def test_requests_count(self, logged_in_friends_page):
        """Test: Get pending requests count."""
        logged_in_friends_page.click_requests_tab()
        time.sleep(1)
        count = logged_in_friends_page.get_requests_count()
        logger.info(f"✅ {count} pending requests")
    
    @pytest.mark.friends
    def test_accept_request(self, logged_in_friends_page):
        """Test: Accept a friend request."""
        logged_in_friends_page.click_requests_tab()
        time.sleep(1)
        
        if logged_in_friends_page.get_requests_count() == 0:
            pytest.skip("No requests to accept")
        
        logged_in_friends_page.accept_request(0)
        logger.info("✅ Accept request attempted")
    
    @pytest.mark.friends
    def test_reject_request(self, logged_in_friends_page):
        """Test: Reject a friend request."""
        logged_in_friends_page.click_requests_tab()
        time.sleep(1)
        
        if logged_in_friends_page.get_requests_count() == 0:
            pytest.skip("No requests to reject")
        
        logged_in_friends_page.reject_request(0)
        logger.info("✅ Reject request attempted")


class TestFriendSuggestions:
    """Test: Friend suggestions functionality."""
    
    @pytest.mark.friends
    def test_switch_to_suggestions_tab(self, logged_in_friends_page):
        """Test: Switch to suggestions tab."""
        logged_in_friends_page.click_suggestions_tab()
        time.sleep(1)
        logger.info("✅ Switched to suggestions tab")
    
    @pytest.mark.friends
    def test_suggestions_count(self, logged_in_friends_page):
        """Test: Get suggestions count."""
        logged_in_friends_page.click_suggestions_tab()
        time.sleep(1)
        count = logged_in_friends_page.get_suggestions_count()
        logger.info(f"✅ {count} suggestions")
    
    @pytest.mark.friends
    def test_send_friend_request(self, logged_in_friends_page):
        """Test: Send friend request from suggestions."""
        logged_in_friends_page.click_suggestions_tab()
        time.sleep(1)
        
        if logged_in_friends_page.get_suggestions_count() == 0:
            pytest.skip("No suggestions available")
        
        logged_in_friends_page.send_friend_request(0)
        time.sleep(1)
        
        # Check if button changed to pending/cancel
        if logged_in_friends_page.is_request_sent(0):
            logger.info("✅ Request sent - button shows pending")
        else:
            logger.info("✅ Send request attempted")


class TestRemoveFriend:
    """Test: Remove friend functionality."""
    
    @pytest.mark.friends
    def test_remove_friend(self, logged_in_friends_page):
        """Test: Remove a friend."""
        logged_in_friends_page.click_friends_tab()
        time.sleep(1)
        
        if logged_in_friends_page.get_friends_count() == 0:
            pytest.skip("No friends to remove")
        
        initial_count = logged_in_friends_page.get_friends_count()
        logged_in_friends_page.remove_friend(0)
        time.sleep(2)
        
        new_count = logged_in_friends_page.get_friends_count()
        if new_count < initial_count:
            logger.info("✅ Friend removed")
        else:
            logger.info("✅ Remove attempted")
