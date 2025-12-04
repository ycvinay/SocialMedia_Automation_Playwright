"""
URL constants for the application.
Centralized URL management for all pages and API endpoints.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class URLs:
    """Application URLs and API endpoints."""
    
    # ==================== BASE URLS ====================
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
    
    # ==================== FRONTEND PAGES ====================
    class Pages:
        """Frontend page URLs."""
        
        @staticmethod
        def get_base_url():
            return URLs.BASE_URL
        
        @staticmethod
        def login():
            return f"{URLs.BASE_URL}/views/login.html"
        
        @staticmethod
        def signup():
            return f"{URLs.BASE_URL}/views/signup.html"
        
        @staticmethod
        def home():
            return f"{URLs.BASE_URL}/views/home.html"
        
        @staticmethod
        def profile():
            return f"{URLs.BASE_URL}/views/profile.html"
        
        @staticmethod
        def user_profile(user_id):
            return f"{URLs.BASE_URL}/views/user-profile.html?id={user_id}"
        
        @staticmethod
        def friends():
            return f"{URLs.BASE_URL}/views/friends.html"
        
        @staticmethod
        def explore():
            return f"{URLs.BASE_URL}/views/explore.html"
        
        @staticmethod
        def notifications():
            return f"{URLs.BASE_URL}/views/notifications.html"
        
        @staticmethod
        def forgot_password():
            return f"{URLs.BASE_URL}/views/forgot-password.html"
        
        @staticmethod
        def reset_password():
            return f"{URLs.BASE_URL}/views/reset-password.html"
    
    # ==================== API ENDPOINTS ====================
    class API:
        """Backend API endpoints."""
        
        # Authentication
        @staticmethod
        def register():
            return f"{URLs.API_BASE_URL}/auth/register"
        
        @staticmethod
        def login():
            return f"{URLs.API_BASE_URL}/auth/login"
        
        # User
        @staticmethod
        def get_current_user():
            return f"{URLs.API_BASE_URL}/user/me"
        
        @staticmethod
        def get_user_profile(user_id):
            return f"{URLs.API_BASE_URL}/user/profile/{user_id}"
        
        @staticmethod
        def update_profile():
            return f"{URLs.API_BASE_URL}/user/update-profile"
        
        @staticmethod
        def search_users():
            return f"{URLs.API_BASE_URL}/user/search"
        
        @staticmethod
        def explore_users():
            return f"{URLs.API_BASE_URL}/user/explore"
        
        # Posts
        @staticmethod
        def create_post():
            return f"{URLs.API_BASE_URL}/posts/create"
        
        @staticmethod
        def edit_post(post_id):
            return f"{URLs.API_BASE_URL}/posts/edit/{post_id}"
        
        @staticmethod
        def delete_post(post_id):
            return f"{URLs.API_BASE_URL}/posts/delete/{post_id}"
        
        @staticmethod
        def get_feed():
            return f"{URLs.API_BASE_URL}/posts/feed"
        
        @staticmethod
        def get_my_posts():
            return f"{URLs.API_BASE_URL}/posts/myPosts"
        
        @staticmethod
        def get_user_posts(user_id):
            return f"{URLs.API_BASE_URL}/posts/user/posts/{user_id}"
        
        @staticmethod
        def like_post():
            return f"{URLs.API_BASE_URL}/posts/like"
        
        @staticmethod
        def unlike_post():
            return f"{URLs.API_BASE_URL}/posts/unlike"
        
        @staticmethod
        def add_comment():
            return f"{URLs.API_BASE_URL}/posts/comments/add"
        
        @staticmethod
        def get_comments(post_id):
            return f"{URLs.API_BASE_URL}/posts/comments/{post_id}"
        
        @staticmethod
        def get_likes(post_id):
            return f"{URLs.API_BASE_URL}/posts/likes/{post_id}"
        
        # Friends
        @staticmethod
        def send_friend_request(user_id):
            return f"{URLs.API_BASE_URL}/friends/send-request/{user_id}"
        
        @staticmethod
        def respond_to_request():
            return f"{URLs.API_BASE_URL}/friends/respond-request"
        
        @staticmethod
        def cancel_request(user_id):
            return f"{URLs.API_BASE_URL}/friends/cancel-request/{user_id}"
        
        @staticmethod
        def get_friend_requests():
            return f"{URLs.API_BASE_URL}/friends/requests"
        
        @staticmethod
        def get_friends_list():
            return f"{URLs.API_BASE_URL}/friends/list"
        
        @staticmethod
        def remove_friend(user_id):
            return f"{URLs.API_BASE_URL}/friends/remove/{user_id}"
