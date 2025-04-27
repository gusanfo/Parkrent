from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from database import get_db_connection
from routes.createUser import createUser, getUserId
from routes.place import *
from routes.login import login
from routes.parking import *
from config.parametros import *
from typing import List
import pymysql

app = FastAPI(max_upload_size=50_000_000)

# Modelo de datos para el request (usando diccionario, luego puedes usar Pydantic)

@app.get("/prueba.php/")
def pruebas(idOwner: int = Query(..., alias="owner")):
    connection = get_db_connection()
    fotos = getParkingByOwner(connection, idOwner)
    return {"parqueaderos": fotos}




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
#Se podria ajustar a post
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

@app.get(PATH_COUNTRIES)
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

@app.get(PATH_STATES)
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

@app.get(PATH_CITIES)
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

@app.get(PATH_GET_PARKING)
def getParking(idParking: int = Query(..., alias="parqueadero")):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        parkings = getParkingByID(connection, idParking)
        if not parkings:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron Datos para el parqueadero {idParking}"
            )
        return parkings
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()

@app.get(PATH_GET_PARKING_OWNER)
def getPArkings(idOwner: int = Query(..., alias="owner")):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        parkings = getParkingByOwner(connection, idOwner)
        if not parkings:
            raise HTTPException(
                status_code=404,
                detail=f"El usuario {idOwner} no posee parqueaderos"
            )
        return {"parqueaderos": parkings}
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()    


@app.post(PATH_NEW_PARKING)
async def createParking(owner: int = Form(...), place: int = Form(...), address: str = Form(...),
    long: float = Form(...), width: float = Form(...), price: float = Form(...),
    files: List[UploadFile] = File(...)):

    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        if not files:
            raise HTTPException(
                status_code=400,
                detail="Debe subir al menos una foto del parqueadero"
            )
        parking_data = {
            OWNER: owner,
            PLACE: place,
            ADDRESS: address,
            LONG: long,
            WIDTH: width,
            PRICE: price
        }
        await addParking(connection, parking_data, files)
        return {MESSAGE: SUCCESSFUL_PARKING}    
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()