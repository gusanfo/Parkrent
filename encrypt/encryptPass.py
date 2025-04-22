"""
Módulo: encrypt/encryptPass.py
Descripción: maneja la encriptacion y verificacion de contraseñas.
Autor: Gustavo Sandoval
Fecha: 2025-04-22
Dependencias:
    - bcrypt (para hashing de contraseñas)
"""
import bcrypt
from config.parametros import *

# Encriptar contraseña

def encrypt(password:str):
    """Genera un hash seguro de una contraseña usando bcrypt.
    Args:
        password (str): Contraseña en texto plano.
    Returns:
        Contraseña hasheada.
    Ejemplo:
        >>> hash = encrypt("mi_contraseña")
        >>> len(hash) > 0
        True
    """
    pas = password.encode(UTF8)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pas, salt)  # Guarda esto en tu DB
    return hashed_password

def veryfyPass(password:str, haspw) -> bool:
    """valida que la ontraseña sea aceptada comparada contr un hash.
    Args:
        password (str): Contraseña en texto plano.
        haspw (bytes): el hash de la contraseña 
    Returns:
        bool: returna si la contraseña concuerda con el hash.
    Ejemplo:
        >>> accept = veryfyPass("mi_contraseña", "y3tgc14bkakdn")
        >>> accept
        False
    """
    if bcrypt.checkpw(password.encode(UTF8), haspw.encode(UTF8)):
        return True
    else:
        return False