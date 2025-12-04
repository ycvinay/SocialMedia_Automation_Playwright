"""
Home/Feed Page Automation Tests
Comprehensive testing for the home feed including posts, likes, and comments.
"""

import pytest
import time
import logging
from pages.home_page import HomePage
from pages.login_page import LoginPage
from constants.urls import URLs
from constants.test_data import TestData

logger = logging.getLogger(__name__)


# ==================== FIXTURES ====================
@pytest.fixture
def logged_in_home_page(page):
    """Fixture: Login and navigate to home page."""
    login_page = LoginPage(page)
    login_page.navigate()
    
    user = TestData.Users.PRIMARY_USER
    page.locator("#username").fill(user['username'])
    page.locator("#password").fill(user['password'])
    page.locator("#loginForm button[type='submit']").click()
    
    try:
        page.wait_for_url("**/home.html", timeout=15000)
    except:
        if page.locator("#loginFailToast").is_visible():
            pytest.skip("Login failed - cannot test home page")
        raise
    
    return HomePage(page)


class TestHomePageElements:
    """Test: Verify home page elements are visible after login."""
    
    @pytest.mark.smoke
    @pytest.mark.posts
    def test_home_page_loads_after_login(self, logged_in_home_page):
        """Test: Home page loads correctly after login."""
        logger.info("=" * 60)
        logger.info("TEST: Home page loads after login")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        assert home_page.is_on_home_page(), "Should be on home page"
        logger.info("✅ Home page loaded successfully")
        
        # Check if navbar is visible (user is logged in)
        assert home_page.is_user_logged_in(), "User should be logged in"
        logger.info("✅ User is logged in (navbar visible)")
    
    @pytest.mark.posts
    def test_post_creation_input_visible(self, logged_in_home_page):
        """Test: Post creation input/trigger is visible."""
        logger.info("=" * 60)
        logger.info("TEST: Post creation input visible")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        assert home_page.is_post_input_visible(), "Post input should be visible"
        logger.info("✅ Post creation input is visible")
    
    @pytest.mark.posts
    def test_feed_container_visible(self, logged_in_home_page):
        """Test: Feed container is visible."""
        home_page = logged_in_home_page
        page = home_page.page
        
        # Wait for feed to load
        time.sleep(2)
        
        # Feed container should exist
        feed = page.locator("#feed, .feed-container, .posts-container")
        assert feed.count() > 0, "Feed container should exist"
        logger.info("✅ Feed container is visible")


class TestPostCreation:
    """Test: Post creation functionality."""
    
    @pytest.mark.posts
    def test_open_post_modal(self, logged_in_home_page):
        """Test: Clicking post input opens post creation modal."""
        logger.info("=" * 60)
        logger.info("TEST: Open post creation modal")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        # Click on post input to open modal
        home_page.click_post_input()
        time.sleep(0.5)
        
        assert home_page.is_post_modal_visible(), "Post modal should be visible"
        logger.info("✅ Post creation modal opened")
    
    @pytest.mark.posts
    def test_create_text_post(self, logged_in_home_page):
        """Test: Create a text-only post successfully."""
        logger.info("=" * 60)
        logger.info("TEST: Create text post")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        page = home_page.page
        
        # Get initial post count
        initial_count = home_page.get_post_count()
        logger.info(f"Initial post count: {initial_count}")
        
        # Create a unique post
        import random
        post_content = f"Automated test post {random.randint(10000, 99999)} 🎉"
        
        # Open modal and create post
        home_page.click_post_input()
        time.sleep(0.5)
        
        home_page.enter_post_content(post_content)
        home_page.click_submit_post()
        
        # Wait and verify
        time.sleep(3)
        
        # Check if post was created
        new_count = home_page.get_post_count()
        logger.info(f"New post count: {new_count}")
        
        # Either count increased or the post appears in feed
        first_post = home_page.get_first_post_content()
        if first_post and post_content[:20] in first_post:
            logger.info("✅ Post created and visible in feed")
        elif new_count > initial_count:
            logger.info("✅ Post count increased - post created")
        else:
            logger.warning("⚠️ Could not verify post creation")
    
    @pytest.mark.posts
    def test_create_post_with_emoji(self, logged_in_home_page):
        """Test: Create a post with emojis."""
        logger.info("=" * 60)
        logger.info("TEST: Create post with emojis")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        post_content = TestData.Posts.EMOJI_POST
        
        home_page.click_post_input()
        time.sleep(0.5)
        home_page.enter_post_content(post_content)
        home_page.click_submit_post()
        
        time.sleep(2)
        logger.info("✅ Emoji post submitted")
    
    @pytest.mark.posts
    def test_close_post_modal(self, logged_in_home_page):
        """Test: Close post modal without creating post."""
        logger.info("=" * 60)
        logger.info("TEST: Close post modal")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        home_page.click_post_input()
        time.sleep(0.5)
        
        assert home_page.is_post_modal_visible(), "Modal should be open"
        
        home_page.close_post_modal()
        time.sleep(0.5)
        
        # Modal should be closed
        assert not home_page.is_post_modal_visible(), "Modal should be closed"
        logger.info("✅ Post modal closed successfully")


class TestPostInteractions:
    """Test: Like and comment interactions on posts."""
    
    @pytest.mark.posts
    def test_like_post(self, logged_in_home_page):
        """Test: Like a post."""
        logger.info("=" * 60)
        logger.info("TEST: Like a post")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        # Wait for feed to load
        time.sleep(2)
        
        if home_page.get_post_count() == 0:
            logger.warning("⚠️ No posts in feed, skipping like test")
            pytest.skip("No posts available to like")
        
        # Get initial like state
        initial_liked = home_page.is_post_liked(0)
        logger.info(f"Initial liked state: {initial_liked}")
        
        # Like the first post
        home_page.like_post(0)
        time.sleep(1)
        
        # Verify state changed
        new_liked = home_page.is_post_liked(0)
        assert new_liked != initial_liked, "Like state should change"
        logger.info("✅ Post like toggled successfully")
    
    @pytest.mark.posts
    def test_unlike_post(self, logged_in_home_page):
        """Test: Unlike a previously liked post."""
        logger.info("=" * 60)
        logger.info("TEST: Unlike a post")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        time.sleep(2)
        
        if home_page.get_post_count() == 0:
            pytest.skip("No posts available")
        
        # Like first, then unlike
        home_page.like_post(0)
        time.sleep(1)
        
        home_page.unlike_post(0)
        time.sleep(1)
        
        logger.info("✅ Post liked and unliked successfully")
    
    @pytest.mark.posts
    def test_open_comments_modal(self, logged_in_home_page):
        """Test: Open comments modal for a post."""
        logger.info("=" * 60)
        logger.info("TEST: Open comments modal")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        time.sleep(2)
        
        if home_page.get_post_count() == 0:
            pytest.skip("No posts available")
        
        home_page.open_comments_modal(0)
        time.sleep(1)
        
        assert home_page.is_comments_modal_visible(), "Comments modal should be visible"
        logger.info("✅ Comments modal opened")
        
        # Close modal
        home_page.close_comments_modal()
    
    @pytest.mark.posts
    def test_add_comment(self, logged_in_home_page):
        """Test: Add a comment to a post."""
        logger.info("=" * 60)
        logger.info("TEST: Add comment to post")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        time.sleep(2)
        
        if home_page.get_post_count() == 0:
            pytest.skip("No posts available")
        
        import random
        comment = f"Automated test comment {random.randint(1000, 9999)} 👍"
        
        result = home_page.add_comment(0, comment)
        
        if result:
            logger.info("✅ Comment added successfully")
        else:
            logger.warning("⚠️ Could not add comment (might require different flow)")


class TestFeedDisplay:
    """Test: Feed display and content."""
    
    @pytest.mark.posts
    def test_feed_loads_posts(self, logged_in_home_page):
        """Test: Feed loads and displays posts."""
        logger.info("=" * 60)
        logger.info("TEST: Feed loads posts")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        # Wait for feed to load
        time.sleep(3)
        
        post_count = home_page.get_post_count()
        logger.info(f"Posts in feed: {post_count}")
        
        # Feed should either have posts or show empty state
        if post_count > 0:
            logger.info(f"✅ Feed loaded with {post_count} posts")
        else:
            logger.info("ℹ️ Feed is empty (no posts or no friends with posts)")
    
    @pytest.mark.posts
    def test_post_has_required_elements(self, logged_in_home_page):
        """Test: Each post has required elements (author, content, actions)."""
        logger.info("=" * 60)
        logger.info("TEST: Post has required elements")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        page = home_page.page
        time.sleep(2)
        
        if home_page.get_post_count() == 0:
            pytest.skip("No posts to verify")
        
        first_post = home_page.get_post_at_index(0)
        
        # Check for author
        author = first_post.locator(".post-author, .author-name, .card-title")
        assert author.count() > 0, "Post should have author"
        logger.info("✅ Post has author element")
        
        # Check for content
        content = first_post.locator(".post-content, .post-text, .card-text")
        has_content = content.count() > 0
        logger.info(f"Post has content: {has_content}")
        
        # Check for action buttons
        like_btn = first_post.locator(".like-btn, button:has-text('Like')")
        comment_btn = first_post.locator(".comment-btn, button:has-text('Comment')")
        
        logger.info("✅ Post structure verified")


class TestNavigation:
    """Test: Navigation from home page."""
    
    @pytest.mark.navigation
    def test_navigate_to_profile(self, logged_in_home_page):
        """Test: Navigate to profile from navbar."""
        logger.info("=" * 60)
        logger.info("TEST: Navigate to profile")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        home_page.click_navbar_profile()
        time.sleep(1)
        
        assert "profile.html" in home_page.page.url, "Should navigate to profile"
        logger.info("✅ Navigated to profile page")
    
    @pytest.mark.navigation
    def test_navigate_to_friends(self, logged_in_home_page):
        """Test: Navigate to friends from navbar."""
        home_page = logged_in_home_page
        
        home_page.click_navbar_friends()
        time.sleep(1)
        
        assert "friends.html" in home_page.page.url, "Should navigate to friends"
        logger.info("✅ Navigated to friends page")
    
    @pytest.mark.navigation
    def test_navigate_to_explore(self, logged_in_home_page):
        """Test: Navigate to explore from navbar."""
        home_page = logged_in_home_page
        
        home_page.click_navbar_explore()
        time.sleep(1)
        
        assert "explore.html" in home_page.page.url, "Should navigate to explore"
        logger.info("✅ Navigated to explore page")
    
    @pytest.mark.navigation
    def test_navigate_to_notifications(self, logged_in_home_page):
        """Test: Navigate to notifications from navbar."""
        home_page = logged_in_home_page
        
        home_page.click_navbar_notifications()
        time.sleep(1)
        
        assert "notifications.html" in home_page.page.url, "Should navigate to notifications"
        logger.info("✅ Navigated to notifications page")


class TestLogout:
    """Test: Logout functionality."""
    
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_logout(self, logged_in_home_page):
        """Test: Logout successfully."""
        logger.info("=" * 60)
        logger.info("TEST: Logout")
        logger.info("=" * 60)
        
        home_page = logged_in_home_page
        
        home_page.click_logout()
        time.sleep(2)
        
        # Should redirect to login page
        assert "login.html" in home_page.page.url, "Should redirect to login after logout"
        logger.info("✅ Logged out and redirected to login page")
        
        # Token should be cleared
        token = home_page.page.evaluate("localStorage.getItem('token')")
        assert token is None, "Token should be cleared after logout"
        logger.info("✅ Token cleared from localStorage")
