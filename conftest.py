import json
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

with open("data/user_data.json", encoding="utf8") as f:
    user_data_list = json.load(f)

@pytest.fixture(params=user_data_list, ids=[str(user) for user in user_data_list])
def user(request):
    return User(**request.param)

@pytest.fixture()
def logged_user(driver, app):
    user = User(username='admin', password='pass', real_name="Admin")
    app.main_page.login_as(user)
    yield user
    app.main_page.logout()
