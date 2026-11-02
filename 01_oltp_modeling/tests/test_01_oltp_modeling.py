"""
Tests para la Actividad 01 : Base de datos OLTP del biobanco de Parasol Corp.
"""
import os
import pytest
import duckdb

SCRIPTS_DIR = os.environ.get("ACTIVITY_DIR", "01_oltp_modeling") + "/scripts"


def load_schema():
    """Carga el schema.py del alumno y devuelve la conexión DuckDB."""
    schema_path = os.path.join(SCRIPTS_DIR, "schema.py")
    if not os.path.exists(schema_path):
        pytest.fail(f"Fichero schema no encontrado: {schema_path}")

    con = duckdb.connect(":memory:")
    with open(schema_path, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace('con = duckdb.connect(":memory:")', '')
    exec(code, {"con": con, "duckdb": duckdb})
    return con


def get_tables(con):
    return [t[0] for t in con.execute("SHOW TABLES").fetchall()]


def get_columns(con, table):
    return [c[0] for c in con.execute(f"DESCRIBE {table}").fetchall()]


ALL_TABLES = ["usuarios", "laboratorios", "donantes", "ubicaciones",
              "muestras", "aliquotas", "movimientos_muestra",
              "controles_calidad", "experimentos", "experimento_aliquotas"]


class TestEsquema:

    def test_schema_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "schema.py"))

    def test_all_tables_exist(self):
        con = load_schema()
        tables = get_tables(con)
        for name in ALL_TABLES:
            assert name in tables, f"Tabla '{name}' no encontrada. Creadas: {tables}"

    def test_muestras_columns(self):
        con = load_schema()
        cols = get_columns(con, "muestras")
        required = ["sample_id", "donante_id", "sample_type",
                    "risk_level", "status", "received_by"]
        for col in required:
            assert col in cols, f"Falta la columna '{col}' en muestras. Encontradas: {cols}"

    def test_aliquotas_columns(self):
        con = load_schema()
        cols = get_columns(con, "aliquotas")
        required = ["aliquota_id", "sample_id", "volumen_ml",
                    "estado", "ubicacion_id"]
        for col in required:
            assert col in cols, f"Falta la columna '{col}' en aliquotas. Encontradas: {cols}"

    def test_movimientos_columns(self):
        con = load_schema()
        cols = get_columns(con, "movimientos_muestra")
        required = ["movimiento_id", "aliquota_id", "ubicacion_origen",
                    "ubicacion_destino", "usuario_id", "fecha", "tipo"]
        for col in required:
            assert col in cols, \
                f"Falta la columna '{col}' en movimientos_muestra. Encontradas: {cols}"

    def test_controles_calidad_columns(self):
        con = load_schema()
        cols = get_columns(con, "controles_calidad")
        required = ["control_id", "aliquota_id", "parametro",
                    "resultado", "fecha", "usuario_id"]
        for col in required:
            assert col in cols, \
                f"Falta la columna '{col}' en controles_calidad. Encontradas: {cols}"

    def test_experimentos_columns(self):
        con = load_schema()
        cols = get_columns(con, "experimentos")
        required = ["experiment_id", "laboratory_id", "usuario_id",
                    "started_at", "ended_at", "status", "cost_eur"]
        for col in required:
            assert col in cols, f"Falta la columna '{col}' en experimentos. Encontradas: {cols}"

    def test_experimento_aliquotas_columns(self):
        con = load_schema()
        cols = get_columns(con, "experimento_aliquotas")
        required = ["experiment_id", "aliquota_id", "cantidad_ml"]
        for col in required:
            assert col in cols, \
                f"Falta la columna '{col}' en experimento_aliquotas. Encontradas: {cols}"


class TestDatos:

    def test_muestras_has_data(self):
        con = load_schema()
        count = con.execute("SELECT COUNT(*) FROM muestras").fetchone()[0]
        assert count >= 6, f"Se esperaban al menos 6 muestras, hay {count}"

    def test_aliquotas_has_data(self):
        con = load_schema()
        count = con.execute("SELECT COUNT(*) FROM aliquotas").fetchone()[0]
        assert count >= 7, f"Se esperaban al menos 7 alícuotas, hay {count}"

    def test_movimientos_has_data(self):
        con = load_schema()
        count = con.execute("SELECT COUNT(*) FROM movimientos_muestra").fetchone()[0]
        assert count >= 5, f"Se esperaban al menos 5 movimientos, hay {count}"

    def test_controles_calidad_has_data(self):
        con = load_schema()
        count = con.execute("SELECT COUNT(*) FROM controles_calidad").fetchone()[0]
        assert count >= 4, f"Se esperaban al menos 4 controles, hay {count}"

    def test_experimentos_has_data(self):
        con = load_schema()
        count = con.execute("SELECT COUNT(*) FROM experimentos").fetchone()[0]
        assert count >= 6, f"Se esperaban al menos 6 experimentos, hay {count}"

    def test_experimento_aliquotas_has_data(self):
        con = load_schema()
        count = con.execute("SELECT COUNT(*) FROM experimento_aliquotas").fetchone()[0]
        assert count >= 6, \
            f"Se esperaban al menos 6 filas en la puente, hay {count}"

    def test_total_experiment_cost(self):
        con = load_schema()
        result = con.execute("SELECT SUM(cost_eur) FROM experimentos").fetchone()
        assert result[0] is not None, "El coste total no debería ser NULL"
        assert float(result[0]) > 0, "El coste total debería ser positivo"


class TestRelaciones:

    def test_relacion_1n_muestras_aliquotas(self):
        """Cada muestra puede tener varias alícuotas (1:N)."""
        con = load_schema()
        result = con.execute("""
            SELECT m.sample_id, COUNT(a.aliquota_id) AS num_aliquotas
            FROM muestras m
            JOIN aliquotas a ON a.sample_id = m.sample_id
            GROUP BY m.sample_id
            HAVING COUNT(a.aliquota_id) >= 2
        """).fetchall()
        assert len(result) >= 1, \
            "Debería haber al menos una muestra con 2+ alícuotas (relación 1:N)"

    def test_relacion_nm_varias_aliquotas_por_experimento(self):
        """N:M: un experimento usa varias alícuotas."""
        con = load_schema()
        result = con.execute("""
            SELECT ea.experiment_id, COUNT(*) AS num_aliquotas
            FROM experimento_aliquotas ea
            GROUP BY ea.experiment_id
            HAVING COUNT(*) >= 2
        """).fetchall()
        assert len(result) >= 1, \
            "Debería haber al menos un experimento con 2+ alícuotas (N:M)"

    def test_relacion_nm_aliquota_en_varios_experimentos(self):
        """N:M: una alícuota se usa en varios experimentos."""
        con = load_schema()
        result = con.execute("""
            SELECT ea.aliquota_id, COUNT(*) AS num_experimentos
            FROM experimento_aliquotas ea
            GROUP BY ea.aliquota_id
            HAVING COUNT(*) >= 2
        """).fetchall()
        assert len(result) >= 1, \
            "Debería haber al menos una alícuota usada en 2+ experimentos (N:M)"

    def test_join_experimentos_con_aliquotas(self):
        con = load_schema()
        result = con.execute("""
            SELECT e.experiment_id, a.aliquota_id
            FROM experimentos e
            JOIN experimento_aliquotas ea ON ea.experiment_id = e.experiment_id
            JOIN aliquotas a ON a.aliquota_id = ea.aliquota_id
            LIMIT 5
        """).fetchall()
        assert len(result) >= 1, "El JOIN N:M experimentos↔alícuotas no devuelve filas"

    def test_join_movimientos_con_aliquotas(self):
        """El ledger se encadena con las alícuotas."""
        con = load_schema()
        result = con.execute("""
            SELECT m.movimiento_id, a.aliquota_id, m.tipo
            FROM movimientos_muestra m
            JOIN aliquotas a ON a.aliquota_id = m.aliquota_id
            LIMIT 5
        """).fetchall()
        assert len(result) >= 1, "El JOIN movimientos↔alícuotas no devuelve filas"

    def test_join_experimentos_con_laboratorios(self):
        con = load_schema()
        result = con.execute("""
            SELECT e.experiment_id, l.laboratory_name
            FROM experimentos e
            JOIN laboratorios l ON l.laboratory_id = e.laboratory_id
            LIMIT 5
        """).fetchall()
        assert len(result) >= 1, "El JOIN experimentos↔laboratorios no devuelve filas"


class TestIntegridad:

    def test_fk_rechaza_referencia_inexistente(self):
        """La FK de experimentos debe rechazar un laboratory_id inexistente."""
        con = load_schema()
        with pytest.raises(Exception):
            con.execute("""
                INSERT INTO experimentos
                VALUES (99999, 999, 1, NULL, NULL, 'test', 0)
            """)

    def test_check_volumen_positivo(self):
        """El CHECK de aliquotas debe rechazar un volumen negativo."""
        con = load_schema()
        with pytest.raises(Exception):
            con.execute("""
                INSERT INTO aliquotas VALUES (99999, 5510, -5, 'Activa', 1)
            """)

    def test_puente_exige_clave_compuesta(self):
        """La PK compuesta de la puente impide duplicar la pareja."""
        con = load_schema()
        with pytest.raises(Exception):
            con.execute("""
                INSERT INTO experimento_aliquotas VALUES (87201, 101, 1)
            """)
