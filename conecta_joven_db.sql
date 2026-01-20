-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-01-2026 a las 06:27:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `conecta_joven_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_actividad_deportiva`
--

CREATE TABLE `p_001_actividad_deportiva` (
  `id_actividad` int(11) NOT NULL,
  `nombre_taller` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL DEFAULT 0.00,
  `id_comuna` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_actividad_deportiva`
--

INSERT INTO `p_001_actividad_deportiva` (`id_actividad`, `nombre_taller`, `precio`, `id_comuna`) VALUES
(1, 'Natación Juvenil - Recrear P24', 15000.00, 1),
(2, 'Boxeo Formativo - Gimnasio Municipal', 0.00, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_articulo_bienestar`
--

CREATE TABLE `p_001_articulo_bienestar` (
  `id_articulo` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `contenido` text NOT NULL,
  `id_autor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_articulo_bienestar`
--

INSERT INTO `p_001_articulo_bienestar` (`id_articulo`, `titulo`, `contenido`, `id_autor`) VALUES
(1, '¿Cómo elegir entre Enfermería y Tec. Médica?', 'Contenido sobre mallas curriculares...', 1),
(2, 'Beneficios del Boxeo en la salud mental', 'El deporte ayuda a liberar estrés...', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_carrera`
--

CREATE TABLE `p_001_carrera` (
  `id_carrera` int(11) NOT NULL,
  `nom_carrera` varchar(100) NOT NULL,
  `tiene_gratuidad` tinyint(1) NOT NULL DEFAULT 0,
  `id_institucion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_carrera`
--

INSERT INTO `p_001_carrera` (`id_carrera`, `nom_carrera`, `tiene_gratuidad`, `id_institucion`) VALUES
(1, 'Tecnología Médica', 1, 2),
(2, 'Enfermería', 1, 2),
(3, 'Reforzamiento PAES Ciencias', 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_comuna`
--

CREATE TABLE `p_001_comuna` (
  `id_comuna` int(11) NOT NULL,
  `nombre_comuna` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_comuna`
--

INSERT INTO `p_001_comuna` (`id_comuna`, `nombre_comuna`) VALUES
(3, 'El Bosque'),
(1, 'La Cisterna'),
(2, 'San Ramón');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_favorito`
--

CREATE TABLE `p_001_favorito` (
  `id_favorito` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_recurso` int(11) NOT NULL,
  `tipo_recurso` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_institucion`
--

CREATE TABLE `p_001_institucion` (
  `id_institucion` int(11) NOT NULL,
  `nombre_inst` varchar(100) NOT NULL,
  `id_comuna` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_institucion`
--

INSERT INTO `p_001_institucion` (`id_institucion`, `nombre_inst`, `id_comuna`) VALUES
(1, 'Preuniversitario Pedro de Valdivia', 1),
(2, 'Universidad de Chile - Facultad de Medicina', 1),
(3, 'Piscina Recrear - Paradero 24', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_rol`
--

CREATE TABLE `p_001_rol` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_rol`
--

INSERT INTO `p_001_rol` (`id_rol`, `nombre_rol`) VALUES
(1, 'Administrador'),
(2, 'Usuario Joven');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `p_001_usuario`
--

CREATE TABLE `p_001_usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre_completo` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `id_rol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `p_001_usuario`
--

INSERT INTO `p_001_usuario` (`id_usuario`, `nombre_completo`, `email`, `password_hash`, `id_rol`) VALUES
(1, 'Stephanie Núñez', 'admin@conectajoven.cl', 'admin123', 1),
(2, 'Eithan', 'eithan.estudiante@gmail.com', 'eithan2025', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `p_001_actividad_deportiva`
--
ALTER TABLE `p_001_actividad_deportiva`
  ADD PRIMARY KEY (`id_actividad`),
  ADD KEY `id_comuna` (`id_comuna`);

--
-- Indices de la tabla `p_001_articulo_bienestar`
--
ALTER TABLE `p_001_articulo_bienestar`
  ADD PRIMARY KEY (`id_articulo`),
  ADD KEY `id_autor` (`id_autor`);

--
-- Indices de la tabla `p_001_carrera`
--
ALTER TABLE `p_001_carrera`
  ADD PRIMARY KEY (`id_carrera`),
  ADD KEY `id_institucion` (`id_institucion`);

--
-- Indices de la tabla `p_001_comuna`
--
ALTER TABLE `p_001_comuna`
  ADD PRIMARY KEY (`id_comuna`),
  ADD UNIQUE KEY `nombre_comuna` (`nombre_comuna`);

--
-- Indices de la tabla `p_001_favorito`
--
ALTER TABLE `p_001_favorito`
  ADD PRIMARY KEY (`id_favorito`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `p_001_institucion`
--
ALTER TABLE `p_001_institucion`
  ADD PRIMARY KEY (`id_institucion`),
  ADD KEY `id_comuna` (`id_comuna`);

--
-- Indices de la tabla `p_001_rol`
--
ALTER TABLE `p_001_rol`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `nombre_rol` (`nombre_rol`);

--
-- Indices de la tabla `p_001_usuario`
--
ALTER TABLE `p_001_usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `p_001_actividad_deportiva`
--
ALTER TABLE `p_001_actividad_deportiva`
  MODIFY `id_actividad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `p_001_articulo_bienestar`
--
ALTER TABLE `p_001_articulo_bienestar`
  MODIFY `id_articulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `p_001_carrera`
--
ALTER TABLE `p_001_carrera`
  MODIFY `id_carrera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `p_001_comuna`
--
ALTER TABLE `p_001_comuna`
  MODIFY `id_comuna` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `p_001_favorito`
--
ALTER TABLE `p_001_favorito`
  MODIFY `id_favorito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `p_001_institucion`
--
ALTER TABLE `p_001_institucion`
  MODIFY `id_institucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `p_001_rol`
--
ALTER TABLE `p_001_rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `p_001_usuario`
--
ALTER TABLE `p_001_usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `p_001_actividad_deportiva`
--
ALTER TABLE `p_001_actividad_deportiva`
  ADD CONSTRAINT `p_001_actividad_deportiva_ibfk_1` FOREIGN KEY (`id_comuna`) REFERENCES `p_001_comuna` (`id_comuna`);

--
-- Filtros para la tabla `p_001_articulo_bienestar`
--
ALTER TABLE `p_001_articulo_bienestar`
  ADD CONSTRAINT `p_001_articulo_bienestar_ibfk_1` FOREIGN KEY (`id_autor`) REFERENCES `p_001_usuario` (`id_usuario`);

--
-- Filtros para la tabla `p_001_carrera`
--
ALTER TABLE `p_001_carrera`
  ADD CONSTRAINT `p_001_carrera_ibfk_1` FOREIGN KEY (`id_institucion`) REFERENCES `p_001_institucion` (`id_institucion`);

--
-- Filtros para la tabla `p_001_favorito`
--
ALTER TABLE `p_001_favorito`
  ADD CONSTRAINT `p_001_favorito_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `p_001_usuario` (`id_usuario`);

--
-- Filtros para la tabla `p_001_institucion`
--
ALTER TABLE `p_001_institucion`
  ADD CONSTRAINT `p_001_institucion_ibfk_1` FOREIGN KEY (`id_comuna`) REFERENCES `p_001_comuna` (`id_comuna`);

--
-- Filtros para la tabla `p_001_usuario`
--
ALTER TABLE `p_001_usuario`
  ADD CONSTRAINT `p_001_usuario_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `p_001_rol` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
