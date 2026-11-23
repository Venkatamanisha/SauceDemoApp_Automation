from playwright.sync_api import Page


class CartPage:
    def  __init__(self,page:Page):
        self.page = page
        self.cartLink = page.locator(".shopping_cart_badge")
        self.itemNames = page.locator(".inventory_item_name")
        self.cartItem = page.locator(".cart_item")
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.firstNameInput = page.get_by_placeholder("First Name")
        self.lastNameInput = page.get_by_placeholder("Last Name")
        self.postalCodeInput = page.get_by_placeholder("Zip/Postal Code")
        self.cancelbutton = page.locator('[data-test="cancel"]')
        self.continue_button = page.get_by_role("button", name="Continue")
        self.subtotal = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total_price = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.checkout_cancel_button = page.locator('[data-test="cancel"]')
        self.back_to_home = page.locator('[data-test="back-to-products"]')
        self.gen_pdf = page.locator('[data-test="generate-pdf-order"]')

    def goTocart(self):
        self.cartLink.click()
    def getAllCartNames(self):
        return self.itemNames.all_inner_texts()

    def getCartItem(self,productName: str):

        return self.cartItem.filter(has_text=productName)

    
    def remove_product_from_cart(self, product_name: str) -> None:
        item_row = self.page.locator(".cart_item", has_text=product_name)
        item_row.locator("button", has_text="Remove").click()

    def getCartItemCount(self) -> int:
        return self.itemNames.count()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    def checkout(self):
        checkout_button = self.page.get_by_role("button", name="Checkout")
        checkout_button.click()
    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.firstNameInput.fill(first_name)
        self.lastNameInput.fill(last_name)
        self.postalCodeInput.fill(postal_code)

    def cancel_button(self):
        self.cancelbutton.click()
    
    def continue_checkout(self):
        self.continue_button.click()

    def getSubTotal(self):
        text = self.subtotal.text_content()
        return float(text.replace("Item total: $",""))
    def getTax(self):
        text = self.tax.text_content()
        return float(text.replace("Tax: $",""))
    def getTotal(self):
        total = self.total_price.text_content()
        return float(total.replace("Total: $",""))
    def checkoutCancelButton(self):
            self.checkout_cancel_button.click()
    def clickFinishButton(self):
        self.finish_button.click()
    def BackToHome(self):
        self.back_to_home.click()
    def Gen_Pdf(self):
        self.gen_pdf.click()

