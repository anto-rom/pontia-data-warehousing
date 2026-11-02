# Actividad 05: Consultas analíticas

**Duración:** ~45 minutos
**Objetivo:** responder a las 7 preguntas de negocio de Wesker con SQL analítico
y cerrar con la comparativa OLTP vs OLAP.

---

## Las 7 preguntas

Están en el [brief de Wesker](../BRIEF.md).

## Qué practicarás

1. Consultas con **GROUP BY** y agregaciones
2. **JOIN** entre tablas de hechos y dimensiones
3. **ROLLUP** para subtotales
4. Filtrado por dimensiones y medidas
5. Comparativa **OLTP vs OLAP** (tarea de cierre)

## Cómo empezar

**Opción 1: Docker (recomendado)**

```bash
cd 05_consultas_analiticas
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

1. `scripts/queries.sql` con las 7 consultas + el ROLLUP.
2. `scripts/oltp_olap.py` con la comparativa.
