from playwright.sync_api import Page, expect
import pytest
from data.users import USERS
from data import constraints
from pages.Login_Page import LoginPage
from utils.config import BASE_URL



@pytest.fixture(autouse=True)
def login_page(page: Page) :
    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page,login_page: LoginPage) -> None:
    login_page.login(username=USERS["standard_user"]["username"], password=USERS["standard_user"]["password"])
    
    expect(page).to_have_url(f"{BASE_URL.rstrip('/')}{constraints.URLS['inventory']}")
    expect(page.locator(".title")).to_have_text(constraints.TEXT["product_title"])


    

