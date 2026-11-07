# ruff: noqa: F821
# Actividad 04 - Star Schema and DW Architecture
# La conexion 'con' es proporcionada por el entorno de ejecucion.

from pathlib import Path

# ============================================================
# 1. SOURCE - LOCALIZACION DE LOS CSV
# ============================================================

SOURCE_DIR = Path(__file__).resolve().parent.parent / "source"

experimentos_csv = SOURCE_DIR / "experimentos_raw.csv"
investigadores_csv = SOURCE_DIR / "investigadores_raw.csv"
laboratorios_csv = SOURCE_DIR / "laboratorios_raw.csv"

# ============================================================
# 2. STAGING - INGESTA DE DATOS
# ============================================================

con.execute(
    """
    CREATE TABLE staging_experimentos AS
    SELECT *
    FROM read_csv_auto(?);
    """,
    [str(experimentos_csv)],
)

con.execute(
    """
    CREATE TABLE staging_investigadores AS
    SELECT *
    FROM read_csv_auto(?);
    """,
    [str(investigadores_csv)],
)

con.execute(
    """
    CREATE TABLE staging_laboratorios AS
    SELECT *
    FROM read_csv_auto(?);
    """,
    [str(laboratorios_csv)],
)

# ============================================================
# 3. STORAGE - DIMENSIONES
# ============================================================

con.execute("""
    CREATE TABLE laboratory_dim (
        laboratory_id INTEGER PRIMARY KEY,
        laboratory_name VARCHAR NOT NULL,
        city VARCHAR,
        country VARCHAR,
        security_level INTEGER
    );
""")

con.execute("""
    INSERT INTO laboratory_dim
    SELECT
        lab_id,
        lab_name,
        city,
        country,
        security_level
    FROM staging_laboratorios;
""")

con.execute("""
    CREATE TABLE researcher_dim (
        researcher_id INTEGER PRIMARY KEY,
        researcher_name VARCHAR NOT NULL,
        department VARCHAR,
        position VARCHAR,
        hire_date DATE,
        country VARCHAR
    );
""")

con.execute("""
    INSERT INTO researcher_dim
    SELECT
        researcher_id,
        full_name,
        department,
        position,
        CAST(hire_date AS DATE),
        country
    FROM staging_investigadores;
""")

con.execute("""
    CREATE TABLE date_dim (
        date_id INTEGER PRIMARY KEY,
        full_date DATE NOT NULL,
        day INTEGER,
        month INTEGER,
        quarter INTEGER,
        year INTEGER,
        month_name VARCHAR,
        day_of_week VARCHAR
    );
""")

con.execute("""
    INSERT INTO date_dim
    SELECT DISTINCT
        CAST(STRFTIME(CAST(experiment_date AS DATE), '%Y%m%d') AS INTEGER),
        CAST(experiment_date AS DATE),
        DAY(CAST(experiment_date AS DATE)),
        MONTH(CAST(experiment_date AS DATE)),
        QUARTER(CAST(experiment_date AS DATE)),
        YEAR(CAST(experiment_date AS DATE)),
        STRFTIME(CAST(experiment_date AS DATE), '%B'),
        STRFTIME(CAST(experiment_date AS DATE), '%A')
    FROM staging_experimentos
    WHERE experiment_date IS NOT NULL;
""")

# ============================================================
# 4. STORAGE - TABLA DE HECHOS
# ============================================================

con.execute("""
    CREATE TABLE experiment_fact (
        experiment_id INTEGER PRIMARY KEY,
        laboratory_id INTEGER NOT NULL,
        researcher_id INTEGER NOT NULL,
        date_id INTEGER NOT NULL,
        experiment_cost DECIMAL(12,2),
        sample_type VARCHAR,
        status VARCHAR,

        FOREIGN KEY (laboratory_id)
            REFERENCES laboratory_dim(laboratory_id),

        FOREIGN KEY (researcher_id)
            REFERENCES researcher_dim(researcher_id),

        FOREIGN KEY (date_id)
            REFERENCES date_dim(date_id)
    );
""")

con.execute("""
    INSERT INTO experiment_fact (
        experiment_id,
        laboratory_id,
        researcher_id,
        date_id,
        experiment_cost,
        sample_type,
        status
    )
    SELECT
        e.experiment_id,
        l.laboratory_id,
        r.researcher_id,
        d.date_id,
        CAST(e.cost_eur AS DECIMAL(12,2)),
        e.sample_type,
        e.status

    FROM staging_experimentos AS e

    INNER JOIN laboratory_dim AS l
        ON e.lab_name = l.laboratory_name

    INNER JOIN researcher_dim AS r
        ON e.researcher_name = r.researcher_name

    INNER JOIN date_dim AS d
        ON CAST(e.experiment_date AS DATE) = d.full_date;
""")

