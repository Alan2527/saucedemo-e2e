"""Page Object del carrito de compras."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import click_y_esperar


class CartPage:
    # --- Locators ---
    NOMBRES = (By.CSS_SELECTOR, ".inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")
    BOTON_SEGUIR_COMPRANDO = (By.ID, "continue-shopping")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def productos_en_carrito(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.NOMBRES))
            return [e.text for e in self.driver.find_elements(*self.NOMBRES)]
        except Exception:
            return []

    def continuar_al_checkout(self):
        click_y_esperar(self.wait, self.BOTON_CHECKOUT, EC.url_contains("checkout-step-one.html"))
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
