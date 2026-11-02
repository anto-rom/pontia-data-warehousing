"""
Tests para la Actividad 05 : Consultas analíticas (queries + comparativa OLTP/OLAP).
"""
import os
import pytest

SCRIPTS_DIR = os.environ.get("ACTIVITY_DIR", "05_consultas_analiticas") + "/scripts"


def load_queries():
    path = os.path.join(SCRIPTS_DIR, "queries.sql")
    if not os.path.exists(path):
        pytest.fail(f"Fichero no encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_oltp_olap():
    path = os.path.join(SCRIPTS_DIR, "oltp_olap.py")
    if not os.path.exists(path):
        pytest.fail(f"Fichero no encontrado: {path}")
    ns = {}
    with open(path, "r", encoding="utf-8") as f:
        exec(f.read(), ns)
    return ns


class TestConsultasAnaliticas:

    def test_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "queries.sql"))

    def test_queries_file_has_content(self):
        content = load_queries()
        assert len(content) > 100, "queries.sql parece demasiado corto"

    def test_q1_group_by_month(self):
        """Q1 debería usar GROUP BY."""
        content = load_queries().lower()
        assert "group by" in content, "Q1 debería usar GROUP BY"

    def test_q1_joins_fact_and_dimensions(self):
        """Las consultas deberían usar JOINs."""
        content = load_queries().lower()
        assert "join" in content, "Las consultas deberían usar JOINs"

    def test_q2_uses_avg(self):
        """Q2 debería usar AVG."""
        content = load_queries().lower()
        assert "avg" in content, "Q2 debería usar AVG"

    def test_q3_filters_risk_level(self):
        """Q3 debería filtrar por risk_level."""
        content = load_queries().lower()
        assert "risk_level" in content, "Q3 debería filtrar por risk_level"

    def test_q4_compares_years(self):
        """Q4 debería comparar 2025 vs 2026."""
        content = load_queries()
        assert "2025" in content, "Q4 debería referenciar 2025"
        assert "2026" in content, "Q4 debería referenciar 2026"

    def test_q5_filters_arklay(self):
        """Q5 debería filtrar por el laboratorio Arklay."""
        content = load_queries().lower()
        assert "arklay" in content, "Q5 debería filtrar por Arklay"

    def test_q6_uses_division(self):
        """Q6 debería calcular coste por muestra (división)."""
        content = load_queries().lower()
        assert "/" in content or "div" in content, "Q6 debería usar división"

    def test_q7_checks_weekend(self):
        """Q7 debería comprobar is_weekend."""
        content = load_queries().lower()
        assert "weekend" in content or "is_weekend" in content, \
            "Q7 debería comprobar is_weekend"

    def test_all_seven_queries(self):
        """Debería haber al menos 7 sentencias SELECT."""
        content = load_queries().upper()
        select_count = content.count("SELECT")
        assert select_count >= 7, \
            f"Se esperaban al menos 7 SELECT, hay {select_count}"


class TestComparativaOLTPvsOLAP:

    def test_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "oltp_olap.py"))

    def test_comparison_exists(self):
        ns = load_oltp_olap()
        assert "oltp_olap_comparison" in ns, \
            "No se encontró la variable 'oltp_olap_comparison'"

    def test_all_fields_filled(self):
        ns = load_oltp_olap()
        comp = ns["oltp_olap_comparison"]
        required = ["oltp_query_type", "olap_query_type", "oltp_rows_affected",
                    "olap_rows_affected", "oltp_optimized_for",
                    "olap_optimized_for", "oltp_use_case", "olap_use_case"]
        for key in required:
            assert key in comp, f"Falta el campo: {key}"
            assert comp[key] != "", f"El campo '{key}' está vacío"

    def test_oltp_simple(self):
        ns = load_oltp_olap()
        val = ns["oltp_olap_comparison"]["oltp_query_type"].lower().strip()
        assert "simple" in val or "sencill" in val, \
            f"Las consultas OLTP deberían ser simples, llegó '{val}'"

    def test_olap_complex(self):
        ns = load_oltp_olap()
        val = ns["oltp_olap_comparison"]["olap_query_type"].lower().strip()
        assert "complex" in val or "complej" in val or "analyt" in val \
            or "analít" in val or "analit" in val, \
            f"Las consultas OLAP deberían ser complejas/analíticas, llegó '{val}'"

    def test_oltp_few_rows(self):
        ns = load_oltp_olap()
        val = ns["oltp_olap_comparison"]["oltp_rows_affected"].lower().strip()
        assert "few" in val or "poc" in val or "one" in val or "una" in val \
            or "small" in val or "reducid" in val or "individual" in val, \
            f"OLTP debería afectar pocas filas, llegó '{val}'"

    def test_olap_many_rows(self):
        ns = load_oltp_olap()
        val = ns["oltp_olap_comparison"]["olap_rows_affected"].lower().strip()
        assert "many" in val or "much" in val or "large" in val or "all" in val \
            or "bulk" in val or "todas" in val or "gran" in val \
            or "millones" in val, \
            f"OLAP debería leer muchas filas, llegó '{val}'"

    def test_oltp_writes(self):
        ns = load_oltp_olap()
        val = ns["oltp_olap_comparison"]["oltp_optimized_for"].lower().strip()
        assert "write" in val or "escrit" in val or "insert" in val \
            or "update" in val or "transaction" in val or "transacc" in val \
            or "delete" in val, \
            f"OLTP debería estar optimizado para escrituras, llegó '{val}'"

    def test_olap_reads(self):
        ns = load_oltp_olap()
        val = ns["oltp_olap_comparison"]["olap_optimized_for"].lower().strip()
        assert "read" in val or "lect" in val or "select" in val \
            or "query" in val or "analyt" in val or "análisis" in val \
            or "analisis" in val or "agregac" in val, \
            f"OLAP debería estar optimizado para lecturas, llegó '{val}'"
