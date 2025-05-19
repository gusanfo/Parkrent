"""
Módulo: utils/fileUtils.py
Descripción: metodos utilitarios
Autor: Gustavo Sandoval
Fecha: 2025-05-18
"""

import re
import unicodedata
from pathlib import Path
from config.parametros import *


async def secureFilename(filename: str, max_length: int = 255) -> str:
    """Sanitiza el nombre de archivo para evitar inyecciones
    Args:
        filename: Nombre original del archivo
    Returns:
        str: Nombre seguro para usar en sistema de archivos
    """
    # Normalizar caracteres Unicode (ej: á → a)
    filename = unicodedata.normalize(NFKD, filename).encode(ASCII, 'ignore').decode(ASCII)
    
    # Eliminar caracteres no permitidos (conserva letras, números, guiones, puntos y espacios)
    filename = re.sub(r'[^\w\s\-_.]', '', filename.strip())
    
    # Reemplazar espacios y múltiples guiones/puntos
    filename = re.sub(r'[\s]+', '_', filename)
    filename = re.sub(r'[\-_.]+', '', filename)
    # Limpiar extremos
    filename = filename.strip('.-_')
    
    # Truncar si es necesario
    if len(filename) > max_length:
        name, ext = Path(filename).stem, Path(filename).suffix
        truncate_at = max_length - len(ext) - 1
        filename = f"{name[:truncate_at]}{ext}"
    
    # Validación final
    if not filename or filename in ('.', '..'):
        raise ValueError("Nombre de archivo resultante no válido")
    
    return filename.lower()