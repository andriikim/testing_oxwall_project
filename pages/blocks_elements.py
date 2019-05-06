from selenium.webdriver.common.by import By

from models import User


class InputTextElement:
    def __init__(self, webelement):
        self.element = webelement

    def input(self, text):
        """Sets the text to the value supplied"""
        self.element.clear()
        self.element.send_keys(text)

    @property
    def placeholder(self):
        """Gets the text of the specified object"""
        return self.element.get_attribute("placeholder")

    @property
    def text_value(self):
        """Gets the text of the specified object"""
        return self.element.get_attribute("value")


class StatusBlock:
    STATUS_TEXT = (By.CLASS_NAME, 'ow_newsfeed_content')
    STATUS_USER = (By.CSS_SELECTOR, ".ow_newsfeed_string > a")
    STATUS_TIME = (By.CSS_SELECTOR, "a.create_time.ow_newsfeed_date")

    def __init__(self, webelement):
        self.webelement = webelement

    @property
    def text(self):
        return self.webelement.find_element(*self.STATUS_TEXT).text

    @property
    def user(self):
        user_element = self.webelement.find_element(*self.STATUS_USER)
        return User(
            username=user_element.get_attribute("href").split("/")[-1],
            real_name=user_element.text
        )

    @property
    def time(self):
        return self.webelement.find_element(*self.STATUS_TIME).text
