"""
Tests for Activity 04 : Star Schema and DW Architecture.
"""
import os
import pytest
import duckdb

SCRIPTS_DIR = os.environ.get("ACTIVITY_DIR", "04_star_schema") + "/scripts"
SOURCE_DIR = os.environ.get("ACTIVITY_DIR", "04_star_schema") + "/source"


def load_solution():
    path = os.path.join(SCRIPTS_DIR, "star_schema_layers.py")
    if not os.path.exists(path):
        pytest.fail(f"Fichero no encontrado: {path}")
    con = duckdb.connect(":memory:")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace('con = duckdb.connect(":memory:")', '')
    exec(code, {"con": con, "duckdb": duckdb, "__file__": path})
    return con


def get_tables(con):
    return [t[0] for t in con.execute("SHOW TABLES").fetchall()]


def get_columns(con, table):
    return [c[0] for c in con.execute(f"DESCRIBE {table}").fetchall()]


class TestSourceLayer:

    def test_experimentos_csv_exists(self):
        assert os.path.exists(os.path.join(SOURCE_DIR, "experimentos_raw.csv"))

    def test_investigadores_csv_exists(self):
        assert os.path.exists(os.path.join(SOURCE_DIR, "investigadores_raw.csv"))

    def test_laboratorios_csv_exists(self):
        assert os.path.exists(os.path.join(SOURCE_DIR, "laboratorios_raw.csv"))


class TestStagingLayer:

    def test_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "star_schema_layers.py"))

    def test_staging_experimentos_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "staging_experimentos" in tables, f"staging_experimentos no encontrada en {tables}"

    def test_staging_investigadores_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "staging_investigadores" in tables, f"staging_investigadores no encontrada en {tables}"

    def test_staging_laboratorios_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "staging_laboratorios" in tables, f"staging_laboratorios no encontrada en {tables}"

    def test_staging_experimentos_has_data(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM staging_experimentos").fetchone()[0]
        assert count >= 10, f"Se esperaban al menos 10 experimentos, hay {count}"

    def test_staging_investigadores_has_data(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM staging_investigadores").fetchone()[0]
        assert count >= 5, f"Se esperaban al menos 5 investigadores, hay {count}"


class TestStorageLayer:

    def test_laboratory_dim_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "laboratory_dim" in tables, f"laboratory_dim no encontrada en {tables}"

    def test_researcher_dim_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "researcher_dim" in tables, f"researcher_dim no encontrada en {tables}"

    def test_date_dim_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "date_dim" in tables, f"date_dim no encontrada en {tables}"

    def test_experiment_fact_exists(self):
        con = load_solution()
        tables = get_tables(con)
        assert "experiment_fact" in tables, f"experiment_fact no encontrada en {tables}"

    def test_experiment_fact_columns(self):
        con = load_solution()
        cols = get_columns(con, "experiment_fact")
        required = ["experiment_id", "laboratory_id", "researcher_id", "date_id", "experiment_cost"]
        for col in required:
            assert col in cols, f"Falta la columna '{col}' en experiment_fact. Encontradas: {cols}"

    def test_experiment_fact_has_data(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM experiment_fact").fetchone()[0]
        assert count >= 10, f"Se esperaban al menos 10 experimentos, hay {count}"

    def test_join_query_works(self):
        con = load_solution()
        result = con.execute("""
            SELECT l.laboratory_name, SUM(f.experiment_cost) as total_cost
            FROM experiment_fact f
            JOIN laboratory_dim l ON f.laboratory_id = l.laboratory_id
            GROUP BY l.laboratory_name
        """).fetchall()
        assert len(result) >= 3, f"Se esperaban al menos 3 laboratorios en el resultado, hay {len(result)}"
