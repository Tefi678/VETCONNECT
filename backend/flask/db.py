import mysql.connector
from config import DB_CONFIG


def obtener_conexion():
    conexion = mysql.connector.connect(**DB_CONFIG)
    return conexion