"""Pruebas del flujo de compra completo."""
import allure
import pytest


@allure.feature("Checkout")
@pytest.mark.checkout
class TestCheckout:

    @allure.title("Compra completa de punta a punta")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_compra_exitosa(self, sesion_estandar):
        checkout = (
            sesion_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "1000")
        )
        assert "Total" in checkout.obtener_total()
        checkout.finalizar_compra()
        assert checkout.mensaje_de_confirmacion() == "Thank you for your order!"

    @allure.title("El checkout exige nombre")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nombre_requerido(self, sesion_estandar):
        checkout = (
            sesion_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("", "Herrera", "1000")
        )
        assert "First Name is required" in checkout.obtener_error()

    @allure.title("El checkout exige código postal")
    @allure.severity(allure.severity_level.NORMAL)
    def test_codigo_postal_requerido(self, sesion_estandar):
        checkout = (
            sesion_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "")
        )
        assert "Postal Code is required" in checkout.obtener_error()
