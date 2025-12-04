"""
CSS/XPath selectors for all pages in the application.
Centralized selector management for easy maintenance.
"""


class Selectors:
    """All CSS selectors organized by page/component."""
    
    # ==================== LOGIN PAGE ====================
    class Login:
        # Form
        FORM = "#loginForm"
        USERNAME_INPUT = "#username"
        PASSWORD_INPUT = "#password"
        LOGIN_BUTTON = "#loginForm button[type='submit']"
        TOGGLE_PASSWORD = "#toggleLoginPassword"
        
        # Links
        SIGNUP_LINK = "a[href='signup.html']"
        FORGOT_PASSWORD_LINK = "a[href='forgot-password.html']"
        
        # Validation
        INVALID_FEEDBACK = ".invalid-feedback"
        IS_INVALID = ".is-invalid"
        
        # Toasts (Bootstrap)
        SUCCESS_TOAST = "#loginToast"
        ERROR_TOAST = "#loginFailToast"
        TOAST_BODY = ".toast-body"
        
        # Loading state
        BTN_SPINNER = "#btnSpinner"
        BTN_TEXT = "#btnText"
        
        # Legacy selectors (for backwards compatibility)
        ERROR_MESSAGE = "#loginFailToast .toast-body"
        SUCCESS_MESSAGE = "#loginToast .toast-body"
    
    # ==================== SIGNUP PAGE ====================
    class Signup:
        # Form
        FORM = "#signupForm"
        NAME_INPUT = "#name"
        USERNAME_INPUT = "#username"
        EMAIL_INPUT = "#email"
        PASSWORD_INPUT = "#newPassword"  # Note: Different ID than login
        SIGNUP_BUTTON = "#signupBtn"
        TOGGLE_PASSWORD = "#togglePassword"
        
        # Alert box for errors
        ALERT_BOX = "#alertBox"
        
        # Links
        LOGIN_LINK = "a[href='login.html']"
        
        # Validation
        INVALID_FEEDBACK = ".invalid-feedback"
        IS_INVALID = ".is-invalid"
        IS_VALID = ".is-valid"
        
        # Toasts (Bootstrap)
        SUCCESS_TOAST = "#signupToast"
        ERROR_TOAST = "#signupFailToast"
        TOAST_BODY = ".toast-body"
        
        # Loading state
        BTN_SPINNER = "#btnSpinner"
        BTN_TEXT = "#btnText"
        
        # Legacy selectors (for backwards compatibility)
        ERROR_MESSAGE = "#signupFailToast .toast-body"
        SUCCESS_MESSAGE = "#signupToast .toast-body"
    
    # ==================== NAVIGATION BAR ====================
    class NavBar:
        HOME_LINK = "a[href='home.html']"
        EXPLORE_LINK = "a[href='explore.html']"
        FRIENDS_LINK = "a[href='friends.html']"
        NOTIFICATIONS_LINK = "a[href='notifications.html']"
        PROFILE_LINK = "a[href='profile.html']"
        LOGOUT_BUTTON = "#logoutBtn, .logout-btn"
        ACTIVE_LINK = ".nav-link.active"
        USER_AVATAR = ".nav-avatar, .user-avatar"
        NOTIFICATION_BADGE = ".notification-badge"
    
    # ==================== HOME/FEED PAGE ====================
    class Home:
        # Post Creation
        CREATE_POST_TEXTAREA = "#postContent, textarea[name='content']"
        POST_IMAGE_INPUT = "input[type='file'][name='image']"
        CREATE_POST_BUTTON = "#createPostBtn, button.create-post-btn"
        
        # Feed
        FEED_CONTAINER = "#feed, .feed-container"
        POST_CARD = ".post-card, .post"
        POST_CONTENT = ".post-content"
        POST_IMAGE = ".post-image img"
        POST_AUTHOR = ".post-author, .author-name"
        POST_TIMESTAMP = ".post-time, .timestamp"
        
        # Post Actions
        LIKE_BUTTON = ".like-btn"
        COMMENT_BUTTON = ".comment-btn"
        SHARE_BUTTON = ".share-btn"
        EDIT_POST_BUTTON = ".edit-post-btn"
        DELETE_POST_BUTTON = ".delete-post-btn"
        POST_OPTIONS = ".post-options, .post-menu"
        
        # Likes & Comments
        LIKE_COUNT = ".like-count"
        COMMENT_COUNT = ".comment-count"
        COMMENT_INPUT = ".comment-input, input[name='comment']"
        SUBMIT_COMMENT_BUTTON = ".submit-comment-btn"
        COMMENT_LIST = ".comments-list"
        COMMENT_ITEM = ".comment-item"
        COMMENT_AUTHOR = ".comment-author"
        COMMENT_TEXT = ".comment-text"
        
        # Modals
        LIKES_MODAL = "#likesModal"
        COMMENTS_MODAL = "#commentsModal"
        EDIT_POST_MODAL = "#editPostModal"
        DELETE_CONFIRM_MODAL = "#deleteConfirmModal"
    
    # ==================== PROFILE PAGE ====================
    class Profile:
        # Profile Header
        PROFILE_AVATAR = ".profile-avatar, .avatar-img"
        PROFILE_NAME = ".profile-name"
        PROFILE_USERNAME = ".profile-username"
        PROFILE_BIO = ".profile-bio"
        EDIT_PROFILE_BUTTON = "#editProfileBtn, .edit-profile-btn"
        
        # Profile Stats
        POSTS_COUNT = ".posts-count"
        FRIENDS_COUNT = ".friends-count"
        FOLLOWERS_COUNT = ".followers-count"
        
        # Profile Actions (for other users)
        ADD_FRIEND_BUTTON = ".add-friend-btn"
        REMOVE_FRIEND_BUTTON = ".remove-friend-btn"
        CANCEL_REQUEST_BUTTON = ".cancel-request-btn"
        ACCEPT_REQUEST_BUTTON = ".accept-request-btn"
        REJECT_REQUEST_BUTTON = ".reject-request-btn"
        MESSAGE_BUTTON = ".message-btn"
        
        # User Posts
        USER_POSTS_CONTAINER = "#userPosts, .user-posts"
        NO_POSTS_MESSAGE = ".no-posts-message"
        
        # Edit Profile Modal
        EDIT_PROFILE_MODAL = "#editProfileModal"
        EDIT_NAME_INPUT = "input[name='name']"
        EDIT_BIO_TEXTAREA = "textarea[name='bio']"
        EDIT_AVATAR_INPUT = "input[type='file'][name='avatar']"
        SAVE_PROFILE_BUTTON = ".save-profile-btn"
        CANCEL_EDIT_BUTTON = ".cancel-edit-btn"
    
    # ==================== FRIENDS PAGE ====================
    class Friends:
        # Tabs
        FRIENDS_TAB = "#friendsTab"
        REQUESTS_TAB = "#requestsTab"
        SUGGESTIONS_TAB = "#suggestionsTab"
        
        # Friends List
        FRIENDS_LIST = "#friendsList, .friends-list"
        FRIEND_ITEM = ".friend-item"
        FRIEND_AVATAR = ".friend-avatar"
        FRIEND_NAME = ".friend-name"
        FRIEND_USERNAME = ".friend-username"
        REMOVE_FRIEND_BUTTON = ".remove-friend-btn"
        VIEW_PROFILE_BUTTON = ".view-profile-btn"
        
        # Friend Requests
        REQUESTS_LIST = "#requestsList, .requests-list"
        REQUEST_ITEM = ".request-item"
        ACCEPT_BUTTON = ".accept-btn"
        REJECT_BUTTON = ".reject-btn"
        
        # Suggestions
        SUGGESTIONS_LIST = "#suggestionsList, .suggestions-list"
        SUGGESTION_ITEM = ".suggestion-item"
        ADD_FRIEND_BUTTON = ".add-friend-btn"
        
        # Empty States
        NO_FRIENDS_MESSAGE = ".no-friends-message"
        NO_REQUESTS_MESSAGE = ".no-requests-message"
        NO_SUGGESTIONS_MESSAGE = ".no-suggestions-message"
    
    # ==================== EXPLORE PAGE ====================
    class Explore:
        SEARCH_INPUT = "#searchInput, input[name='search']"
        SEARCH_BUTTON = ".search-btn"
        SEARCH_RESULTS = "#searchResults, .search-results"
        USER_RESULT_ITEM = ".user-result-item"
        USER_RESULT_AVATAR = ".user-result-avatar"
        USER_RESULT_NAME = ".user-result-name"
        USER_RESULT_USERNAME = ".user-result-username"
        VIEW_PROFILE_BUTTON = ".view-profile-btn"
        ADD_FRIEND_BUTTON = ".add-friend-btn"
        
        # Discover Section
        DISCOVER_SECTION = "#discoverSection"
        DISCOVER_USER_CARD = ".discover-user-card"
        NO_RESULTS_MESSAGE = ".no-results-message"
    
    # ==================== NOTIFICATIONS PAGE ====================
    class Notifications:
        NOTIFICATIONS_LIST = "#notificationsList, .notifications-list"
        NOTIFICATION_ITEM = ".notification-item"
        NOTIFICATION_UNREAD = ".notification-item.unread"
        NOTIFICATION_AVATAR = ".notification-avatar"
        NOTIFICATION_TEXT = ".notification-text"
        NOTIFICATION_TIME = ".notification-time"
        MARK_READ_BUTTON = ".mark-read-btn"
        CLEAR_ALL_BUTTON = "#clearAllBtn"
        NO_NOTIFICATIONS_MESSAGE = ".no-notifications-message"
    
    # ==================== COMMON ELEMENTS ====================
    class Common:
        LOADING_SPINNER = ".spinner, .loading"
        TOAST_MESSAGE = ".toast, .alert"
        MODAL_BACKDROP = ".modal-backdrop"
        CLOSE_MODAL_BUTTON = ".close, .modal-close"
        CONFIRM_BUTTON = ".confirm-btn"
        CANCEL_BUTTON = ".cancel-btn"
        ERROR_MESSAGE = ".error-message, .alert-danger"
        SUCCESS_MESSAGE = ".success-message, .alert-success"
        WARNING_MESSAGE = ".warning-message, .alert-warning"
        INFO_MESSAGE = ".info-message, .alert-info"
