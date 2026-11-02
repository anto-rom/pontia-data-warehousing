# Actividad 02: Normalización (1NF, 2NF, 3NF)

**Duración:** ~45 minutos
**Objetivo:** normalizar una tabla desnormalizada hasta la Tercera Forma Normal.

---

## Contexto

Parasol Corp tiene una única tabla `orders_raw` que lo almacena todo en un solo
lugar: redundancia y anomalías.

---

## Qué practicarás

1. Aplicar la **1NF** (valores atómicos, PK compuesta)
2. Aplicar la **2NF** (eliminar dependencias parciales)
3. Aplicar la **3NF** (eliminar dependencias transitivas)

---

## Cómo empezar

**Opción 1: Docker (recomendado)**

```bash
cd 02_normalization
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

Completa las celdas TODO del notebook y copia el SQL en
`scripts/normalization.py`.
