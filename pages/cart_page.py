"""Page object del carrito de compras."""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".cart_item")
    NOMBRES = (By.CSS_SELECTOR, ".inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")
    BOTON_SEGUIR_COMPRANDO = (By.ID, "continue-shopping")

    def productos_en_carrito(self):
        try:
            return [e.text for e in self.encontrar_todos(self.NOMBRES)]
        except Exception:
            return []

    @allure.step("Continuar al checkout")
    def continuar_al_checkout(self):
        from selenium.webdriver.support import expected_conditions as EC
        from pages.checkout_page import CheckoutPage
        self.click_y_esperar(self.BOTON_CHECKOUT, EC.url_contains("checkout-step-one.html"))
        return CheckoutPage(self.driver)
