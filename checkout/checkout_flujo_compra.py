"""Pruebas del flujo de compra completo."""
import allure


@allure.feature("Checkout")
@allure.story("Compra de punta a punta")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
Recorre el flujo completo de compra: agregar producto, ir al carrito,
completar los datos de envío y confirmar. Valida tanto el resumen (Total)
como el mensaje final de confirmación.
""")
def test_compra_exitosa(login_estandar):
    resultados = []

    with allure.step("1. Agregar producto y avanzar al checkout"):
        checkout = (
            login_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
        )
        allure.attach(checkout.driver.get_screenshot_as_png(), "1_Checkout", allure.attachment_type.PNG)

    with allure.step("2. Completar datos de envío"):
        checkout.completar_datos("Alan", "Herrera", "1000")
        allure.attach(checkout.driver.get_screenshot_as_png(), "2_DatosEnvio", allure.attachment_type.PNG)

    with allure.step("3. Validar resumen de compra"):
        total = checkout.obtener_total()
        assert "Total" in total
        resultados.append(f"Resumen OK: {total}")

    with allure.step("4. Confirmar la compra"):
        checkout.finalizar_compra()
        allure.attach(checkout.driver.get_screenshot_as_png(), "4_Confirmacion", allure.attachment_type.PNG)

    with allure.step("5. Validar mensaje de confirmación final"):
        mensaje = checkout.mensaje_de_confirmacion()
        assert mensaje == "Thank you for your order!"
        resultados.append(f"Confirmación OK: {mensaje}")

    allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)


@allure.feature("Checkout")
@allure.story("Validaciones de formulario")
@allure.severity(allure.severity_level.CRITICAL)
def test_nombre_requerido(login_estandar):
    with allure.step("1. Avanzar al checkout sin completar el nombre"):
        checkout = (
            login_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("", "Herrera", "1000")
        )
        allure.attach(checkout.driver.get_screenshot_as_png(), "1_SinNombre", allure.attachment_type.PNG)

    with allure.step("2. Validar mensaje de campo requerido"):
        assert "First Name is required" in checkout.obtener_error()


@allure.feature("Checkout")
@allure.story("Validaciones de formulario")
@allure.severity(allure.severity_level.NORMAL)
def test_codigo_postal_requerido(login_estandar):
    with allure.step("1. Avanzar al checkout sin completar el código postal"):
        checkout = (
            login_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "")
        )
        allure.attach(checkout.driver.get_screenshot_as_png(), "1_SinCP", allure.attachment_type.PNG)

    with allure.step("2. Validar mensaje de campo requerido"):
        assert "Postal Code is required" in checkout.obtener_error()
