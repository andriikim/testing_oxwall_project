from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from custom_expected_condition import presence_of_num_elements


# class OxwallApp:
#     def __init__(self, driver, base_url="http://127.0.0.1/oxwall/"):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 10)
#         # Open Oxwall site
#         self.driver.get(base_url)

class BasePage:
    """ Common functional that we need for page actions """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.action = webdriver.ActionChains(driver)

    def is_element_present(self, how, what):
        """ If present, return this element"""
        # els = self.driver.find_elements(by=how, value=what)
        # if len(els) == 0:
        #     return False
        # else:
        #     return els
        try:
            el = self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return el


class SignInPage(BasePage):
    """ Locators and actions on Sign In window (Page)"""
    SIGN_IN = (By.NAME, 'submit')
    USERNAME_INPUT = (By.NAME, 'identity')
    PASSWORD_INPUT = (By.NAME, 'password')

    @property
    def username_field(self):
        return self.driver.find_element(*self.USERNAME_INPUT)

    @property
    def passwd_field(self):
        return self.driver.find_element(*self.PASSWORD_INPUT)

    @property
    def signin_button(self):
        return self.driver.find_element(*self.SIGN_IN)

    def input_username(self, user):
        # Input username
        self.username_field.clear()
        self.username_field.send_keys(user.username)

    def input_password(self, user):
        # Input password
        self.passwd_field.clear()
        self.passwd_field.send_keys(user.password)

    def sign_in_click(self):
        self.signin_button.click()
        return DashboardPage(self.driver)


class InternalPages(BasePage):
    """ Locators and actions that common for all Internal Pages - menu actions"""
    RIGHT_MENU_ELEMENTS = (By.CLASS_NAME, "ow_console_item")
    #TODO: extract locators for other elements in logout method

    @property
    def right_menu_items(self):
        return self.driver.find_elements(*self.RIGHT_MENU_ELEMENTS)

    def sign_in_click(self):
        # Initialize login(click Sign in button)
        self.right_menu_items[0].click()
        return SignInPage(self.driver)

    def login_as(self, user):
        sign_in_page = self.sign_in_click()
        sign_in_page.input_username(user)
        sign_in_page.input_password(user)
        dashboard_page = sign_in_page.sign_in_click()
        return dashboard_page

    def logout(self):
        # Logout
        driver = self.driver
        buttons = driver.find_elements_by_css_selector('.ow_console_item.ow_console_dropdown.ow_console_dropdown_hover')
        self.action.move_to_element(buttons[0]).perform()
        self.action.move_to_element(driver.find_element_by_link_text('Sign Out')).click().perform()
        return MainPage(self.driver)


class MainPage(InternalPages):
    """ Locators and actions that we made in Main Page"""
    # TODO: structure and action on Main Page


class DashboardPage(InternalPages):
    """ Locators and actions that we made in Dashboard Page"""
    STATUS_INPUT_FIELD = (By.NAME, 'status')
    SEND_BUTTON =(By.NAME, "save")
    STATUS_BLOCK = (By.XPATH, "//li[contains(@id, 'action-feed')]")
    # TODO: extract locators for other elements

    @property
    def status_input_field(self):
        return self.wait.until(EC.presence_of_element_located(self.STATUS_INPUT_FIELD))

    @property
    def send_button(self):
        return self.driver.find_element(*self.SEND_BUTTON)

    def create_new_text_status(self, input_text):
        driver = self.driver
        # Enter new status text
        self.status_input_field.send_keys(input_text)
        # Submit new status
        self.send_button.click()

    def wait_new_status_appear(self, old_list_of_elements):
        # Wait until new status appears
        new_num = len(old_list_of_elements) + 1
        status_text_elements = self.wait.until(presence_of_num_elements(self.STATUS_BLOCK, new_num))
        return status_text_elements[0]

    @property
    def status_text_elements(self):
        return self.driver.find_elements_by_class_name('ow_newsfeed_content')

    @property
    def user_of_new_status_elements(self):
        return self.driver.find_elements_by_class_name('ow_newsfeed_string')

    def user_menu_present(self):
        return self.is_element_present(By.CSS_SELECTOR, '.ow_console_item.ow_console_dropdown:nth-child(5) > a')
