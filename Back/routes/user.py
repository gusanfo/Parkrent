"""
Módulo: routes/user.py
Descripción: donde se tendra todo el manejo de los usuarios
Autor: Gustavo Sandoval
Fecha: 2025-05-30
"""


from config.parametros import *
from encrypt.encryptPass import encrypt
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

async def updateUserInfo(connection,
                         userId: int,
                         userName: str,
                         lastName: str,
                         password: str,
                         cellphone: str
                         ):
    """actualiza la informacion del usuario
    Args:
        connection: conexion a la base de datos que este abierta.
        userId (int): identificador del usuario
        userName (str): nombre de usuario
        lastName (str): apellido del usuario
        password (str): contraseña del usuario
        cellphone (str): celular del usuario
    Returns:
        dict: diccionario con la informacion del usuario actualizado
    """
    params = {
        USER_ID_EN: userId,
        USER_NAME: userName,
        LASTNAME_EN: lastName,
        CELLPHONE: cellphone
    }

    # Construir el SQL dinámicamente
    if password != '':
        encryptPassword = encrypt(password)
        sql = SQL_UPDATE_USER_INFO1
        params[PASSWORD_EN] = encryptPassword
    else:
        sql = SQL_UPDATE_USER_INFO2
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        connection.commit()
    return {'status': 'success',
            'message': f'Usuario {userId} actualizado correctamente'}