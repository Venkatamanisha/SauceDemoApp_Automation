from playwright.sync_api import Page
import pytest
from pages.Login_Page import LoginPage
from pages.Inventory_Page import InventoryPage
from data.users import USERS
from data import constraints


@pytest.fixture
def inventory_page(page: Page):
    login_page = LoginPage(page)
    
    login_page.open()
    login_page.login(
        username=USERS["standard_user"]["username"],
        password=USERS["standard_user"]["password"],
    )
    return InventoryPage(page)
    


def test_cart_badge_update_add_products(inventory_page: InventoryPage) -> None:


    # Log in first (even the tutorial instructor forgot this line in the screenshot!)
   

    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bike Light_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bolt T-Shirt_Text"])

    cart_badge_count = inventory_page.getCartBadgeCount()
    assert cart_badge_count == 3, f"Expected cart badge count to be 3, but got {cart_badge_count}"

def test_products_sorted_low_to_high(inventory_page: InventoryPage) -> None:
    inventory_page.sortBy(constraints.SORT_OPTIONS["Price (low to high)"])
    prices = inventory_page.getAllProductPrices()
    sorted_prices = sorted(prices)
    assert prices == sorted_prices, f"Expected prices to be sorted low to high, but got {prices}"

def test_products_sorted_high_to_low(inventory_page: InventoryPage) -> None:
    inventory_page.sortBy(constraints.SORT_OPTIONS["Price (high to low)"])
    prices = inventory_page.getAllProductPrices()
    assert prices == sorted(prices, reverse=True), f"Expected prices high to low, got {prices}"


def test_products_sorted_a_to_z(inventory_page: InventoryPage) -> None:
    inventory_page.sortBy(constraints.SORT_OPTIONS["Name (A to Z)"])
    names = inventory_page.getAllProductNames()
    assert names == sorted(names), f"Expected names A to Z, got {names}"


def test_products_sorted_z_to_a(inventory_page: InventoryPage) -> None:
    inventory_page.sortBy(constraints.SORT_OPTIONS["Name (Z to A)"])
    names = inventory_page.getAllProductNames()
    assert names == sorted(names, reverse=True), f"Expected names Z to A, got {names}"