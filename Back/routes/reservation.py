"""
Módulo: routes/reservation.py
Descripción: donde se tendra todo el manejo de las reservas 
Autor: Gustavo Sandoval
Fecha: 2025-05-16
"""

from datetime import datetime, timedelta
from math import ceil
from fastapi import HTTPException, status
from config.parametros import *
from services.emails import sendEmail


"metodos para ver todas las reservas por cliente, por parqueadero por dueño, si se implementa el estado de la reserva en la base de datos un metodo que ejecute cada dia para revisar las fehcas y poner las reservas en un estado especifico"
def calculatedDays(start: datetime, end: datetime) -> int:
    duration = end - start
    total_days = ceil(duration.total_seconds() / DAY_SECONDS)
    return total_days

def calculateCost(start: datetime, end: datetime, price_per_day: float) -> float:
    """Calcula el costo total de la reserva"""
    total_days = calculatedDays(start, end)
    return round(total_days * price_per_day, 3)

async def createReservation(connection,
    clientId: int,
    parkingId: int,
    startDate: datetime,
    enddate: datetime
):
    """Crea una nueva reserva con cálculo automático de costo"""
    
    # Validaciones básicas
    if enddate <= startDate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )
    
    if (enddate - startDate) > timedelta(days=50):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se permiten reservas por más de 50 días"
        )

    with connection.cursor() as cursor:
        # 1. Verificar disponibilidad
        cursor.execute(SQL_CHECK_AVAILABILITY, {
            PARKING: parkingId,
            START_DAY: startDate,
            END_DATE: enddate
        })
        if cursor.fetchone()[COUNT] > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El parqueadero no está disponible en ese horario"
            )
        
        # 2. Obtener precio del parqueadero
        cursor.execute(SQL_GET_PARKING_PRICE, {
            PARKING: parkingId
        })
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parqueadero no encontrado"
            )
        
        price_per_day = result[DAY_COST]
        
        # 3. Calcular costo
        costo = calculateCost(startDate, enddate, price_per_day)
        
        # 4. Crear reserva
        cursor.execute(SQL_CREATE_RESERVATION, {
            CLIENT_ID: clientId,
            PARKING: parkingId,
            START_DAY: startDate,
            END_DATE: enddate,
            COST_RESERVATION: costo
        })
        
        reservation_id = cursor.lastrowid
        connection.commit()
        # 5. enviar correo al cliente
        reservationInfo = await getDataByReservationId(connection, reservation_id)
        await sendEmail(
            to=reservationInfo["correoCliente"],
            subject="Reserva Confirmada",
            body=HTML_RESERVATION_CONFIRMATION_CUSTOMER.format(
                reservation_id=reservation_id,
                startDate=startDate.strftime("%Y-%m-%d %H:%M"),
                endDate=enddate.strftime("%Y-%m-%d %H:%M"),
                address=reservationInfo["direccion"],
                owner=reservationInfo["owner"],
                phone=reservationInfo["telefono"]
            )
        )
        # 6. enviar correo al dueño del parqueadero
        await sendEmail(
            to=reservationInfo["correoOwner"],
            subject="Nueva Reserva Confirmada",
            body=HTML_RESERVATION_CONFIRMATION_OWNER.format(
                reservation_id=reservation_id,
                startDate=startDate.strftime("%Y-%m-%d %H:%M"),
                endDate=enddate.strftime("%Y-%m-%d %H:%M"),
                address=reservationInfo["direccion"],
                customer=reservationInfo["cliente"]
                
            )
        )
        return {
            "status": "success",
            "reservation_id": reservation_id,
            "costo_total": costo,
            "duracion_dias": calculatedDays(startDate, enddate)
        }
    
async def getReservationsByOwner(connection, ownerId: int):
    """
    Obtiene todas las reservas de un propietario
    Args:
        connection: conexión a la base de datos
        clientId: ID del propietario
    Returns:
        list: lista de reservas
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_GET_RESERVATION_BY_OWNER, {
            OWNER: ownerId
        })
        result = cursor.fetchall()
        return result
    
async def getReservationsByClient(connection, clientId: int):
    """
    Obtiene todas las reservas de un cliente
    Args:
        connection: conexión a la base de datos
        clientId: ID del cliente
    Returns:
        list: lista de reservas
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_GET_RESERVATION_BY_CUSTOMER, {
            USER_ID_EN: clientId
        })
        result = cursor.fetchall()
        return result

async def deleteReservation(connection, reservationId: int):
    """
    Elimina una reserva por ID
    Args:
        connection: conexión a la base de datos
        reservationId: ID de la reserva
    Returns:
        dict: estado de la operación
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_DELETE_RESERVATION, {
            RESERVATION: reservationId
        })
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        connection.commit()
        return {"status": "success", "message": "Reserva eliminada correctamente"}
    
async def getDataByReservationId(connection, reservationId: int):
    """
    Obtiene los datos de una reserva por ID
    Args:
        connection: conexión a la base de datos
        reservationId: ID de la reserva
    Returns:
        dict: datos de la reserva
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL_GET_RESERVATION_BY_ID, {
            RESERVATION: reservationId
        })
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        return result