import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Path to Brave Browser executable
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    chrome_options.binary_location = brave_path

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


def type_slowly(element, text, delay=0.1):
    """Function to simulate typing slowly for each character"""
    for character in text:
        element.send_keys(character)
        time.sleep(delay)


def login(browser, email, password):
    """Function to log in and check if login is successful"""
    try:
        # Find email and password fields
        email_field = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        password_field = browser.find_element(By.NAME, 'password')

        # Clear fields before typing
        email_field.clear()
        password_field.clear()

        # Enter email and password
        type_slowly(email_field, email)
        type_slowly(password_field, password)

        # Submit the form
        password_field.send_keys(Keys.RETURN)

        # Verify redirection to the seller dashboard
        WebDriverWait(browser, 20).until(
            EC.url_to_be('http://127.0.0.1:8000/seller/dashboard/')  # Exact URL for seller dashboard
        )
        print("Seller login successful.")
        return True
    except TimeoutException:
        print("Seller login failed or timeout occurred.")
        browser.save_screenshot('seller_login_failed.png')
        return False
    except Exception as e:
        print(f"An error occurred during seller login: {e}")
        browser.save_screenshot('seller_error_screenshot.png')
        return False


def go_to_seller_dashboard(browser):
    """Function to navigate to the seller dashboard and verify elements"""
    try:
        # Wait for the dashboard page to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text()="Seller Dashboard"]'))  # Adjust based on your dashboard structure
        )
        print("Navigated to the Seller Dashboard successfully.")
        # You can add further interactions with elements here if needed
    except TimeoutException:
        print("Failed to navigate to Seller Dashboard.")
        browser.save_screenshot('dashboard_navigation_failed.png')


def test_email_password(browser):
    """Test the seller login and navigate to the seller dashboard"""
    # Navigate to login page
    browser.get('http://127.0.0.1:8000/login/')

    # Test valid seller credentials
    print("Testing valid seller credentials...")
    if login(browser, 'rekha751@gmail.com', 'rekha@3456'):
        go_to_seller_dashboard(browser)  # Check for elements on the dashboard after login
    else:
        pytest.fail("Seller login failed")


if __name__ == "__main__":
    # Run this file only
    pytest.main([__file__, "-v", "--capture=no", "--maxfail=1"])
