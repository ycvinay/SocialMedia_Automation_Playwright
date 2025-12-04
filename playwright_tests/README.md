# 🎭 Playwright UI Automation Test Suite

Comprehensive UI automation testing framework for the Social Media Application using Playwright and Python.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Reports](#test-reports)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)

## 🎯 Overview

This test automation framework provides end-to-end testing for the Social Media Application, covering:
- User authentication (login, signup, logout)
- Post management (create, edit, delete, like, comment)
- Friend system (requests, accept/reject, remove)
- Profile management
- Navigation and UI interactions

## ✨ Features

✅ **Page Object Model (POM)** - Maintainable and reusable test structure  
✅ **Constants Management** - Centralized selectors, URLs, and test data  
✅ **Cross-browser Testing** - Chrome, Firefox, Safari (WebKit)  
✅ **Parallel Execution** - Faster test runs  
✅ **Screenshot on Failure** - Automatic debugging aids  
✅ **Video Recording** - Full test execution recording  
✅ **HTML Reports** - Detailed test reports  
✅ **Allure Integration** - Beautiful test reporting (optional)  
✅ **Pytest Fixtures** - Reusable test setup  
✅ **Environment Configuration** - Flexible test settings  

## 📁 Project Structure

```
playwright_tests/
├── constants/              # Constants and configuration
│   ├── __init__.py
│   ├── selectors.py       # UI element selectors
│   ├── test_data.py       # Test data and credentials
│   ├── urls.py            # Application URLs
│   ├── messages.py        # Expected messages
│   └── config.py          # Test configuration
├── pages/                 # Page Object Model
│   ├── __init__.py
│   ├── base_page.py       # Base page class
│   ├── login_page.py      # Login page
│   ├── signup_page.py     # Signup page
│   ├── home_page.py       # Home/Feed page
│   ├── profile_page.py    # Profile page
│   ├── friends_page.py    # Friends page
│   ├── explore_page.py    # Explore page
│   └── notifications_page.py  # Notifications page
├── tests/                 # Test cases
│   ├── __init__.py
│   ├── test_auth.py       # Authentication tests
│   ├── test_posts.py      # Post tests
│   ├── test_friends.py    # Friend tests
│   ├── test_profile.py    # Profile tests
│   └── test_navigation.py # Navigation tests
├── fixtures/              # Test fixtures
│   ├── __init__.py
│   └── auth_fixtures.py   # Authentication fixtures
├── utils/                 # Helper utilities
│   ├── __init__.py
│   ├── helpers.py         # Helper functions
│   └── screenshot.py      # Screenshot utilities
├── reports/               # Test reports (gitignored)
├── screenshots/           # Screenshots (gitignored)
├── videos/                # Videos (gitignored)
├── conftest.py            # Pytest configuration
├── pytest.ini             # Pytest settings
├── requirements.txt       # Python dependencies
├── .env.test              # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js (for running the application)

### Step 1: Clone and Navigate

```bash
cd f:\pythonSocil\playwright_tests
```

### Step 2: Create Virtual Environment

```bash
python -m venv playwright_venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
playwright_venv\Scripts\activate
```

**macOS/Linux:**
```bash
source playwright_venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install Playwright Browsers

```bash
playwright install
```

### Step 6: Configure Environment

```bash
copy .env.test .env
# Edit .env with your settings
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Application URLs
BASE_URL=http://localhost:5500
API_BASE_URL=http://localhost:5000/api

# Browser Settings
BROWSER_TYPE=chromium
HEADLESS=False
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Timeouts (milliseconds)
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=30000

# Screenshots
SCREENSHOT_ON_FAILURE=True
SCREENSHOT_DIR=screenshots

# Video Recording
VIDEO_ENABLED=False
VIDEO_DIR=videos
```

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Run Specific Test

```bash
pytest tests/test_auth.py::test_login_with_valid_credentials
```

### Run Tests by Marker

```bash
# Run smoke tests
pytest -m smoke

# Run authentication tests
pytest -m auth

# Run post tests
pytest -m posts
```

### Run Tests in Parallel

```bash
pytest -n 4  # 4 workers
```

### Run Tests in Different Browser

```bash
pytest --browser firefox
pytest --browser webkit
```

### Run Tests in Headless Mode

```bash
pytest --headless
```

### Run with Video Recording

```bash
# Set VIDEO_ENABLED=True in .env, then:
pytest
```

## 📝 Writing Tests

### Example Test

```python
import pytest
from pages.login_page import LoginPage
from constants.test_data import TestData
from constants.messages import Messages

@pytest.mark.auth
@pytest.mark.smoke
def test_login_with_valid_credentials(page):
    """Test successful login with valid credentials."""
    # Arrange
    login_page = LoginPage(page)
    user = TestData.Users.PRIMARY_USER
    
    # Act
    login_page.navigate()
    login_page.login(user['username'], user['password'])
    
    # Assert
    assert login_page.is_login_successful()
    assert page.url == URLs.Pages.home()
```

### Using Page Objects

```python
from pages.home_page import HomePage
from constants.test_data import TestData

def test_create_post(page, authenticated_user):
    """Test creating a new post."""
    home_page = HomePage(page)
    post_content = TestData.Posts.TEXT_POSTS[0]
    
    home_page.create_post(post_content)
    
    assert home_page.is_post_visible(post_content)
```

## 📊 Test Reports

### HTML Report

After running tests, view the HTML report:

```bash
# Report is generated at: reports/report.html
start reports/report.html  # Windows
open reports/report.html   # macOS
```

### Allure Report (Optional)

```bash
# Generate Allure report
allure serve allure-results
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      - name: Run tests
        run: pytest --headless
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: screenshots/
```

## 📌 Best Practices

### 1. Use Page Objects
- Keep selectors in constants
- Implement page methods for interactions
- Return page objects for method chaining

### 2. Test Data Management
- Use constants for test data
- Generate random data with Faker
- Keep sensitive data in environment variables

### 3. Assertions
- Use descriptive assertion messages
- Verify both positive and negative scenarios
- Check UI state and API responses

### 4. Test Organization
- Use markers for test categorization
- Group related tests in classes
- Follow naming conventions

### 5. Debugging
- Use `--headed` mode for debugging
- Enable slow motion with `--slow`
- Check screenshots on failure
- Review test logs

## 🛠️ Troubleshooting

### Tests Failing to Start
- Ensure virtual environment is activated
- Check if Playwright browsers are installed: `playwright install`
- Verify application is running on correct URL

### Element Not Found Errors
- Check selectors in `constants/selectors.py`
- Increase timeout in `.env`
- Verify page is fully loaded

### Screenshot/Video Issues
- Check directory permissions
- Ensure directories exist
- Verify disk space

## 📚 Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model](https://playwright.dev/python/docs/pom)

## 🤝 Contributing

1. Write tests following the existing structure
2. Use meaningful test names
3. Add appropriate markers
4. Update documentation
5. Ensure all tests pass

## 📄 License

ISC

---

**Happy Testing! 🎭**
