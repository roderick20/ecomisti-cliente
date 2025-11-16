CREATE TABLE
    tabla_general (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        nombre NVARCHAR (255) NOT NULL,
        parent_id INT NULL,
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_id) REFERENCES tabla_general (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    tipo_cambio (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        fecha DATETIME,
        compra DECIMAL(10, 2),
        venta DECIMAL(10, 2),
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    producto_grupo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        nombre NVARCHAR (255) NOT NULL,
        parent_id INT NULL,
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_id) REFERENCES producto_grupo (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    producto (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        nombre NVARCHAR (255) NOT NULL,
        enlace LONGTEXT NOT NULL,
        abreviatura NVARCHAR (255),
        producto_grupo_id INT,
        producto_unidad_id INT,
        codigo NVARCHAR (255),
        habilitado BOOLEAN DEFAULT TRUE,
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_grupo_id) REFERENCES producto_grupo (id) ON DELETE SET NULL,
        FOREIGN KEY (producto_unidad_id) REFERENCES producto_unidad (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    producto_unidad (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        nombre NVARCHAR (255) NOT NULL,
        abreviatura NVARCHAR (255),
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_grupo_id) REFERENCES producto_grupo (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    producto_imagen (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        producto_id INT,
        path LONGTEXT NOT NULL,
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES producto (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    producto_precio (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        producto_id INT,
        precio_soles DECIMAL(10, 2),
        precio_dolar DECIMAL(10, 2),
        unidad_medida_id INT,
        habilitado BOOLEAN DEFAULT TRUE,
        lista_id INT,
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES producto (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    personeria (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        razon_social LONGTEXT NOT NULL,
        nombre_comercial LONGTEXT NOT NULL,
        tipo_doc NVARCHAR (255),
        numero_doc NVARCHAR (255),
        personeria_tipo INT,
        contacto LONGTEXT NOT NULL,
        telefono LONGTEXT NOT NULL,
        email LONGTEXT NOT NULL,
        cuenta_detraccion LONGTEXT NOT NULL,
        cuenta_cci LONGTEXT NOT NULL,
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    personeria_direccion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        personeria_id INT,
        direccion LONGTEXT NOT NULL,
        departamento NVARCHAR (255),
        provincia NVARCHAR (255),
        ciudad NVARCHAR (255),
        ubigeo NVARCHAR (255),
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (personeria_id) REFERENCES personeria (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    serie_correlativo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        tipo_doc NVARCHAR (255),
        serie NVARCHAR (255),
        correlativo int,        
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    operacion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        tipo_doc NVARCHAR (255),
        serie NVARCHAR (255),
        correlativo NVARCHAR (255),
        fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
        forma_pago NVARCHAR (255),
        tipo_moneda NVARCHAR (255),
        personeria_id INT,
        mto_oper_gravadas DECIMAL(12, 4),
        mto_igv DECIMAL(12, 4),
        total_impuestos DECIMAL(12, 4),
        valor_venta DECIMAL(12, 4),
        sub_total DECIMAL(12, 4),
        mto_imp_venta DECIMAL(12, 4),
        detracion_cod_bien NVARCHAR (255),
        detracion_cod_medio_pago NVARCHAR (255),
        detracion_cta_banco NVARCHAR (255),
        detracion_porcentaje DECIMAL(12, 4),
        detracion_mto DECIMAL(12, 4),
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (personeria_id) REFERENCES personeria (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    operacion_detalle (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uniqueid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID ()),
        operacion_id INT,
        producto_id INT,
        cantidad DECIMAL(12, 4),
        mto_valor_unitario DECIMAL(12, 4),
        mto_valor_venta DECIMAL(12, 4),
        mto_base_igv DECIMAL(12, 4),
        total_impuestos DECIMAL(12, 4),
        mto_precio_unitario DECIMAL(12, 4),
        creado_por INT,
        creado DATETIME DEFAULT CURRENT_TIMESTAMP,
        modificado_por INT NULL,
        modificado TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES producto (id) ON DELETE SET NULL,
        FOREIGN KEY (operacion_id) REFERENCES operacion (id) ON DELETE SET NULL
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;