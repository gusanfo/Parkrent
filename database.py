"""
Módulo: database.py
Descripción: Maneja la conexion con la base de datos 
Autor: Gustavo Sandoval
Fecha: 2025-04-22
Dependencias:
    - pymysql (para conexion con bd mysql)
    - dotenv (para tomar valores de variables de ambiente)
Ejemplo de uso:
    >>> from database import get_db_connection
    >>> get_db_connection()
"""

import pymysql
from pymysql.err import OperationalError
from dotenv import load_dotenv
import os

# Carga variables del archivo .env
load_dotenv()

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),      # Ej: "localhost"
            user=os.getenv("DB_USER"),      # Ej: "root"
            password=os.getenv("DB_PASSWORD"), # Tu contraseña
            database=os.getenv("DB_NAME"),  # Ej: "parqueaderos_db"
            port=int(os.getenv("DB_PORT")), # MySQL default: 3306
            cursorclass=pymysql.cursors.DictCursor
        )
        print("¡Conexión a MySQL exitosa!")
        return connection
    except OperationalError as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
  