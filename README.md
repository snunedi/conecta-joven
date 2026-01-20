Conecta Joven: Plataforma Integral de Apoyo Juvenil
1. Descripción del Proyecto
Conecta Joven es una solución tecnológica desarrollada como respuesta a la fragmentación de información que enfrentan los adolescentes en Chile. La plataforma centraliza recursos críticos en tres áreas fundamentales: Orientación Vocacional, Salud Mental y Deporte. Diseñada bajo un enfoque de factor protector, busca reducir la ansiedad y el estrés asociados a la toma de decisiones en la transición a la vida adulta.

2. Stack Tecnológico (Arquitectura)
El sistema se basa en una arquitectura de tres capas, utilizando tecnologías modernas de código abierto:

Backend: Python 3.12 con el micro-framework Flask.

Frontend: Interfaz responsiva construida con HTML5, JavaScript y CSS3 Modular.

Base de Datos: MySQL 8.0 hospedada en la nube mediante el servicio gestionado de Aiven.

Seguridad: Implementación de hashing de contraseñas mediante Werkzeug (Scrypt) y protocolos de conexión segura SSL/TLS.

Despliegue/Hosting: Repositorio en GitHub y publicación mediante Render.

3. Estructura de Datos (Normalización)
La persistencia de la información se garantiza mediante un modelo relacional normalizado en su Tercera Forma Normal (3FN), compuesto por 8 tablas maestras:

p_001_usuario / p_001_rol: Gestión de acceso basado en roles (RBAC).

p_001_comuna: Maestro geográfico para normalización territorial.

p_001_articulo_bienestar: Repositorio de guías de salud mental.

p_001_actividad_deportiva: Catálogo de oferta recreativa comunal.

p_001_carrera: Guía académica y de beneficios estatales (FUAS).

p_001_favorito: Tabla de intersección para la personalización de recursos.

4. Instalación y Configuración Local
Clonar el proyecto: git clone https://github.com/snunedi/conecta-joven.git

Preparar el entorno: pip install -r requirements.txt

Variables de Entorno: Configurar los parámetros de conexión (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) y el certificado ca.pem para la conexión segura con Aiven.

Ejecutar servidor: python app.py

5. Ciberseguridad Aplicada
Se han implementado rigurosas medidas para proteger el ciclo de vida del dato:

Protección de Credenciales: Las contraseñas se almacenan mediante hashes criptográficos, impidiendo su lectura en texto plano incluso ante accesos no autorizados a la base de datos.

Validación de Sesiones: Control estricto de rutas mediante el objeto session de Flask, asegurando que el panel administrativo sea inaccesible para usuarios sin privilegios.

Integridad en el Despliegue: Uso de GitHub Push Protection para el escaneo y bloqueo preventivo de fugas de secretos en el código fuente.

6. Acceso para Revisión Docente (Cuentas Demo)
Perfil Administrador: snunedi@gmail.com | admin123

Perfil Estudiante: eithan.estudiante@gmail.com | estudiante123
