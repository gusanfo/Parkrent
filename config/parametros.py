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
USER_ID = "id_usuario"
#paths para las apis
PATH_NEW_USER = "/crearusuario/"
PATH_LOGIN = "/login/"
#sqls
SQL1 = """
INSERT INTO usuarios (nombre_usuario, correo_usuario, contrasenia)
VALUES (%s, %s, %s)
"""
SQL2 = "SELECT id_usuario from usuarios where correo_usuario = %s"
SQL3 = """INSERT INTO tipousuario_usuarios (tipoUsuario_id_tipo_usuario , usuarios_id_tipo_usuario)
VALUES (%s, %s)
"""
SQL4 = "SELECT contrasenia from usuarios where correo_usuario = %s"