"""Pruebas del catálogo de productos."""
import allure
import pytest


@allure.feature("Catálogo")
@pytest.mark.inventario
class TestInventario:

    @allure.title("El catálogo muestra los 6 productos")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cantidad_de_productos(self, sesion_estandar):
        assert sesion_estandar.cantidad_de_productos() == 6

    @allure.title("Ordenamiento alfabético Z→A")
    @allure.severity(allure.severity_level.NORMAL)
    def test_orden_alfabetico_descendente(self, sesion_estandar):
        sesion_estandar.ordenar_por("za")
        nombres = sesion_estandar.nombres_de_productos()
        assert nombres == sorted(nombres, reverse=True)

    @allure.title("Ordenamiento por precio menor→mayor")
    @allure.severity(allure.severity_level.NORMAL)
    def test_orden_por_precio_ascendente(self, sesion_estandar):
        sesion_estandar.ordenar_por("lohi")
        precios = sesion_estandar.precios_de_productos()
        assert precios == sorted(precios)

    @allure.title("Cada producto tiene su imagen propia")
    @allure.severity(allure.severity_level.MINOR)
    def test_imagenes_unicas(self, sesion_estandar):
        urls = sesion_estandar.urls_de_imagenes()
        assert len(set(urls)) == len(urls), "Hay productos que comparten la misma imagen"
