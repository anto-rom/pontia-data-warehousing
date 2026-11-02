"""
Conftest para el curso de Data Warehousing - Calificacion automatica.

La nota se calcula como el porcentaje de tests superados sobre el total.
Cada actividad tiene el mismo peso en la calificacion final.

Escala: 0 - 10 puntos
"""
import os
import pytest

# Peso de cada actividad (todas iguales)
ACTIVITIES = {
    "01_oltp_modeling": "Actividad 01: Modelado OLTP",
    "02_normalization": "Actividad 02: Normalización",
    "03_data_marts": "Actividad 03: Data Marts",
    "04_star_schema": "Actividad 04: Esquema Estrella",
    "05_consultas_analiticas": "Actividad 05: Consultas Analíticas",
    "06_scd": "Actividad 06: SCD",
}

MAX_GRADE = 10.0


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print a formatted grade summary table."""
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    errors = len(terminalreporter.stats.get("error", []))
    total = passed + failed + errors

    if total == 0:
        return

    # Grade calculation
    grade = (passed / total) * MAX_GRADE if total > 0 else 0

    terminalreporter.write_sep("=", "CALIFICACION DE ACTIVIDADES")
    terminalreporter.write_line(f"  Tests superados:  {passed}")
    terminalreporter.write_line(f"  Tests fallidos:   {failed}")
    terminalreporter.write_line(f"  Errores:          {errors}")
    terminalreporter.write_line(f"  Total tests:      {total}")
    terminalreporter.write_line("")
    terminalreporter.write_line(f"  NOTA ESTIMADA:    {grade:.2f} / {MAX_GRADE:.2f}")
    terminalreporter.write_sep("=")

    # Per-activity breakdown
    terminalreporter.write_line("")
    terminalreporter.write_line("  Desglose por actividad:")

    # Collect results per activity
    activity_stats = {}
    for category in ["passed", "failed", "error"]:
        for rep in terminalreporter.stats.get(category, []):
            # Extract activity name from test location
            nodeid = rep.nodeid
            for act_name in ACTIVITIES:
                if act_name in nodeid:
                    if act_name not in activity_stats:
                        activity_stats[act_name] = {"passed": 0, "failed": 0}
                    if category == "passed":
                        activity_stats[act_name]["passed"] += 1
                    else:
                        activity_stats[act_name]["failed"] += 1

    for act_name, act_label in ACTIVITIES.items():
        stats = activity_stats.get(act_name, {"passed": 0, "failed": 0})
        act_total = stats["passed"] + stats["failed"]
        act_grade = (stats["passed"] / act_total * MAX_GRADE / len(ACTIVITIES)) if act_total > 0 else 0
        status = "OK" if stats["failed"] == 0 and act_total > 0 else ("PENDIENTE" if act_total == 0 else "INCOMPLETO")
        terminalreporter.write_line(f"    {act_label}: {stats['passed']}/{act_total} tests ({status})")

    terminalreporter.write_sep("=")

    # Write to GitHub Actions summary if available
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("\n## Calificacion de Actividades\n\n")
            f.write(f"| Concepto | Valor |\n")
            f.write(f"|----------|-------|\n")
            f.write(f"| Tests superados | {passed} |\n")
            f.write(f"| Tests fallidos | {failed} |\n")
            f.write(f"| Total tests | {total} |\n")
            f.write(f"| **Nota estimada** | **{grade:.2f} / {MAX_GRADE:.2f}** |\n")
            f.write(f"\n### Desglose por actividad\n\n")
            f.write(f"| Actividad | Tests | Estado |\n")
            f.write(f"|-----------|-------|--------|\n")
            for act_name, act_label in ACTIVITIES.items():
                stats = activity_stats.get(act_name, {"passed": 0, "failed": 0})
                act_total = stats["passed"] + stats["failed"]
                status = "OK" if stats["failed"] == 0 and act_total > 0 else ("PENDIENTE" if act_total == 0 else "INCOMPLETO")
                f.write(f"| {act_label} | {stats['passed']}/{act_total} | {status} |\n")
