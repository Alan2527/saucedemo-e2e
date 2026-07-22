"""Fixtures y hooks compartidos por toda la suite."""
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import config
from pages.login_page import LoginPage


@pytest.fixture
def driver():
    """Instancia de Chrome. Headless por defecto (configurable vía HEADLESS=false)."""
    opciones = Options()
    if config.HEADLESS:
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opciones)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()


@pytest.fixture
def sesion_estandar(driver):
    """Sesión iniciada con el usuario estándar, lista en la página de inventario."""
    login = LoginPage(driver)
    login.abrir()
    return login.iniciar_sesion(config.USUARIO_ESTANDAR, config.PASSWORD)


@pytest.fixture
def sesion_problema(driver):
    """Sesión iniciada con problem_user, para la auditoría de defectos conocidos."""
    login = LoginPage(driver)
    login.abrir()
    return login.iniciar_sesion(config.USUARIO_PROBLEMA, config.PASSWORD)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adjunta una captura de pantalla al reporte Allure cuando un test falla."""
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when == "call" and reporte.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="captura_al_fallar",
                attachment_type=allure.attachment_type.PNG,
            )
