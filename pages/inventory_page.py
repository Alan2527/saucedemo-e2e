"""Page Object del catálogo de productos (inventario)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_click, click_y_esperar, texto_de


class InventoryPage:
    # --- Locators ---
    TITULO = (By.CSS_SELECTOR, ".title")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    NOMBRES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRECIOS = (By.CSS_SELECTOR, ".inventory_item_price")
    IMAGENES = (By.CSS_SELECTOR, ".inventory_item_img img")
    SELECTOR_ORDEN = (By.CSS_SELECTOR, ".product_sort_container")
    BADGE_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge")
    LINK_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_link")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Datos ---
    def titulo(self):
        return texto_de(self.wait, self.TITULO)

    def cantidad_de_productos(self):
        self.wait.until(EC.presence_of_element_located(self.ITEMS))
        return len(self.driver.find_elements(*self.ITEMS))

    def nombres_de_productos(self):
        self.wait.until(EC.presence_of_element_located(self.NOMBRES))
        return [e.text for e in self.driver.find_elements(*self.NOMBRES)]

    def precios_de_productos(self):
        self.wait.until(EC.presence_of_element_located(self.PRECIOS))
        return [float(e.text.replace("$", "")) for e in self.driver.find_elements(*self.PRECIOS)]

    def urls_de_imagenes(self):
        self.wait.until(EC.presence_of_element_located(self.IMAGENES))
        return [e.get_attribute("src") for e in self.driver.find_elements(*self.IMAGENES)]

    def items_en_badge(self):
        elementos = self.driver.find_elements(*self.BADGE_CARRITO)
        if not elementos or not elementos[0].is_displayed():
            return 0
        return int(elementos[0].text)

    # --- Acciones ---
    def ordenar_por(self, criterio):
        Select(self.wait.until(EC.element_to_be_clickable(self.SELECTOR_ORDEN))).select_by_value(criterio)
        return self

    def agregar_al_carrito(self, nombre_producto):
        slug = nombre_producto.lower().replace(" ", "-")
        safe_click(self.wait, (By.ID, f"add-to-cart-{slug}"))
        return self

    def quitar_del_carrito(self, nombre_producto):
        slug = nombre_producto.lower().replace(" ", "-")
        safe_click(self.wait, (By.ID, f"remove-{slug}"))
        return self

    def ir_al_carrito(self):
        click_y_esperar(self.wait, self.LINK_CARRITO, EC.url_contains("cart.html"))
        from pages.cart_page import CartPage
        return CartPage(self.driver)
