CREATE DATABASE restaurante;
USE restaurante;

CREATE TABLE usuarios(
    id_usuario int AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR (255) NOT NULL,
    apellido VARCHAR (255) NOT NULL,
    email  VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol enum ('cliente' , 'administrador')
)

CREATE TABLE reservas(
    id_reservas int AUTO_INCREMENT PRIMARY KEY,
    id_usuario int NOT NULL,
    cantidad_personas int NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    token_qr ??,
    estado_reserva VARCHAR(50) NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
)

CREATE TABLE reseñas(
    id_reseña int AUTO_INCREMENT PRIMARY KEY,
    id_usuario int NOT NULL,
    puntaje int NOT NULL,
    fecha_publicacion DATE NOT NULL,
    comentario VARCHAR (500),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
)

CREATE TABLE menu(
    id_plato int AUTO_INCREMENT PRIMARY KEY,
    nombre_plato VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    url_imagen VARCHAR(255),
    plato_disponible BOOLEAN NOT NULL DEFAULT TRUE
)

CREATE TABLE servicios_extras(
    id_servicio ??,
    nombre_servicio ??
)