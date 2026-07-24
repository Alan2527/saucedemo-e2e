"""Pruebas del carrito de compras."""
import allure

from helpers import paso


@allure.feature("Carrito")
@allure.story("Alta de productos")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Agrega "Sauce Labs Backpack" al carrito desde el catálogo y valida que el
badge del ícono de carrito se actualice a 1, reflejando el alta en tiempo real.
""")
def test_agregar_producto(login_estandar):
    driver = login_estandar.driver

    with paso(driver, "1. Agregar un producto al carrito", "1_Agregado"):
        login_estandar.agregar_al_carrito("sauce labs backpack")

    with paso(driver, "2. Validar badge del carrito", "2_Agregado"):
        assert login_estandar.items_en_badge() == 1


@allure.feature("Carrito")
@allure.story("Alta de productos")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Agrega "Sauce Labs Backpack" al carrito y navega a la página del carrito,
validando que el producto agregado efectivamente aparezca listado ahí (no
solo que el badge suba, sino que el contenido real del carrito sea correcto).
""")
def test_producto_en_carrito(login_estandar):
    driver = login_estandar.driver
    carrito = None

    with paso(driver, "1. Agregar producto e ir al carrito", "1_Carrito"):
        login_estandar.agregar_al_carrito("sauce labs backpack")
        carrito = login_estandar.ir_al_carrito()

    with paso(driver, "2. Validar contenido del carrito", "2_Carrito"):
        assert carrito.productos_en_carrito() == ["Sauce Labs Backpack"]


@allure.feature("Carrito")
@allure.story("Baja de productos")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Agrega "Sauce Labs Bike Light" al carrito y luego lo quita desde el mismo
catálogo, validando que el badge del carrito vuelva a cero (sin quedar un
contador "fantasma" tras la baja).
""")
def test_quitar_producto(login_estandar):
    driver = login_estandar.driver

    with paso(driver, "1. Agregar y luego quitar el mismo producto", "1_Quitado"):
        login_estandar.agregar_al_carrito("sauce labs bike-light")
        login_estandar.quitar_del_carrito("sauce labs bike-light")

    with paso(driver, "2. Validar que el badge quede en cero", "2_Quitado"):
        assert login_estandar.items_en_badge() == 0


@allure.feature("Carrito")
@allure.story("Alta de productos")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Agrega tres productos distintos al carrito en la misma sesión y valida que el
badge acumule correctamente el total (3), en vez de sobreescribir o perder
el conteo de altas previas.
""")
def test_multiples_productos(login_estandar):
    driver = login_estandar.driver

    with paso(driver, "1. Agregar tres productos distintos", "1_TresProductos"):
        login_estandar.agregar_al_carrito("sauce labs backpack")
        login_estandar.agregar_al_carrito("sauce labs bolt-t-shirt")
        login_estandar.agregar_al_carrito("sauce labs onesie")

    with paso(driver, "2. Validar que el badge sume los tres", "2_TresProductos"):
        assert login_estandar.items_en_badge() == 3
