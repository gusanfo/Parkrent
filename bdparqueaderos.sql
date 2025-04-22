CREATE TABLE `lugar` (
  `id_lugar` integer PRIMARY KEY,
  `nombre_lugar` varchar(255),
  `id_ubicacion_padre` integer
);

CREATE TABLE `tipoUsuario` (
  `id_tipo_usuario` integer PRIMARY KEY,
  `tipo_usuario` varchar(255)
);

CREATE TABLE `usuarios` (
  `id_usuario` integer PRIMARY KEY,
  `nombre_usuario` integer,
  `correo_usuario` varchar(255),
  `contrasenia` varchar(255)
);

CREATE TABLE `parqueaderos` (
  `id_parqueadero` integer PRIMARY KEY,
  `dueño` integer,
  `id_ubicacion` integer,
  `direccion` varchar(255),
  `largo` double,
  `ancho` double
);

CREATE TABLE `reserva` (
  `id_reserva` integer PRIMARY KEY,
  `id_cliente` integer,
  `id_parqueadero` integer,
  `fecha_inicio` timestamp,
  `fecha_fin` timestamp,
  `costo` double
);

ALTER TABLE `lugar` ADD CONSTRAINT `ubicaUbi` FOREIGN KEY (`id_ubicacion_padre`) REFERENCES `lugar` (`id_lugar`);

CREATE TABLE `tipoUsuario_usuarios` (
  `tipoUsuario_id_tipo_usuario` integer,
  `usuarios_id_tipo_usuario` integer,
  PRIMARY KEY (`tipoUsuario_id_tipo_usuario`, `usuarios_id_tipo_usuario`)
);

ALTER TABLE `tipoUsuario_usuarios` ADD CONSTRAINT FOREIGN KEY (`tipoUsuario_id_tipo_usuario`) REFERENCES `tipoUsuario` (`id_tipo_usuario`);

ALTER TABLE `tipoUsuario_usuarios` ADD CONSTRAINT FOREIGN KEY (`usuarios_id_tipo_usuario`) REFERENCES `usuarios` (`id_usuario`);


ALTER TABLE `parqueaderos` ADD CONSTRAINT `parlug` FOREIGN KEY (`id_ubicacion`) REFERENCES `lugar` (`id_lugar`);

ALTER TABLE `parqueaderos` ADD CONSTRAINT `usulug` FOREIGN KEY (`dueño`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `reserva` ADD CONSTRAINT `rescli` FOREIGN KEY (`id_cliente`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `reserva` ADD CONSTRAINT `respar` FOREIGN KEY (`id_parqueadero`) REFERENCES `parqueaderos` (`id_parqueadero`);
