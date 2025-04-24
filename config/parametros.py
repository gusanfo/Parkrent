"""
Módulo: config/parametros.py
Descripción: archivo que contiene todas las avriables que se van a utilziar en el proyecto
Autor: Gustavo Sandoval
Fecha: 2025-04-22
"""
UTF8 = "utf-8"
PASSWORRD_ES = "contrasenia"
PASSWORD_EN = "password"
DB_CONECCTION_ERROR = "Error de conexión a la DB"
EMAIL_EN = "email"
EMAIL_ES = "correo"
MESSAGE = "mensaje"
SUCCESSFUL_USER = "usuario creado exitosamente!"
SUCCESSFUL_LOGIN = "login Correcto!"
EMAIL_DONT_EXIST = "el correo no existe por favor cree una cuenta"
INVALID_PASSWORD = "la contraseña es incorrecta"
EMAIL_EXIST = "este correo ya existe, por favor verificar"
USER_TYPE = "tipo"
NAME_ES = "nombre"
LASTNAME_ES = "apellido"
USER_ID = "id_usuario"
OWNER = "duenio"
PLACE = "ubicacion"
ADDRES = "direccion"
LONG = "largo"
WIDTH = "ancho"
COUNTRY = "pais"
STATE = "estado"
COUNTRY_INI = "P"
STATE_INI = "D"
CITY_INI = "C"
COUNTRIES_EN = "countries"
CHILD_LOC = "child_locations"
TYPE = "type"
PARENT_ID = "parent_id"

#paths para las apis
PATH_NEW_USER = "/crearusuario/"
PATH_LOGIN = "/login/"
#sqls
SQL1 = """
INSERT INTO usuarios (nombre, apellido, correo, contrasenia)
VALUES (%(username)s, %(lastname)s, %(email)s, %(password)s)
"""
SQL2 = "SELECT id_usuario from usuarios where correo = %(email)s"
SQL3 = """INSERT INTO usuario_tipo (id_tipo_usuario , id_usuario)
VALUES (%(userType)s, %(userId)s)
"""
SQL4 = "SELECT contrasenia from usuarios where correo = %(email)s"
SQL5 = """INSERT INTO parqueaderos (dueño, id_ubicacion, direccion, largo, ancho)
VALUES (%(duenio)s, %(ubicacion)s, %(direccion)s, %(largo)s, %(ancho)s)
"""
SQL_PLACE = {
    'countries': "SELECT id_lugar, nombre_lugar FROM lugar WHERE tipo_ubicacion = %(type)s",
    'child_locations': """
        SELECT id_lugar, nombre_lugar 
        FROM lugar 
        WHERE tipo_ubicacion = %(type)s 
        AND id_ubicacion_padre = %(parent_id)s
    """
}

