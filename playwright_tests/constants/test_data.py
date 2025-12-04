"""
Test data for UI automation tests.
Contains user credentials, sample content, and test scenarios.
"""

from faker import Faker
import random
import string

fake = Faker()


class TestData:
    """Test data for various test scenarios."""
    
    # ==================== USER CREDENTIALS ====================
    class Users:
        """Predefined test users."""
        
        # Primary test user
        PRIMARY_USER = {
            'name': 'Playwright Test',
            'username': 'playwrighttest',
            'email': 'playwrighttest@example.com',
            'password': 'Test@123456',
            'bio': 'This is a test user account for automation testing.'
        }
        
        # Secondary test user
        SECONDARY_USER = {
            'name': 'Test User Two',
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'Test@123456',
            'bio': 'Another test user for friend interactions.'
        }
        
        # Third test user
        THIRD_USER = {
            'name': 'Test User Three',
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': 'Test@123456',
            'bio': 'Third test user for complex scenarios.'
        }
        
        # Admin user (if applicable)
        ADMIN_USER = {
            'name': 'Admin User',
            'username': 'adminuser',
            'email': 'admin@example.com',
            'password': 'Admin@123456',
            'bio': 'Administrator account.'
        }
    
    # ==================== INVALID DATA ====================
    class InvalidData:
        """Invalid data for negative testing."""
        
        # Invalid names (based on signup.js validation: /^[A-Za-z\s]{2,30}$/)
        INVALID_NAMES = [
            '',           # Empty
            'A',          # Too short (less than 2 chars)
            'Test123',    # Contains numbers
            'Test@Name',  # Contains special characters
            'A' * 31,     # Too long (more than 30 chars)
        ]
        
        # Invalid usernames (based on signup.js: /^[A-Za-z0-9]{2,}$/)
        INVALID_USERNAMES = [
            '',           # Empty
            'a',          # Too short (less than 2 chars)
            'user name',  # Contains space
            'user@name',  # Special characters
            'user-name',  # Hyphen not allowed
        ]
        
        # Invalid emails
        INVALID_EMAILS = [
            '',                   # Empty
            'notanemail',         # No @
            '@example.com',       # No local part
            'user@',              # No domain
            'user @example.com',  # Space
        ]
        
        # Invalid passwords (min 6 characters)
        INVALID_PASSWORDS = [
            '',       # Empty
            '12345',  # Too short (5 chars)
            'abc',    # Too short
        ]
    
    # ==================== POST CONTENT ====================
    class Posts:
        """Sample post content."""
        
        # Text posts
        TEXT_POSTS = [
            "Hello world! This is my first post 🎉",
            "Testing the social media application with Playwright automation.",
            "What a beautiful day! ☀️",
            "Just finished an amazing project! #coding #developer",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5,
        ]
        
        # Short posts
        SHORT_POST = "Hi!"
        
        # Long post
        LONG_POST = "This is a very long post. " * 50
        
        # Post with special characters
        SPECIAL_CHARS_POST = "Testing special chars: @#$%^&*()_+-=[]{}|;':\",./<>?"
        
        # Post with emojis
        EMOJI_POST = "🎉 🎊 🎈 🎁 🎀 🎂 🎃 🎄 🎅 🎆 🎇 ✨"
        
        # Post with hashtags
        HASHTAG_POST = "#testing #automation #playwright #python #socialmedia"
        
        # Post with mentions (if applicable)
        MENTION_POST = "@testuser2 Check out this amazing feature!"
    
    # ==================== COMMENTS ====================
    class Comments:
        """Sample comment content."""
        
        COMMENTS = [
            "Great post!",
            "I totally agree with this! 👍",
            "Thanks for sharing!",
            "This is amazing! 🔥",
            "Very informative, keep it up!",
            "Nice! 😊",
            "Interesting perspective!",
            "Love this! ❤️",
        ]
        
        SHORT_COMMENT = "👍"
        LONG_COMMENT = "This is a very detailed comment. " * 20
    
    # ==================== PROFILE DATA ====================
    class ProfileData:
        """Profile update data."""
        
        UPDATED_BIO = "Updated bio for testing purposes. This is a new bio! 🚀"
        UPDATED_NAME = "Updated Test User"
        
        BIOS = [
            "Software Developer | Tech Enthusiast | Coffee Lover ☕",
            "Building amazing things with code 💻",
            "Life is short, make it sweet 🍰",
            "Traveler | Photographer | Dreamer 📸",
            "Just another human trying to make a difference 🌍",
        ]
    
    # ==================== SEARCH QUERIES ====================
    class SearchQueries:
        """Search test data."""
        
        VALID_QUERIES = [
            "test",
            "user",
            "testuser",
            "Test User",
        ]
        
        NO_RESULTS_QUERY = "xyzabc123nonexistent"
        EMPTY_QUERY = ""
        SPECIAL_CHARS_QUERY = "@#$%"
    
    # ==================== HELPER METHODS ====================
    @staticmethod
    def generate_random_user():
        """Generate a random user for testing."""
        username = fake.user_name() + str(random.randint(1000, 9999))
        return {
            'name': fake.name(),
            'username': username,
            'email': f"{username}@example.com",
            'password': 'Test@' + ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            'bio': fake.text(max_nb_chars=100)
        }
    
    @staticmethod
    def generate_random_post():
        """Generate random post content."""
        post_types = [
            fake.sentence(nb_words=10),
            fake.text(max_nb_chars=200),
            f"{fake.sentence()} {fake.emoji()}",
            f"#{fake.word()} #{fake.word()} {fake.sentence()}",
        ]
        return random.choice(post_types)
    
    @staticmethod
    def generate_random_comment():
        """Generate random comment."""
        return fake.sentence(nb_words=random.randint(3, 15))
    
    @staticmethod
    def generate_random_bio():
        """Generate random bio."""
        return fake.text(max_nb_chars=150)
