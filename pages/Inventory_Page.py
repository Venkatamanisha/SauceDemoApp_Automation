
from playwright.sync_api import Page


class InventoryPage:
    def __init__(self,page:Page):
        self.inventoryItems = page.locator('[data-test="inventory-item"]')
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.sortDropdown = page.locator('[data-test="product-sort-container"]')

    def get_product_card(self, product_name: str):
        return self.inventoryItems.filter(has_text=product_name)
    def add_product_to_cart(self, product_name: str) -> None:
        product_card = self.get_product_card(product_name)
        add_to_cart_button = product_card.get_by_role("button", name="Add to cart")
        add_to_cart_button.click()
   
    def getCartBadgeCount(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def sortBy(self, option: str) -> list: 
        self.sortDropdown.select_option(option) #low-high

    def getAllProductPrices(self) -> list:
        prices = []
        for i in range(self.inventoryItems.count()):
            price_text = self.inventoryItems.nth(i).locator(".inventory_item_price").inner_text()
            price_value = float(price_text.replace("$", ""))
            prices.append(price_value)
        return prices
    
    def getAllProductNames(self) -> list[str]:
        names = []
        for i in range(self.inventoryItems.count()):
            name_text = self.inventoryItems.nth(i).locator(".inventory_item_name").inner_text()
            names.append(name_text)
        return names
