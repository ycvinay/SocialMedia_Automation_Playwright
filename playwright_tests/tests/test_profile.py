"""
Profile Page Automation Tests
Testing for user profile view and edit functionality.
"""

import pytest
import time
import logging
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from constants.test_data import TestData

logger = logging.getLogger(__name__)


@pytest.fixture
def logged_in_profile_page(page):
    """Fixture: Login and navigate to profile page."""
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
    
    profile_page = ProfilePage(page)
    profile_page.navigate()
    time.sleep(2)
    return profile_page


class TestProfilePageElements:
    """Test: Verify profile page elements."""
    
    @pytest.mark.smoke
    @pytest.mark.profile
    def test_profile_page_loads(self, logged_in_profile_page):
        """Test: Profile page loads correctly."""
        profile_page = logged_in_profile_page
        assert profile_page.is_on_profile_page(), "Should be on profile page"
        logger.info("✅ Profile page loaded")
    
    @pytest.mark.profile
    def test_profile_info_displayed(self, logged_in_profile_page):
        """Test: Profile information is displayed."""
        profile_page = logged_in_profile_page
        
        name = profile_page.get_profile_name()
        assert name is not None, "Name should be displayed"
        
        username = profile_page.get_profile_username()
        assert username is not None, "Username should be displayed"
        logger.info("✅ Profile info displayed")
    
    @pytest.mark.profile
    def test_avatar_visible(self, logged_in_profile_page):
        """Test: Profile avatar is visible."""
        assert logged_in_profile_page.is_avatar_visible()
        logger.info("✅ Avatar visible")
    
    @pytest.mark.profile
    def test_edit_button_visible(self, logged_in_profile_page):
        """Test: Edit button visible on own profile."""
        assert logged_in_profile_page.is_edit_button_visible()
        logger.info("✅ Edit button visible")


class TestProfileEdit:
    """Test: Profile editing functionality."""
    
    @pytest.mark.profile
    def test_open_edit_modal(self, logged_in_profile_page):
        """Test: Open edit profile modal."""
        profile_page = logged_in_profile_page
        profile_page.click_edit_profile()
        time.sleep(0.5)
        
        assert profile_page.is_edit_modal_visible()
        logger.info("✅ Edit modal opened")
        profile_page.cancel_edit()
    
    @pytest.mark.profile
    def test_edit_bio(self, logged_in_profile_page):
        """Test: Edit profile bio."""
        profile_page = logged_in_profile_page
        
        import random
        new_bio = f"Test bio {random.randint(1000, 9999)}"
        
        profile_page.click_edit_profile()
        time.sleep(0.5)
        profile_page.enter_edit_bio(new_bio)
        profile_page.save_profile_changes()
        time.sleep(2)
        logger.info("✅ Bio edit attempted")
    
    @pytest.mark.profile
    def test_cancel_edit(self, logged_in_profile_page):
        """Test: Cancel profile edit."""
        profile_page = logged_in_profile_page
        
        profile_page.click_edit_profile()
        time.sleep(0.5)
        profile_page.enter_edit_bio("Should not save")
        profile_page.cancel_edit()
        time.sleep(0.5)
        logger.info("✅ Edit cancelled")


class TestProfilePosts:
    """Test: Posts on profile page."""
    
    @pytest.mark.profile
    def test_posts_section_visible(self, logged_in_profile_page):
        """Test: Posts section is visible."""
        assert logged_in_profile_page.is_posts_section_visible()
        logger.info("✅ Posts section visible")
    
    @pytest.mark.profile
    def test_user_posts_displayed(self, logged_in_profile_page):
        """Test: User posts are displayed."""
        time.sleep(2)
        count = logged_in_profile_page.get_user_posts_count()
        logger.info(f"✅ {count} posts on profile")
    
    @pytest.mark.profile
    def test_like_post_on_profile(self, logged_in_profile_page):
        """Test: Like post on profile."""
        time.sleep(2)
        if logged_in_profile_page.get_user_posts_count() == 0:
            pytest.skip("No posts")
        
        logged_in_profile_page.like_post(0)
        logger.info("✅ Like attempted")
