from flask import Blueprint, request, jsonify
import mysql.connector

from db import obtener_conexion

propietarios_bp = Blueprint(
    "propietarios",
    __name__,
    url_prefix="/api/propietarios"
)


# CONSULTAR PROPIETARIOS
@propietarios_bp.route("", methods=["GET"])
def listar_propietarios():

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM propietarios
            ORDER BY id_propietario DESC
        """)

        resultado = cursor.fetchall()

        return jsonify(resultado), 200

    except mysql.connector.Error as error:
        return jsonify({
            "error": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexion and conexion.is_connected():
            conexion.close()


# REGISTRAR PROPIETARIO
@propietarios_bp.route("", methods=["POST"])
def registrar_propietario():

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere enviar un objeto JSON"
        }), 400

    ci = str(datos.get("ci", "")).strip()
    nombre = str(datos.get("nombre", "")).strip()
    apellido = str(datos.get("apellido", "")).strip()

    if not ci or not nombre or not apellido:
        return jsonify({
            "error": "CI, nombre y apellido son obligatorios"
        }), 400

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO propietarios
            (ci, nombre, apellido, telefono, correo)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            ci,
            nombre,
            apellido,
            datos.get("telefono"),
            datos.get("correo")
        )

        cursor.execute(consulta, valores)
        conexion.commit()

        nuevo_id = cursor.lastrowid

        return jsonify({
            "mensaje": "Propietario registrado correctamente",
            "id_propietario": nuevo_id
        }), 201

    except mysql.connector.IntegrityError:
        if conexion:
            conexion.rollback()

        return jsonify({
            "error": "El CI ya se encuentra registrado"
        }), 409

    except mysql.connector.Error as error:
        if conexion:
            conexion.rollback()

        return jsonify({
            "error": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexion and conexion.is_connected():
            conexion.close()
