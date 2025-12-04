"""
Simple Pytest configuration for Playwright tests.
Uses a SINGLE browser for all tests.
Clears cache only after navigating to our app.
"""

import pytest
import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright
from constants.config import Config
from constants.urls import URLs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Global browser instances
_playwright = None
_browser = None
_context = None
_page = None


@pytest.fixture(scope="session", autouse=True)
def setup_browser():
    """Setup browser once for entire session."""
    global _playwright, _browser, _context, _page
    
    logger.info("=" * 60)
    logger.info("OPENING BROWSER...")
    
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=Config.Browser.HEADLESS,
        slow_mo=Config.Browser.SLOW_MO,
        args=['--start-maximized']
    )
    _context = _browser.new_context(viewport=None, no_viewport=True)
    _page = _context.new_page()
    _page.set_default_timeout(30000)
    
    # Clear cookies first (this works without being on a page)
    _context.clear_cookies()
    
    # Navigate to our app and then clear localStorage/sessionStorage
    logger.info(f"Navigating to app: {URLs.BASE_URL}")
    _page.goto(f"{URLs.BASE_URL}/views/signup.html")
    
    # Now we can clear localStorage and sessionStorage
    _page.evaluate("localStorage.clear(); sessionStorage.clear();")
    
    logger.info("✅ Browser ready, all cache cleared!")
    logger.info("=" * 60)
    
    yield
    
    # Cleanup
    logger.info("=" * 60)
    logger.info("CLOSING BROWSER...")
    _page.close()
    _context.close()
    _browser.close()
    _playwright.stop()
    logger.info("✅ Browser closed")
    logger.info("=" * 60)


@pytest.fixture(scope="function")
def page():
    """Provide the page for each test, resetting state."""
    global _context, _page
    
    # Navigate to signup page first (to ensure we're on our domain)
    _page.goto(f"{URLs.BASE_URL}/views/signup.html")
    
    # Now clear storage
    _page.evaluate("localStorage.clear(); sessionStorage.clear();")
    _context.clear_cookies()
    
    # Reload to apply cleared state
    _page.reload()
    
    yield _page


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the app."""
    return URLs.BASE_URL


# Screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        global _page
        if _page and Config.Screenshot.ON_FAILURE:
            os.makedirs(Config.Screenshot.DIRECTORY, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(Config.Screenshot.DIRECTORY, f"{item.name}_{timestamp}.png")
            try:
                _page.screenshot(path=path, full_page=True)
                logger.info(f"📸 Screenshot: {path}")
            except:
                pass
