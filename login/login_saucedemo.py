"""Pruebas del módulo de autenticación."""
import allure

from helpers import paso
from pages.login_page import LoginPage
from utils import config


@allure.feature("Autenticación")
@allure.story("Login exitoso")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
Inicia sesión con el usuario estándar (standard_user) y valida:
Que el login redirige correctamente al inventario (inventory.html).
Que el título de la página es "Products".
Que el catálogo renderiza al menos un producto.
""")
def test_login_exitoso(driver):
    with paso(driver, "1. Iniciar sesión con usuario estándar", "1_Login"):
        inventario = LoginPage(driver).abrir().iniciar_sesion(
            config.USUARIO_ESTANDAR, config.PASSWORD
        )

    with paso(driver, "2. Validar que aterriza en el inventario", "2_Inventario"):
        assert inventario.titulo() == "Products"
        assert inventario.cantidad_de_productos() > 0


@allure.feature("Autenticación")
@allure.story("Login rechazado")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Intenta iniciar sesión con el usuario estándar pero una contraseña incorrecta,
y valida que el sistema rechaza el acceso mostrando el mensaje de error
"Username and password do not match any user in this service" (sin loguear).
""")
def test_password_incorrecta(driver):
    with paso(driver, "1. Iniciar sesión con contraseña incorrecta", "1_Error"):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion(config.USUARIO_ESTANDAR, "password_incorrecta")

    with paso(driver, "2. Validar mensaje de error", "2_Error"):
        assert "Username and password do not match" in login.obtener_error()


@allure.feature("Autenticación")
@allure.story("Login rechazado")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Intenta iniciar sesión con locked_out_user (usuario deshabilitado a propósito
por SauceDemo) y valida que el sistema bloquea el acceso mostrando el mensaje
"Sorry, this user has been locked out.", en vez de dejarlo pasar.
""")
def test_usuario_bloqueado(driver):
    with paso(driver, "1. Iniciar sesión con usuario bloqueado", "1_Bloqueado"):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion(config.USUARIO_BLOQUEADO, config.PASSWORD)

    with paso(driver, "2. Validar mensaje de bloqueo", "2_Bloqueado"):
        assert "Sorry, this user has been locked out" in login.obtener_error()


@allure.feature("Autenticación")
@allure.story("Login rechazado")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Intenta iniciar sesión sin completar usuario ni contraseña y valida que el
formulario exige el campo obligatorio, mostrando "Username is required" en
vez de intentar autenticar con campos vacíos.
""")
def test_campos_vacios(driver):
    with paso(driver, "1. Intentar iniciar sesión sin usuario ni contraseña", "1_CamposVacios"):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion("", "")

    with paso(driver, "2. Validar mensaje de campo requerido", "2_CamposVacios"):
        assert "Username is required" in login.obtener_error()
