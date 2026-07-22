"""Page object del catálogo de productos."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITULO = (By.CSS_SELECTOR, ".title")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    NOMBRES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRECIOS = (By.CSS_SELECTOR, ".inventory_item_price")
    IMAGENES = (By.CSS_SELECTOR, ".inventory_item_img img")
    SELECTOR_ORDEN = (By.CSS_SELECTOR, ".product_sort_container")
    BADGE_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge")
    LINK_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_link")

    def titulo(self):
        return self.texto_de(self.TITULO)

    def cantidad_de_productos(self):
        return len(self.encontrar_todos(self.ITEMS))

    def nombres_de_productos(self):
        return [e.text for e in self.encontrar_todos(self.NOMBRES)]

    def precios_de_productos(self):
        return [float(e.text.replace("$", "")) for e in self.encontrar_todos(self.PRECIOS)]

    def urls_de_imagenes(self):
        return [e.get_attribute("src") for e in self.encontrar_todos(self.IMAGENES)]

    @allure.step("Ordenar productos por «{criterio}»")
    def ordenar_por(self, criterio):
        Select(self.encontrar(self.SELECTOR_ORDEN)).select_by_value(criterio)
        return self

    @allure.step("Agregar «{nombre_producto}» al carrito")
    def agregar_al_carrito(self, nombre_producto):
        slug = nombre_producto.lower().replace(" ", "-")
        self.click((By.ID, f"add-to-cart-{slug}"))
        return self

    @allure.step("Quitar «{nombre_producto}» del carrito")
    def quitar_del_carrito(self, nombre_producto):
        slug = nombre_producto.lower().replace(" ", "-")
        self.click((By.ID, f"remove-{slug}"))
        return self

    def items_en_badge(self):
        if not self.es_visible(self.BADGE_CARRITO):
            return 0
        return int(self.texto_de(self.BADGE_CARRITO))

    @allure.step("Ir al carrito")
    def ir_al_carrito(self):
        from selenium.webdriver.support import expected_conditions as EC
        from pages.cart_page import CartPage
        self.click_y_esperar(self.LINK_CARRITO, EC.url_contains("cart.html"))
        return CartPage(self.driver)
