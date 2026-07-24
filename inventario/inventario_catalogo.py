"""Pruebas del catálogo de productos."""
import allure

from helpers import paso


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
    driver = login_estandar.driver

    with paso(driver, "1. Validar cantidad de productos en el catálogo", "1_Catalogo"):
        cantidad = login_estandar.cantidad_de_productos()
        assert cantidad == 6, f"Se esperaban 6 productos, se encontraron {cantidad}"
        resultados.append(f"Cantidad de productos OK: {cantidad}")

    with paso(driver, "2. Validar que cada producto tenga imagen propia", "2_Catalogo"):
        urls = login_estandar.urls_de_imagenes()
        assert len(set(urls)) == len(urls), "Hay productos que comparten la misma imagen"
        resultados.append("Imágenes únicas por producto OK")

    allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)


@allure.feature("Catálogo")
@allure.story("Ordenamiento")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Selecciona el ordenamiento "Name (Z to A)" en el catálogo y valida que los
nombres de los productos queden efectivamente en orden alfabético
descendente, comparando el listado renderizado contra su versión ordenada.
""")
def test_orden_alfabetico_descendente(login_estandar):
    driver = login_estandar.driver

    with paso(driver, "1. Ordenar el catálogo Z→A", "1_OrdenZA"):
        login_estandar.ordenar_por("za")

    with paso(driver, "2. Validar orden alfabético descendente", "2_OrdenZA"):
        nombres = login_estandar.nombres_de_productos()
        assert nombres == sorted(nombres, reverse=True)


@allure.feature("Catálogo")
@allure.story("Ordenamiento")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Selecciona el ordenamiento "Price (low to high)" en el catálogo y valida que
los precios de los productos queden en orden ascendente, comparando la lista
de precios renderizada contra su versión ordenada.
""")
def test_orden_por_precio_ascendente(login_estandar):
    driver = login_estandar.driver

    with paso(driver, "1. Ordenar el catálogo por precio (menor a mayor)", "1_OrdenPrecio"):
        login_estandar.ordenar_por("lohi")

    with paso(driver, "2. Validar orden ascendente de precios", "2_OrdenPrecio"):
        precios = login_estandar.precios_de_productos()
        assert precios == sorted(precios)
