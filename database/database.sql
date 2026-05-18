CREATE DATABASE IF NOT EXISTS restaurante;
USE restaurante;

CREATE TABLE IF NOT EXISTS administradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Contraseña para el panel
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS reservas(
    id_reservas int AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    cliente_email VARCHAR(100) NOT NULL,
    cantidad_personas int NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    token_qr varchar(100) NOT NULL UNIQUE,
    estado_reserva ENUM('pendiente', 'confirmada', 'cancelada', 'asistio') DEFAULT 'pendiente'
);
CREATE TABLE IF NOT EXISTS reseñas(
    id_reseña int AUTO_INCREMENT PRIMARY KEY,
    id_reserva int NOT NULL UNIQUE, -- le ponemos unique ya que cada reserva puede tener una sola reseña, cada usuario puede dejar su reseña una sola vez, es una relacion 1:1
    puntaje int CHECK (puntaje >= 1 AND puntaje <= 5), -- nos aseguramos que ponga un numero entre 1 y 5, podemos luego en el front hacer que sea un sistema de estrellas para que el usuario no tenga que escribir el numero
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    FOREIGN KEY (id_reserva) REFERENCES reservas(id_reservas)
)

CREATE TABLE IF NOT EXISTS menu(
    id_plato int AUTO_INCREMENT PRIMARY KEY,
    nombre_plato VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    url_imagen VARCHAR(255),
    restricciones VARCHAR(255), -- por ejemplo: "sin gluten, vegano", esto lo podemos mostrar en el front para que el usuario sepa si el plato tiene alguna restriccion alimentaria
    plato_disponible BOOLEAN NOT NULL DEFAULT TRUE
)

CREATE TABLE IF NOT EXISTS servicios_extras(
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripción TEXT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE -- esto luego podemos hacer que si esta activo se agregue en el footer de la pagina, pero si no lo esta no se muestre, asi el administrador puede agregar o quitar servicios extras sin necesidad de modificar el codigo del front
)