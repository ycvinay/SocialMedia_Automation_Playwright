# 🚀 Quick Start Guide

## Setup (5 minutes)

### 1. Create Virtual Environment
```bash
cd f:\pythonSocil\playwright_tests
python -m venv playwright_venv
```

### 2. Activate Virtual Environment
```bash
# Windows
playwright_venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install chromium
```

### 5. Configure Environment
```bash
# Copy .env.test to .env
copy .env.test .env

# Edit .env if needed (default settings should work)
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
```

### Run Smoke Tests Only
```bash
pytest -m smoke
```

### Run with Visible Browser (Headed Mode)
```bash
# Set HEADLESS=False in .env, or:
pytest --headed
```

### Run in Parallel
```bash
pytest -n 4
```

## Before Running Tests

### ⚠️ Important: Start Your Application

1. **Start Flask Backend**
```bash
cd f:\pythonSocil\flask_backend
python run.py
```

2. **Start Frontend** (using Live Server or similar)
```bash
# Make sure frontend is running on http://localhost:5500
# Or update BASE_URL in .env
```

3. **Create Test Users** (if not exists)
   - Create users matching credentials in `constants/test_data.py`
   - Or update test data with existing users

## Next Steps

1. ✅ Review and update selectors in `constants/selectors.py` to match your actual HTML
2. ✅ Update test data in `constants/test_data.py` with valid credentials
3. ✅ Run smoke tests: `pytest -m smoke`
4. ✅ Expand page objects in `pages/` folder
5. ✅ Add more tests in `tests/` folder

## Troubleshooting

**Tests fail immediately?**
- Check if application is running
- Verify URLs in `.env`
- Check selectors match your HTML

**Import errors?**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**Browser not found?**
- Run `playwright install`

## Documentation

See `README.md` for complete documentation.

---
**Happy Testing! 🎭**
