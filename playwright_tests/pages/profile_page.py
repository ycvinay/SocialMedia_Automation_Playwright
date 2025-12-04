"""
Profile Page Object.
Handles all interactions with the user profile page.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
import logging

logger = logging.getLogger(__name__)


class ProfilePage(BasePage):
    """Profile page object for user profile testing."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.selectors = Selectors.Profile
        self.home_selectors = Selectors.Home
        self.url = URLs.Pages.profile()
    
    def navigate(self):
        """Navigate to own profile page."""
        super().navigate(self.url)
        logger.info("Navigated to profile page")
    
    def navigate_to_user_profile(self, user_id: int):
        """Navigate to another user's profile."""
        url = f"{URLs.BASE_URL}/views/user-profile.html?userId={user_id}"
        super().navigate(url)
        logger.info(f"Navigated to user profile: {user_id}")
    
    def is_on_profile_page(self):
        """Check if currently on profile page."""
        return "profile.html" in self.page.url or "user-profile.html" in self.page.url
    
    # ==================== PROFILE INFO ====================
    def get_profile_name(self):
        """Get profile display name."""
        name_elem = self.page.locator("#displayName, .profile-name")
        if name_elem.count() > 0:
            return name_elem.first.text_content()
        return None
    
    def get_profile_username(self):
        """Get profile username."""
        username_elem = self.page.locator("#userName, .profile-username")
        if username_elem.count() > 0:
            return username_elem.first.text_content()
        return None
    
    def get_profile_bio(self):
        """Get profile bio."""
        bio_elem = self.page.locator("#userBio, .profile-bio")
        if bio_elem.count() > 0:
            return bio_elem.first.text_content()
        return None
    
    def get_avatar_src(self):
        """Get profile avatar image source."""
        avatar = self.page.locator("#profileAvatar, .avatar-img")
        if avatar.count() > 0:
            return avatar.first.get_attribute("src")
        return None
    
    def is_avatar_visible(self):
        """Check if profile avatar is visible."""
        return self.is_visible("#profileAvatar, .avatar-img")
    
    # ==================== PROFILE STATS ====================
    def get_posts_count(self):
        """Get user's posts count."""
        count_elem = self.page.locator(".posts-count, #postsCount")
        if count_elem.count() > 0:
            text = count_elem.first.text_content()
            # Extract number from text
            import re
            match = re.search(r'\d+', text)
            return int(match.group()) if match else 0
        return 0
    
    def get_friends_count(self):
        """Get user's friends count."""
        count_elem = self.page.locator(".friends-count, #friendsCount")
        if count_elem.count() > 0:
            text = count_elem.first.text_content()
            import re
            match = re.search(r'\d+', text)
            return int(match.group()) if match else 0
        return 0
    
    # ==================== EDIT PROFILE ====================
    def is_edit_button_visible(self):
        """Check if edit profile button is visible (own profile)."""
        return self.is_visible("[data-bs-target='#editModal'], #editProfileBtn, .edit-profile-btn")
    
    def click_edit_profile(self):
        """Click edit profile button."""
        logger.info("Clicking edit profile button")
        self.click("[data-bs-target='#editModal'], #editProfileBtn")
        self.wait_for_timeout(500)
    
    def is_edit_modal_visible(self):
        """Check if edit profile modal is visible."""
        return self.is_visible("#editModal")
    
    def enter_edit_name(self, name: str):
        """Enter name in edit modal."""
        self.fill("#editName", name)
    
    def enter_edit_bio(self, bio: str):
        """Enter bio in edit modal."""
        self.fill("#editBio", bio)
    
    def upload_avatar(self, image_path: str):
        """Upload avatar image."""
        logger.info(f"Uploading avatar: {image_path}")
        self.upload_file("#editAvatar, input[type='file']", image_path)
    
    def save_profile_changes(self):
        """Save profile changes."""
        logger.info("Saving profile changes")
        self.click("#saveEditBtn, .save-profile-btn")
        self.wait_for_timeout(2000)
    
    def cancel_edit(self):
        """Cancel edit and close modal."""
        close_btn = self.page.locator("#editModal .btn-close, #editModal [data-bs-dismiss='modal']")
        if close_btn.count() > 0:
            close_btn.first.click()
            self.wait_for_timeout(300)
    
    def update_profile(self, name: str = None, bio: str = None, avatar_path: str = None):
        """
        Update profile with new information.
        
        Args:
            name: New display name
            bio: New bio text
            avatar_path: Path to new avatar image
        """
        logger.info("Updating profile")
        self.click_edit_profile()
        self.wait_for_timeout(500)
        
        if name:
            self.enter_edit_name(name)
        
        if bio:
            self.enter_edit_bio(bio)
        
        if avatar_path:
            self.upload_avatar(avatar_path)
        
        self.save_profile_changes()
    
    # ==================== USER POSTS ====================
    def get_user_posts_count(self):
        """Get number of posts displayed on profile."""
        return self.count_elements(".post-card, .post")
    
    def is_posts_section_visible(self):
        """Check if posts section is visible."""
        return self.is_visible("#userPosts, .user-posts, .posts-section")
    
    def get_first_post_content(self):
        """Get content of first post on profile."""
        posts = self.page.locator(".post-card, .post")
        if posts.count() > 0:
            content = posts.first.locator(".post-content, .post-text")
            if content.count() > 0:
                return content.first.text_content()
        return None
    
    def like_post(self, post_index: int = 0):
        """Like a post on the profile."""
        posts = self.page.locator(".post-card, .post")
        if posts.count() > post_index:
            like_btn = posts.nth(post_index).locator(".like-btn")
            like_btn.click()
            self.wait_for_timeout(500)
            return True
        return False
    
    def open_post_comments(self, post_index: int = 0):
        """Open comments for a post."""
        posts = self.page.locator(".post-card, .post")
        if posts.count() > post_index:
            comment_btn = posts.nth(post_index).locator(".comment-btn")
            comment_btn.click()
            self.wait_for_timeout(500)
    
    def delete_post(self, post_index: int = 0):
        """Delete a post from profile."""
        logger.info(f"Deleting post at index {post_index}")
        posts = self.page.locator(".post-card, .post")
        if posts.count() > post_index:
            # Open dropdown
            dropdown_btn = posts.nth(post_index).locator(".dropdown-toggle, .post-options-btn")
            if dropdown_btn.count() > 0:
                dropdown_btn.first.click()
                self.wait_for_timeout(300)
                
                # Click delete
                delete_btn = self.page.locator(".delete-post-btn, [onclick*='delete']")
                if delete_btn.count() > 0:
                    delete_btn.first.click()
                    self.wait_for_timeout(1000)
                    return True
        return False
    
    def edit_post(self, post_index: int, new_content: str):
        """Edit a post on profile."""
        logger.info(f"Editing post at index {post_index}")
        posts = self.page.locator(".post-card, .post")
        if posts.count() > post_index:
            # Open dropdown
            dropdown_btn = posts.nth(post_index).locator(".dropdown-toggle, .post-options-btn")
            if dropdown_btn.count() > 0:
                dropdown_btn.first.click()
                self.wait_for_timeout(300)
                
                # Click edit
                edit_btn = self.page.locator(".edit-post-btn, [onclick*='openEditPostModal']")
                if edit_btn.count() > 0:
                    edit_btn.first.click()
                    self.wait_for_timeout(500)
                    
                    # Fill new content
                    self.fill("#editPostContent", new_content)
                    self.click("#editPostForm button[type='submit'], #saveEditPost")
                    self.wait_for_timeout(1000)
                    return True
        return False
    
    # ==================== FRIEND ACTIONS (Other user's profile) ====================
    def is_add_friend_button_visible(self):
        """Check if add friend button is visible."""
        return self.is_visible(".add-friend-btn, #addFriendBtn")
    
    def is_remove_friend_button_visible(self):
        """Check if remove friend button is visible."""
        return self.is_visible(".remove-friend-btn, #removeFriendBtn")
    
    def is_pending_request_visible(self):
        """Check if pending request status is visible."""
        return self.is_visible(".cancel-request-btn, .pending-badge")
    
    def click_add_friend(self):
        """Click add friend button."""
        logger.info("Clicking add friend")
        self.click(".add-friend-btn, #addFriendBtn")
        self.wait_for_timeout(1000)
    
    def click_remove_friend(self):
        """Click remove friend button."""
        logger.info("Clicking remove friend")
        self.click(".remove-friend-btn, #removeFriendBtn")
        self.wait_for_timeout(1000)
    
    def click_cancel_request(self):
        """Click cancel friend request button."""
        self.click(".cancel-request-btn")
        self.wait_for_timeout(1000)
    
    def get_friendship_status(self):
        """Get current friendship status with user."""
        if self.is_visible(".remove-friend-btn, .unfriend-btn"):
            return "friends"
        elif self.is_visible(".cancel-request-btn, .pending-badge"):
            return "pending"
        elif self.is_visible(".accept-btn"):
            return "received"
        elif self.is_visible(".add-friend-btn"):
            return "none"
        return "unknown"
    
    # ==================== VALIDATION ====================
    def is_profile_loaded(self):
        """Check if profile page has loaded properly."""
        return (
            self.is_visible("#displayName, .profile-name") or
            self.is_visible("#userName, .profile-username")
        )
    
    def is_own_profile(self):
        """Check if viewing own profile (edit button visible)."""
        return self.is_edit_button_visible()
    
    def is_success_toast_visible(self):
        """Check if success toast is visible."""
        return self.is_visible(".toast.show, .alert-success")
    
    def is_error_toast_visible(self):
        """Check if error toast is visible."""
        return self.is_visible(".toast-error, .alert-danger")
