-- Crear base de datos
CREATE DATABASE IF NOT EXISTS todo_app;
USE todo_app;

-- Tabla de proyectos
CREATE TABLE proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uniqueid CHAR(36) DEFAULT (UUID()),
    nombre VARCHAR(1000) NOT NULL,
    estado ENUM('abierto', 'cerrado') DEFAULT 'abierto',
    creado_por INT,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    modificado_por INT NULL,
    modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);
-- Tabla de sprints
CREATE TABLE sprints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uniqueid CHAR(36)  NOT NULL UNIQUE DEFAULT (UUID()),
    nombre VARCHAR(255) NOT NULL,
    proyecto_id INT NOT NULL,
    estado ENUM('abierto', 'cerrado') DEFAULT 'abierto',
    creado_por INT,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    modificado_por INT NULL,
    modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
);

-- Tabla de tareas
CREATE TABLE tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uniqueid CHAR(36)  NOT NULL UNIQUE DEFAULT (UUID()),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATETIME,
    fecha_fin DATETIME,
    sprint_id INT NOT NULL,
    estado ENUM('abierta', 'cancelada', 'cerrada') DEFAULT 'abierta',
    prioridad ENUM('normal', 'urgente') DEFAULT 'normal',
    archivo_adjunto VARCHAR(255),
    creado_por INT,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    modificado_por INT NULL,
    modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sprint_id) REFERENCES sprints(id) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_sprints_proyecto ON sprints(proyecto_id);
CREATE INDEX idx_tareas_sprint ON tareas(sprint_id);
CREATE INDEX idx_tareas_estado ON tareas(estado);
CREATE INDEX idx_tareas_prioridad ON tareas(prioridad);

-- Datos de ejemplo
INSERT INTO proyectos (nombre, estado) VALUES 
('Proyecto E-commerce', 'abierto'),
('Sistema de Inventario', 'abierto'),
('App Móvil', 'cerrado');

INSERT INTO sprints (nombre, proyecto_id, estado) VALUES
('Sprint 1 - Autenticación', 1, 'abierto'),
('Sprint 2 - Catálogo', 1, 'abierto'),
('Sprint 1 - Base de datos', 2, 'cerrado'),
('Sprint 2 - Reportes', 2, 'abierto');

INSERT INTO tareas (titulo, descripcion, sprint_id, estado, prioridad) VALUES
('Implementar login', 'Crear sistema de autenticación de usuarios', 1, 'abierta', 'urgente'),
('Diseñar interfaz login', 'Crear mockups y diseño de la página de login', 1, 'cerrada', 'normal'),
('Configurar base de datos', 'Instalar y configurar MySQL', 1, 'cerrada', 'urgente'),
('Crear modelo de productos', 'Definir estructura de datos para productos', 2, 'abierta', 'normal'),
('API de productos', 'Desarrollar endpoints para gestión de productos', 2, 'cancelada', 'normal'),
('Crear tablas inventario', 'Diseñar esquema de base de datos', 3, 'cerrada', 'urgente'),
('Dashboard de reportes', 'Crear interfaz para visualización de reportes', 4, 'abierta', 'normal');