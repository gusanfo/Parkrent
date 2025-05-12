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
from fastapi import UploadFile, HTTPException, status

"metodos para añadir parqueadero, editarparqueadero, borrar parqueadero, hacer una reserva, ver todas las reservas"

async def update_parking( connection,
    parkingId: int,
    ownerId: int,
    data: dict,
    filesToDelete = None,
    newFiles = None
):
    """Actualiza un parqueadero con gestión avanzada de fotos
    Args:
        parkingId: ID del parqueadero
        ownerId: ID del dueño (para verificación)
        data: Diccionario con nuevos datos
        files_to_delete: Lista de nombres de archivos a eliminar
        newFiles: Lista de nuevos archivos a subir
    """
    with connection.cursor() as cursor:
        # 1. Verificar propiedad y obtener fotos actuales
        cursor.execute(SQL_PHOTOS_BY_OWNER_PARKING,
            (parkingId, ownerId)
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parqueadero no encontrado o no pertenece al usuario"
            )
        
        current_photos = json.loads(result[PHOTOS]) if result[PHOTOS] else []
        
        # 2. Eliminar fotos especificadas
        updated_photos = current_photos.copy()
        if filesToDelete:
            # Eliminar del filesystem
            await delete_parking_photos(filesToDelete)
            for filename in filesToDelete:
                # Eliminar de la lista
                updated_photos = [p for p in updated_photos if p != filename]
        
        # 3. Añadir nuevas fotos
        if newFiles:
            new_photo_paths = await save_photos_to_disk(newFiles, ownerId)
            updated_photos.extend(new_photo_paths)
        
        # 4. Actualizar en base de datos
        cursor.execute(SQL_UPDATE_PARKING, {
            PARKING: parkingId,
            OWNER: ownerId,
            PLACE: data.get(PLACE),
            ADDRESS: data.get(ADDRESS),
            LONG: data.get(LONG),
            WIDTH: data.get(WIDTH),
            PRICE: data.get(PRICE),
            PHOTO: json.dumps(updated_photos)
        })
        
        connection.commit()
        
        return {
            "status": "success",
            "message": "Parqueadero actualizado",
            "deleted_photos": filesToDelete or [],
            "new_photos": [f.filename for f in newFiles] if newFiles else []
        }


async def delete_parking(connection, parkingId: int, idOwner: int):
    """Elimina un parqueadero por su ID y dueño
    Args:
        parking_id (int): ID del parqueadero a eliminar
        
    Returns:
        dict: Mensaje de éxito o error
    """
    with connection.cursor() as cursor:
        photos = getParkingByID(connection, parkingId)
        if not photos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parqueadero con ID {parkingId} no encontrado"
            )
        cursor.execute(SQL_DELETE_PARKING, {PARKING: parkingId,
                                            OWNER: idOwner})
        await delete_parking_photos(eval(photos[PHOTOS]))
        connection.commit()
        print(photos)
        
        return {
            "status": "success",
            "message": f"Parqueadero {parkingId} eliminado correctamente"
        }


def getParkingByOwner(connection, idOwner: int):
    """trae los datos de los parqueaderos de un dueño
    Args:
        connection: conexion a la base de datos que este abierta.
        idOwner (int): identificador del parqueadero
    Returns:
        dict: diccionario con la informacion del parqueadero
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_PARKINGS[BYOWNER], {
            OWNER: idOwner
            }
        )
        res = cursor.fetchall()
    return res

def getParkingByID(connection, idParking: int):
    """trae los datos de un parqueadero
    Args:
        connection: conexion a la base de datos que este abierta.
        idParking (int): identificador del parqueadero
    Returns:
        dict: diccionario con la informacion del parqueadero
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_PARKINGS[BYID], {
            PARKING: idParking
            }
        )
        res = cursor.fetchone()
    return res

async def addParking(connection, data:dict, photosList):
    """crea un parqueadero
    Args:
        connection: conexion a la base de datos que este abierta.
        data (dict): diccionario con los datos necesarios
        photoList: es la lista con los archivos adjuntos
    Ejemplo:
        >>> connection = get_conection(()
        >>> data = {"owner":1, "place": 1, "address": "avenida americas..", "long": 7,2, "width": 4, "price": 1500,
                    "photo": ["parqueadero1/photo1.png"]}
        >>> createUser(connection, data)
    """
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
        if photo.size==0: return[]
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

async def delete_parking_photos(parkingPhotos: list):
    """Elimina las fotos de un parqueadero"""
    try:
        print(parkingPhotos)
        print(type(parkingPhotos))
        for photoDir in parkingPhotos:
            print(photoDir)
            if os.path.exists(photoDir):
                 os.remove(photoDir)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar fotos: {str(e)}"
        )
