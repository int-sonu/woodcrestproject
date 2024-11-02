import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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


def add_subcategory(browser, subcategory_name, category_name):
    """Function to add a subcategory"""
    try:
        # Navigate to the add subcategory page
        browser.get('http://127.0.0.1:8000/add-subcategory/')

        # Fill in the subcategory name
        subcategory_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'sub_name'))
        )
        subcategory_field.clear()
        subcategory_field.send_keys(subcategory_name)

        # Select the category from dropdown
        category_dropdown = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'category'))
        )
        for option in category_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == category_name:
                option.click()
                break

        # Submit the form
        submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for redirection to the subcategories list page
        WebDriverWait(browser, 10).until(
            EC.url_to_be('http://127.0.0.1:8000/view-subcategories/')
        )

        # Check if we are redirected to the subcategory listing page
        print("Subcategory added successfully, now on the subcategories list page.")
        return True

    except TimeoutException:
        print("Failed to add subcategory or timeout occurred.")
        # Capture a screenshot if an error occurs
        browser.save_screenshot('subcategory_add_failed.png')
        return False


def test_add_existing_subcategory(browser):
    """Test adding an already existing subcategory"""
    subcategory_name = "WOODEN SOFA"
    category_name = "LIVING ROOM"

    # Try adding an existing subcategory
    print("Attempting to add an existing subcategory...")

    if not add_subcategory(browser, subcategory_name, category_name):
        # Check for error message
        try:
            error_message = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))
            )
            print("Error message displayed: ", error_message.text)
        except TimeoutException:
            print("No error message found, but subcategory add failed.")
        pytest.fail("Failed to add subcategory or subcategory already exists.")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--capture=no", "--maxfail=1"])
