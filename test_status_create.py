from pages import DashboardPage


def test_create_status(driver, logged_user):
    input_text = 'Hello, world!!'
    dashboard_page = DashboardPage(driver)
    # Find statuses on page before new status creation
    old_status_list = dashboard_page.status_text_elements()
    # Create new status
    dashboard_page.create_new_text_status(input_text)
    # Wait until new status appears
    dashboard_page.wait_new_status_appear(old_status_list)
    # Verify text of new status
    new_status_element = dashboard_page.status_text_elements()[0]
    assert new_status_element.text == input_text
    assert dashboard_page.user_of_new_status_elements()[0].text == logged_user.real_name
