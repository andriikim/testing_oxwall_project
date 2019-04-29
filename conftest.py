import pytest
from selenium import webdriver
from app_helper import OxwallApp
from models import User


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture()
def app(driver):
    return OxwallApp(driver, base_url="http://127.0.0.1/oxwall/")


@pytest.fixture()
def logged_user(app):
    user = User(username='admin', password='pass', real_name="Admin")
    app.login_as(user)
    yield user
    app.logout()
