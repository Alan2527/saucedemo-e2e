"""
Auditoría de defectos conocidos del usuario problem_user.

SauceDemo incluye a propósito un usuario con bugs plantados. Esta suite los
detecta y documenta: cada test afirma el comportamiento CORRECTO y está
marcado como xfail estricto, de modo que el reporte Allure los exponga como
defectos conocidos sin romper el pipeline — y si algún bug se corrige, el
pipeline avisa (xfail que pasa = failure).
"""
import allure
import pytest


@allure.feature("Auditoría de defectos (problem_user)")
@allure.story("Catálogo")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.xfail(reason="Defecto conocido: problem_user ve la misma imagen 404 en los 6 productos", strict=True)
def test_imagenes_unicas(login_problema):
    with allure.step("1. Revisar las imágenes del catálogo"):
        urls = login_problema.urls_de_imagenes()
        allure.attach(login_problema.driver.get_screenshot_as_png(), "1_Catalogo", allure.attachment_type.PNG)

    with allure.step("2. Validar que cada producto tenga imagen propia"):
        assert len(set(urls)) == len(urls), f"Las 6 imágenes apuntan a: {set(urls)}"


@allure.feature("Auditoría de defectos (problem_user)")
@allure.story("Catálogo")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(reason="Defecto conocido: problem_user no puede reordenar el catálogo", strict=True)
def test_ordenamiento(login_problema):
    with allure.step("1. Intentar ordenar el catálogo Z→A"):
        login_problema.ordenar_por("za")
        allure.attach(login_problema.driver.get_screenshot_as_png(), "1_Orden", allure.attachment_type.PNG)

    with allure.step("2. Validar orden alfabético descendente"):
        nombres = login_problema.nombres_de_productos()
        assert nombres == sorted(nombres, reverse=True)


@allure.feature("Auditoría de defectos (problem_user)")
@allure.story("Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.xfail(reason="Defecto conocido: el campo Last Name de problem_user no retiene lo tipeado", strict=True)
def test_apellido_en_checkout(login_problema):
    with allure.step("1. Completar el checkout con datos válidos"):
        checkout = (
            login_problema
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "1000")
        )
        allure.attach(checkout.driver.get_screenshot_as_png(), "1_Checkout", allure.attachment_type.PNG)

    with allure.step("2. Validar que el flujo avance al resumen de compra"):
        # Con datos válidos el flujo debería avanzar al resumen, en vez de
        # quedar atascado por el campo Last Name que no retiene el valor.
        assert "Total" in checkout.obtener_total()
