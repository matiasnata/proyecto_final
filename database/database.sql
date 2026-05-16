CREATE DATABASE restaurante;
USE restaurante;

CREATE TABLE usuarios(
    id_usuario int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR (255) NOT NULL,
    apellido VARCHAR (255) NOT NULL,
    email  VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol enum ('cliente' , 'administrador')
)

CREATE TABLE reservas(
    id_reservas int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_usuario 
    cantidad_personas
    fecha
    hora
    estado_reserva
    token_QR
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)

)