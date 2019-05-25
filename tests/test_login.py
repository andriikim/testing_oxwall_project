import pytest


def test_login(app, user):                     # TODO: post-condition - logout
    app.main_page.sign_in_click()
    assert app.sign_in_page.is_this_page()
    app.sign_in_page.input_username(user)
    app.sign_in_page.input_password(user)
    app.sign_in_page.submit_form()
    # TODO: Check message
    assert app.dashboard_page.active_menu.text == "DASHBOARD"
    assert app.dashboard_page.user_menu_present()
    assert app.dashboard_page.user_menu_present().text == user.real_name


@pytest.mark.nondestructive
def test_check_login_placeholders(app):
    app.main_page.sign_in_click()
    assert app.sign_in_page.is_this_page()
    assert app.sign_in_page.username_field.placeholder == "Username/Email"
    assert app.sign_in_page.passwd_field.placeholder == "Password"
