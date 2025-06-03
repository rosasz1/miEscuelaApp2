# -*- coding: utf-8 -*-

import logging

# Configuración básica del logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

# Obtener el logger
log = logging.getLogger('logger_base')

# Función de prueba para loguear mensajes con diferentes niveles
def test_logging():
    try:
        log.debug("Este es un mensaje de DEBUG")  # Mensaje para depuración
        log.info("Este es un mensaje de INFO")   # Mensaje informativo
        log.warning("Este es un mensaje de WARNING")  # Advertencia
        log.error("Este es un mensaje de ERROR")    # Error
        log.critical("Este es un mensaje CRÍTICO")  # Crítico
    except Exception as e:
        log.exception("Ocurrió un error: %s", str(e))


# Llamada a la función para probar el logging
if __name__ == "__main__":
    test_logging()
