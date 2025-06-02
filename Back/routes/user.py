"""
Módulo: routes/user.py
Descripción: donde se tendra todo el manejo de los usuarios
Autor: Gustavo Sandoval
Fecha: 2025-05-30
"""


from config.parametros import *
import json
from services.fileService import savePhotosToDisk, deletePhotos
from fastapi import HTTPException, status