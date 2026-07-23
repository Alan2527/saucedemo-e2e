"""Pruebas del módulo de autenticación."""
import allure

from pages.login_page import LoginPage
from utils import config


@allure.feature("Autenticación")
@allure.story("Login exitoso")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_exitoso(driver):
    with allure.step("1. Iniciar sesión con usuario estándar"):
        inventario = LoginPage(driver).abrir().iniciar_sesion(
            config.USUARIO_ESTANDAR, config.PASSWORD
        )
        allure.attach(driver.get_screenshot_as_png(), "1_Login", allure.attachment_type.PNG)

    with allure.step("2. Validar que aterriza en el inventario"):
        assert inventario.titulo() == "Products"
        assert inventario.cantidad_de_productos() > 0
        allure.attach(driver.get_screenshot_as_png(), "2_Inventario", allure.attachment_type.PNG)


@allure.feature("Autenticación")
@allure.story("Login rechazado")
@allure.severity(allure.severity_level.CRITICAL)
def test_password_incorrecta(driver):
    with allure.step("1. Iniciar sesión con contraseña incorrecta"):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion(config.USUARIO_ESTANDAR, "password_incorrecta")
        allure.attach(driver.get_screenshot_as_png(), "1_Error", allure.attachment_type.PNG)

    with allure.step("2. Validar mensaje de error"):
        assert "Username and password do not match" in login.obtener_error()


@allure.feature("Autenticación")
@allure.story("Login rechazado")
@allure.severity(allure.severity_level.CRITICAL)
def test_usuario_bloqueado(driver):
    with allure.step("1. Iniciar sesión con usuario bloqueado"):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion(config.USUARIO_BLOQUEADO, config.PASSWORD)
        allure.attach(driver.get_screenshot_as_png(), "1_Bloqueado", allure.attachment_type.PNG)

    with allure.step("2. Validar mensaje de bloqueo"):
        assert "Sorry, this user has been locked out" in login.obtener_error()


@allure.feature("Autenticación")
@allure.story("Login rechazado")
@allure.severity(allure.severity_level.NORMAL)
def test_campos_vacios(driver):
    with allure.step("1. Intentar iniciar sesión sin usuario ni contraseña"):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion("", "")
        allure.attach(driver.get_screenshot_as_png(), "1_CamposVacios", allure.attachment_type.PNG)

    with allure.step("2. Validar mensaje de campo requerido"):
        assert "Username is required" in login.obtener_error()
