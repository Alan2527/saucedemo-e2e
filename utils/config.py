"""Configuración central de la suite."""
import os

BASE_URL = "https://www.saucedemo.com/"

USUARIO_ESTANDAR = "standard_user"
USUARIO_BLOQUEADO = "locked_out_user"
USUARIO_PROBLEMA = "problem_user"
PASSWORD = "secret_sauce"

HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
