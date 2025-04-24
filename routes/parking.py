"""
Módulo: routes/parking.py
Descripción: donde se tendra todo el manejo de los parqueaderos 
Autor: Gustavo Sandoval
Fecha: 2025-04-23
Dependencias:
    - encryptPass (para hash de contraseñas)
"""

from config.parametros import *

"metodos para añadir parqueadero, editarparqueadero, borrar parqueadero, hacer una reserva, ver todas las reservas"

def addParking(connection, data:dict):
    """crea un parqueadero
    Args:
        connection: conexion a la base de datos que este abierta.
        data (dict): diccionario con los datos necesarios 
    Ejemplo:
        >>> connection = get_conection(()
        >>> user = {"dueño":1, "ubicacion": 1, "direccion": "avenida americas..", "largo": 7,2, "ancho": 4}
        >>> createUser(connection, user)
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL5, {
            'dueño': data[OWNER],
            'ubicacion': data[PLACE],
            'direccion': data[ADDRES],
            'largo': data[LONG],
            'ancho': data[WIDTH]
            }        
        )
    connection.commit()
