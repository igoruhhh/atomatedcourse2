from oxwall_site_model import OxwallSite
import pytest


@pytest.mark.regression
def test_login_using_page_object(driver, user, logout):
    app = OxwallSite(driver)
    app.main_page.sign_in_click()
    assert app.sign_in_page.is_this_page()
    assert app.sign_in_page.username_field.placeholder == "Username/Email"
    assert app.sign_in_page.password_field.placeholder == "Password"
    app.sign_in_page.username_field.input(user.username)
    app.sign_in_page.password_field.input(user.password)
    app.sign_in_page.submit_form()
    assert app.dash_page.is_this_page()
    assert app.dash_page.is_logged_in()
    assert app.dash_page.user_menu.text == user.real_name
