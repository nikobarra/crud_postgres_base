import psycopg2


USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


# Menu
def create_user(connect, cursor):
    """A) Crear usuario"""
    username = input("Ingrese el nombre de usuario: ")
    email = input("Ingrese un email: ")
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    values = (username, email)
    cursor.execute(query, values)
    connect.commit()


def list_users(connect, cursor):
    """B) Listar usuarios"""
    query = "SELECT * FROM users"
    cursor.execute(query)
    for user in cursor.fetchall():
        print(user)


def update_user(connect, cursor):
    """C) Actualizar usuario"""
    pass


def delete_user(connect, cursor):
    """D) Borrar usuario"""
    pass


def default(*args):
    print("opción no valida")


options = {"a": create_user, "b": list_users, "c": update_user, "d": delete_user}
# conexion a la BD
try:
    connect = psycopg2.connect("postgresql://niko:niko1979@localhost/project_crud")

    with connect.cursor() as cursor:
        cursor.execute(USERS_TABLE)
        connect.commit()
        # ciclo que recorre las opciones del menu segun lo elegido
        while True:
            for function in options.values():
                print(function.__doc__)
            print("quit para salir")
            option = input("Selecciona una opción: ").lower()
            if option == "quit" or option == "q":
                break

            function = options.get(option, default)
            function(connect, cursor)
    connect.close()

except UnicodeDecodeError as err:
    print("conexion fallida")
