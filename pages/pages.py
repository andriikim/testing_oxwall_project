from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from custom_expected_condition import presence_of_num_elements
from pages.blocks_elements import InputTextElement, StatusBlock


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

    def is_element_present(self, locator):
        """ If present, return this element"""
        # els = self.driver.find_elements(by=how, value=what)
        # if len(els) == 0:
        #     return False
        # else:
        #     return els
        try:
            el = self.driver.find_element(*locator)
        except NoSuchElementException as e:
            return False
        return el

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator),
                               message=f"Can't find element by locator {locator}")

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator),
                               message=f"Can't find elements by locator {locator}")

    def find_visible_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator),
                               message=f"Can't find visible element by locator {locator}")

    def find_any_visible_elements(self, locator):
        return self.wait.until(EC.visibility_of_any_elements_located(locator),
                               message=f"Can't find any visible elements by locator {locator}")

    def find_all_visible_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator),
                               message=f"Can't find all visible elements by locator {locator}")


class SignInPage(BasePage):
    """ Locators and actions on Sign In window (Page)"""
    SIGN_IN = (By.NAME, 'submit')
    USERNAME_INPUT = (By.NAME, 'identity')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_WINDOW_BOX = (By.CLASS_NAME, "floatbox_container")
    LOGIN_BACKGROUND = (By.ID, "floatbox_overlay")

    @property
    def username_field(self):
        return InputTextElement(self.find_element(self.USERNAME_INPUT))

    @property
    def passwd_field(self):
        return InputTextElement(self.find_element(self.PASSWORD_INPUT))

    @property
    def signin_button(self):
        return self.find_element(self.SIGN_IN)

    def is_this_page(self):
        return self.is_element_present(self.LOGIN_WINDOW_BOX)

    def input_username(self, user):
        # Input username
        self.username_field.input(user.username)

    def input_password(self, user):
        # Input password
        self.passwd_field.input(user.password)

    def submit_form(self):
        self.signin_button.click()
        # TODO explain!
        # need to wait disappearing background before making some action on Dashboard page
        self.wait.until(EC.invisibility_of_element_located(self.LOGIN_BACKGROUND),
                        "Login background is still visible")

        return DashboardPage(self.driver)   # This can be deleted in this approach!


class InternalPages(BasePage):
    """ Locators and actions that common for all Internal Pages - menu actions"""
    RIGHT_MENU_ELEMENTS = (By.CLASS_NAME, "ow_console_item")
    ACTIVE_MENU = (By.XPATH, "//div[contains(@class, 'ow_menu_wrap')]//li[contains(@class, 'active')]")
    #TODO: extract locators for other elements in logout method

    @property
    def active_menu(self):
        return self.find_element(self.ACTIVE_MENU)

    @property
    def right_menu_items(self):
        return self.find_elements(self.RIGHT_MENU_ELEMENTS)

    def sign_in_click(self):
        # Initialize login(click Sign in button)
        self.right_menu_items[0].click()
        return SignInPage(self.driver)

    def login_as(self, user):
        sign_in_page = self.sign_in_click()
        sign_in_page.input_username(user)
        sign_in_page.input_password(user)
        dashboard_page = sign_in_page.submit_form()
        return dashboard_page  # This can be deleted in App (page aggregator) approach

    def logout(self):
        # TODO: extract elements
        # Logout
        driver = self.driver
        buttons = driver.find_elements_by_css_selector('.ow_console_item.ow_console_dropdown.ow_console_dropdown_hover')
        self.action.move_to_element(buttons[0]).perform()
        self.action.move_to_element(driver.find_element_by_link_text('Sign Out')).click().perform()
        return MainPage(self.driver)  # This can be deleted in App (page aggregator) approach


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
        return InputTextElement(self.find_visible_element(self.STATUS_INPUT_FIELD))

    @property
    def send_button(self):
        return self.find_visible_element(self.SEND_BUTTON)

    @property
    def statuses(self):
        return [StatusBlock(item) for item in self.find_elements(self.STATUS_BLOCK)]

    # @property
    # def status_text_elements(self):
    #     return self.find_all_visible_elements(self.STATUS_TEXT)
    #
    # @property
    # def user_of_new_status_elements(self):
    #     return self.find_all_visible_elements(self.STATUS_USER)

    def create_new_text_status(self, input_text):
        # Enter new status text
        self.status_input_field.input(input_text)
        # Submit new status
        self.send_button.click()

    def wait_new_status_appear(self, old_list_of_elements):
        # Wait until new status appears
        new_num = len(old_list_of_elements) + 1
        status_text_elements = self.wait.until(presence_of_num_elements(self.STATUS_BLOCK, new_num))
        return status_text_elements[0]

    def user_menu_present(self):
        # TODO: new style, extract element and locator
        return self.is_element_present((By.CSS_SELECTOR, '.ow_console_item.ow_console_dropdown:nth-child(5) > a'))
