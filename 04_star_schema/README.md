# Actividad 04: Esquema Estrella y Arquitectura del Data Warehouse

**Duración:** ~60 minutos
**Objetivo:** diseñar un esquema estrella con el enfoque de Kimball e
implementarlo a través de las capas del DW (Source, Staging, Storage).

---

## Contexto

Las preguntas de negocio que debe responder el warehouse están en el
[brief de Wesker](../BRIEF.md).

## Qué practicarás

1. Aplicar los **4 pasos de Kimball** para diseñar un esquema estrella
2. Declarar el **grain** del modelo
3. Identificar **dimensiones** y **hechos**
4. Mover datos a través de las **capas del DW**

## Estructura

| Parte | Contenido |
|-------|-----------|
| Pasos 1-4 | Diseño del esquema estrella (Kimball) |
| 1 | Source: explorar datos crudos (CSV) |
| 2 | Staging: cargar y limpiar datos |
| 3 | Storage: construir el DW (esquema estrella) |

## Cómo empezar

**Opción 1: Docker (recomendado)**

```bash
cd 04_star_schema
docker compose up --build
```

Después abre JupyterLab en tu navegador: http://localhost:8888

**Opción 2: Local**

```bash
pip install duckdb pandas jupyterlab pytest
jupyter lab
```

## Entregable

Completa las celdas TODO del notebook y copia tu solución en
`scripts/star_schema_layers.py`.

## Verificación

```bash
pytest tests/ -v
```
