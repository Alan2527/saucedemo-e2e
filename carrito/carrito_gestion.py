"""Pruebas del carrito de compras."""
import allure


@allure.feature("Carrito")
@allure.story("Alta de productos")
@allure.severity(allure.severity_level.CRITICAL)
def test_agregar_producto(login_estandar):
    with allure.step("1. Agregar un producto al carrito"):
        login_estandar.agregar_al_carrito("sauce labs backpack")
        allure.attach(login_estandar.driver.get_screenshot_as_png(), "1_Agregado", allure.attachment_type.PNG)

    with allure.step("2. Validar badge del carrito"):
        assert login_estandar.items_en_badge() == 1


@allure.feature("Carrito")
@allure.story("Alta de productos")
@allure.severity(allure.severity_level.CRITICAL)
def test_producto_en_carrito(login_estandar):
    with allure.step("1. Agregar producto e ir al carrito"):
        login_estandar.agregar_al_carrito("sauce labs backpack")
        carrito = login_estandar.ir_al_carrito()
        allure.attach(carrito.driver.get_screenshot_as_png(), "1_Carrito", allure.attachment_type.PNG)

    with allure.step("2. Validar contenido del carrito"):
        assert carrito.productos_en_carrito() == ["Sauce Labs Backpack"]


@allure.feature("Carrito")
@allure.story("Baja de productos")
@allure.severity(allure.severity_level.NORMAL)
def test_quitar_producto(login_estandar):
    with allure.step("1. Agregar y luego quitar el mismo producto"):
        login_estandar.agregar_al_carrito("sauce labs bike-light")
        login_estandar.quitar_del_carrito("sauce labs bike-light")
        allure.attach(login_estandar.driver.get_screenshot_as_png(), "1_Quitado", allure.attachment_type.PNG)

    with allure.step("2. Validar que el badge quede en cero"):
        assert login_estandar.items_en_badge() == 0


@allure.feature("Carrito")
@allure.story("Alta de productos")
@allure.severity(allure.severity_level.NORMAL)
def test_multiples_productos(login_estandar):
    with allure.step("1. Agregar tres productos distintos"):
        login_estandar.agregar_al_carrito("sauce labs backpack")
        login_estandar.agregar_al_carrito("sauce labs bolt-t-shirt")
        login_estandar.agregar_al_carrito("sauce labs onesie")
        allure.attach(login_estandar.driver.get_screenshot_as_png(), "1_TresProductos", allure.attachment_type.PNG)

    with allure.step("2. Validar que el badge sume los tres"):
        assert login_estandar.items_en_badge() == 3
