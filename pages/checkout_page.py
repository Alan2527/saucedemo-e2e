"""Page object del flujo de checkout (datos, resumen y confirmación)."""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    NOMBRE = (By.ID, "first-name")
    APELLIDO = (By.ID, "last-name")
    CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_FINALIZAR = (By.ID, "finish")
    MENSAJE_ERROR = (By.CSS_SELECTOR, '[data-test="error"]')
    TOTAL = (By.CSS_SELECTOR, ".summary_total_label")
    CONFIRMACION = (By.CSS_SELECTOR, ".complete-header")

    @allure.step("Completar datos de envío")
    def completar_datos(self, nombre, apellido, codigo_postal):
        self.escribir(self.NOMBRE, nombre)
        self.escribir(self.APELLIDO, apellido)
        self.escribir(self.CODIGO_POSTAL, codigo_postal)
        self.click(self.BOTON_CONTINUAR)
        return self

    @allure.step("Confirmar la compra")
    def finalizar_compra(self):
        self.click(self.BOTON_FINALIZAR)
        return self

    def obtener_error(self):
        return self.texto_de(self.MENSAJE_ERROR)

    def obtener_total(self):
        return self.texto_de(self.TOTAL)

    def mensaje_de_confirmacion(self):
        return self.texto_de(self.CONFIRMACION)
