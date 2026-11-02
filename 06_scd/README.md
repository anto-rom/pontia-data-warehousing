# Actividad 06: Slowly Changing Dimensions (SCD)

**Duración:** ~40 minutos
**Objetivo:** implementar las tres estrategias SCD (Type I, II, III) sobre la
dimensión `researcher_dim` y compararlas.

> **Módulo final del curso.**

---

## El evento

Rebecca Chambers va a ser ascendida. ¿Cómo rastreamos este cambio en nuestro
Data Warehouse?

## Qué practicarás

1. **SCD Type I**: sobrescribir
2. **SCD Type II**: nueva fila con ventana de validez
3. **SCD Type III**: columna de valor anterior

---

## Cómo empezar

**Opción 1: Docker (recomendado)**

```bash
cd 06_scd
docker compose up --build
```

**Opción 2: Local**

```bash
pip install duckdb pandas jupyterlab pytest
jupyter lab
```

## Verificación

```bash
pytest tests/ -v
```

## Entregable

Completa las celdas TODO del notebook y copia tu solución en `scripts/scd.py`
(incluye `scd_recommendation` y `scd_justification`).
