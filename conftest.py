import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import config
from pages.login_page import LoginPage


# =================================================================
# DRIVER
# =================================================================
@pytest.fixture
def driver():
    """Instancia de Chrome. Headless por defecto (configurable vía HEADLESS=false)."""
    opciones = Options()
    if config.HEADLESS:
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=opciones)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()


# =================================================================
# FIXTURES DE SESIÓN
#   Devuelven un page object ya logueado y listo en el inventario, evitando
#   reescribir el login por UI en cada test.
# =================================================================
@pytest.fixture
def login_estandar(driver):
    """Sesión iniciada con el usuario estándar, lista en el inventario."""
    with allure.step("Login como standard_user"):
        return LoginPage(driver).abrir().iniciar_sesion(config.USUARIO_ESTANDAR, config.PASSWORD)


@pytest.fixture
def login_problema(driver):
    """Sesión iniciada con problem_user, para la auditoría de defectos conocidos."""
    with allure.step("Login como problem_user"):
        return LoginPage(driver).abrir().iniciar_sesion(config.USUARIO_PROBLEMA, config.PASSWORD)


# Alias retrocompatible con nombres usados en versiones anteriores de la suite.
@pytest.fixture
def sesion_estandar(login_estandar):
    return login_estandar


@pytest.fixture
def sesion_problema(login_problema):
    return login_problema


# =================================================================
# CAPTURA AUTOMÁTICA AL FALLAR
# =================================================================
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


# =================================================================
# AUTO-MARCADO POR CARPETA
#   Marca cada test según su ubicación: @login / @inventario / @carrito /
#   @checkout / @defectos. Permite correr suites selectivas: `pytest -m carrito`.
# =================================================================
def pytest_collection_modifyitems(config, items):
    for item in items:
        path = str(item.fspath).replace("\\", "/")
        for marcador in ("login", "inventario", "carrito", "checkout", "defectos"):
            if f"/{marcador}/" in path:
                item.add_marker(getattr(pytest.mark, marcador))


# =================================================================
# ALLURE ENVIRONMENT
# =================================================================
def pytest_sessionfinish(session, exitstatus):
    """Genera environment.properties para el panel 'Environment' de Allure."""
    allure_dir = "allure-results"
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)

    env_file = os.path.join(allure_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write("Entorno=SauceDemo (demo publica)\n")
        f.write("Navegador=Chrome (Headless)\n")
        f.write(f"URL={config.BASE_URL}\n")
        f.write("Framework=Pytest+Selenium\n")
