"""
Signup Page Object.
Handles all interactions with the signup/registration page.
Updated to match actual HTML structure with Bootstrap toasts.
"""

from playwright.sync_api import Page
from .base_page import BasePage
from constants.selectors import Selectors
from constants.urls import URLs
from constants.messages import Messages
import logging

logger = logging.getLogger(__name__)


class SignupPage(BasePage):
    """Signup page object for registration testing."""
    
    def __init__(self, page: Page):
        """
        Initialize signup page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        self.selectors = Selectors.Signup
        self.url = URLs.Pages.signup()
    
    # ==================== NAVIGATION ====================
    
    def navigate(self):
        """Navigate to signup page."""
        super().navigate(self.url)
        logger.info("Navigated to signup page")
    
    def is_on_signup_page(self) -> bool:
        """
        Check if currently on signup page.
        
        Returns:
            True if on signup page, False otherwise
        """
        return "signup.html" in self.get_current_url()
    
    # ==================== FORM ACTIONS ====================
    
    def enter_name(self, name: str):
        """
        Enter full name in the signup form.
        
        Args:
            name: Full name to enter
        """
        logger.info(f"Entering name: {name}")
        self.fill(self.selectors.NAME_INPUT, name)
    
    def enter_username(self, username: str):
        """
        Enter username in the signup form.
        
        Args:
            username: Username to enter
        """
        logger.info(f"Entering username: {username}")
        self.fill(self.selectors.USERNAME_INPUT, username)
    
    def enter_email(self, email: str):
        """
        Enter email in the signup form.
        
        Args:
            email: Email address to enter
        """
        logger.info(f"Entering email: {email}")
        self.fill(self.selectors.EMAIL_INPUT, email)
    
    def enter_password(self, password: str):
        """
        Enter password in the signup form.
        
        Args:
            password: Password to enter
        """
        logger.info("Entering password")
        self.fill(self.selectors.PASSWORD_INPUT, password)
    
    def click_signup_button(self):
        """Click the signup button to submit the form."""
        logger.info("Clicking signup button")
        self.click(self.selectors.SIGNUP_BUTTON)
    
    def click_login_link(self):
        """Click the 'Log In' link to navigate to login page."""
        logger.info("Clicking login link")
        self.click(self.selectors.LOGIN_LINK)
    
    def toggle_password_visibility(self):
        """Toggle password field visibility."""
        logger.info("Toggling password visibility")
        self.click(self.selectors.TOGGLE_PASSWORD)
    
    def signup(self, name: str, username: str, email: str, password: str):
        """
        Perform complete signup action.
        Note: This app does not have confirm password field.
        
        Args:
            name: Full name
            username: Username
            email: Email address
            password: Password
        """
        logger.info(f"Signing up with username: {username}")
        self.enter_name(name)
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.click_signup_button()
        
        # Wait for either redirect or toast message
        self.wait_for_timeout(2500)
    
    def signup_with_user_data(self, user_data: dict):
        """
        Perform signup using a user data dictionary.
        
        Args:
            user_data: Dictionary with 'name', 'username', 'email', 'password' keys
        """
        self.signup(
            name=user_data.get('name', ''),
            username=user_data.get('username', ''),
            email=user_data.get('email', ''),
            password=user_data.get('password', '')
        )
    
    # ==================== VALIDATION METHODS ====================
    
    def is_signup_successful(self) -> bool:
        """
        Check if signup was successful by verifying redirect to login page.
        
        Returns:
            True if redirected to login page, False otherwise
        """
        try:
            self.wait_for_url("**/login.html", timeout=5000)
            logger.info("Signup successful - redirected to login page")
            return True
        except Exception:
            logger.warning("Signup failed - not redirected to login page")
            return False
    
    def is_success_toast_displayed(self) -> bool:
        """
        Check if success toast is displayed.
        
        Returns:
            True if success toast is visible, False otherwise
        """
        try:
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
    
    # ==================== FIELD VALIDATION ====================
    
    def is_field_invalid(self, field: str) -> bool:
        """
        Check if a field has validation error (is-invalid class).
        
        Args:
            field: Field selector
            
        Returns:
            True if field has is-invalid class
        """
        try:
            return self.page.locator(f"{field}.is-invalid").is_visible()
        except Exception:
            return False
    
    def is_field_valid(self, field: str) -> bool:
        """
        Check if a field has been validated successfully (is-valid class).
        
        Args:
            field: Field selector
            
        Returns:
            True if field has is-valid class
        """
        try:
            return self.page.locator(f"{field}.is-valid").is_visible()
        except Exception:
            return False
    
    def is_name_invalid(self) -> bool:
        """Check if name field has validation error."""
        return self.is_field_invalid(self.selectors.NAME_INPUT)
    
    def is_name_valid(self) -> bool:
        """Check if name field has been validated successfully."""
        return self.is_field_valid(self.selectors.NAME_INPUT)
    
    def is_username_invalid(self) -> bool:
        """Check if username field has validation error."""
        return self.is_field_invalid(self.selectors.USERNAME_INPUT)
    
    def is_username_valid(self) -> bool:
        """Check if username field has been validated successfully."""
        return self.is_field_valid(self.selectors.USERNAME_INPUT)
    
    def is_email_invalid(self) -> bool:
        """Check if email field has validation error."""
        return self.is_field_invalid(self.selectors.EMAIL_INPUT)
    
    def is_email_valid(self) -> bool:
        """Check if email field has been validated successfully."""
        return self.is_field_valid(self.selectors.EMAIL_INPUT)
    
    def is_password_invalid(self) -> bool:
        """Check if password field has validation error."""
        return self.is_field_invalid(self.selectors.PASSWORD_INPUT)
    
    def is_password_valid(self) -> bool:
        """Check if password field has been validated successfully."""
        return self.is_field_valid(self.selectors.PASSWORD_INPUT)
    
    def trigger_field_validation(self, field_selector: str):
        """
        Trigger field validation by focusing and then blurring the field.
        
        Args:
            field_selector: CSS selector of the field
        """
        self.page.locator(field_selector).focus()
        self.page.locator(field_selector).blur()
        self.wait_for_timeout(100)
    
    def validate_all_fields(self):
        """Trigger validation on all form fields."""
        self.trigger_field_validation(self.selectors.NAME_INPUT)
        self.trigger_field_validation(self.selectors.USERNAME_INPUT)
        self.trigger_field_validation(self.selectors.EMAIL_INPUT)
        self.trigger_field_validation(self.selectors.PASSWORD_INPUT)
    
    # ==================== LOADING STATE ====================
    
    def is_loading(self) -> bool:
        """
        Check if signup form is in loading state (spinner visible).
        
        Returns:
            True if spinner is visible, False otherwise
        """
        try:
            spinner = self.page.locator(self.selectors.BTN_SPINNER)
            class_attr = spinner.get_attribute("class") or ""
            return "d-none" not in class_attr
        except Exception:
            return False
    
    def is_button_disabled(self) -> bool:
        """Check if signup button is disabled."""
        return self.is_disabled(self.selectors.SIGNUP_BUTTON)
    
    # ==================== LEGACY COMPATIBILITY METHODS ====================
    
    def is_error_message_displayed(self) -> bool:
        """Legacy alias for is_error_toast_displayed."""
        return self.is_error_toast_displayed()
    
    def get_error_message(self) -> str:
        """Legacy alias for get_error_toast_message."""
        return self.get_error_toast_message()
    
    def is_success_message_displayed(self) -> bool:
        """Legacy alias for is_success_toast_displayed."""
        return self.is_success_toast_displayed()
    
    def get_success_message(self) -> str:
        """Legacy alias for get_success_toast_message."""
        return self.get_success_toast_message()
    
    # ==================== FIELD STATE METHODS ====================
    
    def get_name_value(self) -> str:
        """Get current value in name field."""
        return self.get_value(self.selectors.NAME_INPUT)
    
    def get_username_value(self) -> str:
        """Get current value in username field."""
        return self.get_value(self.selectors.USERNAME_INPUT)
    
    def get_email_value(self) -> str:
        """Get current value in email field."""
        return self.get_value(self.selectors.EMAIL_INPUT)
    
    def get_password_value(self) -> str:
        """Get current value in password field."""
        return self.get_value(self.selectors.PASSWORD_INPUT)
    
    def is_password_visible(self) -> bool:
        """Check if password is visible (type='text')."""
        password_type = self.get_attribute(self.selectors.PASSWORD_INPUT, "type")
        return password_type == "text"
    
    # ==================== HELPER METHODS ====================
    
    def clear_name(self):
        """Clear name field."""
        self.fill(self.selectors.NAME_INPUT, "")
    
    def clear_username(self):
        """Clear username field."""
        self.fill(self.selectors.USERNAME_INPUT, "")
    
    def clear_email(self):
        """Clear email field."""
        self.fill(self.selectors.EMAIL_INPUT, "")
    
    def clear_password(self):
        """Clear password field."""
        self.fill(self.selectors.PASSWORD_INPUT, "")
    
    def clear_form(self):
        """Clear all signup form fields."""
        self.clear_name()
        self.clear_username()
        self.clear_email()
        self.clear_password()
    
    # ==================== PAGE ELEMENT VERIFICATION ====================
    
    def is_form_visible(self) -> bool:
        """Check if signup form is visible."""
        return self.is_visible(self.selectors.FORM)
    
    def is_name_input_visible(self) -> bool:
        """Check if name input is visible."""
        return self.is_visible(self.selectors.NAME_INPUT)
    
    def is_username_input_visible(self) -> bool:
        """Check if username input is visible."""
        return self.is_visible(self.selectors.USERNAME_INPUT)
    
    def is_email_input_visible(self) -> bool:
        """Check if email input is visible."""
        return self.is_visible(self.selectors.EMAIL_INPUT)
    
    def is_password_input_visible(self) -> bool:
        """Check if password input is visible."""
        return self.is_visible(self.selectors.PASSWORD_INPUT)
    
    def is_signup_button_visible(self) -> bool:
        """Check if signup button is visible."""
        return self.is_visible(self.selectors.SIGNUP_BUTTON)
    
    def is_login_link_visible(self) -> bool:
        """Check if login link is visible."""
        return self.is_visible(self.selectors.LOGIN_LINK)
    
    def are_all_elements_visible(self) -> bool:
        """
        Check if all essential signup page elements are visible.
        
        Returns:
            True if all elements are visible, False otherwise
        """
        return all([
            self.is_form_visible(),
            self.is_name_input_visible(),
            self.is_username_input_visible(),
            self.is_email_input_visible(),
            self.is_password_input_visible(),
            self.is_signup_button_visible(),
            self.is_login_link_visible()
        ])
    
    # ==================== ASSERTIONS ====================
    
    def assert_on_signup_page(self):
        """Assert that we are on signup page."""
        assert self.is_on_signup_page(), "Not on signup page"
        logger.info("Assertion passed: On signup page")
    
    def assert_signup_successful(self):
        """Assert that signup was successful (redirected to login)."""
        assert self.is_signup_successful(), "Signup was not successful"
        logger.info("Assertion passed: Signup successful")
    
    def assert_signup_failed(self):
        """Assert that signup failed (not redirected)."""
        assert not self.is_signup_successful(), "Signup should have failed but succeeded"
        logger.info("Assertion passed: Signup failed as expected")
    
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
    
    def assert_field_invalid(self, field_name: str):
        """
        Assert that a specific field has validation error.
        
        Args:
            field_name: Name of field ('name', 'username', 'email', 'password')
        """
        field_checks = {
            'name': self.is_name_invalid,
            'username': self.is_username_invalid,
            'email': self.is_email_invalid,
            'password': self.is_password_invalid
        }
        
        check_func = field_checks.get(field_name)
        if check_func:
            assert check_func(), f"Field '{field_name}' should be invalid but is not"
            logger.info(f"Assertion passed: {field_name} field is invalid")
        else:
            raise ValueError(f"Unknown field name: {field_name}")
    
    def assert_field_valid(self, field_name: str):
        """
        Assert that a specific field has been validated successfully.
        
        Args:
            field_name: Name of field ('name', 'username', 'email', 'password')
        """
        field_checks = {
            'name': self.is_name_valid,
            'username': self.is_username_valid,
            'email': self.is_email_valid,
            'password': self.is_password_valid
        }
        
        check_func = field_checks.get(field_name)
        if check_func:
            assert check_func(), f"Field '{field_name}' should be valid but is not"
            logger.info(f"Assertion passed: {field_name} field is valid")
        else:
            raise ValueError(f"Unknown field name: {field_name}")
    
    def assert_all_elements_visible(self):
        """Assert that all essential signup page elements are visible."""
        assert self.are_all_elements_visible(), "Not all signup page elements are visible"
        logger.info("Assertion passed: All signup page elements visible")
