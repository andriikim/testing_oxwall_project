from models import User
from pages import MainPage


def test_login(driver):                     # TODO: post-condition - logout
    user = User(username='admin', password='pass', real_name="Admin")
    main_page = MainPage(driver)
    dashboard_page = main_page.login_as(user)
    assert dashboard_page.user_menu_present()
    assert dashboard_page.user_menu_present().text == user.real_name
