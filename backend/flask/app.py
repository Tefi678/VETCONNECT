from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

from db import obtener_conexion
from routes.propietarios import propietarios_bp
from routes.mascotas import mascotas_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(propietarios_bp)
app.register_blueprint(mascotas_bp)


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "Bienvenido a VETCONNECT",
        "estado": "Servidor funcionando"
    }), 200


# Comprobar conexión con MySQL
@app.route("/api/health", methods=["GET"])
def comprobar_conexion():

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]

        return jsonify({
            "servidor": "Funcionando",
            "mysql": "Conectado",
            "version": version
        }), 200

    except mysql.connector.Error as error:
        return jsonify({
            "servidor": "Funcionando",
            "mysql": "Desconectado",
            "detalle": str(error)
        }), 503

    finally:
        if cursor:
            cursor.close()

        if conexion and conexion.is_connected():
            conexion.close()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
