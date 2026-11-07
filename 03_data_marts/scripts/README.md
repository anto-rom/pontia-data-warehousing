# Actividad 03 — Data Marts y Data Warehouse

## 1. Objetivo

Diseñar e implementar una arquitectura analítica para Parasol Corp utilizando DuckDB y Python, mediante tres Data Marts independientes y una capa de Data Warehouse que integra información de experimentos, investigación biológica y finanzas.

## 2. Arquitectura

La solución está organizada en cuatro esquemas:

| Esquema | Función |
|---|---|
| `dm_experimentos` | Gestión de laboratorios, investigadores y experimentos |
| `dm_bioresearch` | Gestión de donantes, tipos de muestra y muestras biológicas |
| `dm_finance` | Gestión de departamentos, proyectos y gastos |
| `dw` | Integración analítica mediante vistas SQL |

Cada Data Mart mantiene sus propias tablas y relaciones internas. La integración entre dominios se realiza en el Data Warehouse mediante consultas SQL, evitando dependencias físicas entre Data Marts.

## 3. Modelo de datos

### Data Mart de Experimentos
- `laboratorios`
- `investigadores`
- `experimentos`

### Data Mart de Bioresearch
- `donantes`
- `tipos_muestra`
- `muestras`

### Data Mart de Finanzas
- `departamentos`
- `proyectos`
- `gastos`

Las nueve tablas utilizan claves primarias y las relaciones internas correspondientes se implementan mediante claves foráneas.

## 4. Data Warehouse

Se han creado tres vistas analíticas:

**`dw.v_experimentos_full`**

Integra información de experimentos, investigadores, laboratorios, muestras biológicas, proyectos y gastos correspondientes a 2026.

**`dw.v_coste_por_laboratorio`**

Calcula el número de experimentos, el coste total y el coste medio por laboratorio.

**`dw.v_muestras_alto_riesgo`**

Identifica los experimentos asociados a muestras clasificadas con nivel de riesgo `High`.

Las vistas consultan los datos de origen, por lo que reflejan las modificaciones realizadas en las tablas subyacentes.

## 5. Decisiones de diseño

- Separación de dominios mediante esquemas independientes.
- Integridad referencial mediante claves primarias y foráneas internas.
- Ausencia de claves foráneas entre Data Marts.
- Integración lógica mediante vistas SQL.
- Selección de gastos de 2026 para evitar duplicidades derivadas de múltiples ejercicios presupuestarios.
- Uso de DuckDB como motor analítico.

## 6. Validación

La solución se ha validado mediante las pruebas automatizadas proporcionadas para la actividad.

**Resultado: 17 tests superados de 17 ejecutados.**

También se han realizado comprobaciones de sintaxis con `py_compile` y análisis estático con Ruff.

## 7. Ejecución de pruebas

Desde la raíz del repositorio:

```bash
python -m pytest 03_data_marts/tests/test_03_data_marts.py -v
```

Validación de estilo:

```bash
python -m ruff check 03_data_marts/scripts/data_marts.py
```

## 8. Tecnologías

- Python 3.12
- DuckDB
- SQL
- Pytest
- Ruff
- Jupyter Notebook

## 9. Resultado

Se ha implementado una arquitectura modular que permite consultar información de tres dominios funcionales de manera integrada, manteniendo la independencia de sus modelos operativos.
