"""Page Object del flujo de checkout (datos, resumen y confirmación)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import safe_send_keys, click_y_esperar, texto_de


class CheckoutPage:
    # --- Locators ---
    NOMBRE = (By.ID, "first-name")
    APELLIDO = (By.ID, "last-name")
    CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_FINALIZAR = (By.ID, "finish")
    MENSAJE_ERROR = (By.CSS_SELECTOR, '[data-test="error"]')
    TOTAL = (By.CSS_SELECTOR, ".summary_total_label")
    CONFIRMACION = (By.CSS_SELECTOR, ".complete-header")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def completar_datos(self, nombre, apellido, codigo_postal):
        safe_send_keys(self.wait, self.NOMBRE, nombre)
        safe_send_keys(self.wait, self.APELLIDO, apellido)
        safe_send_keys(self.wait, self.CODIGO_POSTAL, codigo_postal)
        click_y_esperar(
            self.wait,
            self.BOTON_CONTINUAR,
            EC.any_of(
                EC.url_contains("checkout-step-two.html"),
                EC.visibility_of_element_located(self.MENSAJE_ERROR),
            ),
        )
        return self

    def finalizar_compra(self):
        click_y_esperar(self.wait, self.BOTON_FINALIZAR, EC.url_contains("checkout-complete.html"))
        return self

    def obtener_error(self):
        return texto_de(self.wait, self.MENSAJE_ERROR)

    def obtener_total(self):
        return texto_de(self.wait, self.TOTAL)

    def mensaje_de_confirmacion(self):
        return texto_de(self.wait, self.CONFIRMACION)
