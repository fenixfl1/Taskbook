-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-08-2020 a las 21:03:20
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `taskbook`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `class_schedule`
--

CREATE TABLE `class_schedule` (
  `id` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `day` char(1) NOT NULL,
  `start_date` time NOT NULL,
  `end_date` time NOT NULL,
  `classroom` varchar(5) NOT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `course`
--

CREATE TABLE `course` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `name` varchar(80) NOT NULL,
  `finished` tinyint(1) DEFAULT NULL,
  `qualification` char(1) DEFAULT NULL,
  `table_name` varchar(10) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `course`
--

INSERT INTO `course` (`id`, `user_id`, `teacher_id`, `name`, `finished`, `qualification`, `table_name`, `state`) VALUES
(1, 1, 1, 'Matemática I', 0, NULL, 'courses', 1),
(2, 1, NULL, 'Teoría de Base de Datos', 0, NULL, 'courses', 1),
(3, 1, NULL, 'Sistema Operativo I', 0, NULL, 'courses', 1),
(4, 1, NULL, 'Diseño de Sistema', 0, NULL, 'courses', 1),
(5, 1, NULL, 'Matematica II', 0, NULL, 'courses', 1),
(6, 1, NULL, 'Calculo I', 0, NULL, 'courses', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `event`
--

CREATE TABLE `event` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `title` varchar(150) NOT NULL,
  `location` varchar(100) NOT NULL,
  `url` text DEFAULT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `comment` varchar(100) DEFAULT NULL,
  `table_name` varchar(10) DEFAULT NULL,
  `finished_in` datetime DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notify`
--

CREATE TABLE `notify` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(250) NOT NULL,
  `msg` text NOT NULL,
  `notify_time` datetime NOT NULL,
  `published_at` datetime DEFAULT NULL,
  `readed` tinyint(1) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `role`
--

INSERT INTO `role` (`id`, `name`, `description`) VALUES
(1, 'Admin', 'Control total de la applicacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles_users`
--

CREATE TABLE `roles_users` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `roles_users`
--

INSERT INTO `roles_users` (`id`, `user_id`, `role_id`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `study_plan`
--

CREATE TABLE `study_plan` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `start_date` date NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `done` tinyint(1) DEFAULT NULL,
  `table_name` varchar(10) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `study_plan`
--

INSERT INTO `study_plan` (`id`, `user_id`, `name`, `start_date`, `created_at`, `done`, `table_name`, `state`) VALUES
(1, 1, 'Curso de Python', '2020-08-25', '2020-08-01 23:19:05', 0, 'study-plan', 1),
(2, 1, 'Curso de SQL', '2020-08-15', '2020-08-01 23:19:49', 0, 'study-plan', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `study_plan_goals`
--

CREATE TABLE `study_plan_goals` (
  `id` int(11) NOT NULL,
  `plan_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `url` text DEFAULT NULL,
  `deadline` datetime NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `table_name` varchar(25) DEFAULT NULL,
  `finished_in` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `done` tinyint(1) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `study_plan_goals`
--

INSERT INTO `study_plan_goals` (`id`, `plan_id`, `title`, `url`, `deadline`, `comment`, `table_name`, `finished_in`, `created_at`, `done`, `state`) VALUES
(1, 1, 'Manejo de Strings', NULL, '2020-08-03 00:00:00', NULL, 'study_plan_goals', NULL, '2020-08-03 16:48:09', 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `name` varchar(80) NOT NULL,
  `assigned_in` datetime DEFAULT NULL,
  `delivery_day` datetime NOT NULL,
  `finished_in` datetime DEFAULT NULL,
  `comment` varchar(150) DEFAULT NULL,
  `table_name` varchar(10) DEFAULT NULL,
  `done` tinyint(1) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `task`
--

INSERT INTO `task` (`id`, `user_id`, `course_id`, `name`, `assigned_in`, `delivery_day`, `finished_in`, `comment`, `table_name`, `done`, `state`) VALUES
(1, 1, 1, 'Números Complejos', '0008-01-02 00:39:00', '2020-08-09 00:00:00', NULL, NULL, 'tasks', 0, 1),
(2, 1, 2, 'Sentencias SQL', '2010-08-01 00:00:00', '2010-08-05 00:00:00', NULL, '', 'tasks', 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `teacher`
--

CREATE TABLE `teacher` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `full_name` varchar(80) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(22) DEFAULT NULL,
  `table_name` varchar(10) DEFAULT NULL,
  `state` tinyint(1) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `teacher`
--

INSERT INTO `teacher` (`id`, `user_id`, `full_name`, `email`, `phone_number`, `table_name`, `state`) VALUES
(1, 1, 'Maria Sanchez', NULL, NULL, 'teachers', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `country` varchar(2) NOT NULL,
  `gender` varchar(3) NOT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `current_login_at` datetime DEFAULT NULL,
  `current_login_ip` varchar(100) DEFAULT NULL,
  `login_count` int(11) DEFAULT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  `table_name` varchar(10) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `email`, `first_name`, `last_name`, `password`, `phone_number`, `country`, `gender`, `last_login_at`, `current_login_at`, `current_login_ip`, `login_count`, `confirmed_at`, `table_name`, `active`) VALUES
(1, 'benjaminfl119@gmail.com', 'Benjamin', 'Rosario', '$6$rounds=656000$Oi6RuqIVJRJm8/0Q$.4/l.I0HQdtxmNh04earOOV2NLhn2UCdaQ0rAhwjp0TPaIlUBT034JNG31.FPYzyNTCJI0WYygnGXRMEDbWlk1', '+18293594707', 'DO', 'M', '2020-08-08 05:59:43', '2020-08-08 17:35:07', '127.0.0.1', 64, '2020-08-01 20:46:15', 'users', 1),
(2, 'tvfenix43@gmail.com', 'benjamin', 'rosario', '$6$rounds=656000$Uh3okkQnU0puZQ6V$clgy4x1ZJk5sDinrGUIr.sZuHMi/SdXyPpJUxmrh1MnTNRJtlyeKYBEkkxAEUa1xI50HwzhxscGEZswGu1.Cz1', '+18098696786', 'DO', 'M', NULL, NULL, NULL, NULL, NULL, 'users', 1),
(3, 'solojuegosfl119@gmail.com', 'benjamin', 'rosario', '$6$rounds=656000$9eGhuYISKQhlYdda$uA7ol0vMCKc6OMmmC/oHie4dnmQyFdsxX/kGA9qTjg74piyh2AX1z.Rlowqmw/Vr.xm.OxqpM.1GxUVq2oRR40', '+18098696786', 'DO', 'M', NULL, NULL, NULL, NULL, NULL, 'users', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `class_schedule`
--
ALTER TABLE `class_schedule`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indices de la tabla `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indices de la tabla `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `notify`
--
ALTER TABLE `notify`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `roles_users`
--
ALTER TABLE `roles_users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `role_id` (`role_id`);

--
-- Indices de la tabla `study_plan`
--
ALTER TABLE `study_plan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `study_plan_goals`
--
ALTER TABLE `study_plan_goals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plan_id` (`plan_id`);

--
-- Indices de la tabla `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indices de la tabla `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `full_name` (`full_name`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `class_schedule`
--
ALTER TABLE `class_schedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `course`
--
ALTER TABLE `course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `event`
--
ALTER TABLE `event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `notify`
--
ALTER TABLE `notify`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `role`
--
ALTER TABLE `role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `roles_users`
--
ALTER TABLE `roles_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `study_plan`
--
ALTER TABLE `study_plan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `study_plan_goals`
--
ALTER TABLE `study_plan_goals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `task`
--
ALTER TABLE `task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `teacher`
--
ALTER TABLE `teacher`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `class_schedule`
--
ALTER TABLE `class_schedule`
  ADD CONSTRAINT `class_schedule_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`);

--
-- Filtros para la tabla `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `notify`
--
ALTER TABLE `notify`
  ADD CONSTRAINT `notify_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `roles_users`
--
ALTER TABLE `roles_users`
  ADD CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);

--
-- Filtros para la tabla `study_plan`
--
ALTER TABLE `study_plan`
  ADD CONSTRAINT `study_plan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `study_plan_goals`
--
ALTER TABLE `study_plan_goals`
  ADD CONSTRAINT `study_plan_goals_ibfk_1` FOREIGN KEY (`plan_id`) REFERENCES `study_plan` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `task`
--
ALTER TABLE `task`
  ADD CONSTRAINT `task_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `task_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `teacher`
--
ALTER TABLE `teacher`
  ADD CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
