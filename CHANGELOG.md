# v 0.0.7
* se avanza con el frontEnd para crear usuario
* se avanza con la vista frontEnd para los usuarios que son propietarios de parqueaderos, donde esta la lista de parqueaderos, agregar parqueaderos y ver reservas
* Se puede editar el parqueadero y cambiar sus datos basicos
* se puede eliminar un parqueadero
* se ajusta la base de datos para que tenga triggers cuando se "borren" usuarios, parqueaderos o se cancele una reserva
* Se genera api para traer las reservas que tenga un owner

# v 0.0.6
* se crea en el backend una metodo para traer la informacion basica del usuario
* se crea la estructura basica del frontend
* se genera la pagina inicial de frontend
* se agregan los css del login y un css de stilos
* se agrega el javascript del login y del main
* se agrega el html para realziar el login y se conecta con el backend

# v 0.0.5
* Se modifica la estructura del proyecto, se divide en back y front
* se crea la clase reservation.py
* en la clase reservation.py se genera el metodo para realizar una reserva, el cual tiene  manejo de excepciones
* se genera el api para generar una reserva
* se crea la clase fileUtils y fileService para manejar la logica de guardado de imagenes y archivos

# v 0.0.4
* se modifican los metodos de la classe parking.py
* se agregan dos api, una para eliminar parqueaderoy otra para actualizar parqueadero
* la api de elimnar parqueadero elimina el parqueadero de la base de datos y elimina las fotos del sistema de archivos
* El api de editar parqueadero permite elimar fotos, añadir fotos, y editarlos datos del parqueadero, sino se queiren agregar mas fotos ni eliminar esos parametros no se envian

# v 0.0.3
* se modifican los metodos de la classe parking.py
* se genera una nueva api para agregar parqueaderos, y añadir fotos
* permite que el parqueadero creado se genere sin fotos
* Se crean apis, una para traer la informacion de parqueaderopor id, y otra para traer parqueaderos por dueño

# v 0.0.2
* Actualizacion de la bd
* actualizacion de sqls
* creacion clases place.py y parking.py
* se generan 3 nuevos api, para traer paises, estados o departamentos y ciudades

# v 0.0.1
* version inicial del proyecto de renta de parqueaderos
* se tienen los archivos database.py, main.py .env
* se tienen las carpetas routes, encrypt, config
* en la carpeta routes existen los archivos createUder.py, login.py
* en la carpeta encrypt existe el archivo encryptPass.py
* en la carpeta config existe el archivo parametros.py
