from flask import Blueprint, request, jsonify
import mysql.connector

from db import obtener_conexion

mascotas_bp = Blueprint(
    "mascotas",
    __name__,
    url_prefix="/api/mascotas"
)


# CONSULTAR MASCOTAS
@mascotas_bp.route("", methods=["GET"])
def listar_mascotas():

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                m.id_mascota,
                m.nombre,
                m.especie,
                m.raza,
                m.edad,
                m.id_propietario,
                p.nombre AS nombre_propietario,
                p.apellido AS apellido_propietario
            FROM mascotas m
            INNER JOIN propietarios p
                ON m.id_propietario = p.id_propietario
        """)

        mascotas = cursor.fetchall()

        return jsonify(mascotas), 200

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


# REGISTRAR MASCOTA
@mascotas_bp.route("", methods=["POST"])
def registrar_mascota():

    datos = request.get_json(silent=True) or {}

    nombre = str(datos.get("nombre", "")).strip()
    especie = str(datos.get("especie", "")).strip()

    try:
        id_propietario = int(datos.get("id_propietario"))
        edad = datos.get("edad")
        edad = int(edad) if edad not in (None, "") else None
    except (TypeError, ValueError):
        return jsonify({
            "error": "El propietario y la edad deben tener valores validos"
        }), 400

    if id_propietario <= 0 or (edad is not None and edad < 0):
        return jsonify({"error": "Los valores numericos no son validos"}), 400

    if not nombre or not especie:
        return jsonify({
            "error": "El nombre y la especie son obligatorios"
        }), 400

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO mascotas
            (id_propietario, nombre, especie, raza, edad)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            id_propietario,
            nombre,
            especie,
            datos.get("raza"),
            edad
        )

        cursor.execute(consulta, valores)
        conexion.commit()

        return jsonify({
            "mensaje": "Mascota registrada correctamente",
            "id_mascota": cursor.lastrowid
        }), 201

    except mysql.connector.IntegrityError:
        if conexion:
            conexion.rollback()

        return jsonify({
            "error": "El propietario indicado no existe"
        }), 400

    except mysql.connector.Error as error:
        if conexion:
            conexion.rollback()

        return jsonify({"error": str(error)}), 500

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
