"""Pruebas del carrito de compras."""
import allure
import pytest


@allure.feature("Carrito")
@pytest.mark.carrito
class TestCarrito:

    @allure.title("Agregar un producto actualiza el badge del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_agregar_producto(self, sesion_estandar):
        sesion_estandar.agregar_al_carrito("sauce labs backpack")
        assert sesion_estandar.items_en_badge() == 1

    @allure.title("El producto agregado aparece en el carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_producto_en_carrito(self, sesion_estandar):
        sesion_estandar.agregar_al_carrito("sauce labs backpack")
        carrito = sesion_estandar.ir_al_carrito()
        assert carrito.productos_en_carrito() == ["Sauce Labs Backpack"]

    @allure.title("Quitar un producto vacía el badge")
    @allure.severity(allure.severity_level.NORMAL)
    def test_quitar_producto(self, sesion_estandar):
        sesion_estandar.agregar_al_carrito("sauce labs bike-light")
        sesion_estandar.quitar_del_carrito("sauce labs bike-light")
        assert sesion_estandar.items_en_badge() == 0

    @allure.title("Agregar múltiples productos suma en el badge")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiples_productos(self, sesion_estandar):
        sesion_estandar.agregar_al_carrito("sauce labs backpack")
        sesion_estandar.agregar_al_carrito("sauce labs bolt-t-shirt")
        sesion_estandar.agregar_al_carrito("sauce labs onesie")
        assert sesion_estandar.items_en_badge() == 3
