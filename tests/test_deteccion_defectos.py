"""Auditoría de defectos conocidos del usuario problem_user.

SauceDemo incluye a propósito un usuario con bugs plantados. Esta suite los
detecta y documenta: cada test afirma el comportamiento CORRECTO y está marcado
como xfail, de modo que el reporte Allure los exponga como defectos conocidos
sin romper el pipeline.
"""
import allure
import pytest


@allure.feature("Auditoría de defectos (problem_user)")
@pytest.mark.defectos
class TestDefectosConocidos:

    @allure.title("BUG: todos los productos muestran la misma imagen")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Defecto conocido: problem_user ve la misma imagen 404 en los 6 productos", strict=True)
    def test_imagenes_unicas(self, sesion_problema):
        urls = sesion_problema.urls_de_imagenes()
        assert len(set(urls)) == len(urls), f"Las 6 imágenes apuntan a: {set(urls)}"

    @allure.title("BUG: el ordenamiento alfabético Z→A no funciona")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Defecto conocido: problem_user no puede reordenar el catálogo", strict=True)
    def test_ordenamiento(self, sesion_problema):
        sesion_problema.ordenar_por("za")
        nombres = sesion_problema.nombres_de_productos()
        assert nombres == sorted(nombres, reverse=True)

    @allure.title("BUG: el apellido no se conserva en el formulario de checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Defecto conocido: el campo Last Name de problem_user no retiene lo tipeado", strict=True)
    def test_apellido_en_checkout(self, sesion_problema):
        checkout = (
            sesion_problema
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "1000")
        )
        # Con datos válidos el flujo debería avanzar al resumen de compra
        assert "Total" in checkout.obtener_total()
