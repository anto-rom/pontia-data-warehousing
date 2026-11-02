"""
Tests para la Actividad 06 : Slowly Changing Dimensions.
"""
import os
import pytest

SCRIPTS_DIR = os.environ.get("ACTIVITY_DIR", "06_scd") + "/scripts"


def load_scd():
    path = os.path.join(SCRIPTS_DIR, "scd.py")
    if not os.path.exists(path):
        pytest.fail(f"Fichero no encontrado: {path}")
    ns = {}
    with open(path, "r", encoding="utf-8") as f:
        exec(f.read(), ns)
    return ns


class TestSCD:

    def test_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "scd.py"))

    def test_type1_overwrite_exists(self):
        """El Tipo I debería tener una sentencia UPDATE."""
        path = os.path.join(SCRIPTS_DIR, "scd.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        assert "update" in content, "El Tipo I debería usar UPDATE para sobrescribir"

    def test_type2_has_surrogate_key(self):
        """El Tipo II debería usar una surrogate key (researcher_sk)."""
        path = os.path.join(SCRIPTS_DIR, "scd.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        assert "researcher_sk" in content or "surrogate" in content, \
            "El Tipo II debería usar una surrogate key"

    def test_type2_has_validity_dates(self):
        """El Tipo II debería tener columnas valid_from y valid_to."""
        path = os.path.join(SCRIPTS_DIR, "scd.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        assert "valid_from" in content, "El Tipo II debería tener la columna valid_from"
        assert "valid_to" in content, "El Tipo II debería tener la columna valid_to"

    def test_type2_has_is_current(self):
        """El Tipo II debería tener el flag is_current."""
        path = os.path.join(SCRIPTS_DIR, "scd.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        assert "is_current" in content, "El Tipo II debería tener la columna is_current"

    def test_type3_has_previous_columns(self):
        """El Tipo III debería tener columnas previous_*."""
        path = os.path.join(SCRIPTS_DIR, "scd.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        assert "previous_" in content, "El Tipo III debería tener columnas previous_*"

    def test_recommendation_exists(self):
        """Debería recomendar un tipo de SCD."""
        ns = load_scd()
        assert "scd_recommendation" in ns, "No se encontró la variable 'scd_recommendation'"
        val = ns["scd_recommendation"].strip()
        assert val != "", "scd_recommendation está vacía"
        assert any(t in val for t in ["Type I", "Type II", "Type III",
                                      "type i", "type ii", "type iii"]), \
            f"La recomendación debería ser 'Type I', 'Type II' o 'Type III', llegó '{val}'"

    def test_justification_exists(self):
        """Debería justificar su recomendación."""
        ns = load_scd()
        assert "scd_justification" in ns, "No se encontró la variable 'scd_justification'"
        val = ns["scd_justification"].strip()
        assert len(val) > 20, f"Justificación demasiado corta: '{val}'"
