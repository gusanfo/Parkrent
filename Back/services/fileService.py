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
from PIL import Image
import io

async def resize_image(image_data: bytes) -> bytes:
    """
    Redimensiona una imagen manteniendo el aspect ratio y optimiza su tamaño
    
    Args:
        image_data: Bytes de la imagen original
        
    Returns:
        bytes: Bytes de la imagen redimensionada y optimizada
    """
    try:
        # Abrir imagen desde bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Redimensionar manteniendo aspect ratio
        image.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
        
        # Optimizar y convertir a bytes
        output = io.BytesIO()
        
        # Guardar en formato adecuado
        if image.format == 'PNG':
            image.save(output, format='PNG', optimize=True)
        else:
            image.save(output, format='JPEG', quality=QUALITY, optimize=True)
        
        return output.getvalue()
    
    except Exception as e:
        raise ValueError(f"Error al procesar imagen: {str(e)}")



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

            # Leer contenido de la imagen
            image_data = await photo.read()
            # Redimensionar y optimizar imagen
            optimized_image = await resize_image(image_data)
            
            # Guardar archivo
            with open(file_path, "wb") as buffer:
                buffer.write(optimized_image)
            # Verificar si el archivo se guardó correctamente
            if not os.path.exists(file_path):
                raise ValueError(f"Error al guardar la imagen: {photo.filename}")
            
            # Guardar ruta relativa
            saved_files.append(file_path)
            
        except Exception as e:
            # Si hay error con una foto, borrar las que ya se subieron
            for file in saved_files:
                try:
                    os.remove(file)
                except:
                    pass
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al procesar imágenes: {str(e)}"
            )
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
