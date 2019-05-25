import json
import os
import pytest
from selenium import webdriver

from db_connector import OxwallDB
from pages.pages import OxwallApp
from models import User

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture()
def driver(selenium):
    driver = selenium
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def app(driver):
    base_url = "http://127.0.0.1/oxwall/"
    driver.get(base_url)
    return OxwallApp(driver)

@pytest.fixture(scope="session")
def db():
    db = OxwallDB()
    yield db
    db.close()

with open(os.path.join(PROJECT_DIR, "data", "user_data.json"), encoding="utf8") as f:
    user_data_list = json.load(f)

@pytest.fixture(params=user_data_list, ids=[str(user) for user in user_data_list])
def user(request, db):
    user = User(**request.param)
    db.create_user(user)
    yield user
    db.delete_user(user)

@pytest.fixture()
def logged_user(driver, app):
    user = User(username='admin', password='pass', real_name="Admin")
    app.main_page.login_as(user)
    yield user
    app.main_page.logout()
