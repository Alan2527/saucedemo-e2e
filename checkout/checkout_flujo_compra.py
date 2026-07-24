"""Pruebas del flujo de compra completo."""
import allure

from helpers import paso


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
    driver = login_estandar.driver
    checkout = None

    with paso(driver, "1. Agregar producto y avanzar al checkout", "1_Checkout"):
        checkout = (
            login_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
        )

    with paso(driver, "2. Completar datos de envío", "2_DatosEnvio"):
        checkout.completar_datos("Alan", "Herrera", "1000")

    with paso(driver, "3. Validar resumen de compra", "3_Resumen"):
        total = checkout.obtener_total()
        assert "Total" in total
        resultados.append(f"Resumen OK: {total}")

    with paso(driver, "4. Confirmar la compra", "4_Confirmacion"):
        checkout.finalizar_compra()

    with paso(driver, "5. Validar mensaje de confirmación final", "5_Confirmacion"):
        mensaje = checkout.mensaje_de_confirmacion()
        assert mensaje == "Thank you for your order!"
        resultados.append(f"Confirmación OK: {mensaje}")

    allure.attach("\n".join(resultados), "Validaciones realizadas", allure.attachment_type.TEXT)


@allure.feature("Checkout")
@allure.story("Validaciones de formulario")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Intenta avanzar el checkout dejando el campo Nombre vacío y valida que el
formulario lo exige, mostrando "First Name is required" en vez de dejar
avanzar el flujo con datos incompletos.
""")
def test_nombre_requerido(login_estandar):
    driver = login_estandar.driver
    checkout = None

    with paso(driver, "1. Avanzar al checkout sin completar el nombre", "1_SinNombre"):
        checkout = (
            login_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("", "Herrera", "1000")
        )

    with paso(driver, "2. Validar mensaje de campo requerido", "2_SinNombre"):
        assert "First Name is required" in checkout.obtener_error()


@allure.feature("Checkout")
@allure.story("Validaciones de formulario")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Intenta avanzar el checkout dejando el campo Código Postal vacío y valida
que el formulario lo exige, mostrando "Postal Code is required" en vez de
dejar avanzar el flujo con datos incompletos.
""")
def test_codigo_postal_requerido(login_estandar):
    driver = login_estandar.driver
    checkout = None

    with paso(driver, "1. Avanzar al checkout sin completar el código postal", "1_SinCP"):
        checkout = (
            login_estandar
            .agregar_al_carrito("sauce labs backpack")
            .ir_al_carrito()
            .continuar_al_checkout()
            .completar_datos("Alan", "Herrera", "")
        )

    with paso(driver, "2. Validar mensaje de campo requerido", "2_SinCP"):
        assert "Postal Code is required" in checkout.obtener_error()
