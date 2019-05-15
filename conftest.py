import pytest
from selenium import webdriver
from pages.pages import OxwallApp
from models import User


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def app(driver):
    base_url = "http://127.0.0.1/oxwall/"
    driver.get(base_url)
    return OxwallApp(driver)

@pytest.fixture()
def logged_user(driver, app):
    user = User(username='admin', password='pass', real_name="Admin")
    app.main_page.login_as(user)
    yield user
    app.main_page.logout()
