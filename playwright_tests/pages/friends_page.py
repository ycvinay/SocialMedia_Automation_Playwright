"""
Friends Page Object.
Handles all interactions with the friends page including friend list, requests, and suggestions.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
import logging

logger = logging.getLogger(__name__)


class FriendsPage(BasePage):
    """Friends page object for friend management testing."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.selectors = Selectors.Friends
        self.url = URLs.Pages.friends()
    
    def navigate(self):
        """Navigate to friends page."""
        super().navigate(self.url)
        logger.info("Navigated to friends page")
    
    def is_on_friends_page(self):
        """Check if currently on friends page."""
        return "friends.html" in self.page.url
    
    # ==================== TAB NAVIGATION ====================
    def click_friends_tab(self):
        """Click the Friends tab."""
        logger.info("Clicking Friends tab")
        tab = self.page.locator("#friendsTab, [data-tab='friends'], .nav-link:has-text('Friends')")
        if tab.count() > 0:
            tab.first.click()
            self.wait_for_timeout(500)
    
    def click_requests_tab(self):
        """Click the Friend Requests tab."""
        logger.info("Clicking Requests tab")
        tab = self.page.locator("#requestsTab, [data-tab='requests'], .nav-link:has-text('Requests')")
        if tab.count() > 0:
            tab.first.click()
            self.wait_for_timeout(500)
    
    def click_suggestions_tab(self):
        """Click the Suggestions tab."""
        logger.info("Clicking Suggestions tab")
        tab = self.page.locator("#suggestionsTab, [data-tab='suggestions'], .nav-link:has-text('Suggestions')")
        if tab.count() > 0:
            tab.first.click()
            self.wait_for_timeout(500)
    
    def is_friends_tab_active(self):
        """Check if Friends tab is active."""
        tab = self.page.locator("#friendsTab.active, [data-tab='friends'].active")
        return tab.count() > 0
    
    def is_requests_tab_active(self):
        """Check if Requests tab is active."""
        tab = self.page.locator("#requestsTab.active, [data-tab='requests'].active")
        return tab.count() > 0
    
    def is_suggestions_tab_active(self):
        """Check if Suggestions tab is active."""
        tab = self.page.locator("#suggestionsTab.active, [data-tab='suggestions'].active")
        return tab.count() > 0
    
    # ==================== FRIENDS LIST ====================
    def get_friends_count(self):
        """Get number of friends displayed."""
        return self.count_elements(".friend-card, .friend-item, #friendsContainer .card")
    
    def get_friend_names(self):
        """Get list of friend names."""
        friends = self.page.locator(".friend-card .friend-name, .friend-item .friend-name, #friendsContainer .card-title")
        names = []
        for i in range(friends.count()):
            names.append(friends.nth(i).text_content())
        return names
    
    def is_friend_visible(self, username: str):
        """Check if a specific friend is visible in the list."""
        return self.is_visible(f".friend-card:has-text('{username}'), .friend-item:has-text('{username}')")
    
    def remove_friend(self, friend_index: int = 0):
        """Remove a friend by index."""
        logger.info(f"Removing friend at index {friend_index}")
        cards = self.page.locator(".friend-card, #friendsContainer .card")
        if cards.count() > friend_index:
            remove_btn = cards.nth(friend_index).locator(".remove-friend-btn, .unfriend-btn, button:has-text('Unfriend')")
            if remove_btn.count() > 0:
                remove_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def remove_friend_by_name(self, name: str):
        """Remove a friend by name."""
        logger.info(f"Removing friend: {name}")
        card = self.page.locator(f".friend-card:has-text('{name}'), #friendsContainer .card:has-text('{name}')")
        if card.count() > 0:
            remove_btn = card.locator(".remove-friend-btn, .unfriend-btn, button:has-text('Unfriend')")
            if remove_btn.count() > 0:
                remove_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def view_friend_profile(self, friend_index: int = 0):
        """Navigate to friend's profile."""
        cards = self.page.locator(".friend-card, #friendsContainer .card")
        if cards.count() > friend_index:
            # Click on the card or view profile button
            view_btn = cards.nth(friend_index).locator(".view-profile-btn, a.btn")
            if view_btn.count() > 0:
                view_btn.first.click()
            else:
                cards.nth(friend_index).click()
            self.wait_for_timeout(1000)
    
    def is_no_friends_message_visible(self):
        """Check if 'no friends' message is visible."""
        return self.is_visible(".no-friends-message, .empty-state:has-text('friend')")
    
    # ==================== FRIEND REQUESTS ====================
    def get_requests_count(self):
        """Get number of pending friend requests."""
        return self.count_elements(".request-card, .request-item, #requestsContainer .card")
    
    def get_request_sender_names(self):
        """Get list of request sender names."""
        requests = self.page.locator(".request-card .sender-name, .request-item .friend-name, #requestsContainer .card-title")
        names = []
        for i in range(requests.count()):
            names.append(requests.nth(i).text_content())
        return names
    
    def accept_request(self, request_index: int = 0):
        """Accept a friend request by index."""
        logger.info(f"Accepting request at index {request_index}")
        cards = self.page.locator(".request-card, #requestsContainer .card")
        if cards.count() > request_index:
            accept_btn = cards.nth(request_index).locator(".accept-btn, button:has-text('Accept')")
            if accept_btn.count() > 0:
                accept_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def reject_request(self, request_index: int = 0):
        """Reject a friend request by index."""
        logger.info(f"Rejecting request at index {request_index}")
        cards = self.page.locator(".request-card, #requestsContainer .card")
        if cards.count() > request_index:
            reject_btn = cards.nth(request_index).locator(".reject-btn, button:has-text('Reject')")
            if reject_btn.count() > 0:
                reject_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def accept_request_by_name(self, name: str):
        """Accept a friend request by sender name."""
        logger.info(f"Accepting request from: {name}")
        card = self.page.locator(f".request-card:has-text('{name}'), #requestsContainer .card:has-text('{name}')")
        if card.count() > 0:
            accept_btn = card.locator(".accept-btn, button:has-text('Accept')")
            if accept_btn.count() > 0:
                accept_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def reject_request_by_name(self, name: str):
        """Reject a friend request by sender name."""
        logger.info(f"Rejecting request from: {name}")
        card = self.page.locator(f".request-card:has-text('{name}'), #requestsContainer .card:has-text('{name}')")
        if card.count() > 0:
            reject_btn = card.locator(".reject-btn, button:has-text('Reject')")
            if reject_btn.count() > 0:
                reject_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def is_no_requests_message_visible(self):
        """Check if 'no requests' message is visible."""
        return self.is_visible(".no-requests-message, .empty-state:has-text('request')")
    
    # ==================== SUGGESTIONS ====================
    def get_suggestions_count(self):
        """Get number of friend suggestions."""
        return self.count_elements(".suggestion-card, .user-card, #suggestionsContainer .card")
    
    def get_suggestion_names(self):
        """Get list of suggested user names."""
        suggestions = self.page.locator(".suggestion-card .user-name, .user-card .card-title, #suggestionsContainer .card-title")
        names = []
        for i in range(suggestions.count()):
            names.append(suggestions.nth(i).text_content())
        return names
    
    def send_friend_request(self, suggestion_index: int = 0):
        """Send friend request to a suggestion by index."""
        logger.info(f"Sending request to suggestion at index {suggestion_index}")
        cards = self.page.locator(".suggestion-card, .user-card, #suggestionsContainer .card")
        if cards.count() > suggestion_index:
            add_btn = cards.nth(suggestion_index).locator(".add-friend-btn, button:has-text('Add Friend'), button:has-text('Send Request')")
            if add_btn.count() > 0:
                add_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def send_request_to_user(self, username: str):
        """Send friend request to a specific user."""
        logger.info(f"Sending request to: {username}")
        card = self.page.locator(f".suggestion-card:has-text('{username}'), .user-card:has-text('{username}')")
        if card.count() > 0:
            add_btn = card.locator(".add-friend-btn, button:has-text('Add Friend')")
            if add_btn.count() > 0:
                add_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def cancel_sent_request(self, suggestion_index: int = 0):
        """Cancel a sent friend request."""
        cards = self.page.locator(".suggestion-card, .user-card, #suggestionsContainer .card")
        if cards.count() > suggestion_index:
            cancel_btn = cards.nth(suggestion_index).locator(".cancel-request-btn, button:has-text('Cancel')")
            if cancel_btn.count() > 0:
                cancel_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def is_request_sent(self, suggestion_index: int = 0):
        """Check if request is sent to a user (button shows 'Cancel' or 'Pending')."""
        cards = self.page.locator(".suggestion-card, .user-card, #suggestionsContainer .card")
        if cards.count() > suggestion_index:
            pending = cards.nth(suggestion_index).locator(".cancel-request-btn, button:has-text('Cancel'), button:has-text('Pending'), .pending-badge")
            return pending.count() > 0
        return False
    
    def is_no_suggestions_message_visible(self):
        """Check if 'no suggestions' message is visible."""
        return self.is_visible(".no-suggestions-message, .empty-state:has-text('suggestion')")
    
    def view_suggestion_profile(self, suggestion_index: int = 0):
        """Navigate to suggested user's profile."""
        cards = self.page.locator(".suggestion-card, .user-card, #suggestionsContainer .card")
        if cards.count() > suggestion_index:
            view_btn = cards.nth(suggestion_index).locator(".view-profile-btn, a.btn, .user-avatar")
            if view_btn.count() > 0:
                view_btn.first.click()
            else:
                cards.nth(suggestion_index).click()
            self.wait_for_timeout(1000)
    
    # ==================== PAGE VALIDATION ====================
    def is_page_loaded(self):
        """Check if friends page has loaded."""
        return (
            self.is_visible("#friendsTab, .nav-link:has-text('Friends')") or
            self.is_visible("#friendsContainer")
        )
    
    def wait_for_page_load(self):
        """Wait for friends page to load completely."""
        self.page.wait_for_load_state("networkidle")
        self.wait_for_timeout(1000)
    
    def is_success_toast_visible(self):
        """Check if success toast is visible."""
        return self.is_visible(".toast.show:has-text('success'), .alert-success")
    
    def is_error_toast_visible(self):
        """Check if error toast is visible."""
        return self.is_visible(".toast.show:has-text('error'), .alert-danger")
