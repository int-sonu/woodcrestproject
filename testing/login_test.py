import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
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


def login(browser: WebDriver, email, password):
    """Function to log in and check if login is successful"""
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

        # Verify successful login or error
        try:
            WebDriverWait(browser, 10).until(
                EC.url_contains('customer_index')  # Change according to the post-login URL
            )
            return True
        except TimeoutException:
            browser.save_screenshot('login_failed.png')
            return False
    except Exception as e:
        print(f"An error occurred during login: {e}")
        browser.save_screenshot('error_screenshot.png')
        return False


def test_email_password(browser: WebDriver):
    """Test different email and password scenarios"""
    # Navigate to login page
    browser.get('http://127.0.0.1:8000/login/')

    # Test valid credentials
    print("Testing valid credentials...")
    assert login(browser, 'sonusebastian528@gmail.com', 'sonu@3456'), "Valid login failed"

    # Test invalid credentials
    print("Testing invalid credentials...")
    assert not login(browser, 'invalid@example.com', 'wrongpassword'), "Invalid login succeeded"

    # Test empty fields
    print("Testing empty email and password...")
    assert not login(browser, '', ''), "Empty login succeeded"

    # Test valid email with incorrect password
    print("Testing valid email with incorrect password...")
    assert not login(browser, 'sonusebastian528@gmail.com', 'wrongpassword'), "Login succeeded with incorrect password"

    # Test invalid email format
    print("Testing invalid email format...")
    assert not login(browser, 'sonusebastian', 'sonu@3456'), "Login succeeded with invalid email format"


if __name__ == "__main__":
    # To run this script as a standalone script, use pytest
    pytest.main(["-v", "--capture=no", "--maxfail=1"])
