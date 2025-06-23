"""
Módulo: routes/user.py
Descripción: donde se tendra todo el manejo de los usuarios
Autor: Gustavo Sandoval
Fecha: 2025-05-30
"""


from config.parametros import *
import json
from services.fileService import savePhotosToDisk, deletePhotos
from fastapi import HTTPException, status


async def getOwnerInfoByParking(connection, idParking: int):
    """trae los datos de los parqueaderos de un dueño
    Args:
        connection: conexion a la base de datos que este abierta.
        idOwner (int): identificador del parqueadero
    Returns:
        dict: diccionario con la informacion del parqueadero
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_GET_OWNER_INFO_BY_PARKING, {
            PARKING: idParking
            }
        )
        res = cursor.fetchone()
        print(res)
    return res