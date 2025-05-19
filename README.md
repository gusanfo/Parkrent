# Parkrent
para aplicacion web y movil para rentar parqueaderos

## Para la ejecucion en local del servidor de python se debe realziar de la siguiente forma
* uvicorn main:app --reload;  este codigo iria en la consola de comandos donde desde la carpeta donde se encuentre el archivo main
* para probar cada uno de los apis se debe desde una aplicacion que permita enviar los datos o desde postman

## La estructura que poseer el proyecto
 ```
├── Back
|    ├── .env
|    ├── database.py
|    ├── main.py
|    ├── config
|    |    ├── __init__.py
|    |    ├── parametros.py
|    ├── routes
|    |    ├── __init__.py
|    |    ├── login.py
|    |    ├── createUser.py
|    |    ├── parking.py
|    |    ├── place.py
|    |    ├── reservation.py
|    ├── services/               # Nueva carpeta para lógica de negocio
|    │    ├── __init__.py
|    │    ├── fileService.py    # Clase para manejo de archivos
|    ├── utils/                  # Funciones auxiliares
|    │    ├── __init__.py
|    │    ├── fileUtils.py
|    ├── upload
|    ├── encrypt
|    |    ├── __init__.py
|    |    ├── encryptPass.py
 ``` 