"""Página base: helpers de espera e interacción que heredan todos los page objects."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.TIMEOUT)

    def encontrar(self, localizador):
        return self.wait.until(EC.visibility_of_element_located(localizador))

    def encontrar_todos(self, localizador):
        self.wait.until(EC.presence_of_element_located(localizador))
        return self.driver.find_elements(*localizador)

    def click(self, localizador):
        self.wait.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        elemento = self.encontrar(localizador)
        elemento.clear()
        elemento.send_keys(texto)

    def texto_de(self, localizador):
        return self.encontrar(localizador).text

    def es_visible(self, localizador):
        try:
            self.encontrar(localizador)
            return True
        except Exception:
            return False
