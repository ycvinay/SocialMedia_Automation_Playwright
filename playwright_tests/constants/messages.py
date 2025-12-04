"""
Expected messages and text content for validation.
Success messages, error messages, and UI text.
"""


class Messages:
    """Expected messages throughout the application."""
    
    # ==================== AUTHENTICATION MESSAGES ====================
    class Auth:
        """Authentication related messages."""
        
        # Success messages
        LOGIN_SUCCESS = "Login successful"
        SIGNUP_SUCCESS = "Registration successful"
        LOGOUT_SUCCESS = "Logged out successfully"
        
        # Error messages
        INVALID_CREDENTIALS = "Invalid credentials"
        USER_NOT_FOUND = "User not found"
        USER_ALREADY_EXISTS = "User already exists"
        USERNAME_TAKEN = "Username already taken"
        EMAIL_TAKEN = "Email already registered"
        
        # Validation messages
        USERNAME_REQUIRED = "Username is required"
        PASSWORD_REQUIRED = "Password is required"
        EMAIL_REQUIRED = "Email is required"
        NAME_REQUIRED = "Name is required"
        PASSWORD_MISMATCH = "Passwords do not match"
        PASSWORD_TOO_SHORT = "Password must be at least 6 characters"
        INVALID_EMAIL = "Invalid email format"
        
        # Session messages
        SESSION_EXPIRED = "Session expired"
        UNAUTHORIZED = "Unauthorized access"
        LOGIN_REQUIRED = "Please login to continue"
    
    # ==================== POST MESSAGES ====================
    class Posts:
        """Post related messages."""
        
        # Success messages
        POST_CREATED = "Post created successfully"
        POST_UPDATED = "Post updated successfully"
        POST_DELETED = "Post deleted successfully"
        POST_LIKED = "Post liked"
        POST_UNLIKED = "Post unliked"
        COMMENT_ADDED = "Comment added successfully"
        
        # Error messages
        POST_NOT_FOUND = "Post not found"
        CANNOT_EDIT_POST = "You cannot edit this post"
        CANNOT_DELETE_POST = "You cannot delete this post"
        POST_CONTENT_REQUIRED = "Post content is required"
        COMMENT_REQUIRED = "Comment cannot be empty"
        
        # Validation messages
        POST_TOO_LONG = "Post content is too long"
        INVALID_IMAGE = "Invalid image file"
        IMAGE_TOO_LARGE = "Image file is too large"
        
        # Empty states
        NO_POSTS = "No posts yet"
        NO_POSTS_FOUND = "No posts found"
        NO_COMMENTS = "No comments yet"
        NO_LIKES = "No likes yet"
    
    # ==================== PROFILE MESSAGES ====================
    class Profile:
        """Profile related messages."""
        
        # Success messages
        PROFILE_UPDATED = "Profile updated successfully"
        AVATAR_UPDATED = "Avatar updated successfully"
        
        # Error messages
        PROFILE_NOT_FOUND = "Profile not found"
        UPDATE_FAILED = "Failed to update profile"
        INVALID_AVATAR = "Invalid avatar file"
        AVATAR_TOO_LARGE = "Avatar file is too large"
        
        # Validation messages
        NAME_REQUIRED = "Name is required"
        BIO_TOO_LONG = "Bio is too long"
    
    # ==================== FRIEND MESSAGES ====================
    class Friends:
        """Friend related messages."""
        
        # Success messages
        FRIEND_REQUEST_SENT = "Friend request sent"
        FRIEND_REQUEST_ACCEPTED = "Friend request accepted"
        FRIEND_REQUEST_REJECTED = "Friend request rejected"
        FRIEND_REQUEST_CANCELLED = "Friend request cancelled"
        FRIEND_REMOVED = "Friend removed"
        
        # Error messages
        REQUEST_ALREADY_SENT = "Friend request already sent"
        ALREADY_FRIENDS = "Already friends"
        CANNOT_ADD_YOURSELF = "You cannot add yourself as a friend"
        REQUEST_NOT_FOUND = "Friend request not found"
        NOT_FRIENDS = "You are not friends"
        
        # Empty states
        NO_FRIENDS = "No friends yet"
        NO_FRIEND_REQUESTS = "No friend requests"
        NO_SUGGESTIONS = "No suggestions available"
    
    # ==================== SEARCH MESSAGES ====================
    class Search:
        """Search related messages."""
        
        NO_RESULTS = "No users found"
        SEARCH_REQUIRED = "Please enter a search query"
        SEARCH_TOO_SHORT = "Search query is too short"
    
    # ==================== NOTIFICATION MESSAGES ====================
    class Notifications:
        """Notification related messages."""
        
        # Notification types
        FRIEND_REQUEST_RECEIVED = "sent you a friend request"
        FRIEND_REQUEST_ACCEPTED_MSG = "accepted your friend request"
        POST_LIKED = "liked your post"
        POST_COMMENTED = "commented on your post"
        
        # Actions
        NOTIFICATIONS_CLEARED = "All notifications cleared"
        NOTIFICATION_MARKED_READ = "Notification marked as read"
        
        # Empty state
        NO_NOTIFICATIONS = "No notifications"
    
    # ==================== GENERAL MESSAGES ====================
    class General:
        """General application messages."""
        
        # Loading states
        LOADING = "Loading..."
        PLEASE_WAIT = "Please wait..."
        PROCESSING = "Processing..."
        
        # Confirmation messages
        CONFIRM_DELETE = "Are you sure you want to delete this?"
        CONFIRM_REMOVE_FRIEND = "Are you sure you want to remove this friend?"
        CONFIRM_LOGOUT = "Are you sure you want to logout?"
        
        # Network errors
        NETWORK_ERROR = "Network error occurred"
        SERVER_ERROR = "Server error occurred"
        CONNECTION_FAILED = "Connection failed"
        
        # Success
        SUCCESS = "Success"
        OPERATION_SUCCESSFUL = "Operation completed successfully"
        
        # Error
        ERROR = "Error"
        SOMETHING_WENT_WRONG = "Something went wrong"
        TRY_AGAIN = "Please try again"
        
        # Validation
        REQUIRED_FIELD = "This field is required"
        INVALID_INPUT = "Invalid input"
    
    # ==================== PAGE TITLES ====================
    class PageTitles:
        """Expected page titles."""
        
        LOGIN = "Login"
        SIGNUP = "Sign Up"
        HOME = "Home"
        PROFILE = "Profile"
        FRIENDS = "Friends"
        EXPLORE = "Explore"
        NOTIFICATIONS = "Notifications"
