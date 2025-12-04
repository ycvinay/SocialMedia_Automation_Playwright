"""
Base Page class for all page objects.
Contains common methods and utilities used across all pages.
"""

from playwright.sync_api import Page, expect
from constants.config import Config
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page):
        """
        Initialize base page.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.timeout = Config.Timeouts.DEFAULT
    
    # ==================== NAVIGATION ====================
    
    def navigate(self, url: str):
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, timeout=Config.Timeouts.NAVIGATION)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """Wait for page to be fully loaded."""
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=Config.Timeouts.SHORT)
    
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    def reload_page(self):
        """Reload the current page."""
        logger.info("Reloading page")
        self.page.reload()
        self.wait_for_page_load()
    
    # ==================== ELEMENT INTERACTIONS ====================
    
    def click(self, selector: str, timeout: int = None):
        """
        Click an element.
        
        Args:
            selector: CSS selector
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        logger.debug(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector: str, text: str, timeout: int = None):
        """
        Fill an input field.
        
        Args:
            selector: CSS selector
            text: Text to fill
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        logger.debug(f"Filling '{selector}' with: {text}")
        self.page.fill(selector, text, timeout=timeout)
    
    def type_text(self, selector: str, text: str, delay: int = 50):
        """
        Type text with delay (simulates human typing).
        
        Args:
            selector: CSS selector
            text: Text to type
            delay: Delay between keystrokes in ms
        """
        logger.debug(f"Typing into '{selector}': {text}")
        self.page.type(selector, text, delay=delay)
    
    def select_option(self, selector: str, value: str):
        """
        Select an option from dropdown.
        
        Args:
            selector: CSS selector
            value: Option value to select
        """
        logger.debug(f"Selecting option '{value}' in '{selector}'")
        self.page.select_option(selector, value)
    
    def check(self, selector: str):
        """Check a checkbox."""
        logger.debug(f"Checking checkbox: {selector}")
        self.page.check(selector)
    
    def uncheck(self, selector: str):
        """Uncheck a checkbox."""
        logger.debug(f"Unchecking checkbox: {selector}")
        self.page.uncheck(selector)
    
    def upload_file(self, selector: str, file_path: str):
        """
        Upload a file.
        
        Args:
            selector: File input selector
            file_path: Path to file
        """
        logger.debug(f"Uploading file '{file_path}' to '{selector}'")
        self.page.set_input_files(selector, file_path)
    
    # ==================== ELEMENT QUERIES ====================
    
    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: CSS selector
            timeout: Optional timeout override
            
        Returns:
            True if visible, False otherwise
        """
        timeout = timeout or Config.Timeouts.ELEMENT_WAIT
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def is_hidden(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is hidden.
        
        Args:
            selector: CSS selector
            timeout: Optional timeout override
            
        Returns:
            True if hidden, False otherwise
        """
        timeout = timeout or Config.Timeouts.ELEMENT_WAIT
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
            return True
        except Exception:
            return False
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        return self.page.is_enabled(selector)
    
    def is_disabled(self, selector: str) -> bool:
        """Check if element is disabled."""
        return self.page.is_disabled(selector)
    
    def is_checked(self, selector: str) -> bool:
        """Check if checkbox is checked."""
        return self.page.is_checked(selector)
    
    def get_text(self, selector: str) -> str:
        """
        Get text content of element.
        
        Args:
            selector: CSS selector
            
        Returns:
            Text content
        """
        return self.page.text_content(selector) or ""
    
    def get_inner_text(self, selector: str) -> str:
        """Get inner text of element."""
        return self.page.inner_text(selector)
    
    def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Get attribute value of element.
        
        Args:
            selector: CSS selector
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        return self.page.get_attribute(selector, attribute) or ""
    
    def get_value(self, selector: str) -> str:
        """Get value of input element."""
        return self.page.input_value(selector)
    
    def count_elements(self, selector: str) -> int:
        """
        Count number of elements matching selector.
        
        Args:
            selector: CSS selector
            
        Returns:
            Number of elements
        """
        return self.page.locator(selector).count()
    
    # ==================== WAIT METHODS ====================
    
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = None):
        """
        Wait for selector.
        
        Args:
            selector: CSS selector
            state: Element state (visible, hidden, attached, detached)
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for selector '{selector}' to be {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
    
    def wait_for_url(self, url: str, timeout: int = None):
        """
        Wait for URL to match.
        
        Args:
            url: Expected URL (can be regex)
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for URL: {url}")
        self.page.wait_for_url(url, timeout=timeout)
    
    def wait_for_timeout(self, timeout: int):
        """
        Wait for specified timeout.
        
        Args:
            timeout: Timeout in milliseconds
        """
        logger.debug(f"Waiting for {timeout}ms")
        self.page.wait_for_timeout(timeout)
    
    # ==================== ASSERTIONS ====================
    
    def expect_visible(self, selector: str):
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible()
    
    def expect_hidden(self, selector: str):
        """Assert element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden()
    
    def expect_text(self, selector: str, text: str):
        """Assert element contains text."""
        expect(self.page.locator(selector)).to_contain_text(text)
    
    def expect_value(self, selector: str, value: str):
        """Assert input has value."""
        expect(self.page.locator(selector)).to_have_value(value)
    
    def expect_url(self, url: str):
        """Assert current URL."""
        expect(self.page).to_have_url(url)
    
    # ==================== SCREENSHOT ====================
    
    def take_screenshot(self, path: str, full_page: bool = True):
        """
        Take screenshot.
        
        Args:
            path: Screenshot file path
            full_page: Capture full page
        """
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path, full_page=full_page)
    
    # ==================== JAVASCRIPT EXECUTION ====================
    
    def execute_script(self, script: str, *args):
        """
        Execute JavaScript.
        
        Args:
            script: JavaScript code
            *args: Arguments to pass to script
            
        Returns:
            Script return value
        """
        return self.page.evaluate(script, *args)
    
    def scroll_to_element(self, selector: str):
        """Scroll element into view."""
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    def scroll_to_top(self):
        """Scroll to top of page."""
        self.execute_script("window.scrollTo(0, 0)")
    
    # ==================== LOCAL STORAGE ====================
    
    def get_local_storage(self, key: str) -> str:
        """Get item from local storage."""
        return self.execute_script(f"return localStorage.getItem('{key}')")
    
    def set_local_storage(self, key: str, value: str):
        """Set item in local storage."""
        self.execute_script(f"localStorage.setItem('{key}', '{value}')")
    
    def clear_local_storage(self):
        """Clear local storage."""
        self.execute_script("localStorage.clear()")
    
    # ==================== ALERTS & DIALOGS ====================
    
    def accept_alert(self):
        """Accept alert dialog."""
        self.page.on("dialog", lambda dialog: dialog.accept())
    
    def dismiss_alert(self):
        """Dismiss alert dialog."""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
