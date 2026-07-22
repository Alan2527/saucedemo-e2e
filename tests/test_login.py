"""Pruebas del módulo de autenticación."""
import allure
import pytest

from pages.login_page import LoginPage
from utils import config


@allure.feature("Autenticación")
@pytest.mark.login
class TestLogin:

    @allure.title("Login exitoso con usuario estándar")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_exitoso(self, driver):
        inventario = LoginPage(driver).abrir().iniciar_sesion(
            config.USUARIO_ESTANDAR, config.PASSWORD
        )
        assert inventario.titulo() == "Products"
        assert inventario.cantidad_de_productos() > 0

    @allure.title("Login rechazado con contraseña incorrecta")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_password_incorrecta(self, driver):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion(config.USUARIO_ESTANDAR, "password_incorrecta")
        assert "Username and password do not match" in login.obtener_error()

    @allure.title("Login rechazado para usuario bloqueado")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_usuario_bloqueado(self, driver):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion(config.USUARIO_BLOQUEADO, config.PASSWORD)
        assert "Sorry, this user has been locked out" in login.obtener_error()

    @allure.title("Login rechazado con campos vacíos")
    @allure.severity(allure.severity_level.NORMAL)
    def test_campos_vacios(self, driver):
        login = LoginPage(driver).abrir()
        login.iniciar_sesion("", "")
        assert "Username is required" in login.obtener_error()
