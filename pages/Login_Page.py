from playwright.sync_api import Page
from utils.config import BASE_URL
from data.users import USERS
class LoginPage:
    def __init__(self,page:Page):
        self.page = page
        self.base_url = BASE_URL

        # locators
        self.usernameInput = page.get_by_placeholder("Username")
        self.passwordInput = page.get_by_placeholder("Password")
        self.login_btn     = page.get_by_role('button', name='Login')

    def open(self)->None:
        self.page.goto(self.base_url)
        print("Login page opened successfully")  

    def login(self,username: str, password: str)->None:
        self.usernameInput.fill(username)
        self.passwordInput.fill(password)
        self.login_btn.click()
        
        print("Login successful")

      