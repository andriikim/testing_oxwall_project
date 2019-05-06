from models import User
from pages.pages import MainPage


def test_login(driver):                     # TODO: post-condition - logout
    user = User(username='admin', password='pass', real_name="Admin")
    main_page = MainPage(driver)
    sing_in_page = main_page.sign_in_click()
    assert sing_in_page.username_field.placeholder == "Username/Email"
    assert sing_in_page.passwd_field.placeholder == "Password"
    sing_in_page.input_username(user)
    sing_in_page.input_password(user)
    dashboard_page = sing_in_page.sign_in_click()
    # dashboard_page = main_page.login_as(user)
    assert dashboard_page.user_menu_present()
    assert dashboard_page.user_menu_present().text == user.real_name
