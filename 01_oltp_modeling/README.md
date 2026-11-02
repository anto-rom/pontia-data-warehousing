# Actividad 01: Base de datos OLTP para el biobanco de Parasol Corp

**Duración:** ~90 minutos
**Objetivo:** diseñar la base de datos OLTP del biobanco de Parasol Corp
(muestras, alícuotas, movimientos, experimentos) con relaciones 1:N y N:M, y
practicar transacciones ACID.

---

## Contexto

El biobanco de Parasol Corp recibe muestras biológicas de donantes, las divide
en **alícuotas**, las congela en ubicaciones controladas, registra cada
movimiento y cada control de calidad, y proporciona alícuotas a los experimentos
de los laboratorios.

Caso de negocio: [brief de Wesker](../BRIEF.md).

---

## Qué practicarás

1. Diseño de tablas con **Primary Keys**, **Foreign Keys** y relaciones **1:N**
2. Relaciones **N:M** con **tabla puente**
3. **Ledger de auditoría** (movimientos registrados, nunca borrados)
4. Restricciones **CHECK** e integridad referencial
5. Transacciones **ACID** sobre el propio dominio del biobanco

---

## Cómo empezar

**Opción 1: Docker (recomendado)**

```bash
cd 01_oltp_modeling
docker compose up --build
```

Después abre JupyterLab en tu navegador: http://localhost:8888

**Opción 2: Local**

```bash
pip install duckdb pandas jupyterlab pytest
jupyter lab
```

---

## Pasos

Abre `notebook.ipynb` y sigue las instrucciones paso a paso. Al final tendrás
un modelo de **10 tablas**: 4 de referencia (usuarios, laboratorios, donantes,
ubicaciones) y 6 que diseñas (muestras, alícuotas, movimientos, controles de
calidad, experimentos y la puente experimentos<->alícuotas).

## Verificación

```bash
pytest tests/ -v
```

## Entregable

Copia tus sentencias `CREATE TABLE` e `INSERT INTO` (las 10 tablas) en
`scripts/schema.py`.
