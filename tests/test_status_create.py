import json
import os
import pytest
import allure

from conftest import PROJECT_DIR
from data.random_string import random_string
from pages.pages import DashboardPage

# TODO explain
with open(os.path.join(PROJECT_DIR, "data", "status_data.json"), encoding="utf8") as f:
    status_text_list = json.load(f)

status_text_list.append(random_string())
# status_text_list.extend([random_string() for _ in range(5)])


@allure.feature("Status feature")
@allure.story("Create status")
@pytest.mark.parametrize("input_text", status_text_list)
def test_create_status(driver, logged_user, input_text, db):
    dashboard_page = DashboardPage(driver)
    with allure.step("Given initial amount of status in Oxwall database"):
        old_status_list = dashboard_page.statuses
    with allure.step(f'When I add a status with "{input_text}" in Dashboard page'):
        dashboard_page.create_new_text_status(input_text)
        # Wait until new status appears
        dashboard_page.wait_new_status_appear(old_status_list)
    with allure.step("Then a new status block appears before old list of status"):
        # Verify text of new status
        assert db.get_last_text_status() == input_text
        new_status = dashboard_page.statuses[0]
    with allure.step(f"Then this status block has this {input_text} and author as this user {logged_user} and time \"within 1 minute\""):
        assert new_status.text == input_text
        assert new_status.user == logged_user
        assert new_status.time == "within 1 minute"
