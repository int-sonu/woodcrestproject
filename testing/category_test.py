import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Path to Brave Browser executable (use Chrome path if using Chrome)
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    chrome_options.binary_location = brave_path

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


def add_category(browser, category_name):
    """Function to add a category"""
    try:
        # Navigate to the add category page
        browser.get('http://127.0.0.1:8000/add-category/')

        # Fill in the category name
        category_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'name'))
        )
        category_field.clear()
        category_field.send_keys(category_name)

        # Submit the form
        submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for redirection to the category list page
        WebDriverWait(browser, 10).until(
            EC.url_to_be('http://127.0.0.1:8000/view-category/')
        )

        # Check if we are redirected to the category listing page
        print("Category added successfully, now on the category list page.")
        return True

    except TimeoutException:
        print("Failed to add category or timeout occurred.")
        # Capture a screenshot if an error occurs
        browser.save_screenshot('category_add_failed.png')
        return False


def test_add_existing_category(browser):
    """Test adding an already existing category"""
    category_name = "LIVING ROOM"

    # Try adding an existing category
    print("Attempting to add an existing category...")

    if not add_category(browser, category_name):
        # Check for error message if category already exists
        try:
            error_message = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))  # Assuming error message uses 'alert-danger'
            )
            print("Error message displayed: ", error_message.text)
        except TimeoutException:
            print("No error message found, but category add failed.")
        pytest.fail("Failed to add category or category already exists.")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--capture=no", "--maxfail=1"])
