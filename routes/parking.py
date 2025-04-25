"""
Módulo: routes/parking.py
Descripción: donde se tendra todo el manejo de los parqueaderos 
Autor: Gustavo Sandoval
Fecha: 2025-04-23
Dependencias:
    - encryptPass (para hash de contraseñas)
"""

from config.parametros import *
import json
import os
import shutil
from fastapi import UploadFile, HTTPException

"metodos para añadir parqueadero, editarparqueadero, borrar parqueadero, hacer una reserva, ver todas las reservas"

async def addParking(connection, data:dict, photosList):
    """crea un parqueadero
    Args:
        connection: conexion a la base de datos que este abierta.
        data (dict): diccionario con los datos necesarios 
    Ejemplo:
        >>> connection = get_conection(()
        >>> data = {"owner":1, "place": 1, "address": "avenida americas..", "long": 7,2, "width": 4, "price": 1500,
                    "photo": ["parqueadero1/photo1.png"]}
        >>> createUser(connection, data)
    """
    print("AQUI")
    print(data)
    photos = await save_photos_to_disk(photosList, data[OWNER])
    with connection.cursor() as cursor:
        cursor.execute(SQL5, {
            OWNER: data[OWNER],
            PLACE: data[PLACE],
            ADDRESS: data[ADDRESS],
            LONG: data[LONG],
            WIDTH: data[WIDTH],
            PRICE: data[PRICE],
            PHOTO: json.dumps(photos)
            }        
        )
    connection.commit()

async def save_photos_to_disk(photos: list[UploadFile], owner_id: int):
    """Guarda fotos en el sistema de archivos y retorna rutas relativas
    
    Args:
        photos: Lista de archivos subidos
        owner_id: ID del dueño para crear estructura de directorios
        
    Returns:
        List[str]: Lista de rutas relativas de las fotos guardadas
    """
    saved_files = []
    upload_dir = f"{PHOTOS_PARKING_DIR}/{owner_id}"
    
    # Crear directorio si no existe
    os.makedirs(upload_dir, exist_ok=True)
    
    for photo in photos:
        try:
            # Validar extensión del archivo
            if not photo.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValueError(BAD_IMAGES)
                
            # Generar nombre seguro para el archivo
            safe_filename = await secure_filename(photo.filename)
            file_path = f"{upload_dir}/{safe_filename}"
            
            # Guardar archivo
            with open(file_path, "wb") as buffer:
                # Para UploadFile de FastAPI necesitamos await si es async
                if hasattr(photo.file, 'read'):
                    buffer.write(await photo.read())
                else:
                    shutil.copyfileobj(photo.file, buffer)
            
            # Guardar ruta relativa
            saved_files.append(file_path)
            
        except Exception as e:
            # Si hay error con una foto, borrar las que ya se subieron
            for file in saved_files:
                try:
                    os.remove(file)
                except:
                    pass
            raise 
    return saved_files

async def secure_filename(filename: str) -> str:
    """Sanitiza el nombre de archivo para evitar inyecciones
    Args:
        filename: Nombre original del archivo
    Returns:
        str: Nombre seguro para usar en sistema de archivos
    """
    # Implementación básica - puedes mejorarla
    keepchars = ('-', '_', '.')
    return ''.join(c for c in filename if c.isalnum() or c in keepchars).rstrip()