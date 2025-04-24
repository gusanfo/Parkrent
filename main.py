from fastapi import FastAPI, HTTPException, Query
from database import get_db_connection
from routes.createUser import createUser, getUserId
from routes.place import *
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

@app.get("/countries/")
def countries():
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        countries = fetchLocations(connection, COUNTRY_INI)
        if not countries:
            raise HTTPException(status_code=404, detail="No se encontraron países")
        return countries
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()

@app.get("/states/")
def states(countryId: int = Query(..., example=1, description="id del pais", alias="Pais")):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        states = fetchLocations(connection, STATE_INI, countryId)
        if not states:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron estados para el país ID {countryId}"
            )
        return states
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()

@app.get("/cities/")
def cities(stateId: int = Query(..., example=1, description="id del paiestados", alias="Estado")):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        states = fetchLocations(connection, CITY_INI, stateId)
        if not states:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron ciudades para el estado ID {stateId}"
            )
        return states
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()