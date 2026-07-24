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

from helpers import paso


@allure.feature("Auditoría de defectos (problem_user)")
@allure.story("Catálogo")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Documenta un defecto conocido: con problem_user, los 6 productos del
catálogo muestran la misma imagen (rota/404) en vez de la imagen propia de
cada producto. El test afirma el comportamiento CORRECTO (imágenes únicas) y
está marcado xfail estricto: mientras el bug exista, aparece en el reporte
como defecto documentado sin romper el pipeline; si se corrige, el pipeline
avisa.
""")
@pytest.mark.xfail(reason="Defecto conocido: problem_user ve la misma imagen 404 en los 6 productos", strict=True)
def test_imagenes_unicas(login_problema):
    driver = login_problema.driver

    with paso(driver, "1. Revisar las imágenes del catálogo", "1_Catalogo"):
        urls = login_problema.urls_de_imagenes()

    with paso(driver, "2. Validar que cada producto tenga imagen propia", "2_Catalogo"):
        assert len(set(urls)) == len(urls), f"Las 6 imágenes apuntan a: {set(urls)}"


@allure.feature("Auditoría de defectos (problem_user)")
@allure.story("Catálogo")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Documenta un defecto conocido: con problem_user, el selector de orden
"Name (Z to A)" no reordena el catálogo. El test afirma el comportamiento
CORRECTO (orden alfabético descendente real) y está marcado xfail estricto
por la misma razón que el resto de esta suite.
""")
@pytest.mark.xfail(reason="Defecto conocido: problem_user no puede reordenar el catálogo", strict=True)
def test_ordenamiento(login_problema):
    driver = login_problema.driver

    with paso(driver, "1. Intentar ordenar el catálogo Z→A", "1_Orden"):
        login_problema.ordenar_por("za")

    with paso(driver, "2. Validar orden alfabético descendente", "2_Orden"):
        nombres = login_problema.nombres_de_productos()
        assert nombres == sorted(nombres, reverse=True)


@allure.feature("Auditoría de defectos (problem_user)")
@allure.story("Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Documenta un defecto conocido: con problem_user, el campo Last Name del
formulario de checkout no retiene el valor tipeado. El test completa el
formulario con datos válidos y afirma el comportamiento CORRECTO (el flujo
avanza al resumen de compra); está marcado xfail estricto por la misma razón
que el resto de esta suite.
""")
@pytest.mark.xfail(reason="Defecto conocido: el campo Last Name de problem_user no retiene lo tipeado", strict=True)
def test_apellido_en_checkout(login_problema):
    driver = login_problema.driver
    checkout = None

    with paso(driver, "1. Completar el checkout con datos válidos", "1_Checkout"):
        checkout = (
            login_problema
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "1000")
        )

    with paso(driver, "2. Validar que el flujo avance al resumen de compra", "2_Checkout"):
        # Con datos válidos el flujo debería avanzar al resumen, en vez de
        # quedar atascado por el campo Last Name que no retiene el valor.
        assert "Total" in checkout.obtener_total()
