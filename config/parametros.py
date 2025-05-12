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
USER_TYPE = "tipo"
NAME_ES = "nombre"
USER_NAME = "username"
LASTNAME_ES = "apellido"
LASTNAME_EN = "lastname"
USER_ID = "id_usuario"
OWNER = "owner"
PLACE = "place"
ADDRESS = "address"
LONG = "long"
WIDTH = "width"
PRICE = "price"
COUNTRY = "pais"
STATE = "estado"
COUNTRY_INI = "P"
STATE_INI = "D"
CITY_INI = "C"
COUNTRIES_EN = "countries"
CHILD_LOC = "child_locations"
TYPE = "type"
PARENT_ID = "parent_id"
USER_ID_EN = "userId"
USER_TYPE_EN = "userType"
PHOTO = "photo"
PHOTOS_PARKING_DIR = "upload/fotos/parqueaderos"
PHOTOS_UDER_DIR = "upload/fotos/usuarios"
BYID = "ById"
BYOWNER = "ByOwner"
PARKING = "parking"
PHOTOS = "fotos"

#mensaje
MESSAGE = "mensaje"
SUCCESSFUL_USER = "usuario creado exitosamente!"
SUCCESSFUL_LOGIN = "login Correcto!"
EMAIL_DONT_EXIST = "el correo no existe por favor cree una cuenta"
INVALID_PASSWORD = "la contraseña es incorrecta"
EMAIL_EXIST = "este correo ya existe, por favor verificar"
SUCCESSFUL_PARKING = "parqueadero agregado de forma exitosa"
BAD_IMAGES = "Solo se permiten imágenes JPG/PNG"

#paths para las apis
PATH_NEW_USER = "/crearusuario/"
PATH_LOGIN = "/login.php/"
PATH_CITIES = "/cities.php/"
PATH_STATES = "/states.php/"
PATH_COUNTRIES = "/countries.php/"
PATH_NEW_PARKING = "/create_parking.php/"
PATH_GET_PARKING = "/get_parking.php/"
PATH_GET_PARKING_OWNER = "/get_parkings_by_owner.php/"
PATH_DELETE_PARKING = "/delete_parking.php/{ownwer_id}/{parking_id}/"
PATH_UPDATE_PARKING = "/UPDATE_parking.php/"

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
SQL5 = """INSERT INTO parqueaderos (dueño, id_ubicacion, direccion, largo, ancho, costo_dia, fotos)
VALUES (%(owner)s, %(place)s, %(address)s, %(long)s, %(width)s, %(price)s, %(photo)s)
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
SQL_PARKINGS = {
    'ById': """select direccion, largo, ancho, costo_dia, fotos
                from parqueaderos where id_parqueadero = %(parking)s""",
    'ByOwner': """SELECT id_parqueadero, id_ubicacion, direccion, largo, ancho, costo_dia, fotos 
                FROM parqueaderos 
                WHERE dueño = %(owner)s"""
}
SQL_DELETE_PARKING = """
DELETE FROM parqueaderos 
WHERE id_parqueadero = %(parking)s
AND dueño = %(owner)s
"""
SQL_UPDATE_PARKING = """
UPDATE parqueaderos 
SET 
    id_ubicacion = %(place)s,
    direccion = %(address)s,
    largo = %(long)s,
    ancho = %(width)s,
    costo_dia = %(price)s,
    fotos = %(photo)s
WHERE 
    id_parqueadero = %(parking)s 
    AND dueño = %(owner)s
"""
SQL_PHOTOS_BY_OWNER_PARKING = "SELECT fotos FROM parqueaderos WHERE id_parqueadero = %s AND dueño = %s"