"""Quick test to verify basic functionality works."""
import sys
sys.path.insert(0, '.')

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from constants.urls import URLs

def test_login_page():
    print(f"Testing with BASE_URL: {URLs.BASE_URL}")
    print(f"Login URL: {URLs.Pages.login()}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        print(f"Current URL: {page.url}")
        print(f"Is on login page: {login_page.is_on_login_page()}")
        print(f"Username input visible: {login_page.is_username_input_visible()}")
        print(f"Password input visible: {login_page.is_password_input_visible()}")
        print(f"Login button visible: {login_page.is_login_button_visible()}")
        
        # Take screenshot
        page.screenshot(path="login_page_test.png")
        print("Screenshot saved to login_page_test.png")
        
        browser.close()
        print("Test completed successfully!")

if __name__ == "__main__":
    test_login_page()
