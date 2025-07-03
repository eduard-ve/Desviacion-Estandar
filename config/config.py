import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración MySQL
# Las credenciales se cargan de las variables de entorno para mayor seguridad.
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''), 
    'database': os.environ.get('DB_NAME', 'calculadora_estadisticas')
}

# El nombre de la base de datos se obtiene de la configuración principal para evitar redundancia
DATABASE_NAME = DATABASE_CONFIG['database']

# Consulta SQL para crear la tabla de análisis si no existe
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS analisis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset TEXT,
    media DECIMAL(10,4),
    desviacion_estandar DECIMAL(10,4),
    cantidad_datos INT,
    fecha DATETIME,
    tipo_calculo VARCHAR(20)
)
"""
