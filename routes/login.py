from encrypt.encryptPass import veryfyPass
from config.parametros import *

def login(password, email, connection) -> tuple[bool, bool]:
	"""permite saber si un usuario existe
    Args:
		password: contrasenia del usuario
		emial: correo del usuario
        connection: conexion a la base de datos que este abierta.
    return
        tuple[bool, bool]: retorna booleano dependiendo si el correo existe y la contraseña cocuerda
    """
	with connection.cursor() as cursor:
		cursor.execute(SQL4, 
				 {
            EMAIL_EN: email}
		)
		hPass = cursor.fetchone()
	if hPass is None:
		return False, False
	else:
		loginRes = veryfyPass(password, hPass[PASSWORRD_ES])
		return True, loginRes