"""
Helper Utilities.
Common helper functions for tests.
"""

import os
import random
import string
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def generate_random_string(length: int = 10) -> str:
    """
    Generate random string.
    
    Args:
        length: Length of string
        
    Returns:
        Random string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email() -> str:
    """
    Generate random email address.
    
    Returns:
        Random email
    """
    username = generate_random_string(8)
    return f"{username}@example.com"


def generate_timestamp() -> str:
    """
    Generate timestamp string.
    
    Returns:
        Timestamp in format YYYYMMDD_HHMMSS
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
    """
    Wait for a condition to be true.
    
    Args:
        condition_func: Function that returns boolean
        timeout: Maximum wait time in seconds
        interval: Check interval in seconds
        
    Returns:
        True if condition met, False if timeout
    """
    import time
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    
    return False


def create_directory_if_not_exists(directory: str):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory: Directory path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")


def clean_directory(directory: str):
    """
    Clean all files in directory.
    
    Args:
        directory: Directory path
    """
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")


def format_test_name(test_name: str) -> str:
    """
    Format test name for display.
    
    Args:
        test_name: Test function name
        
    Returns:
        Formatted test name
    """
    # Remove 'test_' prefix and replace underscores with spaces
    formatted = test_name.replace('test_', '').replace('_', ' ').title()
    return formatted


def log_test_start(test_name: str):
    """Log test start."""
    logger.info("=" * 80)
    logger.info(f"Starting Test: {format_test_name(test_name)}")
    logger.info("=" * 80)


def log_test_end(test_name: str, passed: bool = True):
    """Log test end."""
    status = "PASSED" if passed else "FAILED"
    logger.info("=" * 80)
    logger.info(f"Test {status}: {format_test_name(test_name)}")
    logger.info("=" * 80)
