"""
Authentication Tests.
Comprehensive tests for login, signup, and logout functionality.
Updated to work with Bootstrap-based UI.
"""

import pytest
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from constants.selectors import Selectors
from constants.test_data import TestData
from constants.urls import URLs
from constants.messages import Messages
import logging

logger = logging.getLogger(__name__)


class TestLoginPageElements:
    """Tests to verify login page elements are displayed correctly."""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_login_page_loads_successfully(self, page):
        """Test that login page loads with all elements visible."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        
        # Assert
        assert login_page.is_on_login_page(), "Should be on login page"
        assert login_page.are_all_elements_visible(), "All login elements should be visible"
        logger.info("✓ Test passed: Login page loads successfully")
    
    @pytest.mark.auth
    def test_login_page_form_elements(self, page):
        """Test that all login form elements are present and visible."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        
        # Assert
        assert login_page.is_form_visible(), "Login form should be visible"
        assert login_page.is_username_input_visible(), "Username input should be visible"
        assert login_page.is_password_input_visible(), "Password input should be visible"
        assert login_page.is_login_button_visible(), "Login button should be visible"
        assert login_page.is_signup_link_visible(), "Signup link should be visible"
        assert login_page.is_forgot_password_link_visible(), "Forgot password link should be visible"
        logger.info("✓ Test passed: Login page form elements present")
    
    @pytest.mark.auth
    def test_login_button_initially_enabled(self, page):
        """Test that login button is enabled by default."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        
        # Assert
        assert login_page.is_login_button_enabled(), "Login button should be enabled"
        logger.info("✓ Test passed: Login button initially enabled")


class TestLoginFunctionality:
    """Tests for login functionality."""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, page):
        """Test successful login with valid credentials."""
        # Arrange
        login_page = LoginPage(page)
        user = TestData.Users.PRIMARY_USER
        
        # Act
        login_page.navigate()
        login_page.login(user['username'], user['password'])
        
        # Assert
        assert login_page.is_login_successful(), "Login should be successful"
        assert "home.html" in page.url, "Should redirect to home page"
        logger.info("✓ Test passed: Login with valid credentials")
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_login_with_invalid_username(self, page):
        """Test login with non-existent username."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.login("nonexistent_user_12345", "Test@123456")
        
        # Assert
        assert not login_page.is_login_successful(), "Login should fail"
        assert login_page.is_error_toast_displayed(), "Error toast should be displayed"
        logger.info("✓ Test passed: Login with invalid username shows error")
    
    @pytest.mark.auth
    def test_login_with_invalid_password(self, page):
        """Test login with wrong password."""
        # Arrange
        login_page = LoginPage(page)
        user = TestData.Users.PRIMARY_USER
        
        # Act
        login_page.navigate()
        login_page.login(user['username'], "wrongpassword123")
        
        # Assert
        assert not login_page.is_login_successful(), "Login should fail"
        assert login_page.is_error_toast_displayed(), "Error toast should be displayed"
        logger.info("✓ Test passed: Login with invalid password shows error")
    
    @pytest.mark.auth
    def test_login_with_empty_username(self, page):
        """Test login with empty username field."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.enter_password("Test@123456")
        login_page.click_login_button()
        login_page.wait_for_timeout(500)
        
        # Assert
        assert not login_page.is_login_successful(), "Login should fail"
        assert login_page.is_username_invalid(), "Username field should show validation error"
        logger.info("✓ Test passed: Login with empty username shows validation error")
    
    @pytest.mark.auth
    def test_login_with_empty_password(self, page):
        """Test login with empty password field."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.enter_username("testuser1")
        login_page.click_login_button()
        login_page.wait_for_timeout(500)
        
        # Assert
        assert not login_page.is_login_successful(), "Login should fail"
        assert login_page.is_password_invalid(), "Password field should show validation error"
        logger.info("✓ Test passed: Login with empty password shows validation error")
    
    @pytest.mark.auth
    def test_login_with_both_fields_empty(self, page):
        """Test login with both fields empty."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.click_login_button()
        login_page.wait_for_timeout(500)
        
        # Assert
        assert not login_page.is_login_successful(), "Login should fail"
        assert login_page.is_username_invalid(), "Username should show validation error"
        assert login_page.is_password_invalid(), "Password should show validation error"
        logger.info("✓ Test passed: Login with both fields empty shows validation errors")


class TestLoginNavigation:
    """Tests for login page navigation."""
    
    @pytest.mark.auth
    def test_navigate_to_signup_from_login(self, page):
        """Test navigation to signup page from login page."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.click_signup_link()
        login_page.wait_for_timeout(1000)
        
        # Assert
        assert "signup.html" in page.url, "Should navigate to signup page"
        logger.info("✓ Test passed: Navigate to signup from login")
    
    @pytest.mark.auth
    def test_navigate_to_forgot_password_from_login(self, page):
        """Test navigation to forgot password page from login page."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.click_forgot_password_link()
        login_page.wait_for_timeout(1000)
        
        # Assert
        assert "forgot-password.html" in page.url, "Should navigate to forgot password page"
        logger.info("✓ Test passed: Navigate to forgot password from login")


class TestLoginPasswordVisibility:
    """Tests for password visibility toggle."""
    
    @pytest.mark.auth
    def test_password_hidden_by_default(self, page):
        """Test that password is hidden by default."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.enter_password("testpassword")
        
        # Assert
        assert not login_page.is_password_visible(), "Password should be hidden by default"
        logger.info("✓ Test passed: Password hidden by default")
    
    @pytest.mark.auth
    def test_toggle_password_visibility(self, page):
        """Test password visibility toggle."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate()
        login_page.enter_password("testpassword")
        
        # Password should be hidden initially
        assert not login_page.is_password_visible(), "Password should be hidden initially"
        
        # Toggle to show
        login_page.toggle_password_visibility()
        assert login_page.is_password_visible(), "Password should be visible after toggle"
        
        # Toggle to hide again
        login_page.toggle_password_visibility()
        assert not login_page.is_password_visible(), "Password should be hidden after second toggle"
        
        logger.info("✓ Test passed: Password visibility toggle works")


class TestSignupPageElements:
    """Tests to verify signup page elements are displayed correctly."""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_signup_page_loads_successfully(self, page):
        """Test that signup page loads with all elements visible."""
        # Arrange
        signup_page = SignupPage(page)
        
        # Act
        signup_page.navigate()
        
        # Assert
        assert signup_page.is_on_signup_page(), "Should be on signup page"
        assert signup_page.are_all_elements_visible(), "All signup elements should be visible"
        logger.info("✓ Test passed: Signup page loads successfully")
    
    @pytest.mark.auth
    def test_signup_page_form_elements(self, page):
        """Test that all signup form elements are present and visible."""
        # Arrange
        signup_page = SignupPage(page)
        
        # Act
        signup_page.navigate()
        
        # Assert
        assert signup_page.is_form_visible(), "Signup form should be visible"
        assert signup_page.is_name_input_visible(), "Name input should be visible"
        assert signup_page.is_username_input_visible(), "Username input should be visible"
        assert signup_page.is_email_input_visible(), "Email input should be visible"
        assert signup_page.is_password_input_visible(), "Password input should be visible"
        assert signup_page.is_signup_button_visible(), "Signup button should be visible"
        assert signup_page.is_login_link_visible(), "Login link should be visible"
        logger.info("✓ Test passed: Signup page form elements present")


class TestSignupFunctionality:
    """Tests for signup functionality."""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_signup_with_valid_data(self, page):
        """Test successful signup with valid data."""
        # Arrange
        signup_page = SignupPage(page)
        user = TestData.generate_random_user()
        
        # Act
        signup_page.navigate()
        signup_page.signup(
            name=user['name'],
            username=user['username'],
            email=user['email'],
            password=user['password']
        )
        
        # Assert - Check for success toast or redirect to login
        is_successful = signup_page.is_signup_successful() or signup_page.is_success_toast_displayed()
        assert is_successful, "Signup should be successful"
        logger.info("✓ Test passed: Signup with valid data")
    
    @pytest.mark.auth
    def test_signup_with_existing_username(self, page):
        """Test signup with already existing username."""
        # Arrange
        signup_page = SignupPage(page)
        existing_user = TestData.Users.PRIMARY_USER
        
        # Act
        signup_page.navigate()
        signup_page.signup(
            name="New Test User",
            username=existing_user['username'],  # Existing username
            email="newemail123@example.com",
            password="Test@123456"
        )
        
        # Assert
        assert not signup_page.is_signup_successful(), "Signup should fail"
        assert signup_page.is_error_toast_displayed(), "Error toast should be displayed"
        logger.info("✓ Test passed: Signup with existing username shows error")
    
    @pytest.mark.auth
    def test_signup_with_existing_email(self, page):
        """Test signup with already existing email."""
        # Arrange
        signup_page = SignupPage(page)
        existing_user = TestData.Users.PRIMARY_USER
        
        # Act
        signup_page.navigate()
        signup_page.signup(
            name="New Test User",
            username=f"newuser{TestData.generate_random_user()['username']}",
            email=existing_user['email'],  # Existing email
            password="Test@123456"
        )
        
        # Assert
        assert not signup_page.is_signup_successful(), "Signup should fail"
        assert signup_page.is_error_toast_displayed(), "Error toast should be displayed"
        logger.info("✓ Test passed: Signup with existing email shows error")
    
    @pytest.mark.auth
    def test_signup_with_short_password(self, page):
        """Test signup with password that is too short."""
        # Arrange
        signup_page = SignupPage(page)
        user = TestData.generate_random_user()
        
        # Act
        signup_page.navigate()
        signup_page.signup(
            name=user['name'],
            username=user['username'],
            email=user['email'],
            password="12345"  # Less than 6 characters
        )
        
        # Assert
        assert not signup_page.is_signup_successful(), "Signup should fail"
        logger.info("✓ Test passed: Signup with short password fails")


class TestSignupFieldValidation:
    """Tests for signup form field validation."""
    
    @pytest.mark.auth
    def test_name_validation_on_blur(self, page):
        """Test name field validation when focus leaves the field."""
        # Arrange
        signup_page = SignupPage(page)
        
        # Act
        signup_page.navigate()
        
        # Enter invalid name (numbers)
        signup_page.enter_name("Test123")
        signup_page.trigger_field_validation(signup_page.selectors.NAME_INPUT)
        
        # Assert
        assert signup_page.is_name_invalid(), "Name with numbers should be invalid"
        logger.info("✓ Test passed: Name validation on blur")
    
    @pytest.mark.auth
    def test_email_validation_on_blur(self, page):
        """Test email field validation when focus leaves the field."""
        # Arrange
        signup_page = SignupPage(page)
        
        # Act
        signup_page.navigate()
        
        # Enter invalid email
        signup_page.enter_email("notanemail")
        signup_page.trigger_field_validation(signup_page.selectors.EMAIL_INPUT)
        
        # Assert
        assert signup_page.is_email_invalid(), "Invalid email should show error"
        logger.info("✓ Test passed: Email validation on blur")
    
    @pytest.mark.auth
    def test_valid_email_shows_success(self, page):
        """Test that valid email shows success state."""
        # Arrange
        signup_page = SignupPage(page)
        
        # Act
        signup_page.navigate()
        signup_page.enter_email("valid@example.com")
        signup_page.trigger_field_validation(signup_page.selectors.EMAIL_INPUT)
        
        # Assert
        assert signup_page.is_email_valid(), "Valid email should show success state"
        logger.info("✓ Test passed: Valid email shows success")


class TestSignupNavigation:
    """Tests for signup page navigation."""
    
    @pytest.mark.auth
    def test_navigate_to_login_from_signup(self, page):
        """Test navigation to login page from signup page."""
        # Arrange
        signup_page = SignupPage(page)
        
        # Act
        signup_page.navigate()
        signup_page.click_login_link()
        signup_page.wait_for_timeout(1000)
        
        # Assert
        assert "login.html" in page.url, "Should navigate to login page"
        logger.info("✓ Test passed: Navigate to login from signup")


class TestLogout:
    """Logout functionality tests."""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_logout_functionality(self, page):
        """Test logout functionality."""
        # Arrange
        login_page = LoginPage(page)
        user = TestData.Users.PRIMARY_USER
        
        # Act - Login first
        login_page.navigate()
        login_page.login(user['username'], user['password'])
        assert login_page.is_login_successful(), "Login should be successful"
        
        # Wait for home page to fully load
        login_page.wait_for_timeout(2000)
        
        # Act - Logout
        page.click(Selectors.NavBar.LOGOUT_BUTTON)
        page.wait_for_timeout(2000)
        
        # Assert
        assert "login.html" in page.url, "Should redirect to login page after logout"
        logger.info("✓ Test passed: Logout functionality")
    
    @pytest.mark.auth
    def test_logout_clears_session(self, page):
        """Test that logout clears the user session from localStorage."""
        # Arrange
        login_page = LoginPage(page)
        user = TestData.Users.PRIMARY_USER
        
        # Act - Login first
        login_page.navigate()
        login_page.login(user['username'], user['password'])
        assert login_page.is_login_successful(), "Login should be successful"
        
        # Verify token exists after login
        login_page.wait_for_timeout(1000)
        token_before = login_page.get_local_storage("token")
        assert token_before, "Token should exist after login"
        
        # Act - Logout
        page.click(Selectors.NavBar.LOGOUT_BUTTON)
        page.wait_for_timeout(2000)
        
        # Assert - Token should be cleared
        token_after = login_page.get_local_storage("token")
        assert not token_after, "Token should be cleared after logout"
        logger.info("✓ Test passed: Logout clears session")
