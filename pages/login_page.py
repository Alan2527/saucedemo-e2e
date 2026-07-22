"""Page object de la pantalla de login."""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils import config


class LoginPage(BasePage):
    USUARIO = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    @allure.step("Abrir la página de login")
    def abrir(self):
        self.driver.get(config.BASE_URL)
        return self

    @allure.step("Iniciar sesión como {usuario}")
    def iniciar_sesion(self, usuario, password):
        from pages.inventory_page import InventoryPage
        self.escribir(self.USUARIO, usuario)
        self.escribir(self.PASSWORD, password)
        self.click(self.BOTON_LOGIN)
        return InventoryPage(self.driver)

    def obtener_error(self):
        return self.texto_de(self.MENSAJE_ERROR)
