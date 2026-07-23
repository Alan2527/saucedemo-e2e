# Suite de Regresión E2E — SauceDemo

![CI](https://github.com/Alan2527/saucedemo-e2e/actions/workflows/regresion.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green)
![Allure](https://img.shields.io/badge/Reportes-Allure-orange)

Framework de automatización end-to-end sobre [SauceDemo](https://www.saucedemo.com), construido con **Python + Pytest + Selenium** bajo el patrón **Page Object Model**, integrado a **GitHub Actions** con reportes **Allure** publicados automáticamente en GitHub Pages.

📊 **[Ver el último reporte Allure →](https://alan2527.github.io/saucedemo-e2e/)**

## Qué demuestra este proyecto

- **Arquitectura Page Object Model**: separación estricta entre lógica de páginas y casos de prueba, con navegación fluida entre page objects.
- **Organización por área funcional**: los tests viven en carpetas por módulo (`login/`, `inventario/`, `carrito/`, `checkout/`, `defectos/`) con nombres de archivo descriptivos, y quedan marcados automáticamente según su carpeta (`pytest -m carrito`) sin tener que anotar cada clase a mano.
- **Esperas explícitas** (`WebDriverWait` + `expected_conditions`): sin `sleep()`, sin flakiness.
- **Detección de defectos reales**: SauceDemo incluye un usuario con bugs plantados (`problem_user`). La suite los detecta y los documenta como `xfail` estricto — el reporte los expone sin romper el pipeline, y si un bug se corrige, el pipeline avisa.
- **CI/CD**: cada push ejecuta la regresión completa en GitHub Actions; el workflow es parametrizable por suite (`login`, `inventario`, `carrito`, `checkout`, `defectos`).
- **Reportes Allure con historial**: pasos numerados con captura de pantalla en cada uno, severidades, descripciones y capturas automáticas al fallar.

## Cobertura

| Suite | Casos | Qué valida |
|---|---|---|
| Login | 4 | Autenticación exitosa, credenciales inválidas, usuario bloqueado, campos requeridos |
| Inventario | 3 | Catálogo completo, imágenes únicas, ordenamientos (alfabético y precio) |
| Carrito | 4 | Alta/baja de productos, badge, contenido del carrito |
| Checkout | 3 | Compra de punta a punta, validaciones de formulario |
| Defectos | 3 | Auditoría de bugs conocidos de `problem_user` |

## Estructura

```
├── conftest.py         # Fixtures (driver, sesiones de login), auto-marcado por carpeta,
│                        # captura automática al fallar y environment.properties de Allure
├── helpers.py           # safe_click / safe_send_keys / click_y_esperar — interacciones robustas
├── pages/                # Page objects
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── login/                # Casos de autenticación
├── inventario/           # Casos del catálogo
├── carrito/              # Casos del carrito
├── checkout/             # Casos del flujo de compra
├── defectos/             # Auditoría de bugs conocidos (problem_user)
├── utils/config.py       # Configuración central (URL, usuarios, timeouts)
└── .github/workflows/    # Pipeline de regresión + publicación del reporte
```

## Ejecución local

```bash
pip install -r requirements.txt

# Suite completa (headless por defecto, genera ./allure-results)
pytest

# Una suite puntual, con navegador visible
HEADLESS=false pytest -m checkout

# Ver el reporte
allure serve allure-results
```

## Decisiones de diseño

- **Carpetas por área, no un `tests/` genérico**: cada módulo del sitio (login, inventario, carrito, checkout) tiene su propia carpeta con archivos de nombre descriptivo; `conftest.py` los marca automáticamente según la carpeta en la que viven.
- **`xfail` estricto para defectos conocidos**: un bug documentado no debe pintar de rojo la regresión, pero su corrección silenciosa tampoco debe pasar desapercibida.
- **Fixtures de sesión** (`login_estandar`, `login_problema`): los tests de módulos internos no repiten el login por UI en cada caso, reduciendo tiempo total y puntos de falla.
- **Pasos numerados con evidencia**: cada `allure.step` relevante adjunta su propia captura, para poder reconstruir visualmente el recorrido del test sin correrlo de nuevo.
- **Selectores por `id`/`data-test`**: prioridad a los atributos más estables del DOM.

---
*Proyecto de portfolio — [Alan Herrera](https://www.linkedin.com/in/alan-herrera-15b8a2215), Sr. QA Analyst.*
