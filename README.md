# Data Warehouse: Actividades Prácticas

**Modelado de datos y Data Warehousing** - 2026

---

## Descripción

Repositorio con las **6 actividades prácticas** del curso de Data Warehousing.
En cada actividad construirás, paso a paso, un data warehouse para **Parasol
Corp**, una empresa ficticia de investigación farmacéutica.

El caso de negocio está en [BRIEF.md](BRIEF.md).

---

## Actividades

| # | Tema | Duración |
|---|------|----------|
| 01 | Modelado OLTP (PK, FK, relaciones) + transacciones ACID | ~45 min |
| 02 | Normalización (1NF, 2NF, 3NF) | ~45 min |
| 03 | Data Marts departamentales | ~30 min |
| 04 | Esquema estrella y capas del DW (Kimball) | ~60 min |
| 05 | Consultas analíticas (7 preguntas + ROLLUP) | ~45 min |
| 06 | Slowly Changing Dimensions (módulo final) | ~40 min |

---

## Cómo usar

### Opción 1: Docker (recomendado)

```bash
cd 01_oltp_modeling
docker compose up --build
```

Abre JupyterLab en el navegador: http://localhost:8888

### Opción 2: Local

```bash
pip install duckdb pandas jupyterlab pytest

cd 01_oltp_modeling
jupyter lab
```

### Ejecutar tests

```bash
# Todas las actividades
pytest */tests/ -v

# Una actividad concreta
pytest 01_oltp_modeling/tests/ -v
```

---

## Estructura del repositorio

```
dw_activities/
├── BRIEF.md                   <- Caso de negocio
├── 01_oltp_modeling/
│   ├── notebook.ipynb         <- Abre este fichero
│   ├── tests/                 <- Tests para verificar tu trabajo
│   ├── Dockerfile
│   └── docker-compose.yml
├── 02_normalization/
├── 03_data_marts/
├── 04_star_schema/
│   └── source/                <- Datos crudos de la actividad
├── 05_consultas_analiticas/
├── 06_scd/
└── ...
```

---

## Empresa ficticia: Parasol Corp

> Parasol Corp es una empresa de investigación farmacéutica y biotecnológica
> con laboratorios en todo el mundo. Ver [BRIEF.md](BRIEF.md).

### Personajes

| Rol | Personaje | Responsabilidad |
|-----|-----------|-----------------|
| Data Analyst | Jill Valentine | Preguntas de negocio, validación |
| Data Scientist | Rebecca Chambers | Investigación, modelado |
| Data Engineer | Chris Redfield | ETL, infraestructura |
| DBA | Richard Aiken | Operaciones de base de datos |

---

## Tecnologías

- **DuckDB** - base de datos analítica embebida
- **Python** - pandas, duckdb
- **Jupyter notebooks** - entorno interactivo
- **Docker** - entorno reproducible
- **pytest** - tests automatizados
