from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from custom_expected_condition import presence_of_num_elements


class OxwallApp:
    def __init__(self, driver, base_url="http://127.0.0.1/oxwall/"):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Open Oxwall site
        self.driver.get(base_url)

    def login_as(self, username, password):
        driver = self.driver
        # Initialize login(click Sign in button)
        button = driver.find_elements_by_class_name("ow_console_item")
        button[0].click()
        # Input username
        username_field = driver.find_element_by_name("identity")
        username_field.send_keys(username)
        # Input password
        passwd_field = driver.find_element_by_name('password')
        passwd_field.send_keys(password)
        # Sign in
        button = driver.find_element_by_name('submit')
        button.click()

    def logout(self):
        # Logout
        driver = self.driver
        buttons = driver.find_elements_by_css_selector('.ow_console_item.ow_console_dropdown.ow_console_dropdown_hover')
        action = webdriver.ActionChains(driver)
        action.move_to_element(buttons[0]).perform()
        action.move_to_element(driver.find_element_by_link_text('Sign Out')).click().perform()

    def create_new_text_status(self, input_text):
        driver = self.driver
        # Enter new status text
        status_input_field = self.wait.until(EC.presence_of_element_located((By.NAME, 'status')))
        status_input_field.send_keys(input_text)
        # Submit new status
        driver.find_element_by_name('save').click()

    def wait_new_status_appear(self, old_list_of_elements):
        # Wait until new status appears
        new_num = len(old_list_of_elements) + 1
        status_text_elements = self.wait.until(presence_of_num_elements((By.CLASS_NAME, 'ow_newsfeed_content'), new_num))
        return status_text_elements[0]

    def status_text_elements(self):
        return self.driver.find_elements_by_class_name('ow_newsfeed_content')
