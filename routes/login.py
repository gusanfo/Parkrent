from encrypt.encryptPass import veryfyPass
from config.parametros import *

def login(password, email, connection):
	with connection.cursor() as cursor:
		cursor.execute(SQL4, 
				 {
            "email": email}
		)
		hPass = cursor.fetchone()
	if hPass is None:
		return False, False
	else:
		loginRes = veryfyPass(password, hPass[PASSWORRD_ES])
		return True, loginRes