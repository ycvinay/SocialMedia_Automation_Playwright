"""
Login Page Object.
Handles all interactions with the login page.
Updated to match actual HTML structure with Bootstrap toasts.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
from constants.messages import Messages
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object for authentication testing."""
    
    def __init__(self, page: Page):
        """
        Initialize login page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        self.selectors = Selectors.Login
        self.url = URLs.Pages.login()
    
    # ==================== NAVIGATION ====================
    
    def navigate(self):
        """Navigate to login page."""
        super().navigate(self.url)
        logger.info("Navigated to login page")
    
    def is_on_login_page(self) -> bool:
        """
        Check if currently on login page.
        
        Returns:
            True if on login page, False otherwise
        """
        return "login.html" in self.get_current_url()
    
    # ==================== FORM ACTIONS ====================
    
    def enter_username(self, username: str):
        """
        Enter username in the login form.
        
        Args:
            username: Username to enter
        """
        logger.info(f"Entering username: {username}")
        self.fill(self.selectors.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        """
        Enter password in the login form.
        
        Args:
            password: Password to enter
        """
        logger.info("Entering password")
        self.fill(self.selectors.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click the login button to submit the form."""
        logger.info("Clicking login button")
        self.click(self.selectors.LOGIN_BUTTON)
    
    def click_signup_link(self):
        """Click the 'Sign Up' link to navigate to signup page."""
        logger.info("Clicking signup link")
        self.click(self.selectors.SIGNUP_LINK)
    
    def click_forgot_password_link(self):
        """Click the 'Forgot Password' link."""
        logger.info("Clicking forgot password link")
        self.click(self.selectors.FORGOT_PASSWORD_LINK)
    
    def toggle_password_visibility(self):
        """Toggle password field visibility."""
        logger.info("Toggling password visibility")
        self.click(self.selectors.TOGGLE_PASSWORD)
    
    def login(self, username: str, password: str):
        """
        Perform complete login action.
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        # Wait for either redirect or toast message
        self.wait_for_timeout(2500)
    
    def quick_login(self, username: str, password: str):
        """
        Quick login without page navigation (assumes already on login page).
        
        Args:
            username: Username
            password: Password
        """
        self.login(username, password)
    
    # ==================== VALIDATION METHODS ====================
    
    def is_login_successful(self) -> bool:
        """
        Check if login was successful by verifying redirect to home page.
        
        Returns:
            True if redirected to home page, False otherwise
        """
        try:
            self.wait_for_url("**/home.html", timeout=5000)
            logger.info("Login successful - redirected to home page")
            return True
        except Exception:
            logger.warning("Login failed - not redirected to home page")
            return False
    
    def is_success_toast_displayed(self) -> bool:
        """
        Check if success toast is displayed.
        
        Returns:
            True if success toast is visible, False otherwise
        """
        try:
            # Bootstrap toast appears with 'show' class
            self.wait_for_selector(f"{self.selectors.SUCCESS_TOAST}.show", timeout=3000)
            return True
        except Exception:
            return False
    
    def is_error_toast_displayed(self) -> bool:
        """
        Check if error toast is displayed.
        
        Returns:
            True if error toast is visible, False otherwise
        """
        try:
            self.wait_for_selector(f"{self.selectors.ERROR_TOAST}.show", timeout=3000)
            return True
        except Exception:
            return False
    
    def get_success_toast_message(self) -> str:
        """
        Get the message from success toast.
        
        Returns:
            Success toast message text
        """
        if self.is_success_toast_displayed():
            return self.get_text(f"{self.selectors.SUCCESS_TOAST} {self.selectors.TOAST_BODY}")
        return ""
    
    def get_error_toast_message(self) -> str:
        """
        Get the message from error toast.
        
        Returns:
            Error toast message text
        """
        if self.is_error_toast_displayed():
            return self.get_text(f"{self.selectors.ERROR_TOAST} {self.selectors.TOAST_BODY}")
        return ""
    
    def is_field_invalid(self, field: str) -> bool:
        """
        Check if a field has validation error (is-invalid class).
        
        Args:
            field: Field selector (e.g., self.selectors.USERNAME_INPUT)
            
        Returns:
            True if field has is-invalid class
        """
        try:
            return self.page.locator(f"{field}.is-invalid").is_visible()
        except Exception:
            return False
    
    def is_username_invalid(self) -> bool:
        """Check if username field has validation error."""
        return self.is_field_invalid(self.selectors.USERNAME_INPUT)
    
    def is_password_invalid(self) -> bool:
        """Check if password field has validation error."""
        return self.is_field_invalid(self.selectors.PASSWORD_INPUT)
    
    def is_loading(self) -> bool:
        """
        Check if login form is in loading state (spinner visible).
        
        Returns:
            True if spinner is visible, False otherwise
        """
        try:
            # Spinner has d-none class when hidden
            spinner = self.page.locator(self.selectors.BTN_SPINNER)
            return not spinner.get_attribute("class").find("d-none") >= 0
        except Exception:
            return False
    
    # ==================== LEGACY COMPATIBILITY METHODS ====================
    # These methods maintain backwards compatibility with existing tests
    
    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed (legacy method).
        Uses toast for Bootstrap implementation.
        
        Returns:
            True if error toast is visible, False otherwise
        """
        return self.is_error_toast_displayed()
    
    def get_error_message(self) -> str:
        """
        Get error message text (legacy method).
        
        Returns:
            Error message text from toast
        """
        return self.get_error_toast_message()
    
    def is_success_message_displayed(self) -> bool:
        """
        Check if success message is displayed (legacy method).
        
        Returns:
            True if success toast is visible, False otherwise
        """
        return self.is_success_toast_displayed()
    
    def get_success_message(self) -> str:
        """
        Get success message text (legacy method).
        
        Returns:
            Success message text from toast
        """
        return self.get_success_toast_message()
    
    # ==================== FIELD STATE METHODS ====================
    
    def is_username_field_empty(self) -> bool:
        """Check if username field is empty."""
        return self.get_value(self.selectors.USERNAME_INPUT) == ""
    
    def is_password_field_empty(self) -> bool:
        """Check if password field is empty."""
        return self.get_value(self.selectors.PASSWORD_INPUT) == ""
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        return self.is_enabled(self.selectors.LOGIN_BUTTON)
    
    def is_login_button_disabled(self) -> bool:
        """Check if login button is disabled."""
        return self.is_disabled(self.selectors.LOGIN_BUTTON)
    
    def is_password_visible(self) -> bool:
        """Check if password is visible (type='text')."""
        password_type = self.get_attribute(self.selectors.PASSWORD_INPUT, "type")
        return password_type == "text"
    
    # ==================== HELPER METHODS ====================
    
    def clear_username(self):
        """Clear username field."""
        self.fill(self.selectors.USERNAME_INPUT, "")
    
    def clear_password(self):
        """Clear password field."""
        self.fill(self.selectors.PASSWORD_INPUT, "")
    
    def clear_form(self):
        """Clear all login form fields."""
        self.clear_username()
        self.clear_password()
    
    def get_username_value(self) -> str:
        """Get current value in username field."""
        return self.get_value(self.selectors.USERNAME_INPUT)
    
    def get_password_value(self) -> str:
        """Get current value in password field."""
        return self.get_value(self.selectors.PASSWORD_INPUT)
    
    # ==================== PAGE ELEMENT VERIFICATION ====================
    
    def is_form_visible(self) -> bool:
        """Check if login form is visible."""
        return self.is_visible(self.selectors.FORM)
    
    def is_username_input_visible(self) -> bool:
        """Check if username input is visible."""
        return self.is_visible(self.selectors.USERNAME_INPUT)
    
    def is_password_input_visible(self) -> bool:
        """Check if password input is visible."""
        return self.is_visible(self.selectors.PASSWORD_INPUT)
    
    def is_login_button_visible(self) -> bool:
        """Check if login button is visible."""
        return self.is_visible(self.selectors.LOGIN_BUTTON)
    
    def is_signup_link_visible(self) -> bool:
        """Check if signup link is visible."""
        return self.is_visible(self.selectors.SIGNUP_LINK)
    
    def is_forgot_password_link_visible(self) -> bool:
        """Check if forgot password link is visible."""
        return self.is_visible(self.selectors.FORGOT_PASSWORD_LINK)
    
    def are_all_elements_visible(self) -> bool:
        """
        Check if all essential login page elements are visible.
        
        Returns:
            True if all elements are visible, False otherwise
        """
        return all([
            self.is_form_visible(),
            self.is_username_input_visible(),
            self.is_password_input_visible(),
            self.is_login_button_visible(),
            self.is_signup_link_visible()
        ])
    
    # ==================== ASSERTIONS ====================
    
    def assert_on_login_page(self):
        """Assert that we are on login page."""
        assert self.is_on_login_page(), "Not on login page"
        logger.info("Assertion passed: On login page")
    
    def assert_login_successful(self):
        """Assert that login was successful."""
        assert self.is_login_successful(), "Login was not successful"
        logger.info("Assertion passed: Login successful")
    
    def assert_login_failed(self):
        """Assert that login failed (not redirected)."""
        assert not self.is_login_successful(), "Login should have failed but succeeded"
        logger.info("Assertion passed: Login failed as expected")
    
    def assert_error_toast_displayed(self, expected_message: str = None):
        """
        Assert that error toast is displayed.
        
        Args:
            expected_message: Optional expected message text (partial match)
        """
        assert self.is_error_toast_displayed(), "Error toast not displayed"
        
        if expected_message:
            actual_message = self.get_error_toast_message()
            assert expected_message.lower() in actual_message.lower(), \
                f"Expected message '{expected_message}' not found in '{actual_message}'"
        
        logger.info("Assertion passed: Error toast displayed")
    
    def assert_success_toast_displayed(self, expected_message: str = None):
        """
        Assert that success toast is displayed.
        
        Args:
            expected_message: Optional expected message text (partial match)
        """
        assert self.is_success_toast_displayed(), "Success toast not displayed"
        
        if expected_message:
            actual_message = self.get_success_toast_message()
            assert expected_message.lower() in actual_message.lower(), \
                f"Expected message '{expected_message}' not found in '{actual_message}'"
        
        logger.info("Assertion passed: Success toast displayed")
    
    def assert_all_elements_visible(self):
        """Assert that all essential login page elements are visible."""
        assert self.are_all_elements_visible(), "Not all login page elements are visible"
        logger.info("Assertion passed: All login page elements visible")
    
    # Legacy alias for backwards compatibility
    def assert_error_message_displayed(self, expected_message: str = None):
        """Legacy alias for assert_error_toast_displayed."""
        self.assert_error_toast_displayed(expected_message)
