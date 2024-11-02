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
    """Function to simulate typing slowly for each character."""
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

def login(browser, email, password):
    """Function to log in as an admin and check if login is successful."""
    try:
        # Find email and password fields
        email_field = WebDriverWait(browser, 10).until(
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

        # Verify redirection to the admin dashboard
        WebDriverWait(browser, 20).until(
            EC.url_to_be('http://127.0.0.1:8000/admin_dashboard/')  # Adjust based on your dashboard structure
        )
        print("Admin login successful.")
        return True
    except TimeoutException:
        print("Admin login failed or timeout occurred.")
        browser.save_screenshot('admin_login_failed.png')
        return False
    except Exception as e:
        print(f"An error occurred during admin login: {e}")
        browser.save_screenshot('admin_error_screenshot.png')
        return False

def go_to_admin_dashboard(browser):
    """Function to navigate to the admin dashboard and verify elements."""
    try:
        # Wait for the dashboard page to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text()="Admin Dashboard"]'))  # Adjust based on your dashboard structure
        )
        print("Navigated to the Admin Dashboard successfully.")
    except TimeoutException:
        print("Failed to navigate to Admin Dashboard.")
        browser.save_screenshot('dashboard_navigation_failed.png')

def test_admin_login(browser):
    """Test the admin login and navigate to the admin dashboard."""
    # Navigate to the login page
    browser.get('http://127.0.0.1:8000/login/')

    # Test valid admin credentials
    print("Testing valid admin credentials...")
    if login(browser, 'admin751@gmail.com', 'admin@2025#'):  # Replace with actual admin credentials
        go_to_admin_dashboard(browser)  # Check for elements on the dashboard after login
    else:
        pytest.fail("Admin login failed")

# Main entry point
if __name__ == "__main__":
    # Run pytest specifically for this file only
    pytest.main([__file__, "-v", "--capture=no", "--maxfail=1"])
