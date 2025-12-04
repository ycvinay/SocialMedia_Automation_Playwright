"""Simple test to verify fixture setup."""
import pytest

def test_simple_page_load(page, base_url):
    """Just load the login page and verify it works."""
    print(f"Base URL: {base_url}")
    page.goto(f"{base_url}/views/login.html")
    print(f"Page URL: {page.url}")
    assert "login" in page.url.lower()
    print("Test passed!")
