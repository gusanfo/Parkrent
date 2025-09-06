"""
Módulo: config/parametros.py
Descripción: archivo que contiene todas las avriables que se van a utilziar en el proyecto
Autor: Gustavo Sandoval
Fecha: 2025-04-22
"""
NFKD = "NFKD"
UTF8 = "utf-8"
ASCII = "ascii"
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
CELLPHONE = "cellphone"
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
CITY = "city"
DAY_SECONDS = 86400 #segundos que tiene un dia
DAY_COST =  "costo_dia"
CLIENT_ID = "id_cliente"
START_DAY = "fecha_inicio"
END_DATE = "fecha_fin"
COST_RESERVATION = "costo"
DESCRIPTION = "description"
DATE_FORMAT = "%Y-%m-%d"
COUNT = "conteo"
FINAL_TIME =" 23:59:59"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
RESERVATION = "reservation"
MAX_WIDTH = 1920  # Ancho máximo en píxeles
MAX_HEIGHT = 1080  # Alto máximo en píxeles
QUALITY = 85 # Calidad de la imagen (0-100, donde 100 es la mejor calidad)

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
PATH_CREATE_RESERVATION = "/new_reservation.php/"
PATH_GET_RESERVATIONS_OWNER = "/get_reservations_by_owner.php/{owner_id}/"
PATH_RESERVATION_BY_CUSTOMER = "/get_reservations_by_customer.php/{client_id}/"
PATH_GET_RANDOM_PARKINGS = "/get_random_parkings.php/"
PATH_OWNER_INFO_BY_PARKING = "/get_owner_info_by_parking.php/{parking_id}/"
PATH_DELETE_RESERVATION = "/delete_reservation.php/{reservation_id}/"
PATH_GET_PARKING_BY_CITY = "/get_parkings_by_city.php/{city}/"
PATH_REGISTER_CLIENT = "/register_client.php/"
PATH_REGISTER_OWNER = "/register_owner.php/"
PATH_UPDATE_USER_INFO = "/update_user_info.php/"

#sqls
SQL1 = """
INSERT INTO usuarios (nombre, apellido, correo, contrasenia, telefono)
VALUES (%(username)s, %(lastname)s, %(email)s, %(password)s, %(cellphone)s)
"""
SQL2 = "SELECT id_usuario from usuarios where correo = %(email)s AND estado = '1'"
SQL_USER_INFO = """
SELECT u.id_usuario, u.nombre, u.apellido, u.foto_perfil, u.telefono, GROUP_CONCAT(tu.tipo_usuario) as tipo_usuario
from usuarios u, usuario_tipo t, tipousuario tu
WHERE u.id_usuario = t.id_usuario
AND t.id_tipo_usuario = tu.id_tipo_usuario
AND correo = %(email)s
GROUP BY u.id_usuario, u.nombre, u.apellido, u.foto_perfil
"""
SQL3 = """INSERT INTO usuario_tipo (id_tipo_usuario , id_usuario)
VALUES (%(userType)s, %(userId)s)
"""
SQL4 = "SELECT contrasenia from usuarios where correo = %(email)s"
SQL5 = """INSERT INTO parqueaderos (dueño, id_ubicacion, direccion, largo, ancho, costo_dia, fotos, descripcion)
VALUES (%(owner)s, %(place)s, %(address)s, %(long)s, %(width)s, %(price)s, %(photo)s, %(description)s)
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
    'ById': """select p.direccion, p.descripcion, p.largo, p.ancho, p.costo_dia, p.fotos, l.nombre_lugar
                from parqueaderos p, lugar l
                where p.id_parqueadero = %(parking)s
                and p.id_ubicacion = l.id_lugar""",
    'ByOwner': """SELECT id_parqueadero, descripcion, id_ubicacion, direccion, largo, ancho, costo_dia, fotos 
                FROM parqueaderos 
                WHERE dueño = %(owner)s
                AND estado = '1'"""
}
SQL_DELETE_PARKING = """
UPDATE parqueaderos 
SET 
   estado = '2'
WHERE 
    id_parqueadero = %(parking)s 
    AND dueño = %(owner)s
"""
SQL_UPDATE_PARKING = """
UPDATE parqueaderos 
SET 
    direccion = %(address)s,
    descripcion = %(description)s,
    largo = %(long)s,
    ancho = %(width)s,
    costo_dia = %(price)s,
    fotos = %(photo)s
WHERE 
    id_parqueadero = %(parking)s 
    AND dueño = %(owner)s
"""
SQL_PHOTOS_BY_OWNER_PARKING = "SELECT fotos FROM parqueaderos WHERE id_parqueadero = %s AND dueño = %s"

SQL_CREATE_RESERVATION = """
INSERT INTO reserva 
(id_cliente, id_parqueadero, fecha_inicio, fecha_fin, costo) 
VALUES 
(%(id_cliente)s, %(parking)s, %(fecha_inicio)s, %(fecha_fin)s, %(costo)s)
"""

SQL_GET_PARKING_PRICE = """
SELECT costo_dia FROM parqueaderos 
WHERE id_parqueadero = %(parking)s
"""

SQL_CHECK_AVAILABILITY = """
SELECT COUNT(*) as conteo FROM reserva 
WHERE id_parqueadero = %(parking)s
AND (
    (fecha_inicio BETWEEN %(fecha_inicio)s AND %(fecha_fin)s)
    OR 
    (fecha_fin BETWEEN %(fecha_inicio)s AND %(fecha_fin)s)
)
AND estado = '1'
"""

SQL_GET_RESERVATION_BY_OWNER = """
select r.estado, r.id_reserva, r.id_parqueadero, r.fecha_inicio, r.fecha_fin, r.costo
	, CONCAT(c.nombre, " ", c.apellido) as 'cliente', p.direccion, p.estado as 'estado_parqueadero', c.telefono as telefono_cliente
    FROM reserva r
        INNER JOIN parqueaderos p
            ON r.id_parqueadero = p.id_parqueadero
        INNER JOIN usuarios c
            ON c.id_usuario = r.id_cliente
        INNER JOIN usuarios u
            ON u.id_usuario = p.dueño
    WHERE u.id_usuario = %(owner)s
    order by r.estado asc, r.fecha_fin desc
"""
SQL_GET_RESERVATION_BY_CUSTOMER = """select r.estado, r.id_reserva, r.id_parqueadero, r.fecha_inicio, r.fecha_fin, r.costo
	,p.direccion, p.estado as 'estado_parqueadero', p.id_parqueadero, CONCAT(d.nombre, " ", d.apellido) as dueño, d.telefono
    FROM reserva r
        INNER JOIN parqueaderos p
            ON r.id_parqueadero = p.id_parqueadero
        INNER JOIN usuarios c
            ON c.id_usuario = r.id_cliente
        INNER JOIN usuarios d
        	ON d.id_usuario = p.dueño
        WHERE c.id_usuario = %(userId)s
        AND r.estado = '1'
        ORDER BY r.fecha_fin DESC
        """

SQL_GET_RAMDOM_PARKING = """
WITH random_parks AS (
    SELECT id_parqueadero 
    FROM parqueaderos 
    WHERE estado = '1'
    ORDER BY RAND()
    LIMIT 18
)
SELECT p.id_parqueadero, p.direccion, p.largo, p.ancho, p.fotos, p.costo_dia, l.nombre_lugar
FROM parqueaderos p
INNER JOIN lugar l ON p.id_ubicacion = l.id_lugar
INNER JOIN random_parks r ON p.id_parqueadero = r.id_parqueadero
"""

SQL_GET_RESERVATION_BY_PARKING = """select fecha_inicio, fecha_fin
	from reserva 
    where estado = "1"
    and fecha_fin > CURRENT_DATE-1
    and id_parqueadero = %(parking)s
"""

SQL_GET_OWNER_INFO_BY_PARKING = """SELECT 
CONCAT(u.nombre, " ", u.apellido) as dueño, u.telefono, p.direccion 
FROM `parqueaderos` p, usuarios u
where u.id_usuario = p.dueño
and p.id_parqueadero = %(parking)s
"""

SQL_GET_RESERVATION_BY_ID = """SELECT r.id_reserva, r.fecha_inicio,r.fecha_fin, CONCAT(c.nombre," ", c.apellido ) as cliente, c.correo as correoCliente,
    p.direccion, CONCAT(d.nombre, " ", d.apellido) as owner, d.telefono, d.correo as correoOwner
FROM reserva r
INNER JOIN usuarios c ON c.id_usuario = r.id_cliente
INNER JOIN parqueaderos p ON p.id_parqueadero = r.id_parqueadero
INNER JOIN usuarios d ON p.dueño = d.id_usuario
WHERE r.id_reserva = %(reservation)s"""

SQL_DELETE_RESERVATION = """
UPDATE reserva
SET
   estado = '2'
WHERE id_reserva = %(reservation)s 
"""

SQL_GET_PARKING_BY_CITY = """SELECT p.id_parqueadero, p.direccion, p.largo, p.ancho, p.fotos, p.costo_dia, l.nombre_lugar
FROM parqueaderos p
INNER JOIN lugar l ON p.id_ubicacion = l.id_lugar
WHERE l.id_lugar = %(city)s
AND p.estado = '1'
"""

SQL_REGISTER_CLIENTOWNER = """INSERT INTO usuario_tipo (id_tipo_usuario, id_usuario) 
VALUES (%(userType)s, %(userId)s)
"""

SQL_UPDATE_USER_INFO1 = """UPDATE usuarios
SET 
    nombre = %(username)s,
    apellido = %(lastname)s,
    contrasenia = %(password)s,
    telefono = %(cellphone)s 
WHERE id_usuario = %(userId)s
"""
SQL_UPDATE_USER_INFO2 = """UPDATE usuarios
SET 
    nombre = %(username)s,
    apellido = %(lastname)s,
    telefono = %(cellphone)s 
WHERE id_usuario = %(userId)s
"""

HTML_REGISTER = """
<!DOCTYPE html>
<html>
<head>
    <title>Bienvenido</title>
</head>
<body>
    <h1>¡Bienvenido, {username}  {lastname}!</h1>
    <p>Gracias por registrarte en nuestra plataforma, desde ahora podrás disfrutar de nuestros servicios.</p>

    <p> Nota: no responder a este correo, este correo es solo informativo</p>
    <p>Saludos,</p>
    <p>El equipo de Parkrent</p>

    <h3> PARKRENT</h3>
</body>
</html>
"""

HTML_RESERVATION_CONFIRMATION_CUSTOMER = """<!DOCTYPE html>
<html>
<head>
    <title>RESERVATION</title>
</head>
<body>
    <h1>Reserva confirmada</h1>
    <p>Gracias por confiar en nosotros para tu reserva.</p>
    <p>Detalles de la reserva:</p>
    <ul>
        <li>ID de reserva: {reservation_id}</li>
        <li>Fecha de inicio: {startDate}</li>
        <li>Fecha de fin: {endDate}</li>
        <li>Dueño: {owner}</li>
        <li>Dirección: {address}</li>
        <li>Teléfono de contacto: {phone}</li>
    </ul>

    <p> Nota: no responder a este correo, este correo es solo informativo</p>
    <p>Saludos,</p>
    <p>El equipo de Parkrent</p>

    <h3> PARKRENT</h3>
</body>
</html>"""


HTML_RESERVATION_CONFIRMATION_OWNER = """<!DOCTYPE html>
<html>
<head>
    <title>RESERVATION</title>
</head>
<body>
    <h1>Reserva confirmada</h1>
    <p>Tu parqueadero ha sido reservado</p>
    <p>Detalles de la reserva:</p>
    <ul>
        <li>ID de reserva: {reservation_id}</li>
        <li>Fecha de inicio: {startDate}</li>
        <li>Fecha de fin: {endDate}</li>
        <li>Cliente: {customer}</li>
        <li>Parqueadero reservado: {address}</li>
    </ul>

    <p> Nota: no responder a este correo, este correo es solo informativo</p>
    <p>Saludos,</p>
    <p>El equipo de Parkrent</p>

    <h3> PARKRENT</h3>
</body>
</html>"""