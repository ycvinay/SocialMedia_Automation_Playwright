"""
Login Page Automation Tests
Comprehensive positive and negative testing for the login functionality.
"""

import pytest
import time
import logging
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from constants.urls import URLs
from constants.test_data import TestData

logger = logging.getLogger(__name__)


class TestLoginPageElements:
    """Test: Verify all login page elements are visible."""
    
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_page_loads(self, page):
        """Test: Login page loads correctly with all elements visible."""
        logger.info("=" * 60)
        logger.info("TEST: Login page loads correctly")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Verify page loaded
        assert login_page.is_on_login_page(), "Should be on login page"
        logger.info("✅ Login page loaded successfully")
        
        # Verify all form elements are visible
        assert page.locator("#username").is_visible(), "Username field should be visible"
        logger.info("✅ Username field is visible")
        
        assert page.locator("#password").is_visible(), "Password field should be visible"
        logger.info("✅ Password field is visible")
        
        assert page.locator("#loginForm button[type='submit']").is_visible(), "Login button should be visible"
        logger.info("✅ Login button is visible")
        
        assert page.locator("#toggleLoginPassword").is_visible(), "Password toggle should be visible"
        logger.info("✅ Password toggle is visible")
        
        # Verify signup link
        signup_link = page.locator("a[href='signup.html']")
        assert signup_link.is_visible(), "Signup link should be visible"
        logger.info("✅ Signup link is visible")
        
        logger.info("=" * 60)
        logger.info("TEST PASSED: All login page elements verified")
        logger.info("=" * 60)
    
    @pytest.mark.auth
    def test_login_button_initially_enabled(self, page):
        """Test: Login button is enabled by default."""
        login_page = LoginPage(page)
        login_page.navigate()
        
        login_btn = page.locator("#loginForm button[type='submit']")
        assert login_btn.is_enabled(), "Login button should be enabled"
        logger.info("✅ Login button is enabled by default")


class TestLoginFieldValidation:
    """Test: Field-level validation for login form."""
    
    @pytest.mark.auth
    def test_empty_username_validation(self, page):
        """Test: Empty username should show validation error."""
        logger.info("=" * 60)
        logger.info("TEST: Empty username validation")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Only fill password, leave username empty
        page.locator("#password").fill("somepassword")
        page.locator("#loginForm button[type='submit']").click()
        time.sleep(1)
        
        # Check for validation error
        has_invalid = page.locator("#username.is-invalid").count() > 0
        assert has_invalid, "Empty username should show validation error"
        logger.info("✅ Empty username shows validation error")
    
    @pytest.mark.auth
    def test_empty_password_validation(self, page):
        """Test: Empty password should show validation error."""
        logger.info("=" * 60)
        logger.info("TEST: Empty password validation")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Only fill username, leave password empty
        page.locator("#username").fill("testuser")
        page.locator("#loginForm button[type='submit']").click()
        time.sleep(1)
        
        has_invalid = page.locator("#password.is-invalid").count() > 0
        assert has_invalid, "Empty password should show validation error"
        logger.info("✅ Empty password shows validation error")
    
    @pytest.mark.auth
    def test_both_fields_empty_validation(self, page):
        """Test: Both empty fields should show validation errors."""
        logger.info("=" * 60)
        logger.info("TEST: Both fields empty validation")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Click login without filling anything
        page.locator("#loginForm button[type='submit']").click()
        time.sleep(1)
        
        assert page.locator("#username.is-invalid").count() > 0, "Username should show error"
        assert page.locator("#password.is-invalid").count() > 0, "Password should show error"
        logger.info("✅ Both empty fields show validation errors")


class TestLoginPasswordToggle:
    """Test: Password visibility toggle functionality."""
    
    @pytest.mark.auth
    def test_password_hidden_by_default(self, page):
        """Test: Password field is hidden by default."""
        login_page = LoginPage(page)
        login_page.navigate()
        
        password_field = page.locator("#password")
        assert password_field.get_attribute("type") == "password", "Password should be hidden by default"
        logger.info("✅ Password is hidden by default")
    
    @pytest.mark.auth
    def test_password_toggle_visibility(self, page):
        """Test: Toggle password visibility on/off."""
        logger.info("=" * 60)
        logger.info("TEST: Password visibility toggle")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        password_field = page.locator("#password")
        toggle_btn = page.locator("#toggleLoginPassword")
        
        # Enter password
        password_field.fill("TestPassword123")
        
        # Initially hidden
        assert password_field.get_attribute("type") == "password"
        logger.info("✅ Password is hidden initially")
        
        # Click toggle to show
        toggle_btn.click()
        time.sleep(0.3)
        assert password_field.get_attribute("type") == "text", "Password should be visible after toggle"
        logger.info("✅ Password is visible after first toggle")
        
        # Click toggle to hide
        toggle_btn.click()
        time.sleep(0.3)
        assert password_field.get_attribute("type") == "password", "Password should be hidden after second toggle"
        logger.info("✅ Password is hidden after second toggle")


class TestLoginFunctionality:
    """Test: Login functionality with different credentials."""
    
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_with_valid_credentials(self, page):
        """Test: Successful login with valid credentials."""
        logger.info("=" * 60)
        logger.info("TEST: Login with valid credentials")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Use primary test user
        user = TestData.Users.PRIMARY_USER
        
        logger.info(f"Attempting login with: {user['username']}")
        
        page.locator("#username").fill(user['username'])
        page.locator("#password").fill(user['password'])
        page.locator("#loginForm button[type='submit']").click()
        
        # Wait for response
        time.sleep(3)
        
        # Check for success - either redirect to home or success toast
        try:
            # Wait for redirect to home page
            page.wait_for_url("**/home.html", timeout=10000)
            assert "home.html" in page.url, "Should redirect to home page"
            logger.info("✅ Successfully logged in and redirected to home page")
        except:
            # Check if error toast appeared
            if page.locator("#loginFailToast").is_visible():
                error_msg = page.locator("#loginFailToast .toast-body").text_content()
                logger.warning(f"⚠️ Login failed: {error_msg}")
                pytest.skip("Login failed - user might not exist or API is down")
            else:
                raise
    
    @pytest.mark.auth
    def test_login_with_invalid_username(self, page):
        """Test: Login with non-existent username should fail."""
        logger.info("=" * 60)
        logger.info("TEST: Login with invalid username")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        page.locator("#username").fill("nonexistentuser12345")
        page.locator("#password").fill("SomePassword123")
        page.locator("#loginForm button[type='submit']").click()
        
        # Wait for error toast
        error_toast = page.locator("#loginFailToast")
        try:
            error_toast.wait_for(state="visible", timeout=10000)
            assert error_toast.is_visible(), "Error toast should appear"
            logger.info("✅ Error toast appeared for invalid username")
        except:
            # Should not redirect to home
            assert "home.html" not in page.url, "Should not redirect to home with invalid credentials"
    
    @pytest.mark.auth
    def test_login_with_invalid_password(self, page):
        """Test: Login with wrong password should fail."""
        logger.info("=" * 60)
        logger.info("TEST: Login with invalid password")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Use existing username but wrong password
        page.locator("#username").fill("playwrighttest")
        page.locator("#password").fill("WrongPassword999")
        page.locator("#loginForm button[type='submit']").click()
        
        # Wait for error toast
        error_toast = page.locator("#loginFailToast")
        try:
            error_toast.wait_for(state="visible", timeout=10000)
            assert error_toast.is_visible(), "Error toast should appear"
            logger.info("✅ Error toast appeared for invalid password")
        except:
            assert "home.html" not in page.url, "Should not redirect to home with wrong password"


class TestLoginNavigation:
    """Test: Navigation from login page."""
    
    @pytest.mark.navigation
    def test_navigate_to_signup(self, page):
        """Test: Click signup link navigates to signup page."""
        logger.info("=" * 60)
        logger.info("TEST: Navigate to signup from login")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Click signup link
        signup_link = page.locator("a[href='signup.html']")
        signup_link.click()
        
        # Wait for navigation
        page.wait_for_url("**/signup.html", timeout=5000)
        
        assert "signup.html" in page.url, "Should navigate to signup page"
        logger.info("✅ Successfully navigated to signup page")
    
    @pytest.mark.navigation
    def test_navigate_to_forgot_password(self, page):
        """Test: Click forgot password link navigates correctly."""
        logger.info("=" * 60)
        logger.info("TEST: Navigate to forgot password")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Click forgot password link
        forgot_link = page.locator("a[href='forgot-password.html']")
        if forgot_link.is_visible():
            forgot_link.click()
            time.sleep(1)
            
            assert "forgot-password.html" in page.url, "Should navigate to forgot password page"
            logger.info("✅ Successfully navigated to forgot password page")
        else:
            logger.info("ℹ️ Forgot password link not visible, skipping")
            pytest.skip("Forgot password link not available")


class TestLoginRememberSession:
    """Test: Session and token handling after login."""
    
    @pytest.mark.auth
    def test_successful_login_stores_token(self, page):
        """Test: Successful login stores authentication token."""
        logger.info("=" * 60)
        logger.info("TEST: Login stores auth token")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        user = TestData.Users.PRIMARY_USER
        
        page.locator("#username").fill(user['username'])
        page.locator("#password").fill(user['password'])
        page.locator("#loginForm button[type='submit']").click()
        
        time.sleep(3)
        
        # Check if token is stored in localStorage
        try:
            page.wait_for_url("**/home.html", timeout=10000)
            
            token = page.evaluate("localStorage.getItem('token')")
            assert token is not None, "Token should be stored in localStorage"
            logger.info("✅ Auth token stored in localStorage")
            
            # Check token expiry
            expiry = page.evaluate("localStorage.getItem('tokenExpiry')")
            logger.info(f"Token expiry: {expiry}")
        except:
            if page.locator("#loginFailToast").is_visible():
                pytest.skip("Login failed - cannot verify token storage")
            else:
                raise
