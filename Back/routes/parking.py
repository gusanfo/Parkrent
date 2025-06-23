"""
Módulo: routes/parking.py
Descripción: donde se tendra todo el manejo de los parqueaderos 
Autor: Gustavo Sandoval
Fecha: 2025-04-23
"""

from config.parametros import *
import json
from services.fileService import savePhotosToDisk, deletePhotos
from fastapi import HTTPException, status


async def updateParking( connection,
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
            await deletePhotos(filesToDelete)
            for filename in filesToDelete:
                # Eliminar de la lista
                updated_photos = [p for p in updated_photos if p != filename]
        
        # 3. Añadir nuevas fotos
        if newFiles:
            pathOwnerParking = str(ownerId) + "/" + str(parkingId)
            new_photo_paths = await savePhotosToDisk(newFiles, pathOwnerParking, PHOTOS_PARKING_DIR)
            updated_photos.extend(new_photo_paths)
        

        # 4. Actualizar en base de datos
        cursor.execute(SQL_UPDATE_PARKING, {
            DESCRIPTION : data.get(DESCRIPTION),
            PARKING: parkingId,
            OWNER: ownerId,
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


async def deleteParking(connection, parkingId: int, idOwner: int):
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
        await deletePhotos(eval(photos[PHOTOS]))
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
        cursor.execute(SQL_GET_RESERVATION_BY_PARKING, {
            PARKING: idParking
        })
        res["reservations"] = cursor.fetchall()
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
                description: "parqueadero en el centro", "photo": ["parqueadero1/photo1.png"]}
        >>> createUser(connection, data)
    """
    photos = []
    print(data)
    with connection.cursor() as cursor:
        cursor.execute(SQL5, {
            DESCRIPTION: data[DESCRIPTION],
            OWNER: data[OWNER],
            PLACE: data[PLACE],
            ADDRESS: data[ADDRESS],
            LONG: data[LONG],
            WIDTH: data[WIDTH],
            PRICE: data[PRICE],
            PHOTO: json.dumps(photos)
            }        
        )
    # obtener el id del parqueadero insertado
    parking_id = cursor.lastrowid
    print(f"Parqueadero creado con ID: {parking_id}")
    connection.commit()
    parking_data = {
        DESCRIPTION: data[DESCRIPTION],
        ADDRESS: data.get(ADDRESS),
        LONG: data.get(LONG),
        WIDTH: data.get(WIDTH),
        PRICE: data.get(PRICE),
    }
    await updateParking(connection, parking_id, data[OWNER], parking_data, None, photosList)


async def getRandomParkings(connection):
    """Obtiene un número aleatorio de parqueaderos
    Args:
        connection: conexión a la base de datos
        limit (int): número máximo de parqueaderos a obtener
    Returns:
        list: lista de diccionarios con los parqueaderos
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_GET_RAMDOM_PARKING)
        res = cursor.fetchall()
    return res if res else []

async def getParkingsByCity(connection, cityId: int):
    """Obtiene parqueaderos por ciudad
    Args:
        connection: conexión a la base de datos
        cityId (int): ID de la ciudad
    Returns:
        list: lista de diccionarios con los parqueaderos
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_GET_PARKING_BY_CITY, {CITY: cityId})
        res = cursor.fetchall()
    return res if res else []