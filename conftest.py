import json
import os.path
import pytest
from selenium import webdriver

from db.db_connector import DbConnector
from oxwall_site_model import OxwallSite
from value_models.user import User

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PROJECT_DIR, "config.json")) as f:
    config = json.load(f)


@pytest.fixture(scope="session")
def db():
    db = DbConnector(config["db"])
    yield db
    db.close()


@pytest.fixture()
def driver(selenium, base_url):
    # Open browser driver settings
    driver = selenium
    driver.implicitly_wait(5)
    # driver.maximize_window()git
    driver.get(base_url)
    yield driver
    # Close browser
    driver.quit()


with open(os.path.join(PROJECT_DIR, "data", "user_data.json")) as f:
    user_data = json.load(f)


@pytest.fixture(params=user_data, ids=[str(user) for user in user_data])
def user(request, db):
    u = User(**request.param)
    db.create_user(u)
    yield u
    db.delete_user(u)


@pytest.fixture()
def signed_in_user(driver, user):
    app = OxwallSite(driver)
    app.login_as(user)
    yield user
    app.logout_as(user)


@pytest.fixture()
def logout(driver):
    yield
    app = OxwallSite(driver)
    app.dash_page.sign_out()
