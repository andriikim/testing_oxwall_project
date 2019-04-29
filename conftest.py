import pytest
from selenium import webdriver

@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture()
def session(driver):
    driver.get("http://127.0.0.1/oxwall/")
    button = driver.find_elements_by_class_name("ow_console_item")
    button[0].click()
    username = driver.find_element_by_name("identity")
    username.send_keys('admin')
    passwd = driver.find_element_by_name('password')
    passwd.send_keys('pass')
    button = driver.find_element_by_name('submit')
    button.click()
    yield
    buttons = driver.find_elements_by_css_selector('.ow_console_item.ow_console_dropdown.ow_console_dropdown_hover')
    action = webdriver.ActionChains(driver)
    action.move_to_element(buttons[0]).perform()
    action.move_to_element(driver.find_element_by_link_text('Sign Out')).click().perform()
