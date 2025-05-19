from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, Path
from typing import Optional, List
from database import get_db_connection
from routes.createUser import createUser, getUserId
from routes.place import *
from routes.login import login
from routes.parking import *
from routes.reservation import *
from config.parametros import *
from typing import List
from datetime import datetime
import pymysql

app = FastAPI(max_upload_size=60_000_000) #60MB

# Modelo de datos para el request (usando diccionario, luego puedes usar Pydantic)

@app.get("/prueba.php/")
def pruebas(idOwner: int = Query(..., alias="owner")):
    connection = get_db_connection()
    fotos = getParkingByOwner(connection, idOwner)
    return {"parqueaderos": fotos}
#En el metodo de crear usuario modificarlo para agregar fotos y que no solo resiva un json sino un formulario
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

@app.delete(PATH_DELETE_PARKING)
async def delete_parking_endpoint(
        parking_id: int = Path(..., title="ID del parqueadero", gt=0),
        ownwer_id: int = Path(..., title="dueño del parqueadero", gt=0)
):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    try:
        return await deleteParking(connection,parking_id, ownwer_id)
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()

@app.patch(PATH_UPDATE_PARKING)
async def update_parking_endpoint(
    parkingId: int = Form(...),
    ownerId: int = Form(...),
    place: Optional[int] = Form(None),
    address: Optional[str] = Form(None),
    long: Optional[float] = Form(None),
    width: Optional[float] = Form(None),
    price: Optional[float] = Form(None),
    fileToDelete: Optional[str] = Form(None),
    newFiles: Optional[List[UploadFile]] = File(None)
):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    
    try:
        update_data = {
            'place': place,
            'address': address,
            'long': long,
            'width': width,
            'price': price
        }
        print(newFiles)
        print(fileToDelete)
        
        return await updateParking( connection,
            parkingId=parkingId,
            ownerId=ownerId,
            data=update_data,
            filesToDelete=fileToDelete.split(","),
            newFiles=newFiles
        )
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()

@app.post(PATH_CREATE_RESERVATION)
async def make_reservation(
    id_cliente: int = Form(...),
    id_parqueadero: int = Form(...),
    fecha_inicio: str = Form(...),  # Formato: "YYYY-MM-DD"
    fecha_fin: str = Form(...)
):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=DB_CONECCTION_ERROR)
    
    try:
        # Convertir strings a datetime
        start = datetime.strptime(fecha_inicio, DATE_FORMAT)
        end = datetime.strptime(fecha_fin, DATE_FORMAT)
        
        return await createReservation(connection,
            id_cliente,
            id_parqueadero,
            start,
            end
        )
    except pymysql.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error : {e} revisar")
    finally:
        connection.close()
