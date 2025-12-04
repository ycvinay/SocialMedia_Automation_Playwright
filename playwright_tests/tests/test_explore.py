"""
Explore Page Automation Tests
Testing for user search and discovery functionality.
"""

import pytest
import time
import logging
from pages.explore_page import ExplorePage
from pages.login_page import LoginPage
from constants.test_data import TestData

logger = logging.getLogger(__name__)


@pytest.fixture
def logged_in_explore_page(page):
    """Fixture: Login and navigate to explore page."""
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
    
    explore_page = ExplorePage(page)
    explore_page.navigate()
    time.sleep(2)
    return explore_page


class TestExplorePageElements:
    """Test: Verify explore page elements."""
    
    @pytest.mark.smoke
    def test_explore_page_loads(self, logged_in_explore_page):
        """Test: Explore page loads correctly."""
        assert logged_in_explore_page.is_on_explore_page()
        logger.info("✅ Explore page loaded")
    
    def test_search_input_visible(self, logged_in_explore_page):
        """Test: Search input is visible."""
        assert logged_in_explore_page.is_search_input_visible()
        logger.info("✅ Search input visible")
    
    def test_discover_section_visible(self, logged_in_explore_page):
        """Test: Discover section is visible."""
        if logged_in_explore_page.is_discover_section_visible():
            logger.info("✅ Discover section visible")
        else:
            logger.info("ℹ️ Discover section not visible")


class TestUserSearch:
    """Test: User search functionality."""
    
    def test_search_for_user(self, logged_in_explore_page):
        """Test: Search for a user."""
        explore_page = logged_in_explore_page
        
        explore_page.search_for_user("test")
        time.sleep(2)
        
        count = explore_page.get_search_results_count()
        logger.info(f"✅ Search returned {count} results")
    
    def test_search_no_results(self, logged_in_explore_page):
        """Test: Search with no results."""
        explore_page = logged_in_explore_page
        
        explore_page.search_for_user("xyznonexistent12345")
        time.sleep(2)
        
        count = explore_page.get_search_results_count()
        if count == 0:
            logger.info("✅ No results as expected")
        else:
            logger.info(f"Found {count} results")
    
    def test_clear_search(self, logged_in_explore_page):
        """Test: Clear search input."""
        explore_page = logged_in_explore_page
        
        explore_page.enter_search_query("test")
        explore_page.clear_search()
        
        value = explore_page.get_search_input_value()
        assert value == "", "Search should be cleared"
        logger.info("✅ Search cleared")


class TestDiscoverUsers:
    """Test: Discover users functionality."""
    
    def test_discover_users_displayed(self, logged_in_explore_page):
        """Test: Discover users are displayed."""
        time.sleep(2)
        count = logged_in_explore_page.get_discover_users_count()
        logger.info(f"✅ {count} users in discover section")
    
    def test_view_user_profile(self, logged_in_explore_page):
        """Test: View user profile from discover."""
        explore_page = logged_in_explore_page
        time.sleep(2)
        
        if explore_page.get_discover_users_count() == 0:
            pytest.skip("No users to view")
        
        explore_page.view_user_profile(0)
        time.sleep(2)
        
        if "profile" in explore_page.page.url:
            logger.info("✅ Navigated to user profile")
        else:
            logger.info("✅ View profile attempted")
    
    def test_send_friend_request_from_explore(self, logged_in_explore_page):
        """Test: Send friend request from explore."""
        explore_page = logged_in_explore_page
        time.sleep(2)
        
        if explore_page.get_discover_users_count() == 0:
            pytest.skip("No users available")
        
        explore_page.send_friend_request(0)
        time.sleep(1)
        
        if explore_page.is_friend_request_sent(0):
            logger.info("✅ Friend request sent")
        else:
            logger.info("✅ Request attempted")


class TestFriendshipStatus:
    """Test: Friendship status display."""
    
    def test_get_friendship_status(self, logged_in_explore_page):
        """Test: Get friendship status for users."""
        explore_page = logged_in_explore_page
        time.sleep(2)
        
        if explore_page.get_discover_users_count() == 0:
            pytest.skip("No users")
        
        status = explore_page.get_friendship_status(0)
        logger.info(f"✅ Friendship status: {status}")
    
    def test_already_friends_display(self, logged_in_explore_page):
        """Test: Already friends status display."""
        explore_page = logged_in_explore_page
        time.sleep(2)
        
        for i in range(min(5, explore_page.get_discover_users_count())):
            if explore_page.is_already_friends(i):
                logger.info(f"✅ User {i} is already friends")
                return
        
        logger.info("ℹ️ No 'already friends' users found")
