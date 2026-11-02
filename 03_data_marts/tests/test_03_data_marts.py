"""
Tests para la Actividad 03 : Data Marts y Data Warehouse.
"""
import os
import pytest
import duckdb

SCRIPTS_DIR = os.environ.get("ACTIVITY_DIR", "03_data_marts") + "/scripts"

ESQUEMAS = ["dm_experimentos", "dm_bioresearch", "dm_finance", "dw"]

TABLAS_POR_MART = {
    "dm_experimentos": ["experimentos", "investigadores", "laboratorios"],
    "dm_bioresearch": ["donantes", "muestras", "tipos_muestra"],
    "dm_finance": ["departamentos", "gastos", "proyectos"],
}

COLUMNAS_REQUERIDAS = {
    ("dm_experimentos", "experimentos"): [
        "experiment_id", "experiment_name", "researcher_id", "lab_id",
        "project_id", "cost_eur", "status",
    ],
    ("dm_experimentos", "investigadores"): ["researcher_id", "researcher_name", "department"],
    ("dm_experimentos", "laboratorios"): ["lab_id", "lab_name", "country"],
    ("dm_bioresearch", "muestras"): ["sample_id", "experiment_id", "donante_id", "sample_type", "risk_level"],
    ("dm_bioresearch", "donantes"): ["donante_id", "tipo", "pais"],
    ("dm_bioresearch", "tipos_muestra"): ["sample_type", "descripcion", "temp_conservacion_c"],
    ("dm_finance", "gastos"): ["gasto_id", "project_id", "year", "budget_eur", "spent_eur"],
    ("dm_finance", "proyectos"): ["project_id", "project_name", "department", "priority"],
    ("dm_finance", "departamentos"): ["department", "director", "centro_coste"],
}

VISTAS_DW = ["v_coste_por_laboratorio", "v_experimentos_full", "v_muestras_alto_riesgo"]


def load_solution():
    path = os.path.join(SCRIPTS_DIR, "data_marts.py")
    if not os.path.exists(path):
        pytest.fail(f"Fichero no encontrado: {path}")
    con = duckdb.connect(":memory:")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace('con = duckdb.connect(":memory:")', '')
    exec(code, {"con": con, "duckdb": duckdb})
    return con


def get_schemas(con):
    return [r[0] for r in con.execute(
        "SELECT schema_name FROM information_schema.schemata"
    ).fetchall()]


def get_tables(con, schema):
    return sorted(t[0] for t in con.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = ? AND table_type = 'BASE TABLE'", [schema]
    ).fetchall())


def get_views(con, schema):
    return sorted(v[0] for v in con.execute(
        "SELECT table_name FROM information_schema.views WHERE table_schema = ?", [schema]
    ).fetchall())


def get_columns(con, schema, table):
    return [c[0] for c in con.execute(f"DESCRIBE {schema}.{table}").fetchall()]


class TestEsquemas:

    def test_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "data_marts.py"))

    def test_los_4_esquemas_existen(self):
        con = load_solution()
        schemas = get_schemas(con)
        for s in ESQUEMAS:
            assert s in schemas, f"El esquema '{s}' no existe. Encontrados: {schemas}"

    def test_cada_mart_tiene_3_tablas(self):
        con = load_solution()
        for schema, tablas in TABLAS_POR_MART.items():
            found = get_tables(con, schema)
            assert sorted(tablas) == found, (
                f"El esquema '{schema}' debe tener exactamente {sorted(tablas)}, tiene {found}"
            )


class TestDataMarts:

    def test_columnas_requeridas(self):
        con = load_solution()
        for (schema, table), cols in COLUMNAS_REQUERIDAS.items():
            found = get_columns(con, schema, table)
            for col in cols:
                assert col in found, (
                    f"Falta la columna '{col}' en {schema}.{table}. Encontradas: {found}"
                )

    def test_claves_primarias(self):
        con = load_solution()
        pks = con.execute("""
            SELECT table_name, COUNT(*) FROM duckdb_constraints()
            WHERE constraint_type = 'PRIMARY KEY'
            GROUP BY table_name
        """).fetchall()
        pks = dict(pks)
        for schema, tablas in TABLAS_POR_MART.items():
            for t in tablas:
                assert pks.get(t, 0) == 1, f"{schema}.{t} debe tener una PRIMARY KEY"

    def test_claves_externas_dentro_de_cada_mart(self):
        con = load_solution()
        fks = con.execute("""
            SELECT schema_name, table_name FROM duckdb_constraints()
            WHERE constraint_type = 'FOREIGN KEY'
        """).fetchall()
        # Cada mart tiene FKs internas: experimentos (2), muestras (2), gastos (1), proyectos (1)
        por_esquema = {}
        for schema, table in fks:
            por_esquema.setdefault(schema, []).append(table)
        for schema in TABLAS_POR_MART:
            assert schema in por_esquema, f"El mart '{schema}' no tiene ninguna FOREIGN KEY interna"

    def test_experimentos_tiene_datos(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM dm_experimentos.experimentos").fetchone()[0]
        assert count >= 5, f"Se esperaban al menos 5 experimentos, hay {count}"

    def test_muestras_tiene_datos(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM dm_bioresearch.muestras").fetchone()[0]
        assert count >= 5, f"Se esperaban al menos 5 muestras, hay {count}"

    def test_gastos_tiene_datos(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM dm_finance.gastos").fetchone()[0]
        assert count >= 5, f"Se esperaban al menos 5 gastos, hay {count}"

    def test_fk_de_experimentos_aplicada(self):
        con = load_solution()
        with pytest.raises(Exception):
            con.execute(
                "INSERT INTO dm_experimentos.experimentos VALUES "
                "(99, 'Bad', 9999, 3, 1, 1.0, 'Completed')"
            )


class TestDataWarehouse:

    def test_los_3_marts_son_independientes(self):
        """No hay FKs entre esquemas: la integracion la hace el DW."""
        con = load_solution()
        fks = con.execute("""
            SELECT schema_name, table_name, referenced_table
            FROM duckdb_constraints() WHERE constraint_type = 'FOREIGN KEY'
        """).fetchall()
        for schema, table, ref in fks:
            ref_schema = con.execute(
                "SELECT table_schema FROM information_schema.tables WHERE table_name = ? "
                "UNION ALL SELECT table_schema FROM information_schema.views WHERE table_name = ?",
                [ref, ref]
            ).fetchall()
            for (rs,) in ref_schema:
                assert rs == schema, (
                    f"{schema}.{table} hace FK a '{ref}' en el esquema '{rs}': "
                    "los marts no deben depender entre si"
                )

    def test_dw_tiene_las_3_vistas(self):
        con = load_solution()
        vistas = get_views(con, "dw")
        assert vistas == VISTAS_DW, f"El esquema dw debe tener {VISTAS_DW}, tiene {vistas}"

    def test_v_experimentos_full_columnas(self):
        con = load_solution()
        cols = get_columns(con, "dw", "v_experimentos_full")
        requeridas = ["experiment_id", "experiment_name", "cost_eur", "researcher_name",
                      "lab_name", "sample_type", "risk_level", "project_name",
                      "budget_eur", "spent_eur"]
        for col in requeridas:
            assert col in cols, f"Falta '{col}' en dw.v_experimentos_full. Encontradas: {cols}"

    def test_v_experimentos_full_integra_los_3_marts(self):
        con = load_solution()
        count = con.execute("SELECT COUNT(*) FROM dw.v_experimentos_full").fetchone()[0]
        assert count >= 5, f"La vista debe integrar al menos 5 experimentos, hay {count}"

    def test_v_coste_por_laboratorio_agrupa(self):
        con = load_solution()
        cols = get_columns(con, "dw", "v_coste_por_laboratorio")
        for col in ["lab_name", "n_experimentos", "coste_total"]:
            assert col in cols, f"Falta '{col}' en dw.v_coste_por_laboratorio. Encontradas: {cols}"
        count = con.execute("SELECT COUNT(*) FROM dw.v_coste_por_laboratorio").fetchone()[0]
        assert count >= 3, f"Se esperaban al menos 3 laboratorios, hay {count}"

    def test_v_muestras_alto_riesgo_filtra(self):
        con = load_solution()
        rows = con.execute(
            "SELECT risk_level FROM dw.v_muestras_alto_riesgo"
        ).fetchall()
        assert len(rows) >= 2, f"Se esperaban al menos 2 muestras de alto riesgo, hay {len(rows)}"
        for (nivel,) in rows:
            assert nivel in ("High", "Alto"), f"La vista debe filtrar risk_level = High, devuelve '{nivel}'"

    def test_vistas_no_copian_datos(self):
        """Las vistas se calculan al consultar: si cambia el mart, cambia la vista."""
        con = load_solution()
        con.execute("""
            INSERT INTO dm_experimentos.experimentos VALUES
            (6, 'Zeta Check', 14, 3, 1, 100.00, 'Completed')
        """)
        con.execute("""
            INSERT INTO dm_bioresearch.muestras VALUES
            (106, 6, 1, 'Blood', 'High')
        """)
        count = con.execute("SELECT COUNT(*) FROM dw.v_experimentos_full").fetchone()[0]
        assert count >= 6, (
            "Tras insertar en los marts, dw.v_experimentos_full debe reflejarlo "
            f"(no copia datos). Filas: {count}"
        )
