# Actividad 03: Data Marts y Data Warehouse para Parasol Corp

**Duración:** ~60 minutos
**Objetivo:** crear los 3 Data Marts departamentales de Parasol Corp en esquemas
independientes y construir el Data Warehouse con vistas que los integran.

---

## Qué practicarás

1. Crear **esquemas** (`CREATE SCHEMA`) como namespaces para cada data mart
2. Modelar **3 tablas por mart** con sus PK y FK internas
3. Construir un **Data Warehouse** con **vistas** (`CREATE VIEW`) que integran
   los marts sin copiar datos

## Estructura

| Parte | Contenido |
|-------|-----------|
| 1 | `dm_experimentos`: experimentos, investigadores, laboratorios |
| 2 | `dm_bioresearch`: muestras, donantes, tipos_muestra |
| 3 | `dm_finance`: gastos, proyectos, departamentos |
| 4 | `dw`: `v_experimentos_full`, `v_coste_por_laboratorio`, `v_muestras_alto_riesgo` |

## Cómo empezar

**Opción 1: Docker (recomendado)**

```bash
cd 03_data_marts
docker compose up --build
```

Después abre JupyterLab en tu navegador: http://localhost:8888

**Opción 2: Local**

```bash
pip install duckdb pandas jupyterlab pytest
jupyter lab
```

## Entregable

Completa las celdas TODO del notebook y copia tu trabajo en
`scripts/data_marts.py`.

## Verificación

```bash
pytest tests/ -v
```
