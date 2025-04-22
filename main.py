from fastapi import FastAPI, HTTPException
from database import get_db_connection
from routes.createUser import createUser, getUserId
from routes.login import login
from config.parametros import *
import pymysql

app = FastAPI()

# Modelo de datos para el request (usando diccionario, luego puedes usar Pydantic)

@app.post(PATH_NEW_USER)
def crearusuario(user: dict):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        userId = getUserId(user[EMAIL_ES], connection)
        if userId is None:
            createUser(connection, user)
            return {MESSAGE: SUCCESSFUL_USER}
        else:
            return {MESSAGE: EMAIL_EXIST}
            
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()

@app.get(PATH_LOGIN)
def loginUser(data: dict):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        rsLogin = login(data[PASSWORD_EN], data[EMAIL_EN], connection)
        match rsLogin:
            case (True,True):
                userId = getUserId(data[EMAIL_EN], connection)[USER_ID]
                return {MESSAGE: SUCCESSFUL_LOGIN, USER_ID: userId}
            case (False,False):
                return {MESSAGE: EMAIL_DONT_EXIST}
            case _:
                return {MESSAGE: INVALID_PASSWORD}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()