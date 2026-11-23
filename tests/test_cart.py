import re

from playwright.sync_api import Page, expect
import pytest
from pages.Login_Page import LoginPage
from pages.Inventory_Page import InventoryPage
from pages.cart import CartPage
from data.users import USERS
from data import constraints


@pytest.fixture
def setup(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.open()
    login_page.login(
        username=USERS["standard_user"]["username"],
        password=USERS["standard_user"]["password"],
    )
    return inventory_page, cart_page


def test_added_products_appear_correctly_in_cart(setup) -> None:
   
    inventory_page,cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bike Light_Text"])

    cart_page.goTocart()
    expect(cart_page.page).to_have_url(re.compile(f".*{constraints.URLS['cart']}$"))
    itemNames = cart_page.getAllCartNames()
    assert constraints.TEXT["Sauce Labs Backpack_Text"] in itemNames, (
        f"Expected '{constraints.TEXT['Sauce Labs Backpack_Text']}' to be in cart, but got {itemNames}"
    )
    assert constraints.TEXT["Sauce Labs Bike Light_Text"] in itemNames, (
        f"Expected '{constraints.TEXT['Sauce Labs Bike Light_Text']}' to be in cart, but got {itemNames}"
    )

def test_remove_product_from_cart(setup) -> None:
    inventory_page,cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bike Light_Text"])
    
    cart_page.goTocart()
    cart_page.remove_product_from_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    cart_item_count = cart_page.getCartItemCount()

    assert cart_item_count == 1, f"Expected 1 item in cart, but got {cart_item_count}"
    remaining_item_names = cart_page.getAllCartNames()
    assert constraints.TEXT["Sauce Labs Bike Light_Text"] in remaining_item_names, f"Expected '{constraints.TEXT['Sauce Labs Bike Light_Text']}' to remain in cart, but it was not found."

def test_continue_shopping_and_add_more_items(setup) -> None:
    inventory_page, cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])

    cart_page.goTocart()
    expect(cart_page.continue_shopping_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_visible()

    # Return to inventory page and add a second product
    cart_page.continue_shopping()
    expect(cart_page.page).to_have_url(re.compile(f".*{re.escape(constraints.URLS['inventory'])}$"))
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bolt T-Shirt_Text"])

    # Go back to cart and confirm both items are present
    cart_page.goTocart()
    expect(cart_page.itemNames).to_have_text([
        constraints.TEXT["Sauce Labs Backpack_Text"],
        constraints.TEXT["Sauce Labs Bolt T-Shirt_Text"],
    ])

def test_cancel_button_navigates_to_checkout_page(setup) -> None:
    inventory_page,cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bike Light_Text"])
    cart_page.goTocart()
    cart_page.checkout()
    cart_page.cancel_button()
    expect(cart_page.page).to_have_url(re.compile(f".*{re.escape(constraints.URLS['cart'])}$"))
def test_checkout_button_navigates_to_cancel_page(setup) -> None:
    inventory_page,cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bike Light_Text"])
    cart_page.goTocart()
    cart_page.checkout()
    cart_page.fill_info(
        first_name=constraints.CHECKOUT_INFO["first_name"],
        last_name=constraints.CHECKOUT_INFO["last_name"],
        postal_code=constraints.CHECKOUT_INFO["postal_code"]
    )
    cart_page.continue_checkout()
    
    expect(cart_page.page).to_have_url(re.compile(f".*{constraints.URLS['checkout2url']}$"))
    subtotal = cart_page.getSubTotal()
    tax = cart_page.getTax()
    total = cart_page.getTotal()
    assert total == pytest.approx((subtotal+tax),abs=0.01)
    cart_page.checkoutCancelButton()
    expect(cart_page.page).to_have_url(re.compile(f".*{constraints.URLS['inventory']}$"))


def test_checkout_button_navigates_to_checkout_page(setup) -> None:
    inventory_page,cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Bike Light_Text"])
    cart_page.goTocart()
    cart_page.checkout()
    cart_page.fill_info(
        first_name=constraints.CHECKOUT_INFO["first_name"],
        last_name=constraints.CHECKOUT_INFO["last_name"],
        postal_code=constraints.CHECKOUT_INFO["postal_code"]
    )
    cart_page.continue_checkout()
    
    expect(cart_page.page).to_have_url(re.compile(f".*{constraints.URLS['checkout2url']}$"))
    subtotal = cart_page.getSubTotal()
    tax = cart_page.getTax()
    total = cart_page.getTotal()
    assert total == pytest.approx((subtotal+tax),abs=0.01)


    cart_page.clickFinishButton()
    expect(cart_page.page).to_have_url(re.compile(f".*{constraints.URLS['thankyoupage']}$"))
    expect(cart_page.complete_header).to_have_text('Thank you for your order!')
    cart_page.BackToHome()
    expect(cart_page.page).to_have_url(re.compile(f".*{constraints.URLS['inventory']}$"))
def test_generate_pdf_downloads_file(setup) -> None:
    inventory_page, cart_page = setup
    inventory_page.add_product_to_cart(constraints.TEXT["Sauce Labs Backpack_Text"])
    cart_page.goTocart()
    cart_page.checkout()
    cart_page.fill_info(
        first_name=constraints.CHECKOUT_INFO["first_name"],
        last_name=constraints.CHECKOUT_INFO["last_name"],
        postal_code=constraints.CHECKOUT_INFO["postal_code"],
    )
    cart_page.continue_checkout()
    cart_page.clickFinishButton()

    # Capture the PDF download triggered by Gen_Pdf()
    with cart_page.page.expect_download() as download_info:
        cart_page.Gen_Pdf()

    download = download_info.value
    assert download.suggested_filename.endswith(".pdf")
    download.save_as(f"downloads/{download.suggested_filename}")

