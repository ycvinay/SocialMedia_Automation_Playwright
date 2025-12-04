"""
Explore Page Object.
Handles all interactions with the explore/search page for user discovery.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
import logging

logger = logging.getLogger(__name__)


class ExplorePage(BasePage):
    """Explore page object for user discovery and search testing."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.selectors = Selectors.Explore
        self.url = URLs.Pages.explore()
    
    def navigate(self):
        """Navigate to explore page."""
        super().navigate(self.url)
        logger.info("Navigated to explore page")
    
    def is_on_explore_page(self):
        """Check if currently on explore page."""
        return "explore.html" in self.page.url
    
    # ==================== SEARCH FUNCTIONALITY ====================
    def is_search_input_visible(self):
        """Check if search input is visible."""
        return self.is_visible("#searchInput, input[type='search'], .search-input")
    
    def enter_search_query(self, query: str):
        """Enter search query in search input."""
        logger.info(f"Entering search query: {query}")
        self.fill("#searchInput, input[type='search']", query)
    
    def click_search_button(self):
        """Click search button."""
        self.click(".search-btn, button[type='submit'], #searchBtn")
        self.wait_for_timeout(1000)
    
    def search_for_user(self, query: str):
        """Perform a user search."""
        logger.info(f"Searching for: {query}")
        self.enter_search_query(query)
        self.click_search_button()
        self.wait_for_timeout(1500)
    
    def clear_search(self):
        """Clear the search input."""
        search_input = self.page.locator("#searchInput, input[type='search']")
        if search_input.count() > 0:
            search_input.fill("")
    
    def get_search_input_value(self):
        """Get current value of search input."""
        search_input = self.page.locator("#searchInput, input[type='search']")
        if search_input.count() > 0:
            return search_input.input_value()
        return ""
    
    # ==================== SEARCH RESULTS ====================
    def get_search_results_count(self):
        """Get number of search results."""
        return self.count_elements(".user-card, .search-result-item, #searchResults .card")
    
    def is_search_results_visible(self):
        """Check if search results section is visible."""
        return self.is_visible("#searchResults, .search-results")
    
    def get_result_usernames(self):
        """Get list of usernames from search results."""
        results = self.page.locator(".user-card .username, .search-result-item .username, #searchResults .card-subtitle")
        usernames = []
        for i in range(results.count()):
            usernames.append(results.nth(i).text_content())
        return usernames
    
    def get_result_names(self):
        """Get list of names from search results."""
        results = self.page.locator(".user-card .user-name, .search-result-item .name, #searchResults .card-title")
        names = []
        for i in range(results.count()):
            names.append(results.nth(i).text_content())
        return names
    
    def is_user_in_results(self, username: str):
        """Check if a specific user is in the search results."""
        return self.is_visible(f".user-card:has-text('{username}'), #searchResults .card:has-text('{username}')")
    
    def is_no_results_message_visible(self):
        """Check if 'no results' message is visible."""
        return self.is_visible(".no-results-message, .empty-state:has-text('No users found')")
    
    # ==================== USER CARD ACTIONS ====================
    def view_user_profile(self, result_index: int = 0):
        """Navigate to user's profile from search results."""
        logger.info(f"Viewing profile at result index {result_index}")
        cards = self.page.locator(".user-card, #searchResults .card, #usersContainer .card")
        if cards.count() > result_index:
            # Click on avatar or view button
            view_btn = cards.nth(result_index).locator(".view-profile-btn, a.btn, .user-avatar")
            if view_btn.count() > 0:
                view_btn.first.click()
            else:
                cards.nth(result_index).click()
            self.wait_for_timeout(1000)
    
    def send_friend_request(self, result_index: int = 0):
        """Send friend request to user in search results."""
        logger.info(f"Sending friend request to user at index {result_index}")
        cards = self.page.locator(".user-card, #searchResults .card, #usersContainer .card")
        if cards.count() > result_index:
            add_btn = cards.nth(result_index).locator(".add-friend-btn, button:has-text('Add Friend'), button:has-text('Send Request')")
            if add_btn.count() > 0:
                add_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def send_request_to_username(self, username: str):
        """Send friend request to a specific username."""
        logger.info(f"Sending friend request to: {username}")
        card = self.page.locator(f".user-card:has-text('{username}'), #searchResults .card:has-text('{username}')")
        if card.count() > 0:
            add_btn = card.locator(".add-friend-btn, button:has-text('Add Friend')")
            if add_btn.count() > 0:
                add_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def cancel_friend_request(self, result_index: int = 0):
        """Cancel a sent friend request."""
        cards = self.page.locator(".user-card, #searchResults .card, #usersContainer .card")
        if cards.count() > result_index:
            cancel_btn = cards.nth(result_index).locator(".cancel-request-btn, button:has-text('Cancel')")
            if cancel_btn.count() > 0:
                cancel_btn.first.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def is_friend_request_sent(self, result_index: int = 0):
        """Check if friend request is sent to a user."""
        cards = self.page.locator(".user-card, #searchResults .card, #usersContainer .card")
        if cards.count() > result_index:
            pending = cards.nth(result_index).locator(".cancel-request-btn, button:has-text('Pending'), button:has-text('Cancel'), .pending-badge")
            return pending.count() > 0
        return False
    
    def is_already_friends(self, result_index: int = 0):
        """Check if already friends with a user."""
        cards = self.page.locator(".user-card, #searchResults .card, #usersContainer .card")
        if cards.count() > result_index:
            friends = cards.nth(result_index).locator(".friends-badge, button:has-text('Friends'), .remove-friend-btn")
            return friends.count() > 0
        return False
    
    def get_friendship_status(self, result_index: int = 0):
        """Get friendship status with user at index."""
        cards = self.page.locator(".user-card, #searchResults .card, #usersContainer .card")
        if cards.count() > result_index:
            card = cards.nth(result_index)
            
            if card.locator(".friends-badge, .remove-friend-btn, button:has-text('Friends')").count() > 0:
                return "friends"
            elif card.locator(".cancel-request-btn, button:has-text('Cancel'), button:has-text('Pending')").count() > 0:
                return "sent"
            elif card.locator(".accept-btn, button:has-text('Accept')").count() > 0:
                return "received"
            elif card.locator(".add-friend-btn, button:has-text('Add Friend')").count() > 0:
                return "none"
        return "unknown"
    
    # ==================== DISCOVER SECTION ====================
    def is_discover_section_visible(self):
        """Check if discover/suggestions section is visible."""
        return self.is_visible("#discoverSection, .discover-section, #usersContainer")
    
    def get_discover_users_count(self):
        """Get number of users in discover section."""
        return self.count_elements("#usersContainer .card, .discover-user-card")
    
    def get_discover_usernames(self):
        """Get usernames from discover section."""
        users = self.page.locator("#usersContainer .card .card-subtitle, .discover-user-card .username")
        usernames = []
        for i in range(users.count()):
            usernames.append(users.nth(i).text_content())
        return usernames
    
    # ==================== PAGE VALIDATION ====================
    def is_page_loaded(self):
        """Check if explore page has loaded."""
        return (
            self.is_search_input_visible() or
            self.is_discover_section_visible()
        )
    
    def wait_for_results(self, timeout: int = 5000):
        """Wait for search results to load."""
        try:
            self.page.wait_for_selector(".user-card, #searchResults .card, #usersContainer .card", timeout=timeout)
            return True
        except:
            return False
    
    def is_success_toast_visible(self):
        """Check if success toast is visible."""
        return self.is_visible(".toast.show:has-text('success'), .alert-success")
    
    def is_error_toast_visible(self):
        """Check if error toast is visible."""
        return self.is_visible(".toast.show:has-text('error'), .alert-danger")
    
    # ==================== NAVBAR SEARCH (if exists) ====================
    def is_navbar_search_visible(self):
        """Check if navbar search is visible."""
        return self.is_visible("#navSearchInput, .navbar .search-input")
    
    def navbar_search(self, query: str):
        """Perform search using navbar search."""
        logger.info(f"Navbar search for: {query}")
        self.fill("#navSearchInput, .navbar .search-input", query)
        # Trigger search (enter key or button)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(1000)
