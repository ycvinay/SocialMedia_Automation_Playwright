"""
Notifications Page Object.
Handles all interactions with the notifications page.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
import logging

logger = logging.getLogger(__name__)


class NotificationsPage(BasePage):
    """Notifications page object for notification testing."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.selectors = Selectors.Notifications
        self.url = URLs.Pages.notifications()
    
    def navigate(self):
        """Navigate to notifications page."""
        super().navigate(self.url)
        logger.info("Navigated to notifications page")
    
    def is_on_notifications_page(self):
        """Check if currently on notifications page."""
        return "notifications.html" in self.page.url
    
    # ==================== NOTIFICATIONS LIST ====================
    def get_notifications_count(self):
        """Get total number of notifications."""
        return self.count_elements(".notification-item, .notification-card, #notificationsList .list-group-item")
    
    def get_unread_notifications_count(self):
        """Get number of unread notifications."""
        return self.count_elements(".notification-item.unread, .notification-card.unread, .list-group-item.unread")
    
    def get_notification_messages(self):
        """Get list of notification messages."""
        notifications = self.page.locator(".notification-text, .notification-message, #notificationsList .list-group-item p")
        messages = []
        for i in range(notifications.count()):
            messages.append(notifications.nth(i).text_content())
        return messages
    
    def get_notification_at_index(self, index: int):
        """Get notification element at specific index."""
        notifications = self.page.locator(".notification-item, #notificationsList .list-group-item")
        if notifications.count() > index:
            return notifications.nth(index)
        return None
    
    def get_notification_type(self, index: int = 0):
        """Get type of notification (like, comment, friend_request, etc.)."""
        notification = self.get_notification_at_index(index)
        if notification:
            classes = notification.get_attribute("class") or ""
            text = notification.text_content().lower()
            
            if "friend_request" in classes or "friend request" in text:
                return "friend_request"
            elif "like" in classes or "liked" in text:
                return "like"
            elif "comment" in classes or "commented" in text:
                return "comment"
        return "unknown"
    
    def is_notification_unread(self, index: int = 0):
        """Check if notification at index is unread."""
        notification = self.get_notification_at_index(index)
        if notification:
            classes = notification.get_attribute("class") or ""
            return "unread" in classes
        return False
    
    # ==================== NOTIFICATION ACTIONS ====================
    def click_notification(self, index: int = 0):
        """Click on a notification."""
        logger.info(f"Clicking notification at index {index}")
        notification = self.get_notification_at_index(index)
        if notification:
            notification.click()
            self.wait_for_timeout(1000)
            return True
        return False
    
    def mark_notification_as_read(self, index: int = 0):
        """Mark a specific notification as read."""
        logger.info(f"Marking notification {index} as read")
        notifications = self.page.locator(".notification-item, #notificationsList .list-group-item")
        if notifications.count() > index:
            mark_btn = notifications.nth(index).locator(".mark-read-btn, button:has-text('Mark Read')")
            if mark_btn.count() > 0:
                mark_btn.click()
                self.wait_for_timeout(500)
                return True
        return False
    
    def mark_all_as_read(self):
        """Mark all notifications as read."""
        logger.info("Marking all notifications as read")
        mark_all_btn = self.page.locator("#markAllReadBtn, button:has-text('Mark All Read')")
        if mark_all_btn.count() > 0:
            mark_all_btn.click()
            self.wait_for_timeout(1000)
            return True
        return False
    
    def clear_all_notifications(self):
        """Clear all notifications."""
        logger.info("Clearing all notifications")
        clear_btn = self.page.locator("#clearAllBtn, button:has-text('Clear All')")
        if clear_btn.count() > 0:
            clear_btn.click()
            self.wait_for_timeout(1000)
            return True
        return False
    
    def delete_notification(self, index: int = 0):
        """Delete a specific notification."""
        notifications = self.page.locator(".notification-item, #notificationsList .list-group-item")
        if notifications.count() > index:
            delete_btn = notifications.nth(index).locator(".delete-btn, .dismiss-btn, button:has-text('Delete')")
            if delete_btn.count() > 0:
                delete_btn.click()
                self.wait_for_timeout(500)
                return True
        return False
    
    # ==================== FRIEND REQUEST NOTIFICATIONS ====================
    def get_friend_request_notifications_count(self):
        """Get count of friend request notifications."""
        return self.count_elements(".notification-item:has-text('friend request'), .friend-request-notification")
    
    def accept_friend_request_from_notification(self, index: int = 0):
        """Accept friend request directly from notification."""
        notifications = self.page.locator(".notification-item:has-text('friend request'), .friend-request-notification")
        if notifications.count() > index:
            accept_btn = notifications.nth(index).locator(".accept-btn, button:has-text('Accept')")
            if accept_btn.count() > 0:
                accept_btn.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    def reject_friend_request_from_notification(self, index: int = 0):
        """Reject friend request directly from notification."""
        notifications = self.page.locator(".notification-item:has-text('friend request'), .friend-request-notification")
        if notifications.count() > index:
            reject_btn = notifications.nth(index).locator(".reject-btn, button:has-text('Reject')")
            if reject_btn.count() > 0:
                reject_btn.click()
                self.wait_for_timeout(1000)
                return True
        return False
    
    # ==================== EMPTY STATE ====================
    def is_no_notifications_message_visible(self):
        """Check if 'no notifications' message is visible."""
        return self.is_visible(".no-notifications-message, .empty-state, p:has-text('No notifications')")
    
    def get_empty_state_message(self):
        """Get the empty state message text."""
        empty_state = self.page.locator(".no-notifications-message, .empty-state")
        if empty_state.count() > 0:
            return empty_state.text_content()
        return None
    
    # ==================== NOTIFICATION BADGE ====================
    def get_navbar_notification_badge_count(self):
        """Get the notification badge count from navbar."""
        badge = self.page.locator(".notification-badge, #notificationCount, .badge")
        if badge.count() > 0:
            text = badge.first.text_content()
            try:
                return int(text)
            except:
                return 0
        return 0
    
    def is_notification_badge_visible(self):
        """Check if notification badge is visible in navbar."""
        return self.is_visible(".notification-badge, #notificationCount")
    
    # ==================== FILTERING ====================
    def filter_by_type(self, notification_type: str):
        """Filter notifications by type (if filter exists)."""
        filter_btn = self.page.locator(f"[data-filter='{notification_type}'], button:has-text('{notification_type}')")
        if filter_btn.count() > 0:
            filter_btn.click()
            self.wait_for_timeout(500)
    
    def show_all_notifications(self):
        """Show all notifications (remove filter)."""
        all_btn = self.page.locator("[data-filter='all'], button:has-text('All')")
        if all_btn.count() > 0:
            all_btn.click()
            self.wait_for_timeout(500)
    
    # ==================== PAGE VALIDATION ====================
    def is_page_loaded(self):
        """Check if notifications page has loaded."""
        return (
            self.is_visible("#notificationsList, .notifications-container") or
            self.is_no_notifications_message_visible()
        )
    
    def wait_for_notifications_load(self, timeout: int = 5000):
        """Wait for notifications to load."""
        try:
            self.page.wait_for_selector(".notification-item, .empty-state, #notificationsList", timeout=timeout)
            return True
        except:
            return False
    
    def refresh_notifications(self):
        """Refresh the notifications list."""
        refresh_btn = self.page.locator("#refreshNotifications, button:has-text('Refresh')")
        if refresh_btn.count() > 0:
            refresh_btn.click()
            self.wait_for_timeout(1000)
        else:
            self.reload_page()
    
    # ==================== TIMESTAMPS ====================
    def get_notification_time(self, index: int = 0):
        """Get timestamp of notification at index."""
        notification = self.get_notification_at_index(index)
        if notification:
            time_elem = notification.locator(".notification-time, .timestamp, small")
            if time_elem.count() > 0:
                return time_elem.first.text_content()
        return None
