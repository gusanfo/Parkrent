"""
Módulo: routes/place.py
Descripción: donde se traeran los paises, departamentos y ciudades
Autor: Gustavo Sandoval
Fecha: 2025-04-23
Dependencias:
    - database (para realizar conexion a la base de datos)
"""
from config.parametros import *

def fetchLocations(connection, type:str, parentId = None)-> list[dict]:
    """Tae los registros de los lugares dependiendo el tipo
    Args:
        connection: conexion a la base de datos que este abierta.
        type (str): tipo de lugar que se necesita
        parentId: es si el lugar que se busca tiene un padre
    return
        list[dict]: Resultado de la consulta
    """
    with connection.cursor() as cursor:
        if parentId is None:
            cursor.execute(SQL_PLACE[COUNTRIES_EN], {
                TYPE: type
                }
            )
        else:
            cursor.execute(SQL_PLACE[CHILD_LOC], {
                TYPE: type,
                PARENT_ID: parentId
                }
            )
        return cursor.fetchall()
