from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from custom_expected_condition import presence_of_num_elements


def test_create_status(driver, session):
    input_text = 'Hello, world!!'
    # Find statuses on page before new status creation
    old_status_list = driver.find_elements_by_class_name('ow_newsfeed_content')
    # Create new status
    driver.find_element_by_name('status').send_keys(input_text)
    driver.find_element_by_name('save').click()
    # Wait until new status appears
    wait = WebDriverWait(driver, 10)
    new_num = len(old_status_list) + 1
    el = wait.until(presence_of_num_elements((By.CLASS_NAME, 'ow_newsfeed_content'), new_num))
    # Verify text of new status
    assert el[0].text == input_text
