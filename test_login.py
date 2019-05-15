from models import User
from pages.pages import MainPage, SignInPage, DashboardPage


def test_login(driver):                     # TODO: post-condition - logout
    user = User(username='admin', password='pass', real_name="Admin")
    main_page = MainPage(driver)
    main_page.sign_in_click()
    sign_in_page = SignInPage(driver)
    assert sign_in_page.is_this_page()
    assert sign_in_page.username_field.placeholder == "Username/Email"
    assert sign_in_page.passwd_field.placeholder == "Password"
    sign_in_page.input_username(user)
    sign_in_page.input_password(user)
    sign_in_page.submit_form()
    dashboard_page = DashboardPage(driver)
    assert dashboard_page.active_menu.text == "DASHBOARD"
    assert dashboard_page.user_menu_present()
    assert dashboard_page.user_menu_present().text == user.real_name
