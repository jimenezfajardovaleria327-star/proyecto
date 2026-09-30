# Students App

Aplicación de ejemplo construida con Flask y PostgreSQL, pensada para enseñar
el flujo completo: primero clonar y preparar el entorno local, después
Dockerizar la aplicación.

## Cómo se conecta a la base de datos

La app se conecta a PostgreSQL con `psycopg2`, indicando host, usuario,
contraseña y nombre de la base de datos (ver [`app.py`](app.py)):

```python
psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME"),
)
```

Ninguno de esos valores está escrito directamente en el código
(`hardcodeado`). Cada uno se lee con `os.getenv(...)` desde una variable de
entorno, y esas variables se definen en un archivo `.env` que cada quien crea
localmente a partir de [`.env.example`](.env.example) y que **nunca se sube al
repositorio** (está en [`.gitignore`](.gitignore)). Así, las credenciales
pueden cambiar entre tu máquina, la de un compañero o producción, sin tocar
una sola línea de código.

## 1. Entorno local (sin Docker)

Este paso no requiere tener una base de datos levantada. La app arranca igual
y, si no encuentra la base de datos, la página de alumnos se muestra vacía en
vez de dar un error.

### Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
```

### Instalar las dependencias

```bash
pip install -r requirements.txt
```

### Configurar las variables de entorno

```bash
cp .env.example .env
```

Puedes revisar y ajustar los valores en `.env` si lo necesitas.

### Ejecutar la aplicación

```bash
python3 app.py
```

Abre [http://localhost:5000](http://localhost:5000). Verás "No hay alumnos
registrados." porque todavía no hay ninguna base de datos disponible — y no
un error 500, que es justo el comportamiento esperado en este punto.

## 2. Con Docker (base de datos incluida)

Una vez entendido el paso anterior, se levanta todo el stack (app + PostgreSQL)
con Docker Compose:

```bash
docker compose up --build
```

Esto crea el contenedor de PostgreSQL, carga los datos iniciales de
[`database_students.sql`](database_students.sql) y arranca la app conectada a
esa base de datos. Fíjate que en `docker-compose.yml` las mismas variables
(`DB_HOST`, `DB_USER`, etc.) se definen directamente ahí en vez de en un
`.env` — es Docker Compose quien se las entrega al contenedor. Ahora en
[http://localhost:5000](http://localhost:5000) sí se verá el listado de
alumnos.

Para detener y eliminar los contenedores:

```bash
docker compose down
```

## Estructura del proyecto

```
app.py                    # Aplicación Flask (rutas + conexión a la BD)
templates/                # Vistas Jinja2 (Bootstrap)
database_students.sql     # Datos iniciales para PostgreSQL
.env.example               # Plantilla de variables de entorno
```
