import psycopg2

DROP_USERS_TABLE = "DROP TABLE IF EXISTS users"

USERS_TABLE = """
CREATE TABLE users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

try:
    connect = psycopg2.connect("postgresql://niko:niko1979@localhost/project_crud")

    with connect.cursor() as cursor:
        cursor.execute(DROP_USERS_TABLE)
        cursor.execute(USERS_TABLE)
        connect.commit()
    connect.close()

except UnicodeDecodeError as err:
    print("conexion fallida")
