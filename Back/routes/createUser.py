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
    """crea un registro en usuarios
    Args:
        connection: conexion a la base de datos que este abierta.
        user (dict): diccionario con los datos necesarios 
    Ejemplo:
        >>> connection = get_conection(()
        >>> user = {"nombre": "prueba", "apellido":"perez" ,"correo": "correo@correo.com", "contrasenia": "esta es mi contraenia"}
        >>> createUser(connection, user)
    """
    hashPass = encrypt(user[PASSWORRD_ES])
    with connection.cursor() as cursor:
        cursor.execute(SQL1, {
            USER_NAME: user[NAME_ES],
            LASTNAME_EN: user[LASTNAME_ES],
            EMAIL_EN: user[EMAIL_ES],
            PASSWORD_EN: hashPass,
            CELLPHONE: user[CELLPHONE] if CELLPHONE in user else None,}        
        )
    connection.commit()
    userType(user, connection)
    

def getUserId(email:str, connection)-> dict:
    """valida el correo del usuario y si exise retornar su user_id.
    Args:
        email(str): string del correo electronico
        connection: conexion a la base de datos que este abierta.
    return
        dict: resultado de la consulta
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL2, {
            EMAIL_EN: email})
        userId = cursor.fetchone()
    return userId


def userType(user:dict, connection):
    """crea un registro de usuario tipo de usuario.
    Args:
        user (dict): diccionario con los datos necesarios 
        connection: conexion a la base de datos que este abierta.
    """
    print(getUserId(user[EMAIL_ES], connection))
    userId = getUserId(user[EMAIL_ES], connection)[USER_ID]
    print(user)
    userType = user[USER_TYPE]
    with connection.cursor() as cursor:
        cursor.execute(SQL3, {
            USER_TYPE_EN: userType,
            USER_ID_EN: userId} 
        )
    connection.commit()

async def registerLikeCustomerOwner(user, userType, connection):
    """registra un usuario como cliente o propietario
    Args:
        user: ide del usuario
        userType: tipo de usuario (cliente o propietario)
        connection: conexion a la base de datos que este abierta.
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_REGISTER_CLIENTOWNER, {
            USER_ID_EN: user,
            USER_TYPE_EN: userType
        })
        connection.commit()
    return {MESSAGE: "dueño registrado"} if userType == 2 else {MESSAGE: "cliente registrado"}
