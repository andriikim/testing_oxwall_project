import pytest
from selenium import webdriver
from app_helper import OxwallApp


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
def session(app):
    app.login_as(username='admin', password='pass')
    yield
    app.logout()
