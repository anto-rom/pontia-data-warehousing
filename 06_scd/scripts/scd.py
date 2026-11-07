
"""
Actividad 06 - Slowly Changing Dimensions (SCD).

Demostracion de SCD Type I, Type II y Type III con DuckDB.
Cada estrategia utiliza una tabla independiente.
"""

import duckdb


scd_recommendation = "Type II"

scd_justification = (
    "Se recomienda SCD Type II porque conserva el historial completo "
    "de cambios de puesto y departamento de los investigadores. "
    "Las claves sustitutas y las ventanas de validez permiten asociar "
    "cada experimento a la version historica correcta del investigador, "
    "garantizando trazabilidad y precision en el analisis de costes."
)


def create_base_data(con):
    """Crear tabla de hechos con los experimentos originales."""
    con.execute("""
        CREATE TABLE experiment_fact (
            experiment_id INTEGER PRIMARY KEY,
            date_id INTEGER,
            researcher_id INTEGER,
            experiment_cost DECIMAL(12, 2)
        )
    """)

    con.execute("""
        INSERT INTO experiment_fact VALUES
        (9001, 20250115, 1, 1200.00),
        (9002, 20250220, 1, 1500.00),
        (9003, 20260105, 1, 1700.00),
        (9004, 20260410, 1, 1800.00)
    """)


def scd_type1(con):
    """Type I: sobrescribir el valor anterior."""
    con.execute("""
        CREATE TABLE researcher_type1 (
            researcher_id INTEGER PRIMARY KEY,
            researcher_name VARCHAR,
            position VARCHAR,
            department VARCHAR
        )
    """)

    con.execute("""
        INSERT INTO researcher_type1 VALUES
        (1, 'Rebecca Chambers', 'Junior Scientist', 'Bioresearch')
    """)

    con.execute("""
        UPDATE researcher_type1
        SET position = 'Lead Scientist',
            department = 'Bio-Weapons Research'
        WHERE researcher_id = 1
    """)


def scd_type2(con):
    """Type II: conservar versiones historicas con fechas de validez."""
    con.execute("""
        CREATE TABLE researcher_type2 (
            researcher_sk INTEGER PRIMARY KEY,
            researcher_id INTEGER,
            researcher_name VARCHAR,
            position VARCHAR,
            department VARCHAR,
            valid_from DATE,
            valid_to DATE,
            is_current BOOLEAN
        )
    """)

    con.execute("""
        INSERT INTO researcher_type2 VALUES
        (1, 1, 'Rebecca Chambers', 'Junior Scientist',
         'Bioresearch', DATE '2023-09-01', DATE '2026-04-01', FALSE),
        (2, 1, 'Rebecca Chambers', 'Lead Scientist',
         'Bio-Weapons Research', DATE '2026-04-01', NULL, TRUE)
    """)


def scd_type3(con):
    """Type III: conservar el valor actual y el anterior."""
    con.execute("""
        CREATE TABLE researcher_type3 (
            researcher_id INTEGER PRIMARY KEY,
            researcher_name VARCHAR,
            position VARCHAR,
            previous_position VARCHAR,
            department VARCHAR,
            previous_department VARCHAR
        )
    """)

    con.execute("""
        INSERT INTO researcher_type3 VALUES
        (1, 'Rebecca Chambers', 'Junior Scientist', NULL,
         'Bioresearch', NULL)
    """)

    con.execute("""
        UPDATE researcher_type3
        SET previous_position = position,
            previous_department = department,
            position = 'Lead Scientist',
            department = 'Bio-Weapons Research'
        WHERE researcher_id = 1
    """)


def main():
    con = duckdb.connect(":memory:")

    try:
        create_base_data(con)
        scd_type1(con)
        scd_type2(con)
        scd_type3(con)

        print("=== SCD TYPE I ===")
        print(con.execute("SELECT * FROM researcher_type1").df())

        print("\n=== SCD TYPE II ===")
        print(con.execute("SELECT * FROM researcher_type2").df())

        print("\n=== SCD TYPE III ===")
        print(con.execute("SELECT * FROM researcher_type3").df())

        print("\n=== ANALISIS HISTORICO TYPE II ===")

        result = con.execute("""
            SELECT
                r.position,
                COUNT(*) AS total_experiments,
                SUM(f.experiment_cost) AS total_cost
            FROM experiment_fact AS f
            JOIN researcher_type2 AS r
                ON f.researcher_id = r.researcher_id
                AND STRPTIME(
                    CAST(f.date_id AS VARCHAR), '%Y%m%d'
                )::DATE >= r.valid_from
                AND (
                    r.valid_to IS NULL
                    OR STRPTIME(
                        CAST(f.date_id AS VARCHAR), '%Y%m%d'
                    )::DATE < r.valid_to
                )
            GROUP BY r.position
            ORDER BY r.position
        """).df()

        print(result)
        print("\nRecomendacion:", scd_recommendation)
        print("Justificacion:", scd_justification)

    finally:
        con.close()


if __name__ == "__main__":
    main()
