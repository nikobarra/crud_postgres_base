import psycopg2
import os

USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def cleanup(function):
    def wrapper(connect, cursor):
        os.system("cls")
        function(connect, cursor)
        input("Presione enter para continuar")
        os.system("cls")

    wrapper.__doc__ = function.__doc__
    return wrapper


def search_user(connect, cursor, user_id):
    query = "SELECT id FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    usuario = cursor.fetchone()
    return usuario


def user_not_exists(user):
    print("--------------------------------------")
    print(f">>>> El usuario {user} no existe <<<<")
    print("--------------------------------------")


def user_success(action):
    print("-----------------------------------------")
    print(f"<<<< Usuario {action} correctamente >>>>")
    print("-----------------------------------------")


def cancel():
    print("--------------------------------------")
    print(">>>>>    accion cancelada    <<<<<")
    print("--------------------------------------")


def execute_query(connect, cursor, query, values, action):
    try:
        cursor.execute(query, values)
        connect.commit()
        user_success(action)
    except Exception as e:
        print(f"Error al {action} el usuario: {e}")


# Menu
@cleanup
def create_user(connect, cursor):
    """A) Crear usuario"""
    username = input("Ingrese el nombre de usuario: ")
    email = input("Ingrese un email: ")
    if username and email:
        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        values = (username, email)
        execute_query(connect, cursor, query, values, "Creado")
    else:
        cancel()


@cleanup
def list_users(connect, cursor):
    """B) Listado de usuarios"""
    query = "SELECT id, username, email FROM users"
    cursor.execute(query)
    print("--------------------------------------")
    for id, username, email in cursor.fetchall():
        print(id, "-", username, "-", email)
    print("--------------------------------------")


@cleanup
def update_user(connect, cursor):
    """C) Actualizar usuario"""
    print("--------------------------------------")
    list_users(connect, cursor)
    print("--------------------------------------")
    user_upd = input("Ingrese el ID del usuario a modificar: ")
    print("--------------------------------------")
    if user_upd:
        user_find = search_user(connect, cursor, user_upd)
        if user_find:
            username = input("Ingrese un nuevo nombre de usuario: ")
            email = input("Ingrese un nuevo email: ")
            if username != "" and email != "":
                query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
                values = (username, email, user_upd)
                upd = True
            elif username != "":
                query = "UPDATE users SET username = %s WHERE id= %s"
                values = (username, user_upd)
                upd = True
            elif email != "":
                query = "UPDATE users SET email = %s WHERE id= %s"
                values = (email, user_upd)
                upd = True
            else:
                cancel()
                upd = False
            if upd:
                execute_query(connect, cursor, query, values, "Actualizado")
        else:
            user_not_exists(user_upd)
    else:
        cancel()


@cleanup
def delete_user(connect, cursor):
    """D) Borrar usuario"""
    print("--------------------------------------")
    list_users(connect, cursor)
    user_del = input("Que usuario desea eliminar? :")
    print("--------------------------------------")
    if user_del:
        query = "SELECT id FROM users WHERE id = %s"
        user_find = search_user(connect, cursor, user_del)
        if user_find:
            res = input("Esta seguro? s/n: ").lower()
            if res == "s":
                query = "DELETE FROM users WHERE id = %s"
                execute_query(connect, cursor, query, (user_del,), "Eliminado")
            else:
                cancel()
        else:
            user_not_exists(user_del)
    else:
        cancel()


@cleanup
def default(*args):
    print("opción no valida")
    print("--------------------------------------")


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
