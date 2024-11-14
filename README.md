# Índice

1. [Introducción](#api-restful-flask-con-docker)
2. [Requisitos](#requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Detener los Contenedores](#detener-los-contenedores)
6. [Rutas de la API](#rutas-de-la-api)
    - [Autenticación y Usuarios](#autenticación-y-usuarios)
    - [Confirmación de Email](#confirmación-de-email)
    - [Empresas](#empresas)
    - [Remates](#remates)
    - [Artículos](#artículos)
    - [Pujas](#pujas)
7. [Ejemplos](#ejemplos)
8. [Licencia](#licencia)

---
# API RESTful Flask con Docker 

Este proyecto contiene una API RESTful implementada con Flask, gestionando los siguientes recursos:

- **Usuarios**: Registro, autenticación y gestión de usuarios.
- **Empresas**: Gestión de información de empresas.
- **Remates**: Creación y gestión de remates de artículos.
- **Artículos**: Creación, edición y eliminación de artículos en remates.
- **Pujas**: Realización de pujas en artículos de remates.

El proyecto está compuesto por varios contenedores Docker que interactúan entre sí para proporcionar la funcionalidad completa.

## Requisitos

Este proyecto se ejecuta utilizando Docker y depende de los siguientes servicios:

- **api**: El servidor principal que maneja la lógica de la aplicación.
- **socket**: Para manejar la comunicación en tiempo real (WebSockets).
- **db**: Contenedor de base de datos (por ejemplo, PostgreSQL o MySQL).
- **redis**: Usado para la gestión de tareas asíncronas con Celery y almacenamiento en caché.
- **celery**: Procesamiento de tareas en segundo plano.
- **web**: La interfaz de usuario para interactuar con la aplicación a través de una página web.


## Tecnologías en api

- **Flask**: Framework web para crear la API.
- **SQLAlchemy**: ORM para la interacción con la base de datos.
- **Redis**: Para gestionar la comunicación con los contenedores celery y socket.
- **Docker**: Para guardar en contenedores los servicios.

## Estructura del Proyecto

    /python
    │
    ├── app/
    │   ├── connections/        # Conexión a los diversos servicios (Socket, Celery, Redis y SqlAlchemist)
    │   ├── helpers/            # Archivos que facilitan utilidades diversas (manejo de sesiones, enviar email, validar datos, etc.)
    │   ├── models/             # Definición y acciones sobre los modelos de la base de datos
    │   ├── resources/          # Procesa las peticiones a la API
    │   ├── static/             # Archivo css para la pagina de documentación de la API
    │   ├── template/           # Archivos ``HTML`` encargados de documentar la aplicación 
    │   ├── __init__.py         # Inicialización de la aplicación Flask y enrutamiento
    │   ├── db_config.py        # Archivo que devuelve una ruta legible de a la base de datos
    │   └── endpoint.json       # Archivo json que contiene todas las rutas y los métodos de validación
    ├── config.py               # Configuración de la base de datos
    ├── docker-compose.yml      # Configuración de Docker Compose para levantar los servicios
    ├── Dockerfile              # Archivo para crear el contenedor Docker de la API Flask
    ├── requirements.txt        # Dependencias de Python
    ├── run.py                  # Ejecuta la aplicación
    └── version.txt             # Contiene la ultima version de la imagen 

## Instalación y Configuración

1. **Crear docker-compose**:
    Cree un archivo llamado ``docker-compose.yml`` que contenga:
    ```
    version: '3.3'

    services:
        db:
            image: gastonnicora/remates-sql
            expose:
                - "3306"
            restart: always
            environment:
                MYSQL_ROOT_PASSWORD: root
                MYSQL_USER: user
                MYSQL_PASSWORD: user
                MYSQL_DATABASE: Remates
            volumes:
                - db_data:/var/lib/mysql
            networks:
                - mynetwork 

        web:
            image: gastonnicora/remates-vue
            ports:
                - "80:80"
            restart: always
            depends_on:
                - api
                - socket
            networks:
                - socket
                - conn 

        api:
            image: gastonnicora/remates-python
            restart: always
            environment:
                DB_HOST: db:3306
                DB_USER: user
                DB_PASS: user
                DB_NAME: Remates
                REDIS_HOST: redis
            depends_on:
                - db
                - redis
            ports:
                - "4000:4000"
            networks:
                - mynetwork 
                - conn 
        
        socket:
            image: gastonnicora/remates-socket
            restart: always
            environment:
                REDIS_HOST: redis
            depends_on:
                - api
                - redis
            expose:
                - "4001"
            ports:
              - "4001:4001"
            networks:
                - mynetwork
                - socket 

        celery:
            image: gastonnicora/remates-celery
            restart: always
            depends_on:
                - redis
                - api
            ports:
                - "5555:5555"
            expose:
                - "5000" 
            networks:
                - mynetwork 

        phpmyadmin:
            image: phpmyadmin
            restart: always
            environment:
                PMA_HOST: db
                PMA_PORT: 3306
            ports:
                - "90:80"
            depends_on:
                - db
            networks:
                - mynetwork 

        redis:
            image: redis:7-alpine
            expose:
                - "6379"
            volumes:
                - redis_data:/data
            networks:
                - mynetwork

    networks:
        mynetwork:
        socket:
            driver: bridge 
        conn:
            driver: bridge 

    volumes:
        db_data:
        redis_data: 

    ```

2. **Construye y levanta los contenedores con Docker Compose**:

    Asegúrate de que Docker y Docker Compose estén instalados en tu máquina.

    Ejecuta el siguiente comando para construir y levantar los contenedores necesarios:

    ```bash
    docker-compose up --build 
    ```

    Este comando levantará los siguientes contenedores:

    - **api**: Contenedor que ejecuta la API RESTful.
    - **db**: Contenedor de la base de datos (MySQL).
    - **redis**: Contenedor para el almacenamiento de tareas de Celery y la comunicación entre la API, el WebSocket y Celery
    - **celery**: Contenedor para ejecutar tareas asíncronas.
    - **socket**: Contenedor para gestionar las conexiones WebSocket en tiempo real.
    - **web**: Contenedor con la interfaz de usuario 


3. **Accede a la API**:

    Una vez que los contenedores estén levantados, puedes acceder a la API en la siguiente dirección:

    ```
    http://localhost:5000
    ```
    Las rutas de la API estarán disponibles a través de este servidor.

## Detener los Contenedores
Para detener y eliminar los contenedores en ejecución, ejecuta el siguiente comando:

```bash
docker-compose down
```
Si deseas eliminar también los volúmenes, usa la opción ``-v``:

```bash
docker-compose down -v
```
## Rutas de la API
### Autenticación y Usuarios:

- **<span style="color:#2d2">POST /userCreate</span>**: Crear un nuevo usuario.
  - **Descripción**: Crea y devuelve un usuario.
  - **Explicación**: Se elimina el usuario y el enlace de confirmación después de 24 horas.
  - **Campos requeridos**: `name`, `lastName`, `password`, `repetitionPass`, `email`, `birthdate`.

- **<span style="color:#2d2">POST /login</span>**: Autenticación de usuario (devuelve un token JWT y datos del usuario).
  - **Descripción**: Inicia la sesión de un usuario y devuelve los datos necesarios.
  - **Campos requeridos**: `email`, `password`.

- **<span style="color:#2dd">GET /logout</span>**: Cerrar sesión de un usuario.
  - **Descripción**: Finaliza la sesión del usuario actual.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /users</span>**: Obtener todos los usuarios.
  - **Descripción**: Devuelve la lista de todos los usuarios registrados.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /user/{uuid}</span>**: Obtener un usuario por su UUID.
  - **Descripción**: Devuelve la información de un usuario específico según su identificador único (UUID).
  - **Campos requeridos**: `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d2d">PUT /userUpdate</span>**: Modificar un usuario por su UUID, obtenido de su sesión.
  - **Descripción**: Modifica los datos de un usuario específico (por ejemplo, nombre, apellido, fecha de nacimiento).
  - **Campos requeridos**: `name`, `lastName`, `birthdate`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d2d">PUT /userUpdatePassword</span>**: Modificar la contraseña del usuario.
  - **Descripción**: Permite cambiar la contraseña del usuario.
  - **Campos requeridos**: `oldPassword`, `password`, `repetitionPass`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d22">DELETE /userDelete</span>**: Eliminar al usuario que lo solicito.
  - <span style="color:red">**Requiere sesión iniciada**</span>

### Confirmación de Email:

- **<span style="color:#2dd">GET /confirmEmail/{uuid}</span>**: Confirmación de email.
  - **Descripción**: Confirma el email de un usuario y elimina el enlace de confirmación pendiente de la tabla de confirmaciones.
  - **Campos requeridos**: `uuid`.

- **<span style="color:#2dd">GET /get_confirmEmail/{uuid}</span>**: Obtener una confirmación de email.
  - **Descripción**: Obtiene el estado de la confirmación de un email mediante su `uuid`.
  - **Campos requeridos**: `uuid`.

- **<span style="color:#2dd">GET /confirmEmails</span>**: Lista todas las confirmaciones de email.
  - **Descripción**: Devuelve todas las confirmaciones de email, sin orden específico.

  - **Descripción**: Devuelve una lista de todas las confirmaciones de email, sin un orden específico.
  - <span style="color:red">**Requiere sesión iniciada**</span>

### Empresas:

- **<span style="color:#2d2">POST /companyCreate</span>**: Creación de una empresa que va a rematar objetos.
  - **Descripción**: Crea y devuelve una empresa.
  - **Explicación**: Se crea una nueva empresa que puede comenzar a rematar objetos.
  - **Campos requeridos**: `name`, `address`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /companies</span>**: Obtener todas las empresas.
  - **Descripción**: Devuelve una lista de todas las empresas registradas.

- **<span style="color:#2dd">GET /company/{uuid}</span>**: Obtener una empresa por su UUID.
  - **Descripción**: Devuelve la información de una empresa específica usando su `uuid`.
  - **Campos requeridos**: `uuid`.

- **<span style="color:#d2d">PUT /companyUpdate</span>**: Modificar una empresa por su UUID.
  - **Descripción**: Modifica los datos de una empresa específica.
  - **Campos requeridos**: `name`, `address`, `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d22">DELETE /companyDelete/{uuid}</span>**: Eliminar una empresa por su UUID.
  - **Descripción**: Elimina una empresa específica usando su `uuid`.
  - **Campos requeridos**: `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>


### Remates:

- **<span style="color:#2d2">POST /auctionCreate</span>**: Creación de un remate.
  - **Descripción**: Crea y devuelve un remate.
  - **Explicación**: Se crea un remate con los parámetros especificados.
  - **Campos requeridos**: `company`, `description`, `dateStart`, `type`, `dateFinish`, `timeAfterBid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /auctions</span>**: Obtener todos los remates.
  - **Descripción**: Devuelve una lista de todos los remates.
  - No requiere sesión iniciada.

- **<span style="color:#2dd">GET /auctionsFinished</span>**: Obtener todos los remates terminados.
  - **Descripción**: Devuelve una lista de los remates que ya han finalizado.
  - No requiere sesión iniciada.

- **<span style="color:#2dd">GET /auctionsNotFinished</span>**: Obtener todos los remates no terminados.
  - **Descripción**: Devuelve una lista de los remates que no han terminado aún.
  - No requiere sesión iniciada.

- **<span style="color:#2dd">GET /auctionsStarted</span>**: Obtener todos los remates que han comenzado pero no han terminado.
  - **Descripción**: Devuelve una lista de los remates que han empezado y no han terminado.
  - No requiere sesión iniciada.

- **<span style="color:#2dd">GET /auctionsNotStarted</span>**: Obtener todos los remates que no han comenzado aún.
  - **Descripción**: Devuelve una lista de los remates que aún no han comenzado.
  - No requiere sesión iniciada.

- **<span style="color:#2dd">GET /auction/{uuid}</span>**: Obtener un remate por su UUID.
  - **Descripción**: Devuelve la información de un remate específico según su `uuid`.
  - **Campos requeridos**: `uuid`.
  - No requiere sesión iniciada.

- **<span style="color:#2dd">GET /auctionsByCompany/{company}</span>**: Obtener todos los remates de una empresa.
  - **Descripción**: Devuelve una lista de los remates asociados a una empresa específica.
  - **Campos requeridos**: `company`.
  - No requiere sesión iniciada.

- **<span style="color:#d2d">PUT /auctionUpdate</span>**: Modificar un remate por su UUID.
  - **Descripción**: Modifica un remate existente utilizando su `uuid`.
  - **Campos requeridos**: `company`, `description`, `dateStart`, `uuid`, `type`, `dateFinish`, `timeAfterBid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d22">DELETE /auctionDelete/{uuid}</span>**: Eliminar un remate por su UUID.
  - **Descripción**: Elimina un remate específico utilizando su `uuid`.
  - **Campos requeridos**: `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

### Artículos:

- **<span style="color:#2d2">POST /articleCreate</span>**: Creación de un artículo que se va a rematar.
  - **Descripción**: Crea y devuelve un artículo que será puesto en remate.
  - **Explicación**: El artículo se asocia a una subasta (remate) y tiene varios parámetros asociados como valor mínimo, tiempo de inicio y fin, etc.
  - **Campos requeridos**: `auction`, `before`, `description`, `dateOfStart`, `dateOfFinish`, `timeAfterBid`, `type`, `minValue`, `minStepValue`, `urlPhoto`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /articles</span>**: Obtener todos los artículos.
  - **Descripción**: Devuelve una lista de todos los artículos disponibles en la plataforma.
  
- **<span style="color:#2dd">GET /article/{uuid}</span>**: Obtener un artículo por su UUID.
  - **Descripción**: Devuelve la información de un artículo específico usando su `uuid`.
  - **Campos requeridos**: `uuid`.

- **<span style="color:#d2d">PUT /articleUpdate</span>**: Modificar un artículo por su UUID.
  - **Descripción**: Permite modificar los datos de un artículo específico, como su descripción, fechas de inicio y fin, valores de puja, etc.
  - **Campos requeridos**: `uuid`,`auction`,`description`, `dateOfStart`, `dateOfFinish`, `timeAfterBid`, `type`, `minValue`, `minStepValue`, `urlPhoto`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /myArticlesBought</span>**: Obtener todos los artículos comprados por el usuario.
  - **Descripción**: Devuelve una lista de artículos comprados por el usuario autenticado.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d22">DELETE /articleDelete/{uuid}</span>**: Eliminar un artículo por su UUID.
  - **Descripción**: Elimina un artículo específico usando su `uuid`.
  - **Campos requeridos**: `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

### Pujas:

- **<span style="color:#2d2">POST /bidCreate</span>**: Creación de una puja por un objeto.
  - **Descripción**: Crea y devuelve una puja para un artículo específico.
  - **Explicación**: La puja incluye el valor y el artículo sobre el cual se está pujando.
  - **Campos requeridos**: `value`, `article`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /bids</span>**: Obtener todas las pujas.
  - **Descripción**: Devuelve una lista de todas las pujas realizadas en la plataforma.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /bid/{uuid}</span>**: Obtener una puja por su UUID.
  - **Descripción**: Devuelve la información de una puja específica usando su `uuid`.
  - **Campos requeridos**: `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#d22">DELETE /bidDelete/{uuid}</span>**: Eliminar una puja por su UUID.
  - **Descripción**: Elimina una puja específica usando su `uuid`.
  - **Campos requeridos**: `uuid`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /bidByArticle/{article}</span>**: Obtener todas las pujas sobre un artículo.
  - **Descripción**: Devuelve una lista de todas las pujas realizadas sobre un artículo específico.
  - **Campos requeridos**: `article`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

- **<span style="color:#2dd">GET /bidByUser/{user}</span>**: Obtener todas las pujas de un usuario.
  - **Descripción**: Devuelve una lista de todas las pujas realizadas por un usuario específico.
  - **Campos requeridos**: `user`.
  - <span style="color:red">**Requiere sesión iniciada**</span>

### Ejemplos
La API utiliza JSON Web Tokens (JWT) para autenticar a los usuarios. Para obtener un token, realiza una solicitud POST a ``/login`` con el nombre de usuario y la contraseña. El token debe incluirse en las cabeceras Authorization de las solicitudes posteriores a rutas protegidas.

1. Ejemplo de login:
  ```bash
  curl -X POST http://localhost:4000/login \
      -H "Content-Type: application/json" \
      -d '{
          "email": "usuario@example.com",
          "password": "12345678"
          }'
```
  Respuesta esperada:

```json
{ 
  "content": {
    "birthdate": "01/01/1990",
    "companies": {
    "companies": [
        {
        "address": "7/ 62 y 63 nº 306, La Plata ",
        "companies": [],
        "dateOfCreate": "12/11/2024T23:23:05-0300",
        "dateOfUpdate": "12/11/2024T23:23:33-0300",
        "name": "Remates La Plata",
        "owner": "835a9922-b112-401d-b0fb-7af87374d369",
        "removed": 0,
        "uuid": "a2cad956-0bad-4bfa-a527-fdfa141cbd31"
        }
    ]
    },
    "confirmEmail": 1,
    "dateOfCreate": "12/11/2024T23:19:43-0300",
    "dateOfUpdate": null,
    "email": "usuario@example.com",
    "lastName": "Usuario",
    "login": "13/11/2024 02:51:24",
    "name": "Usuario",
    "removed": 0,
    "terms": 1,
    "users": [],
    "uuid": "835a9922-b112-401d-b0fb-7af87374d369"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiNTc1MTRjMTgtODljZi00OTVjLWI0ZGYtNTc4NWM4Mzk0NDM4In0.KjhJZZcZvhYA0v1TyakRUQpnkGVT5hwVlwrShW3EK7A"
}
```
2. Ejemplo de peticiones que requieres sesión: 

```bash
curl -X PUT http://localhost:4000/userUpdate \
    -H "Content-Type: application/json" \
    -H "x-access-tokens: <tu_token_jwt>" \
    -d '{
        "name": "Juan Carlos",
        "lastName": "Baza Gómez",
        "birthdate": "20/05/1990"
        }'
```
  Respuesta esperada:
```json
{
  "cod":202,
  "content":{
    "birthdate":"20/05/1990",
    "companies":
    {"companies":[
        {
        "address": "7/ 62 y 63 nº 306, La Plata ",
        "companies": [],
        "dateOfCreate": "12/11/2024T23:23:05-0300",
        "dateOfUpdate": "12/11/2024T23:23:33-0300",
        "name": "Remates La Plata",
        "owner": "835a9922-b112-401d-b0fb-7af87374d369",
        "removed": 0,
        "uuid": "a2cad956-0bad-4bfa-a527-fdfa141cbd31"
        }
    ]
    },
    "confirmEmail":1,
    "dateOfCreate":"12/11/2024T23:19:43-0300",
    "dateOfUpdate":"13/11/2024T21:59:46-0300",
    "email":"usuario@example.com",
    "lastName":"Baza G\u00f3mez",
    "name":"Juan Carlos",
    "removed":0,
    "terms":1,
    "users":[],
    "uuid":"835a9922-b112-401d-b0fb-7af87374d369"
    },
  "error":null}
```



## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE)
 para más detalles.



