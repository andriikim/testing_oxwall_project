import pytest
from selenium import webdriver
from pages import MainPage
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


@pytest.fixture()
def logged_user(driver):
    user = User(username='admin', password='pass', real_name="Admin")
    main_page = MainPage(driver)
    main_page.login_as(user)
    yield user
    main_page.logout()
