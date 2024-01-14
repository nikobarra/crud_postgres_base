import psycopg2


USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def search_user(connect, cursor, user_id):
    query = "SELECT id FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    usuario = cursor.fetchone()
    return usuario


# Menu
def create_user(connect, cursor):
    """A) Crear usuario"""
    username = input("Ingrese el nombre de usuario: ")
    email = input("Ingrese un email: ")
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    values = (username, email)
    cursor.execute(query, values)
    connect.commit()
    print("--------------------------------------")
    print("      <<<< Usuario creado >>>>        ")
    print("--------------------------------------")


def list_users(connect, cursor):
    """B) Listado de usuarios"""
    query = "SELECT id, username, email FROM users"
    cursor.execute(query)
    print("--------------------------------------")
    for id, username, email in cursor.fetchall():
        print(id, "-", username, "-", email)
    print("--------------------------------------")


def update_user(connect, cursor):
    """C) Actualizar usuario"""
    print("--------------------------------------")
    list_users(connect, cursor)
    print("--------------------------------------")
    user_upd = int(input("Ingrese el ID del usuario a modificar: "))
    print("--------------------------------------")
    user_find = search_user(connect, cursor, user_upd)
    if user_find:
        username = input("Ingrese un nuevo nombre de usuario: ")
        email = input("Ingrese un nuevo email: ")
        query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        values = (username, email, user_upd)
        cursor.execute(query, values)
        connect.commit()
        print("--------------------------------------")
        print(f"El usuario {username} a sido actualizado correctamente")
        print("--------------------------------------")
    else:
        print("--------------------------------------")
        print(f"El usuario {user_upd} no existe")
        print("--------------------------------------")


def delete_user(connect, cursor):
    """D) Borrar usuario"""
    print("--------------------------------------")
    list_users(connect, cursor)
    user_del = int(input("Que usuario desea eliminar? :"))
    print("--------------------------------------")
    query = "SELECT id FROM users WHERE id = %s"
    user_find = search_user(connect, cursor, user_del)
    if user_find:
        res = input("Esta seguro? s/n: ").lower()
        if res == "s":
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_del,))
            connect.commit()
            print("--------------------------------------")
            print(f"<<< Usuario {user_del} eliminado correctamente >>>")
            print("--------------------------------------")
        else:
            print("--------------------------------------")
            print("accion cancelada")
            print("--------------------------------------")
    else:
        print("--------------------------------------")
        print(f"El usuario {user_del} no existe")
        print("--------------------------------------")


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
