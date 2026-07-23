"""Pruebas del catálogo de productos."""
import allure


@allure.feature("Catálogo")
@allure.story("Listado de productos")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Valida que el catálogo muestre los 6 productos esperados y que cada uno tenga
su propia imagen (no todas apuntando a la misma URL, defecto conocido de
problem_user — ver suite `defectos`).
""")
def test_cantidad_de_productos(login_estandar):
    resultados = []

    with allure.step("1. Validar cantidad de productos en el catálogo"):
        cantidad = login_estandar.cantidad_de_productos()
        assert cantidad == 6, f"Se esperaban 6 productos, se encontraron {cantidad}"
        resultados.append(f"Cantidad de productos OK: {cantidad}")

    with allure.step("2. Validar que cada producto tenga imagen propia"):
        urls = login_estandar.urls_de_imagenes()
        assert len(set(urls)) == len(urls), "Hay productos que comparten la misma imagen"
        resultados.append("Imágenes únicas por producto OK")
        allure.attach(login_estandar.driver.get_screenshot_as_png(), "Catalogo", allure.attachment_type.PNG)

    allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)


@allure.feature("Catálogo")
@allure.story("Ordenamiento")
@allure.severity(allure.severity_level.NORMAL)
def test_orden_alfabetico_descendente(login_estandar):
    with allure.step("1. Ordenar el catálogo Z→A"):
        login_estandar.ordenar_por("za")
        allure.attach(login_estandar.driver.get_screenshot_as_png(), "1_OrdenZA", allure.attachment_type.PNG)

    with allure.step("2. Validar orden alfabético descendente"):
        nombres = login_estandar.nombres_de_productos()
        assert nombres == sorted(nombres, reverse=True)


@allure.feature("Catálogo")
@allure.story("Ordenamiento")
@allure.severity(allure.severity_level.NORMAL)
def test_orden_por_precio_ascendente(login_estandar):
    with allure.step("1. Ordenar el catálogo por precio (menor a mayor)"):
        login_estandar.ordenar_por("lohi")
        allure.attach(login_estandar.driver.get_screenshot_as_png(), "1_OrdenPrecio", allure.attachment_type.PNG)

    with allure.step("2. Validar orden ascendente de precios"):
        precios = login_estandar.precios_de_productos()
        assert precios == sorted(precios)
