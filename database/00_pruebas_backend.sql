CREATE DATABASE IF NOT EXISTS vetconnect_db;

USE vetconnect_db;

CREATE TABLE IF NOT EXISTS propietarios (
    id_propietario INT AUTO_INCREMENT PRIMARY KEY,
    ci VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS mascotas (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    id_propietario INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(60),
    edad INT,
    FOREIGN KEY (id_propietario)
        REFERENCES propietarios(id_propietario)
);
