
import duckdb

con = duckdb.connect(":memory:")

# Tablas de referencia
con.execute("""
CREATE TABLE usuarios (
    usuario_id INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    rol VARCHAR,
    email VARCHAR
);
""")
con.execute("""
INSERT INTO usuarios VALUES
(1, 'Jill Valentine', 'Data Analyst', 'jill@parasol.com'),
(2, 'Rebecca Chambers', 'Data Scientist', 'rebecca@parasol.com'),
(3, 'Chris Redfield', 'Data Engineer', 'chris@parasol.com'),
(4, 'Richard Aiken', 'DBA', 'richard@parasol.com');
""")

con.execute("""
CREATE TABLE laboratorios (
    laboratory_id INTEGER PRIMARY KEY,
    laboratory_name VARCHAR NOT NULL,
    facility_type VARCHAR,
    city VARCHAR,
    country VARCHAR,
    security_level INTEGER,
    opening_date DATE
);
""")
con.execute("""
INSERT INTO laboratorios VALUES
(3, 'Arklay Research Lab', 'Underground Lab', 'Ringtail City', 'USA', 5, '1988-07-12'),
(7, 'Tanuki BioPlant', 'Manufacturing Lab', 'Osaka', 'Japan', 3, '2002-11-30'),
(9, 'Spencer R&D Annex', 'Research Lab', 'Geneva', 'Switzerland', 4, '1995-05-04'),
(11, 'Hive Data Platform', 'Data Center', 'Berlin', 'Germany', 5, '2010-01-15'),
(13, 'Coati Creek Outpost', 'Field Station', 'Coati Creek', 'USA', 2, '2015-09-09');
""")

con.execute("""
CREATE TABLE donantes (
    donante_id INTEGER PRIMARY KEY,
    tipo VARCHAR NOT NULL,
    pais VARCHAR,
    fecha_alta DATE
);
""")
con.execute("""
INSERT INTO donantes VALUES
(1, 'Humano', 'Spain', '2025-11-02'),
(2, 'Humano', 'USA', '2025-12-15'),
(3, 'Animal', 'Japan', '2026-01-10'),
(4, 'Ambiente', 'Germany', '2026-02-01'),
(5, 'Humano', 'Italy', '2026-03-05'),
(6, 'Animal', 'Switzerland', '2026-03-20');
""")

con.execute("""
CREATE TABLE ubicaciones (
    ubicacion_id INTEGER PRIMARY KEY,
    congelador VARCHAR,
    rack VARCHAR,
    posicion VARCHAR,
    temp_c INTEGER
);
""")
con.execute("""
INSERT INTO ubicaciones VALUES
(1, 'Congelador A', 'Rack 1', 'Pos 1', -80),
(2, 'Congelador A', 'Rack 1', 'Pos 2', -80),
(3, 'Congelador A', 'Rack 2', 'Pos 1', -80),
(4, 'Congelador B', 'Rack 1', 'Pos 1', -20),
(5, 'Congelador B', 'Rack 1', 'Pos 2', -20),
(6, 'Congelador C', 'Rack 1', 'Pos 1', 4);
""")

# Entidades operacionales
con.execute("""
CREATE TABLE muestras (
    sample_id INTEGER PRIMARY KEY,
    donante_id INTEGER,
    sample_type VARCHAR NOT NULL,
    collection_date DATE,
    risk_level VARCHAR,
    status VARCHAR,
    received_by INTEGER,
    FOREIGN KEY (donante_id) REFERENCES donantes(donante_id),
    FOREIGN KEY (received_by) REFERENCES usuarios(usuario_id)
);
""")
con.execute("""
INSERT INTO muestras VALUES
(5510, 1, 'Blood', '2026-01-15', 'High', 'Active', 1),
(5511, 1, 'Tissue', '2026-01-15', 'High', 'Active', 1),
(5512, 2, 'Blood', '2026-02-02', 'Medium', 'Active', 2),
(5513, 3, 'Saliva', '2026-02-18', 'Low', 'Active', 2),
(5514, 4, 'Tissue', '2026-03-01', 'Critical', 'Quarantine', 3),
(5515, 5, 'Blood', '2026-03-12', 'Medium', 'Active', 3);
""")

con.execute("""
CREATE TABLE aliquotas (
    aliquota_id INTEGER PRIMARY KEY,
    sample_id INTEGER,
    volumen_ml INTEGER CHECK (volumen_ml > 0),
    estado VARCHAR,
    ubicacion_id INTEGER,
    FOREIGN KEY (sample_id) REFERENCES muestras(sample_id),
    FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(ubicacion_id)
);
""")
con.execute("""
INSERT INTO aliquotas VALUES
(101, 5510, 12, 'Activa', 1),
(102, 5510, 10, 'Activa', 2),
(103, 5511, 8, 'En uso', 3),
(104, 5512, 15, 'Activa', 4),
(105, 5513, 6, 'Activa', 5),
(106, 5514, 9, 'Retenida', 1),
(107, 5515, 11, 'Activa', 2);
""")

con.execute("""
CREATE TABLE movimientos_muestra (
    movimiento_id INTEGER PRIMARY KEY,
    aliquota_id INTEGER,
    ubicacion_origen INTEGER,
    ubicacion_destino INTEGER,
    usuario_id INTEGER,
    fecha TIMESTAMP NOT NULL,
    tipo VARCHAR,
    FOREIGN KEY (aliquota_id) REFERENCES aliquotas(aliquota_id),
    FOREIGN KEY (ubicacion_origen) REFERENCES ubicaciones(ubicacion_id),
    FOREIGN KEY (ubicacion_destino) REFERENCES ubicaciones(ubicacion_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);
""")
con.execute("""
INSERT INTO movimientos_muestra VALUES
(1, 101, NULL, 1, 3, '2026-01-16 10:00:00', 'Entrada'),
(2, 102, NULL, 2, 3, '2026-01-16 10:05:00', 'Entrada'),
(3, 103, 1, 3, 2, '2026-02-20 09:30:00', 'Traslado'),
(4, 104, NULL, 4, 3, '2026-02-03 11:00:00', 'Entrada'),
(5, 105, NULL, 5, 3, '2026-02-25 08:45:00', 'Entrada'),
(6, 106, NULL, 1, 4, '2026-03-02 14:00:00', 'Entrada');
""")

con.execute("""
CREATE TABLE controles_calidad (
    control_id INTEGER PRIMARY KEY,
    aliquota_id INTEGER,
    parametro VARCHAR,
    resultado VARCHAR,
    fecha DATE,
    usuario_id INTEGER,
    FOREIGN KEY (aliquota_id) REFERENCES aliquotas(aliquota_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);
""")
con.execute("""
INSERT INTO controles_calidad VALUES
(1, 101, 'Pureza', 'Pass', '2026-01-20', 2),
(2, 102, 'Volumen', 'Pass', '2026-01-20', 2),
(3, 104, 'Viabilidad', 'Fail', '2026-02-10', 4),
(4, 105, 'Pureza', 'Pass', '2026-03-01', 2),
(5, 106, 'Viabilidad', 'Pass', '2026-03-05', 4);
""")

con.execute("""
CREATE TABLE experimentos (
    experiment_id INTEGER PRIMARY KEY,
    laboratory_id INTEGER,
    usuario_id INTEGER,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    status VARCHAR,
    cost_eur DECIMAL(12,2),
    FOREIGN KEY (laboratory_id) REFERENCES laboratorios(laboratory_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);
""")
con.execute("""
INSERT INTO experimentos VALUES
(87201, 3, 1, '2026-04-01 09:00', '2026-04-01 11:30', 'completed', 1200.00),
(87202, 3, 2, '2026-04-02 09:00', '2026-04-02 12:15', 'completed', 1500.50),
(87203, 7, 1, '2026-04-02 08:00', '2026-04-02 09:30', 'completed', 950.00),
(87204, 7, 3, '2026-04-15 09:12', '2026-04-15 11:48', 'failed', 410.00),
(87205, 9, 2, '2026-04-16 10:00', '2026-04-16 14:00', 'completed', 2200.00),
(87206, 3, 1, '2026-04-18 09:00', '2026-04-18 10:30', 'in progress', 300.00);
""")

con.execute("""
CREATE TABLE experimento_aliquotas (
    experiment_id INTEGER,
    aliquota_id INTEGER,
    cantidad_ml INTEGER,
    PRIMARY KEY (experiment_id, aliquota_id),
    FOREIGN KEY (experiment_id) REFERENCES experimentos(experiment_id),
    FOREIGN KEY (aliquota_id) REFERENCES aliquotas(aliquota_id)
);
""")
con.execute("""
INSERT INTO experimento_aliquotas VALUES
(87201, 101, 12),
(87201, 102, 10),
(87202, 103, 8),
(87203, 104, 15),
(87204, 105, 6),
(87205, 101, 5),
(87205, 106, 9),
(87206, 105, 8);
""")

print("Esquema del biobanco cargado: 10 tablas.")
