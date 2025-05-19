"""
Módulo: services/fileService.py
Descripción: metodos utilitarios
Autor: Gustavo Sandoval
Fecha: 2025-05-18
"""

from config.parametros import *
from utils.fileUtils import secureFilename
import os
import shutil
from fastapi import UploadFile, status, HTTPException


async def savePhotosToDisk(photos: list[UploadFile], owner_id: int, pathPhotos: str):
    """Guarda fotos en el sistema de archivos y retorna rutas relativas
    
    Args:
        photos: Lista de archivos subidos
        owner_id: ID del dueño para crear estructura de directorios
        
    Returns:
        List[str]: Lista de rutas relativas de las fotos guardadas
    """
    saved_files = []
    upload_dir = f"{pathPhotos}/{owner_id}"
    
    # Crear directorio si no existe
    os.makedirs(upload_dir, exist_ok=True)
    
    for photo in photos:
        if photo.size==0: return[]
        try:
            # Validar extensión del archivo
            if not photo.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValueError(BAD_IMAGES)
                
            # Generar nombre seguro para el archivo
            safe_filename = await secureFilename(photo.filename)
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


async def deletePhotos(Photos: list):
    """Elimina las fotos"""
    try:
        for photoDir in Photos:
            if os.path.exists(photoDir):
                 os.remove(photoDir)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar fotos: {str(e)}"
        )
