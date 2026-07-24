"""
Helpers reutilizables para los tests de Selenium.

Centraliza las funciones robustas de interacción (click / escritura) que antes
vivían repetidas en cada page object. Importar desde cualquier page object:

    from helpers import safe_click, safe_send_keys, click_y_esperar
"""

import time
from contextlib import contextmanager

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
    TimeoutException,
)


@contextmanager
def paso(driver, descripcion, nombre_captura=None):
    """Envuelve un `allure.step` adjuntando SIEMPRE una captura de pantalla
    al finalizar el paso, sin importar si terminó bien, con un assert fallido
    o con una excepción a mitad de camino (ej. TimeoutException en un click).

    Sin esto, un paso de solo-validación (un `assert` suelto) no dejaba
    ninguna captura propia al fallar: solo quedaba la captura genérica de
    `pytest_runtest_makereport` al final del test, desconectada del paso
    puntual que rompió. Con `paso`, cada paso queda con su propia evidencia
    visual en el reporte, igual que en el resto de la suite.
    """
    with allure.step(descripcion):
        try:
            yield
        finally:
            allure.attach(
                driver.get_screenshot_as_png(),
                nombre_captura or descripcion,
                allure.attachment_type.PNG,
            )


def safe_click(wait, locator, retries=5):
    """Click resistente a elementos 'stale' (reintenta hasta `retries` veces)."""
    for _ in range(retries):
        try:
            elem = wait.until(EC.element_to_be_clickable(locator))
            elem.click()
            return
        except StaleElementReferenceException:
            time.sleep(1)
    raise Exception(f"No se pudo hacer click: {locator}")


def safe_send_keys(wait, locator, value, retries=5):
    """Escritura robusta: espera visibilidad, limpia y escribe; reintenta si el
    campo todavía no es interactuable."""
    for _ in range(retries):
        try:
            elem = wait.until(EC.visibility_of_element_located(locator))
            elem.clear()
            elem.send_keys(value)
            return
        except (StaleElementReferenceException, ElementNotInteractableException):
            time.sleep(1)
    raise Exception(f"No se pudo escribir en: {locator}")


def click_y_esperar(wait, locator, condicion_de_llegada, reintentos=2):
    """Click con verificación y reintento.

    SauceDemo es una SPA (Angular): en Chrome headless, ocasionalmente el
    listener de click aún no está adjunto en el instante exacto en que
    Selenium lo ejecuta, produciendo un "click muerto" que no navega pero
    tampoco lanza error. Este helper verifica que la navegación realmente
    ocurrió y reintenta el click si no fue así, en lugar de asumir éxito.
    """
    ultimo_error = None
    for _ in range(reintentos):
        safe_click(wait, locator)
        try:
            wait.until(condicion_de_llegada)
            return
        except TimeoutException as error:
            ultimo_error = error
    raise ultimo_error


def texto_de(wait, locator):
    """Espera visibilidad y lee el textContent (DOM renderizado), sin
    depender del viewport."""
    elem = wait.until(EC.visibility_of_element_located(locator))
    return elem.get_attribute("textContent").strip()
