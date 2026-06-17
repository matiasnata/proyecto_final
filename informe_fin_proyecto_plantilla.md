# Informe de Fin de Proyecto
## Plataforma de Gestión y Reservas Gastronómica
- **Institución:** Universidad de Buenos Aires (UBA)
- **Materia / Cátedra:** Introducción al desarrollo del software (Lanzillota)
- **Integrantes:** Joaquin Ponce, Santiago Mobiglia, Lautaro Rodoni, Franco Agustin Marcos, Matias Armida, Elias Antoniadis, Joaquin Salcedo, Bautista Fuertes 
- **Fecha de entrega:** 17/06/2026

---

## Tabla de Contenidos

1. [Introducción y Alcance del Proyecto](#1-introducción-y-alcance-del-proyecto)
2. [Decisiones de Diseño y Arquitectura](#2-decisiones-de-diseño-y-arquitectura)
3. [Conclusiones y Trabajo Futuro](#4-conclusiones-y-trabajo-futuro)

---

## 1. Introducción y Alcance del Proyecto

### 1.1. Resumen Ejecutivo

En este proyecto el equipo decidió realizar el Dominio 2 de desarrollo, consistente en la construcción de una plataforma web para un restaurante (FlamejBresto). El sistema fue diseñado para cubrir dos grandes necesidades: brindar a los clientes una forma fácil y fluida para interactuar con el local, y proveer al personal administrativo un panel de control centralizado para gestionar el día a día en el trabajo.

La arquitectura del sistema se basa en dos aplicaciones Flask desarrolladas en Python: una API dedicada exclusivamente a la lógica de negocio y persistencia de datos (backend), y una segunda aplicación que actúa como intermediaria entre los templates Jinja2 (frontend) y dicha API. Para la persistencia de la información (reservas, reseñas, menú y servicios extra) se utilizó MySQL como sistema de gestión de bases de datos relacionales.

---

### 1.2. Objetivos del Sistema

El objetivo general del proyecto es generar una página web con un apartado para clientes y otro enfocado a administradores.
Los siguientes objetivos de este proyecto se van a diferenciar dependiendo de que nos estemos referenciando dentro del mismo.

#### Objetivos del Frontend para Clientes
Los objetivos para el apartado de los clientes son los siguientes:

- Objetivo 1 —: Permitir que los clientes realicen la reserva de manera autonoma y fácil.
- Objetivo 2 —: Ofrecer visualización del menu con un filtro por restricciones alimenticias.
- Objetivo 3 —: Ofrecer un sistema de reseñas donde puedan expresar sus experiences dentro del restaurante.
- Objetivo 4 —: Confirmar reservas mediante un sistema de validación por código QR, que llega automáticamente al gmail.
- Objetivo 5 —: Exponer información institucional del restaurante (ubicación, contacto) de forma accesible desde el pie de página.


#### Objetivos del Panel de Administración

Los objetivos para el apartado de los administradores son los siguientes:

- Objetivo 1 —: Brindar al personal una interfaz para gestionar reservas en tiempo real.
- Objetivo 2 —: Proveer módulos ABM completos para la gestión de menú, reseñas, servicios-extra y reservas.
- Objetivo 3 —: Exponer dashboards analíticos sobre el flujo de reservas.
- Objetivo 4 —: Gestionar cancelaciones y notificaciones automáticas a los comensales.
- Objetivo 5 —: Ofrecer un apartado especial solamente para administradores donde se almacena toda la información.
- Objetivo 6 —: Apartado especial desde donde se podra leer el codigo QR de los comensales que llegaran.


---

## 2. Decisiones de Diseño y Arquitectura

### 2.1. Stack Tecnológico

El stack tecnológico que se utilizó en este proyecto es cien porciento dependiente de los lineamentos y principios que fueron previamente definidos por la cátedra.
Dicho esto el equipo no estuvo sujeto a decisiones propias, simplemente se aplicó cada tecnología en el ámbito que creemos que fue más conveniente.
A continuación se describe el rol que se utilizó para cada tecnología dentro del sistema.

#### Infraestructura y Capas del sistema

| Tecnología          | Rol en el proyecto                                                                                                                                                         |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python / Flask      | Framework principal de todo el proyecto, es el encargado de hacer funcionar la API del Backend como la del Frontend                                                        |
| Jinja2              | Es el motor que se esconde dentro de los templates, que permite renderizar dinamicamente las vistas de los templates del lado del cliente                                  |
| HTML                | Estructura y Marcado semantico de todas las paginas del sitio                                                                                                              | 
| CSS                 | Estilo visuales y presentacion de la interfaz de usuario                                                                                                                   |
| Javascript          | Comportamiento dinamico del lado del Usuario. Graficos de rendimiento, Alertas borrar/modificar registros, Unica utilizacion de la funcion 'Fetch' para el apartado de QR. |
| MySql               | Persistencia de los registros atravez de este sistema de gestion de base de datos relacionales                                                                             |


### 2.2. Diseño de la Experiencia del Cliente

Para las decisiones del diseño del lado del cliente, nos basamos pura y exclusivamente en un módulo mock-up hecho desde Figma. 
Para el mock-up nos basamos en los requisitos obligatorios solicitados por parte de la catedra para este proyecto.  

#### Módulo de Reservas Ágil

- **Flujo de reserva diseñado:**

  - El cliente accede a la plataforma y puede llegar al formulario de reservas de dos maneras: navegando manualmente por el sitio hasta encontrar la sección correspondiente, o presionando el botón "Reservar mesa ahora" ubicado en el centro de la página principal, que redirige directamente a dicha sección.
    El formulario solicita los siguientes datos mediante botones y campos de texto: fecha, horario, cantidad de personas, nombre y email. Una vez completado y enviado, el cliente recibe automáticamente un correo de confirmación con el código QR asociado a su reserva.
    A partir de ese momento el flujo puede tomar dos caminos:

    - Cancelación: si la reserva es cancelada por cualquier motivo, se envía una notificación automática al email asociado informando la situación.
    - Asistencia: el comensal se presenta en el restaurante en la fecha y horario pautados con su código QR. El administrador lo escanea desde el panel, el sistema valida el código, actualiza el estado de la reserva a "Asistió" y envía automáticamente un email al cliente con un enlace para redactar su reseña.
#### Menú con Restricciones Alimenticias

 - El sistema contempla soporte para restricciones alimenticias tanto a nivel de base de datos como en el panel de administración, donde el administrador puede asociar restricciones a cada plato al momento de darlo de alta o modificarlo. Sin embargo, la visualización de dichos filtros en el apartado del menú orientado a los clientes no llegó a implementarse en el frontend público. Esta omisión no fue detectada a tiempo por el equipo por lo que quedó como funcionalidad parcialmente desarrollada. La lógica de backend y la estructura de datos están presentes y operativas, siendo el paso pendiente únicamente su representación visual en la interfaz del cliente.

#### Módulo de Reseñas

**Flujo de publicación de reseñas:**
  - El acceso al módulo de reseñas está condicionado a la validación presencial del código QR. Una vez que el comensal llega al restaurante y el administrador escanea su código, el sistema actualiza el estado de la reserva a "Asistió" y envía automáticamente un email al correo asociado con un enlace para escribir la reseña, permitiendo que el cliente lo complete cómodamente una vez terminada su experiencia. La reseña solicita un puntaje y un comentario, se almacena directamente en la base de datos al momento de ser enviada, impacta de forma inmediata en el gráfico analítico del dashboard (que muestra el promedio de puntajes mensuales por año), ademas tambien aparece dicha resenia en el apartado público de reseñas del sitio orientado a clientes.
---

### 2.3. Sistema de Validación por QR y Notificaciones

#### Flujo de Generación del Código QR

- **Evento disparador:**
  - Al completarse exitosamente el formulario de reserva, el backend genera de forma inmediata el código QR. Esto ocurre dentro del endpoint POST /reservas, una vez que los datos son validados y la reserva es insertada en la base de datos

- **Datos embebidos en el QR:**
  - El QR codifica únicamente un token de tipo UUID v4, generado con la librería estándar uuid de Python (str(uuid.uuid4())). Este token se almacena en la base de datos junto a la reserva y actúa como identificador único de validación, sin exponer datos personales del cliente

- **Librería / herramienta utilizada:**
  - Se utilizó la librería qrcode de Python. La imagen se genera en memoria como bytes PNG mediante un buffer io.BytesIO, sin escribir ningún archivo en disco, y se adjunta directamente al email de confirmación como imagen inline.

#### Flujo de Envío por Email

- **Contenido del email de confirmación:**
  - El cliente recibe un email HTML con los datos de su reserva (nombre, fecha, hora, cantidad de personas) y el código QR adjunto como imagen embebida. El template es renderizado con Jinja2 desde el propio backend.

- **Servicio de envío utilizado:**
  - Se utilizó el protocolo SMTP a través del servidor smtp.gmail.com. Para garantizar la seguridad de la cuenta emisora sin comprometer las credenciales del administrador, se configuró una Contraseña de Aplicación de 16 dígitos provista por Google Developer Console, integrada en las variables de entorno del backend.

#### Flujo de Cancelación

- **Cancelación iniciada por el cliente:**
  - Cuando los usuarios reciben el email recibiendo la información de que su reserva fue confirmada con éxito, debajo del código qr aparece un botón que permite cancelar la reserva, una vez que se interactúa con el mismo se lo lleva a un template avisándole que su reserva fue cancelada con éxito.

- **Cancelación iniciada por el administrador:**
  - En el dashboard, el apartado de reserva tiene 3 botones, que permiten al administrador poder, modificar o cancelar/eliminar la reserva. Si se cancela dicha reserva, el email asociado a la reserva recibe un gmail informandole sobre la novedad.
  

- **Actualización de estado en el sistema:**
  - Una vez que suceden los cambios, sean por los clientes o los mismo administradores, el estado de esa reserva cambia en la base de datos y se mantiene como cancelada

---

### 2.4. Arquitectura del Panel de Administración y Dashboards

#### Módulos ABM

- **Entidades gestionadas en el panel:**
  - Menú: Implementado como un ABM completo con soporte de baja lógica. Esto permite marcar un plato como no disponible sin eliminarlo de la base de datos, útil para casos donde un producto no está en cocina temporalmente pero se desea conservar el registro. Las consultas al sistema filtran únicamente los platos marcados como disponibles.
  -  Servicios Extra: Comparte la misma estrategia que el módulo de menú, incluyendo baja lógica, modificación y alta desde el panel de administración.
  -  Reseñas: Es el único módulo cuyo alta es iniciada por el cliente. Una vez que el administrador escanea el QR del comensal, se envía automáticamente un email con un enlace para redactar la reseña. El formulario solicita un puntaje y un comentario; el puntaje impacta directamente en el gráfico analítico del dashboard. Desde el panel, el administrador únicamente puede eliminar reseñas en caso de contenido ofensivo o lenguaje inapropiado.

- **Decisiones de acceso y permisos:**
  - Los clientes del sitio no requieren registro ni inicio de sesión para navegar la plataforma. Únicamente al momento de realizar una reserva se solicita un correo electrónico de Gmail, que actúa como medio de comunicación para el envío de notificaciones automáticas (confirmación, QR, cancelaciones y enlace de reseña).
  El acceso al panel de administración requiere inicio de sesión con credenciales. La sesión tiene una duración limitada, vencida la cual el administrador debe autenticarse nuevamente. Solo los usuarios con rol de administrador tienen permisos para acceder a los módulos de gestión y dashboards analíticos.


#### Dashboards Analíticos de Reservas

- **Métricas expuestas en el dashboard:**
El dashboard de reservas se divide en dos apartados diferenciados:
- El primero consiste en una tabla de reservas que centraliza la información de cada reserva registrada en el sistema. Las columnas expuestas son: ID, nombre del cliente, email, cantidad de personas (con un máximo de 12), fecha, hora y estado. Desde esta tabla, el administrador puede gestionar el estado de cada reserva mediante tres acciones:

- Asistió: se marca una vez que el administrador escanea el código QR del comensal al momento de su llegada, actualizando el estado automáticamente y enviando una notificación por email al cliente.
- Editar: permite editar manualmente los datos de una reserva en caso de que el cliente se haya contactado con el restaurante para solicitar un cambio.
- Cancelar: elimina la reserva del sistema y envía una notificación automática por email al cliente informando la cancelación.

El segundo apartado expone un gráfico de líneas que muestra la cantidad de reservas registradas en los últimos 7 días, permitiendo al administrador visualizar la tendencia de ocupación reciente del restaurante.

- **Tecnología de visualización utilizada:**
- Utilizamos funciones de java script para realizar los ambos gráficos, reservas y reseñas. En los gráficos, si bien las decisiones gráficas fue independiente de cada compañero que abarco dicho gráfico, en el fondo los dos utilizaron la biblioteca chart.js

---

## 3. Conclusiones 

### 3.1. Evaluación del Cumplimiento de Objetivos

| Objetivos                                                                                    | Estado  | Observaciones                                                                                                                                                          |
|----------------------------------------------------------------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Permitir que los clientes realicen reservas de forma autónoma y fácil                        | Completado/Logrado | La página web implementa el flujo de reserva cumpliendo con todos los requisitos establecidos                                                                          |
| Ofrecer visualización del menú con filtrado por restricciones alimenticias                   | Parcial | Se desarrolló todo el flujo de restricciones por parte del backend y del front del administrador pero no se logro representarlo visualmente en el menu de los clientes |
| Proveer un módulo de reseñas donde los comensales expresen sus experiencias                  | Completado/Logrado | El sistema de reseñas fue implementado correctamente                                                                                                                   |
| Confirmar reservas mediante código QR enviado automáticamente por email                      | Completado/Logrado | El QR se envía al correo del cliente y es validado presencialmente en el restaurante por el administrador                                                              |
| Exponer información institucional del restaurante en el pie de página                        | Completado/Logrado | El footer contiene la información de ubicación y contacto del establecimiento                                                                                          |
| Gestionar reservas en tiempo real desde una interfaz centralizada                            | Completado/Logrado | El panel permite marcar asistencia, modificar datos de una reserva y cancelarla                                                                                        |
| Proveer módulos ABM completos para la gestión de menú, reseñas, servicios-extra y reservas.  | Completado/Logrado | Todos los módulos ABM fueron implementados                                                                                                                             |
| Exponer dashboards analíticos sobre el flujo de reservas y reseñas                           | Completado/Logrado | Se desarrollaron paneles con gráficos tanto para reservas como para reseñas                                                                                            |
| Gestionar cancelaciones y confirmaciones con notificación automática al comensal             | Completado/Logrado | El sistema notifica al cliente ante cancelaciones y confirmaciones                                                                                                     |
| Restringir el acceso al panel exclusivamente al personal autorizado                          | Completado/Logrado | El panel requiere inicio de sesión y se accede desde la esquina inferior derecha del sitio                                                                             |
| Incorporar una sección de escaneo y validación de códigos QR                                 | Completado/Logrado | Se desarrolló un apartado específico dentro del panel de administración para esta función                                                                              |

---

### 3.2. Lecciones Aprendidas en el Desarrollo


#### Lecciones Técnicas

- Lección 1 : Contar con un mockup hecho en Figma antes de arrancar el desarrollo nos permitió tener siempre un objetivo visual claro en mente. Saber hacia dónde apuntábamos facilitó la toma de decisiones a la hora de codificar las vistas y evitó perder tiempo en cambios de dirección a mitad del proyecto
- Lección 2 : Aun habiendo diseñado el esquema de base de datos antes de comenzar a codificar, pequeñas inconsistencias en los nombres pueden generar errores difíciles de rastrear. En nuestro caso, la columna descripción fue creada en la base de datos con tilde, mientras que las queries del programa la referenciaban como "descripcion", sin acento. Esta discrepancia, aparentemente menor, generó errores silenciosos que llevaron tiempo considerable en ser detectados e identificados como causa raíz.


#### Lecciones de Organización y Trabajo en Equipo

- Leccion 1 : El uso de ramas, divididas para cada uno de los integrantes, redujo los conflictos de merge en la main, manteniendo constantemente a salvo el proyecto de posibles errores graves.
- Leccion 2 : La utilizacion de nuestro product backlog y las modificaciones semanalmente nos permitio poder dividirnos las tareas de manera ágil y eficiente
---

