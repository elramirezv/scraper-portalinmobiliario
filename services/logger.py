import logging

# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un manejador de consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Crear un formato para los logs
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Agregar el manejador al logger
logger.addHandler(console_handler)
