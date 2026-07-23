"""
Page Object de la pantalla de login.

Centraliza los selectores y expone métodos legibles para que el test no
dependa de los detalles del DOM. Si la UI cambia, se ajusta acá (un solo
lugar) y no en cada test.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from helpers import safe_click, safe_send_keys, texto_de
from utils import config


class LoginPage:
    # --- Locators ---
    USUARIO = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def abrir(self):
        self.driver.get(config.BASE_URL)
        return self

    def iniciar_sesion(self, usuario, password):
        safe_send_keys(self.wait, self.USUARIO, usuario)
        safe_send_keys(self.wait, self.PASSWORD, password)
        safe_click(self.wait, self.BOTON_LOGIN)

        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)

    def obtener_error(self):
        return texto_de(self.wait, self.MENSAJE_ERROR)
