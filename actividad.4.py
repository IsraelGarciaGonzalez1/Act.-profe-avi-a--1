
import sqlite3
import os

# CONFIGURACION DE LA BASE DE DATOS

DB = "database/empleados.db"


def conectar():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB)


# CREACION DE LA BASE DE DATOS

def crear_bd():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
            curp TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            telefono TEXT,
            edad INTEGER,
            sueldo_mensual REAL
        )
    """)

    conexion.commit()
    conexion.close()


# 1. ALTAS DE EMPLEADOS

def alta_empleado():
    print("\n===== ALTA DE EMPLEADO =====")

    curp = input("CURP: ").strip().upper()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    telefono = input("Telefono: ").strip()

    try:
        edad = int(input("Edad: "))
        sueldo = float(input("Sueldo mensual: "))

        if edad <= 0 or sueldo < 0:
            print("La edad debe ser positiva y el sueldo no puede ser negativo.")
            return

    except ValueError:
        print("Error: ingrese una edad y un sueldo validos.")
        return

    if not curp or not nombre or not apellido:
        print("CURP, nombre y apellido son obligatorios.")
        return

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO empleado
            (curp, nombre, apellido, calle, colonia,
             telefono, edad, sueldo_mensual)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            curp, nombre, apellido, calle, colonia,
            telefono, edad, sueldo
        ))

        conexion.commit()
        print("\nEmpleado registrado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: esa CURP ya esta registrada.")

    except sqlite3.Error as error:
        print("Error al registrar:", error)

    finally:
        conexion.close()


# 2. BAJAS DE EMPLEADOS

def baja_empleado():
    print("\n===== BAJA DE EMPLEADO =====")

    curp = input("CURP del empleado: ").strip().upper()
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM empleado WHERE curp = ?",
            (curp,)
        )

        empleado = cursor.fetchone()

        if empleado is None:
            print("No se encontro el empleado.")
            return

        print("\nEmpleado encontrado:")
        print("CURP:", empleado[0])
        print("Nombre:", empleado[1])
        print("Apellido:", empleado[2])
        print("Calle:", empleado[3])
        print("Colonia:", empleado[4])
        print("Telefono:", empleado[5])
        print("Edad:", empleado[6])
        print("Sueldo mensual:", empleado[7])

        confirmacion = input(
            "\nDesea eliminar este empleado? (S/N): "
        ).strip().upper()

        if confirmacion == "S":
            cursor.execute(
                "DELETE FROM empleado WHERE curp = ?",
                (curp,)
            )
            conexion.commit()
            print("Empleado eliminado correctamente.")
        else:
            print("Operacion cancelada.")

    except sqlite3.Error as error:
        print("Error al eliminar:", error)

    finally:
        conexion.close()


# 3. MODIFICACIONES DE EMPLEADOS

def modificar_empleado():
    print("\n===== MODIFICACION DE EMPLEADO =====")

    curp = input("CURP del empleado: ").strip().upper()
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, apellido, calle, colonia,
                   telefono, edad, sueldo_mensual
            FROM empleado
            WHERE curp = ?
        """, (curp,))

        empleado = cursor.fetchone()

        if empleado is None:
            print("No se encontro el empleado.")
            return

        print("\nDeje el campo vacio para conservar el dato actual.")

        nombre = input(f"Nombre [{empleado[0]}]: ").strip()
        apellido = input(f"Apellido [{empleado[1]}]: ").strip()
        calle = input(f"Calle [{empleado[2] or ''}]: ").strip()
        colonia = input(f"Colonia [{empleado[3] or ''}]: ").strip()
        telefono = input(f"Telefono [{empleado[4] or ''}]: ").strip()
        edad_txt = input(f"Edad [{empleado[5]}]: ").strip()
        sueldo_txt = input(
            f"Sueldo mensual [{empleado[6]}]: "
        ).strip()

        nombre = nombre or empleado[0]
        apellido = apellido or empleado[1]
        calle = calle or empleado[2] or ""
        colonia = colonia or empleado[3] or ""
        telefono = telefono or empleado[4] or ""

        try:
            edad = int(edad_txt) if edad_txt else empleado[5]
            sueldo = float(sueldo_txt) if sueldo_txt else empleado[6]

            if edad <= 0 or sueldo < 0:
                print("Edad o sueldo no validos.")
                return

        except ValueError:
            print("Error: edad o sueldo no validos.")
            return

        cursor.execute("""
            UPDATE empleado
            SET nombre = ?, apellido = ?, calle = ?,
                colonia = ?, telefono = ?, edad = ?,
                sueldo_mensual = ?
            WHERE curp = ?
        """, (
            nombre, apellido, calle, colonia,
            telefono, edad, sueldo, curp
        ))

        conexion.commit()
        print("\nEmpleado modificado correctamente.")

    except sqlite3.Error as error:
        print("Error al modificar:", error)

    finally:
        conexion.close()


# 4. CONSULTA DE TODOS LOS EMPLEADOS

def consultar_todos():
    print("\n===== LISTADO DE EMPLEADOS =====")

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM empleado
            ORDER BY apellido, nombre
        """)

        empleados = cursor.fetchall()

        if not empleados:
            print("No hay empleados registrados.")
            return

        for empleado in empleados:
            print("-" * 45)
            print("CURP:", empleado[0])
            print("Nombre:", empleado[1])
            print("Apellido:", empleado[2])
            print("Calle:", empleado[3] or "")
            print("Colonia:", empleado[4] or "")
            print("Telefono:", empleado[5] or "")
            print("Edad:", empleado[6])
            print("Sueldo mensual: $", empleado[7])

        print("-" * 45)
        print("Total de empleados:", len(empleados))

    except sqlite3.Error as error:
        print("Error al consultar:", error)

    finally:
        conexion.close()


# 5. CONSULTA POR CURP

def consultar_curp():
    print("\n===== CONSULTA POR CURP =====")

    curp = input("Ingrese la CURP: ").strip().upper()
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM empleado
            WHERE curp = ?
        """, (curp,))

        empleado = cursor.fetchone()

        if empleado:
            print("\n===== DATOS DEL EMPLEADO =====")
            print("CURP:", empleado[0])
            print("Nombre:", empleado[1])
            print("Apellido:", empleado[2])
            print("Calle:", empleado[3] or "")
            print("Colonia:", empleado[4] or "")
            print("Telefono:", empleado[5] or "")
            print("Edad:", empleado[6])
            print("Sueldo mensual: $", empleado[7])
        else:
            print("No se encontro un empleado con esa CURP.")

    except sqlite3.Error as error:
        print("Error al consultar:", error)

    finally:
        conexion.close()


# 6. MENU PRINCIPAL

def menu():
    while True:
        print("\n" + "=" * 40)
        print(" SISTEMA DE EMPLEADOS - EMPRESA ACME ")
        print("=" * 40)
        print("1. Alta de empleado")
        print("2. Baja de empleado")
        print("3. Modificacion de empleado")
        print("4. Consulta de todos los empleados")
        print("5. Consulta por CURP")
        print("6. Salir")
        print("=" * 40)

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            alta_empleado()
        elif opcion == "2":
            baja_empleado()
        elif opcion == "3":
            modificar_empleado()
        elif opcion == "4":
            consultar_todos()
        elif opcion == "5":
            consultar_curp()
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida. Seleccione del 1 al 6.")


# INICIO DEL PROGRAMA

if __name__ == "__main__":
    crear_bd()
    menu()
