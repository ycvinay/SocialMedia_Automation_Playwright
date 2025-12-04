"""
Constants package for Playwright UI automation tests.
Contains all selectors, test data, URLs, messages, and configuration.
"""

from .selectors import Selectors
from .test_data import TestData
from .urls import URLs
from .messages import Messages
from .config import Config

__all__ = ['Selectors', 'TestData', 'URLs', 'Messages', 'Config']
