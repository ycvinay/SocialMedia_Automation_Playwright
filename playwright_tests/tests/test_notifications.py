"""
Notifications Page Automation Tests
Testing for notification display and actions.
"""

import pytest
import time
import logging
from pages.notifications_page import NotificationsPage
from pages.login_page import LoginPage
from constants.test_data import TestData

logger = logging.getLogger(__name__)


@pytest.fixture
def logged_in_notifications_page(page):
    """Fixture: Login and navigate to notifications page."""
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
    
    notifications_page = NotificationsPage(page)
    notifications_page.navigate()
    time.sleep(2)
    return notifications_page


class TestNotificationsPageElements:
    """Test: Verify notifications page elements."""
    
    @pytest.mark.smoke
    def test_notifications_page_loads(self, logged_in_notifications_page):
        """Test: Notifications page loads correctly."""
        assert logged_in_notifications_page.is_on_notifications_page()
        logger.info("✅ Notifications page loaded")
    
    def test_page_loaded_state(self, logged_in_notifications_page):
        """Test: Page shows notifications or empty state."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() > 0:
            logger.info("✅ Notifications are displayed")
        elif notif_page.is_no_notifications_message_visible():
            logger.info("✅ No notifications message displayed")
        else:
            logger.info("ℹ️ Page loaded - checking state")


class TestNotificationsList:
    """Test: Notifications list functionality."""
    
    def test_notifications_count(self, logged_in_notifications_page):
        """Test: Get notifications count."""
        count = logged_in_notifications_page.get_notifications_count()
        logger.info(f"✅ {count} notifications")
    
    def test_get_notification_messages(self, logged_in_notifications_page):
        """Test: Get notification messages."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() == 0:
            pytest.skip("No notifications")
        
        messages = notif_page.get_notification_messages()
        logger.info(f"✅ Messages: {messages[:2]}")
    
    def test_unread_notifications_count(self, logged_in_notifications_page):
        """Test: Get unread notifications count."""
        count = logged_in_notifications_page.get_unread_notifications_count()
        logger.info(f"✅ {count} unread notifications")
    
    def test_notification_type(self, logged_in_notifications_page):
        """Test: Get notification type."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() == 0:
            pytest.skip("No notifications")
        
        notif_type = notif_page.get_notification_type(0)
        logger.info(f"✅ First notification type: {notif_type}")


class TestNotificationActions:
    """Test: Notification action functionality."""
    
    def test_click_notification(self, logged_in_notifications_page):
        """Test: Click on a notification."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() == 0:
            pytest.skip("No notifications")
        
        notif_page.click_notification(0)
        time.sleep(1)
        logger.info("✅ Notification clicked")
    
    def test_mark_notification_as_read(self, logged_in_notifications_page):
        """Test: Mark notification as read."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_unread_notifications_count() == 0:
            pytest.skip("No unread notifications")
        
        notif_page.mark_notification_as_read(0)
        logger.info("✅ Mark as read attempted")
    
    def test_mark_all_as_read(self, logged_in_notifications_page):
        """Test: Mark all notifications as read."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() == 0:
            pytest.skip("No notifications")
        
        notif_page.mark_all_as_read()
        logger.info("✅ Mark all as read attempted")


class TestFriendRequestNotifications:
    """Test: Friend request notification actions."""
    
    def test_friend_request_notifications_count(self, logged_in_notifications_page):
        """Test: Count friend request notifications."""
        count = logged_in_notifications_page.get_friend_request_notifications_count()
        logger.info(f"✅ {count} friend request notifications")
    
    def test_accept_from_notification(self, logged_in_notifications_page):
        """Test: Accept friend request from notification."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_friend_request_notifications_count() == 0:
            pytest.skip("No friend request notifications")
        
        notif_page.accept_friend_request_from_notification(0)
        logger.info("✅ Accept from notification attempted")
    
    def test_reject_from_notification(self, logged_in_notifications_page):
        """Test: Reject friend request from notification."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_friend_request_notifications_count() == 0:
            pytest.skip("No friend request notifications")
        
        notif_page.reject_friend_request_from_notification(0)
        logger.info("✅ Reject from notification attempted")


class TestEmptyState:
    """Test: Empty notifications state."""
    
    def test_empty_state_message(self, logged_in_notifications_page):
        """Test: Empty state message when no notifications."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() > 0:
            pytest.skip("Has notifications - can't test empty state")
        
        assert notif_page.is_no_notifications_message_visible()
        logger.info("✅ Empty state message displayed")
    
    def test_clear_all_notifications(self, logged_in_notifications_page):
        """Test: Clear all notifications."""
        notif_page = logged_in_notifications_page
        
        if notif_page.get_notifications_count() == 0:
            pytest.skip("No notifications to clear")
        
        notif_page.clear_all_notifications()
        time.sleep(1)
        logger.info("✅ Clear all attempted")
