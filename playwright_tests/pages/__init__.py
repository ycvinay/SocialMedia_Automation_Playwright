"""
Pages package for Page Object Model.
Contains page classes for all application pages.
"""

from .base_page import BasePage
from .login_page import LoginPage
from .signup_page import SignupPage
from .home_page import HomePage
from .profile_page import ProfilePage
from .friends_page import FriendsPage
from .explore_page import ExplorePage
from .notifications_page import NotificationsPage

__all__ = [
    'BasePage',
    'LoginPage',
    'SignupPage',
    'HomePage',
    'ProfilePage',
    'FriendsPage',
    'ExplorePage',
    'NotificationsPage'
]
