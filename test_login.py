from models import User


def test_login(app):                     # TODO: post-condition - logout
    user = User(username='admin', password='pass', real_name="Admin")
    app.login_as(user)
    assert app.user_menu_present()
    assert app.user_menu_present().text == user.real_name
