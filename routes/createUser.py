"""
Módulo: routes/createUser.py
Descripción: permite la creacion del usuario 
Autor: Gustavo Sandoval
Fecha: 2025-04-22
Dependencias:
    - encryptPass (para hash de contraseñas)
"""

from encrypt.encryptPass import encrypt
from config.parametros import *

def createUser(connection, user:dict):
    """valida que la ontraseña sea aceptada comparada contr un hash.
    Args:
        connection: conexion a la base de datos que este abierta.
        user (dict): diccionario con los datos necesarios 
    Ejemplo:
        >>> connection = get_conection(()
        >>> user = {"nombre": "prueba", "correo": "correo@correo.com"}
        >>> createUser(connection, user)
    """
    hashPass = encrypt(user[PASSWORRD_ES])
    with connection.cursor() as cursor:
        cursor.execute(SQL1, (
            user[NAME_ES],
            user[EMAIL_ES],
            hashPass        
        ))
    connection.commit()
    userType(user, connection)
    

def getUserId(email:str, connection):
    """valida el correo del usuario y si exise retornar su user_id.
    Args:
        email(str): string del correo electronico
        connection: conexion a la base de datos que este abierta.
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL2, (email))
        userId = cursor.fetchone()
    return userId


def userType(user:dict, connection):
    """crea un registro de usuario tipo de usuario.
    Args:
        user (dict): diccionario con los datos necesarios 
        connection: conexion a la base de datos que este abierta.
    """
    userId = getUserId(user[EMAIL_ES], connection)[USER_ID]
    userType = user[USER_TYPE]
    with connection.cursor() as cursor:
        cursor.execute(SQL3, (userType, userId))
    connection.commit()