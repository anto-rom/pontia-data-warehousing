# Actividad 02 — Normalización de Bases de Datos

**Máster:** Data Engineering — Pontia  
**Alumno:** Antonio Romero González  
**Identificador:** Antonio.Romero.DE0926

## 1. Objetivo

Aplicar los principios de normalización de bases de datos relacionales hasta la Tercera Forma Normal (3NF), utilizando Python y DuckDB.

El ejercicio parte de una tabla desnormalizada de pedidos y desarrolla un modelo relacional que reduce la redundancia y mejora la integridad de los datos.

## 2. Tecnologías utilizadas

- Python 3.12
- DuckDB
- Pytest
- Ruff
- Visual Studio Code
- Jupyter Notebook

## 3. Datos de partida

La tabla `orders_raw` contiene siete registros con información de pedidos, clientes, productos, cantidades y categorías.

Campos originales:

- `order_id`
- `customer_name`
- `customer_city`
- `product_name`
- `quantity`
- `product_category`

## 4. Proceso de normalización

### Primera Forma Normal (1NF)

Se crea `orders_1nf` con una clave primaria compuesta por `order_id` y `product_name`.

Se conservan los siete registros originales.

### Segunda Forma Normal (2NF)

Se eliminan las dependencias parciales mediante la separación de los datos en tres tablas:

| Tabla | Registros | Clave primaria |
|---|---:|---|
| `orders` | 4 | `order_id` |
| `products` | 6 | `product_name` |
| `order_items` | 7 | `order_id`, `product_name` |

Se incorporan claves foráneas para garantizar la integridad referencial.

### Tercera Forma Normal (3NF)

Se eliminan las dependencias transitivas relacionadas con los clientes.

Se crean:

| Tabla | Registros | Clave primaria |
|---|---:|---|
| `customers` | 3 | `customer_id` |
| `orders_3nf` | 4 | `order_id` |

La tabla `orders_3nf` referencia a `customers` mediante `customer_id`.

## 5. Validación de integridad

Se reconstruyen los siete registros originales mediante operaciones `JOIN` entre las tablas normalizadas.

En el notebook se comprueba también la equivalencia de los datos mediante `EXCEPT ALL`, obteniendo cero diferencias.

El script incluye comprobaciones automáticas de los volúmenes esperados.

## 6. Pruebas automatizadas

Desde la raíz del repositorio:

```bash
python -m pytest 02_normalization/tests/test_02_normalization.py -v
```

Resultado:

**13 tests superados de 13.**

Análisis estático:

```bash
uv run ruff check 02_normalization/scripts/normalization.py
```

Resultado:

**All checks passed!**

## 7. Archivos principales

- `notebook.ipynb`: desarrollo interactivo de la normalización.
- `scripts/normalization.py`: implementación de las transformaciones SQL.
- `scripts/README.md`: documentación de la solución.
- `tests/test_02_normalization.py`: pruebas automatizadas de la actividad.

## 8. Conclusión

Se ha implementado un modelo relacional normalizado hasta 3NF, conservando los siete registros originales y verificando la integridad de las relaciones.

La solución supera los 13 tests automatizados y las comprobaciones de Ruff.