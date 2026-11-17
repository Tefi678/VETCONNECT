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

        consulta = """
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
        """

        cursor.execute(consulta)

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


# REGISTRAR MASCOTA
@mascotas_bp.route("", methods=["POST"])
def registrar_mascota():

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere enviar un objeto JSON"
        }), 400

    nombre = str(datos.get("nombre", "")).strip()
    especie = str(datos.get("especie", "")).strip()

    try:
        id_propietario = int(datos.get("id_propietario"))

        edad_recibida = datos.get("edad")
        edad = (
            int(edad_recibida)
            if edad_recibida not in (None, "")
            else None
        )

        if id_propietario <= 0 or (
            edad is not None and edad < 0
        ):
            raise ValueError()

    except (TypeError, ValueError):
        return jsonify({
            "error": "El ID del propietario o la edad son inválidos"
        }), 400

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

        nuevo_id = cursor.lastrowid

        return jsonify({
            "mensaje": "Mascota registrada correctamente",
            "id_mascota": nuevo_id
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

        return jsonify({
            "error": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexion and conexion.is_connected():
            conexion.close()
