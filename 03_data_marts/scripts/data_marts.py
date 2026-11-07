# ruff: noqa: F821
# Actividad 03 - Data Marts y Data Warehouse
# La conexión 'con' es proporcionada por el entorno de ejecución.

# ============================================================
# 1. DATA MART: EXPERIMENTOS
# ============================================================

con.execute("""
    CREATE SCHEMA dm_experimentos;
""")

con.execute("""
    CREATE TABLE dm_experimentos.laboratorios (
        lab_id INTEGER PRIMARY KEY,
        lab_name VARCHAR NOT NULL,
        country VARCHAR
    );
""")

con.execute("""
    CREATE TABLE dm_experimentos.investigadores (
        researcher_id INTEGER PRIMARY KEY,
        researcher_name VARCHAR NOT NULL,
        department VARCHAR
    );
""")

con.execute("""
    CREATE TABLE dm_experimentos.experimentos (
        experiment_id INTEGER PRIMARY KEY,
        experiment_name VARCHAR NOT NULL,
        researcher_id INTEGER,
        lab_id INTEGER,
        project_id INTEGER,
        cost_eur DECIMAL(10,2),
        status VARCHAR,

        FOREIGN KEY (researcher_id)
            REFERENCES dm_experimentos.investigadores(researcher_id),

        FOREIGN KEY (lab_id)
            REFERENCES dm_experimentos.laboratorios(lab_id)
    );
""")

# ============================================================
# 2. CARGA DE DATOS: EXPERIMENTOS
# ============================================================

# Laboratorios
con.execute("""
    INSERT INTO dm_experimentos.laboratorios
        (lab_id, lab_name, country)
    VALUES
        (3, 'Arklay Research Lab', 'USA'),
        (7, 'Tanuki BioPlant', 'Japan'),
        (9, 'Spencer R&D Annex', 'Switzerland');
""")

# Investigadores
con.execute("""
    INSERT INTO dm_experimentos.investigadores
        (researcher_id, researcher_name, department)
    VALUES
        (14, 'Rebecca Chambers', 'Bioresearch'),
        (22, 'Marcus Aiken', 'Bioresearch'),
        (30, 'Ada Wong', 'Advanced Research'),
        (31, 'Leon Kennedy', 'Security'),
        (40, 'Claire Redfield', 'Bioresearch');
""")

# Experimentos
con.execute("""
    INSERT INTO dm_experimentos.experimentos
        (experiment_id, experiment_name, researcher_id,
         lab_id, project_id, cost_eur, status)
    VALUES
        (1, 'Alpha Test', 14, 3, 1, 15000.00, 'Completed'),
        (2, 'Beta Trial', 22, 7, 2, 22000.00, 'Completed'),
        (3, 'Gamma Study', 30, 9, 3, 18500.00, 'Failed'),
        (4, 'Delta Analysis', 31, 3, 4, 9500.00, 'Completed'),
        (5, 'Epsilon Probe', 40, 7, 5, 31000.00, 'In Progress');
""")

# ============================================================
# 3. DATA MART: BIORESEARCH
# ============================================================

con.execute("""
    CREATE SCHEMA dm_bioresearch;
""")

con.execute("""
    CREATE TABLE dm_bioresearch.donantes (
        donante_id INTEGER PRIMARY KEY,
        tipo VARCHAR NOT NULL,
        pais VARCHAR
    );
""")

con.execute("""
    CREATE TABLE dm_bioresearch.tipos_muestra (
        sample_type VARCHAR PRIMARY KEY,
        descripcion VARCHAR,
        temp_conservacion_c INTEGER
    );
""")

con.execute("""
    CREATE TABLE dm_bioresearch.muestras (
        sample_id INTEGER PRIMARY KEY,
        experiment_id INTEGER,
        donante_id INTEGER,
        sample_type VARCHAR,
        risk_level VARCHAR,

        FOREIGN KEY (donante_id)
            REFERENCES dm_bioresearch.donantes(donante_id),

        FOREIGN KEY (sample_type)
            REFERENCES dm_bioresearch.tipos_muestra(sample_type)
    );
""")

# ============================================================
# 4. CARGA DE DATOS: BIORESEARCH
# ============================================================

con.execute("""
    INSERT INTO dm_bioresearch.donantes
        (donante_id, tipo, pais)
    VALUES
        (1, 'Humano', 'Spain'),
        (2, 'Humano', 'USA'),
        (3, 'Animal', 'Japan'),
        (4, 'Ambiente', 'Germany');
""")

con.execute("""
    INSERT INTO dm_bioresearch.tipos_muestra
        (sample_type, descripcion, temp_conservacion_c)
    VALUES
        ('Blood', 'Sangre completa', -80),
        ('Tissue', 'Tejido biológico', -80),
        ('Saliva', 'Muestra de saliva', 4),
        ('DNA', 'ADN purificado', -20);
""")

con.execute("""
    INSERT INTO dm_bioresearch.muestras
        (sample_id, experiment_id, donante_id, sample_type, risk_level)
    VALUES
        (101, 1, 1, 'Blood', 'High'),
        (102, 2, 2, 'Tissue', 'Medium'),
        (103, 3, 3, 'Saliva', 'Low'),
        (104, 4, 1, 'Blood', 'High'),
        (105, 5, 4, 'DNA', 'Medium');
""")

# ============================================================
# 5. DATA MART: FINANZAS
# ============================================================

con.execute("""
    CREATE SCHEMA dm_finance;
""")

con.execute("""
    CREATE TABLE dm_finance.departamentos (
        department VARCHAR PRIMARY KEY,
        director VARCHAR,
        centro_coste VARCHAR
    );
""")

con.execute("""
    CREATE TABLE dm_finance.proyectos (
        project_id INTEGER PRIMARY KEY,
        project_name VARCHAR NOT NULL,
        department VARCHAR,
        priority VARCHAR,

        FOREIGN KEY (department)
            REFERENCES dm_finance.departamentos(department)
    );
""")

con.execute("""
    CREATE TABLE dm_finance.gastos (
        gasto_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        year INTEGER,
        budget_eur DECIMAL(12,2),
        spent_eur DECIMAL(12,2),

        FOREIGN KEY (project_id)
            REFERENCES dm_finance.proyectos(project_id)
    );
""")

# ============================================================
# 6. CARGA DE DATOS: FINANZAS
# ============================================================

# Departamentos
con.execute("""
    INSERT INTO dm_finance.departamentos
        (department, director, centro_coste)
    VALUES
        ('Bioresearch', 'Albert Wesker', 'CC-100'),
        ('Advanced Research', 'William Birkin', 'CC-200'),
        ('IT', 'Annette Birkin', 'CC-300'),
        ('Security', 'HUNK', 'CC-400');
""")

# Proyectos
con.execute("""
    INSERT INTO dm_finance.proyectos
        (project_id, project_name, department, priority)
    VALUES
        (1, 'Alpha Protocol', 'Bioresearch', 'High'),
        (2, 'Beta Shield', 'Advanced Research', 'Critical'),
        (3, 'Gamma Guard', 'Bioresearch', 'Medium'),
        (4, 'Delta Stream', 'IT', 'Low'),
        (5, 'Epsilon Lab', 'Security', 'Medium');
""")

# Gastos de 2025 y 2026
con.execute("""
    INSERT INTO dm_finance.gastos
        (gasto_id, project_id, year, budget_eur, spent_eur)
    VALUES
        (1, 1, 2025, 90000.00, 87000.00),
        (2, 1, 2026, 100000.00, 45000.00),
        (3, 2, 2025, 140000.00, 138000.00),
        (4, 2, 2026, 150000.00, 120000.00),
        (5, 3, 2025, 75000.00, 70000.00),
        (6, 3, 2026, 80000.00, 35000.00),
        (7, 4, 2025, 45000.00, 40000.00),
        (8, 4, 2026, 50000.00, 12000.00),
        (9, 5, 2025, 55000.00, 54000.00),
        (10, 5, 2026, 60000.00, 55000.00);
""")

# ============================================================
# 7. DATA WAREHOUSE - INTEGRACIÓN
# ============================================================

con.execute("""
    CREATE SCHEMA dw;
""")

# Vista principal: integra los tres Data Marts
con.execute("""
    CREATE VIEW dw.v_experimentos_full AS
    SELECT
        e.experiment_id,
        e.experiment_name,
        e.status,
        e.cost_eur,
        i.researcher_name,
        i.department AS researcher_department,
        l.lab_name,
        l.country AS lab_country,
        m.sample_type,
        m.risk_level,
        p.project_name,
        p.priority AS project_priority,
        g.budget_eur,
        g.spent_eur
    FROM dm_experimentos.experimentos AS e
    INNER JOIN dm_experimentos.investigadores AS i
        ON e.researcher_id = i.researcher_id
    INNER JOIN dm_experimentos.laboratorios AS l
        ON e.lab_id = l.lab_id
    INNER JOIN dm_bioresearch.muestras AS m
        ON e.experiment_id = m.experiment_id
    INNER JOIN dm_finance.proyectos AS p
        ON e.project_id = p.project_id
    INNER JOIN dm_finance.gastos AS g
        ON p.project_id = g.project_id
        AND g.year = 2026;
""")

# Vista analítica: costes por laboratorio
con.execute("""
    CREATE VIEW dw.v_coste_por_laboratorio AS
    SELECT
        lab_name,
        COUNT(*) AS n_experimentos,
        SUM(cost_eur) AS coste_total,
        AVG(cost_eur) AS coste_medio
    FROM dw.v_experimentos_full
    GROUP BY lab_name;
""")

# Vista de control: muestras de alto riesgo
con.execute("""
    CREATE VIEW dw.v_muestras_alto_riesgo AS
    SELECT
        experiment_id,
        experiment_name,
        sample_type,
        risk_level,
        researcher_name,
        cost_eur
    FROM dw.v_experimentos_full
    WHERE risk_level = 'High';
""")