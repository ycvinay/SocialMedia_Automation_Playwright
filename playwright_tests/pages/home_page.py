"""
Home/Feed Page Object.
Handles all interactions with the home feed page including posts, likes, and comments.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
import logging

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Home/Feed page object."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.selectors = Selectors.Home
        self.nav_selectors = Selectors.NavBar
        self.url = URLs.Pages.home()
    
    def navigate(self):
        """Navigate to home page."""
        super().navigate(self.url)
        logger.info("Navigated to home page")
    
    def is_on_home_page(self):
        """Check if currently on home page."""
        return "home.html" in self.page.url
    
    # ==================== POST CREATION ====================
    def is_post_input_visible(self):
        """Check if post input/trigger is visible."""
        return self.is_visible("#postInput") or self.is_visible(self.selectors.CREATE_POST_TEXTAREA)
    
    def click_post_input(self):
        """Click on post input to open modal."""
        self.click("#postInput")
        self.wait_for_timeout(500)
    
    def is_post_modal_visible(self):
        """Check if post creation modal is visible."""
        return self.is_visible("#postModal")
    
    def enter_post_content(self, content: str):
        """Enter content in post textarea."""
        logger.info(f"Entering post content: {content[:50]}...")
        self.fill("#postText", content)
    
    def attach_image(self, image_path: str):
        """Attach image to post."""
        logger.info(f"Attaching image: {image_path}")
        self.upload_file("#imageInput", image_path)
    
    def click_submit_post(self):
        """Click submit post button."""
        self.click("#submitPost")
        self.wait_for_timeout(2000)
    
    def create_post(self, content: str, image_path: str = None):
        """
        Create a new post.
        
        Args:
            content: Post content
            image_path: Optional image path
        """
        logger.info(f"Creating post: {content[:50]}...")
        
        # Click on post input to open modal
        self.click_post_input()
        self.wait_for_timeout(500)
        
        # Enter content
        self.enter_post_content(content)
        
        if image_path:
            self.attach_image(image_path)
        
        # Submit
        self.click_submit_post()
        self.wait_for_timeout(2000)
    
    def close_post_modal(self):
        """Close the post creation modal."""
        self.click("#closeModal")
        self.wait_for_timeout(300)
    
    # ==================== FEED INTERACTIONS ====================
    def get_post_count(self):
        """Get number of posts in feed."""
        return self.count_elements(self.selectors.POST_CARD)
    
    def is_feed_loaded(self):
        """Check if feed has loaded with posts."""
        self.wait_for_timeout(2000)
        return self.get_post_count() > 0
    
    def get_first_post_content(self):
        """Get content of first post in feed."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > 0:
            return posts.first.locator(self.selectors.POST_CONTENT).text_content()
        return None
    
    def get_post_at_index(self, index: int):
        """Get post element at specific index."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > index:
            return posts.nth(index)
        return None
    
    # ==================== LIKE FUNCTIONALITY ====================
    def like_post(self, post_index: int = 0):
        """Like a post by index."""
        logger.info(f"Liking post at index {post_index}")
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            like_btn = posts.nth(post_index).locator(self.selectors.LIKE_BUTTON)
            like_btn.click()
            self.wait_for_timeout(1000)
            return True
        return False
    
    def unlike_post(self, post_index: int = 0):
        """Unlike a post by index (same as clicking like again)."""
        return self.like_post(post_index)
    
    def get_like_count(self, post_index: int = 0):
        """Get like count for a post."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            like_count_elem = posts.nth(post_index).locator(self.selectors.LIKE_COUNT)
            if like_count_elem.count() > 0:
                return like_count_elem.text_content()
        return "0"
    
    def is_post_liked(self, post_index: int = 0):
        """Check if post is liked (button has active state)."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            like_btn = posts.nth(post_index).locator(self.selectors.LIKE_BUTTON)
            classes = like_btn.get_attribute("class") or ""
            return "liked" in classes or "active" in classes or "text-danger" in classes
        return False
    
    def open_likes_modal(self, post_index: int = 0):
        """Open modal showing who liked the post."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            like_count = posts.nth(post_index).locator(self.selectors.LIKE_COUNT)
            like_count.click()
            self.wait_for_timeout(500)
    
    # ==================== COMMENT FUNCTIONALITY ====================
    def open_comments_modal(self, post_index: int = 0):
        """Open comments modal for a post."""
        logger.info(f"Opening comments for post {post_index}")
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            comment_btn = posts.nth(post_index).locator(self.selectors.COMMENT_BUTTON)
            comment_btn.click()
            self.wait_for_timeout(500)
    
    def add_comment(self, post_index: int, comment: str):
        """Add comment to a post."""
        logger.info(f"Adding comment to post {post_index}: {comment}")
        
        # Open comments modal
        self.open_comments_modal(post_index)
        
        # Find comment input in modal and fill
        comment_input = self.page.locator("#commentText")
        if comment_input.is_visible():
            comment_input.fill(comment)
            
            # Submit comment
            submit_btn = self.page.locator("#submitComment")
            submit_btn.click()
            self.wait_for_timeout(1000)
            return True
        return False
    
    def get_comment_count(self, post_index: int = 0):
        """Get comment count for a post."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            comment_count_elem = posts.nth(post_index).locator(self.selectors.COMMENT_COUNT)
            if comment_count_elem.count() > 0:
                return comment_count_elem.text_content()
        return "0"
    
    def is_comments_modal_visible(self):
        """Check if comments modal is visible."""
        return self.is_visible("#commentsModal")
    
    def close_comments_modal(self):
        """Close comments modal."""
        modal = self.page.locator("#commentsModal")
        if modal.is_visible():
            close_btn = modal.locator(".btn-close, .close")
            if close_btn.count() > 0:
                close_btn.first.click()
                self.wait_for_timeout(300)
    
    # ==================== POST OPTIONS ====================
    def open_post_options(self, post_index: int = 0):
        """Open post options dropdown."""
        posts = self.page.locator(self.selectors.POST_CARD)
        if posts.count() > post_index:
            options_btn = posts.nth(post_index).locator(".post-options-btn, .dropdown-toggle")
            if options_btn.count() > 0:
                options_btn.first.click()
                self.wait_for_timeout(300)
    
    def delete_post(self, post_index: int = 0):
        """Delete a post."""
        logger.info(f"Deleting post at index {post_index}")
        self.open_post_options(post_index)
        delete_btn = self.page.locator(".delete-post-btn")
        if delete_btn.is_visible():
            delete_btn.click()
            self.wait_for_timeout(1000)
            return True
        return False
    
    def edit_post(self, post_index: int, new_content: str):
        """Edit a post."""
        logger.info(f"Editing post at index {post_index}")
        self.open_post_options(post_index)
        edit_btn = self.page.locator(".edit-post-btn")
        if edit_btn.is_visible():
            edit_btn.click()
            self.wait_for_timeout(500)
            
            # Fill new content
            edit_input = self.page.locator("#editPostContent")
            if edit_input.is_visible():
                edit_input.fill(new_content)
                self.page.locator("#saveEditPost").click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    # ==================== NAVIGATION ====================
    def click_navbar_home(self):
        """Click home link in navbar."""
        self.click(self.nav_selectors.HOME_LINK)
    
    def click_navbar_profile(self):
        """Click profile link in navbar."""
        self.click(self.nav_selectors.PROFILE_LINK)
    
    def click_navbar_friends(self):
        """Click friends link in navbar."""
        self.click(self.nav_selectors.FRIENDS_LINK)
    
    def click_navbar_explore(self):
        """Click explore link in navbar."""
        self.click(self.nav_selectors.EXPLORE_LINK)
    
    def click_navbar_notifications(self):
        """Click notifications link in navbar."""
        self.click(self.nav_selectors.NOTIFICATIONS_LINK)
    
    def click_logout(self):
        """Click logout button."""
        self.click(self.nav_selectors.LOGOUT_BUTTON)
        self.wait_for_timeout(1000)
    
    def is_user_logged_in(self):
        """Check if user is logged in (navbar visible)."""
        return self.is_visible(self.nav_selectors.LOGOUT_BUTTON)
    
    # ==================== USER INFO ====================
    def get_logged_in_username(self):
        """Get logged in user's username from navbar."""
        username_elem = self.page.locator("#navUsername, .nav-username")
        if username_elem.count() > 0:
            return username_elem.text_content()
        return None
    
    def get_user_avatar_src(self):
        """Get user avatar source from navbar."""
        avatar = self.page.locator(self.nav_selectors.USER_AVATAR)
        if avatar.count() > 0:
            return avatar.get_attribute("src")
        return None
