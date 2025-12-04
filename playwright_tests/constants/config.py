"""
Test configuration settings.
Browser settings, timeouts, and test execution parameters.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Test configuration settings."""
    
    # ==================== BROWSER SETTINGS ====================
    class Browser:
        """Browser configuration."""
        
        # Browser type (chromium, firefox, webkit)
        BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')
        
        # Headless mode
        HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
        
        # Slow motion (milliseconds) - useful for debugging
        SLOW_MO = int(os.getenv('SLOW_MO', '0'))
        
        # Browser arguments
        BROWSER_ARGS = [
            '--start-maximized',
            '--disable-blink-features=AutomationControlled',
        ]
        
        # Viewport size
        VIEWPORT_WIDTH = int(os.getenv('VIEWPORT_WIDTH', '1920'))
        VIEWPORT_HEIGHT = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
        
        # Device scale factor
        DEVICE_SCALE_FACTOR = float(os.getenv('DEVICE_SCALE_FACTOR', '1'))
        
        # User agent (optional)
        USER_AGENT = os.getenv('USER_AGENT', '')
    
    # ==================== TIMEOUT SETTINGS ====================
    class Timeouts:
        """Timeout configurations in milliseconds."""
        
        # Default timeout for all operations
        DEFAULT = int(os.getenv('DEFAULT_TIMEOUT', '30000'))  # 30 seconds
        
        # Navigation timeout
        NAVIGATION = int(os.getenv('NAVIGATION_TIMEOUT', '30000'))  # 30 seconds
        
        # Element wait timeout
        ELEMENT_WAIT = int(os.getenv('ELEMENT_WAIT_TIMEOUT', '10000'))  # 10 seconds
        
        # API request timeout
        API_REQUEST = int(os.getenv('API_REQUEST_TIMEOUT', '30000'))  # 30 seconds
        
        # Short timeout for quick operations
        SHORT = int(os.getenv('SHORT_TIMEOUT', '5000'))  # 5 seconds
        
        # Long timeout for slow operations
        LONG = int(os.getenv('LONG_TIMEOUT', '60000'))  # 60 seconds
        
        # File upload timeout
        FILE_UPLOAD = int(os.getenv('FILE_UPLOAD_TIMEOUT', '30000'))  # 30 seconds
    
    # ==================== SCREENSHOT SETTINGS ====================
    class Screenshot:
        """Screenshot configuration."""
        
        # Take screenshot on failure
        ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
        
        # Screenshot directory
        DIRECTORY = os.getenv('SCREENSHOT_DIR', 'screenshots')
        
        # Screenshot format (png, jpeg)
        FORMAT = os.getenv('SCREENSHOT_FORMAT', 'png')
        
        # Full page screenshot
        FULL_PAGE = os.getenv('SCREENSHOT_FULL_PAGE', 'True').lower() == 'true'
        
        # Screenshot quality (0-100 for jpeg)
        QUALITY = int(os.getenv('SCREENSHOT_QUALITY', '90'))
    
    # ==================== VIDEO SETTINGS ====================
    class Video:
        """Video recording configuration."""
        
        # Record video
        ENABLED = os.getenv('VIDEO_ENABLED', 'False').lower() == 'true'
        
        # Video directory
        DIRECTORY = os.getenv('VIDEO_DIR', 'videos')
        
        # Video size
        WIDTH = int(os.getenv('VIDEO_WIDTH', '1920'))
        HEIGHT = int(os.getenv('VIDEO_HEIGHT', '1080'))
        
        # Retain video on success
        RETAIN_ON_SUCCESS = os.getenv('VIDEO_RETAIN_ON_SUCCESS', 'False').lower() == 'true'
    
    # ==================== TEST EXECUTION SETTINGS ====================
    class Execution:
        """Test execution configuration."""
        
        # Parallel execution
        PARALLEL = os.getenv('PARALLEL_EXECUTION', 'False').lower() == 'true'
        
        # Number of workers for parallel execution
        WORKERS = int(os.getenv('WORKERS', '4'))
        
        # Retry failed tests
        RETRY_FAILED = int(os.getenv('RETRY_FAILED', '0'))
        
        # Maximum failures before stopping
        MAX_FAILURES = int(os.getenv('MAX_FAILURES', '0'))  # 0 = no limit
        
        # Test data cleanup
        CLEANUP_TEST_DATA = os.getenv('CLEANUP_TEST_DATA', 'True').lower() == 'true'
    
    # ==================== REPORTING SETTINGS ====================
    class Reporting:
        """Test reporting configuration."""
        
        # Report directory
        DIRECTORY = os.getenv('REPORT_DIR', 'reports')
        
        # Report format (html, json, xml)
        FORMAT = os.getenv('REPORT_FORMAT', 'html')
        
        # Generate Allure report
        ALLURE_ENABLED = os.getenv('ALLURE_ENABLED', 'False').lower() == 'true'
        
        # Allure results directory
        ALLURE_RESULTS_DIR = os.getenv('ALLURE_RESULTS_DIR', 'allure-results')
    
    # ==================== ENVIRONMENT SETTINGS ====================
    class Environment:
        """Environment configuration."""
        
        # Test environment (dev, staging, production)
        ENV = os.getenv('TEST_ENV', 'dev')
        
        # Base URL (from urls.py)
        BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
        
        # API Base URL
        API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
        
        # Database cleanup
        DB_CLEANUP = os.getenv('DB_CLEANUP', 'False').lower() == 'true'
    
    # ==================== LOGGING SETTINGS ====================
    class Logging:
        """Logging configuration."""
        
        # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Log file
        LOG_FILE = os.getenv('LOG_FILE', 'test_execution.log')
        
        # Log format
        FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Console logging
        CONSOLE_LOGGING = os.getenv('CONSOLE_LOGGING', 'True').lower() == 'true'
    
    # ==================== FILE PATHS ====================
    class Paths:
        """File paths for test resources."""
        
        # Test data directory
        TEST_DATA_DIR = 'test_data'
        
        # Sample images for testing
        SAMPLE_AVATAR = os.path.join(TEST_DATA_DIR, 'sample_avatar.jpg')
        SAMPLE_POST_IMAGE = os.path.join(TEST_DATA_DIR, 'sample_post.jpg')
        
        # Test files
        LARGE_IMAGE = os.path.join(TEST_DATA_DIR, 'large_image.jpg')
        INVALID_FILE = os.path.join(TEST_DATA_DIR, 'invalid_file.txt')
