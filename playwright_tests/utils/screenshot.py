"""
Screenshot Utilities.
Helper functions for taking and managing screenshots.
"""

import os
from datetime import datetime
from constants.config import Config
import logging

logger = logging.getLogger(__name__)


class ScreenshotHelper:
    """Screenshot helper class."""
    
    def __init__(self, page):
        """
        Initialize screenshot helper.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.screenshot_dir = Config.Screenshot.DIRECTORY
        
        # Create directory if not exists
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, name: str, full_page: bool = True) -> str:
        """
        Take screenshot.
        
        Args:
            name: Screenshot name
            full_page: Capture full page
            
        Returns:
            Screenshot file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.{Config.Screenshot.FORMAT}"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        self.page.screenshot(path=filepath, full_page=full_page)
        logger.info(f"Screenshot saved: {filepath}")
        
        return filepath
    
    def take_element_screenshot(self, selector: str, name: str) -> str:
        """
        Take screenshot of specific element.
        
        Args:
            selector: Element selector
            name: Screenshot name
            
        Returns:
            Screenshot file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.{Config.Screenshot.FORMAT}"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        element = self.page.locator(selector)
        element.screenshot(path=filepath)
        logger.info(f"Element screenshot saved: {filepath}")
        
        return filepath
    
    def take_failure_screenshot(self, test_name: str) -> str:
        """
        Take screenshot on test failure.
        
        Args:
            test_name: Test name
            
        Returns:
            Screenshot file path
        """
        return self.take_screenshot(f"FAILED_{test_name}")
