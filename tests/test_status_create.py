import json
import os
import pytest

from conftest import PROJECT_DIR
from data.random_string import random_string
from pages.pages import DashboardPage

# TODO explain
with open(os.path.join(PROJECT_DIR, "data", "status_data.json"), encoding="utf8") as f:
    status_text_list = json.load(f)

status_text_list.append(random_string())
# status_text_list.extend([random_string() for _ in range(5)])

@pytest.mark.parametrize("input_text", status_text_list)
def test_create_status(driver, logged_user, input_text):
    dashboard_page = DashboardPage(driver)
    # Find statuses on page before new status creation
    old_status_list = dashboard_page.statuses
    assert dashboard_page.status_input_field.placeholder == "What’s happening?"
    dashboard_page.create_new_text_status(input_text)
    # Wait until new status appears
    dashboard_page.wait_new_status_appear(old_status_list)
    # Verify text of new status
    new_status = dashboard_page.statuses[0]
    assert new_status.text == input_text
    assert new_status.user == logged_user
    assert new_status.time == "within 1 minute"
