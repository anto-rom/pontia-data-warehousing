
-- ACTIVIDAD 05 - CONSULTAS ANALITICAS
-- Parasol Corp - Preguntas de Wesker

-- Q1: Coste total de experimentos por mes
SELECT
    d.year,
    d.month,
    COUNT(f.experiment_id) AS total_experimentos,
    SUM(f.experiment_cost) AS coste_total,
    ROUND(AVG(f.experiment_cost), 2) AS coste_medio
FROM experiment_fact AS f
JOIN date_dim AS d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Q2: Tiempo medio de procesamiento por laboratorio
SELECT
    l.laboratory_name,
    COUNT(f.experiment_id) AS total_experimentos,
    ROUND(AVG(f.processing_time_minutes), 2) AS tiempo_medio_minutos
FROM experiment_fact AS f
JOIN laboratory_dim AS l ON f.laboratory_id = l.laboratory_id
GROUP BY l.laboratory_name
ORDER BY tiempo_medio_minutos DESC;

-- Q3: Experimentos con muestras de alto riesgo
SELECT
    s.risk_level,
    COUNT(f.experiment_id) AS total_experimentos,
    SUM(f.sample_count) AS total_muestras,
    SUM(f.experiment_cost) AS coste_total
FROM experiment_fact AS f
JOIN sample_dim AS s ON f.sample_id = s.sample_id
WHERE s.risk_level = 'High'
GROUP BY s.risk_level;

-- Q4: Comparativa de costes entre 2025 y 2026
SELECT
    d.year,
    COUNT(f.experiment_id) AS total_experimentos,
    SUM(f.experiment_cost) AS coste_total,
    ROUND(AVG(f.experiment_cost), 2) AS coste_medio
FROM experiment_fact AS f
JOIN date_dim AS d ON f.date_id = d.date_id
WHERE d.year IN (2025, 2026)
GROUP BY d.year
ORDER BY d.year;

-- Q5: Experimentos y costes del laboratorio Arklay
SELECT
    l.laboratory_name,
    COUNT(f.experiment_id) AS total_experimentos,
    SUM(f.experiment_cost) AS coste_total
FROM experiment_fact AS f
JOIN laboratory_dim AS l ON f.laboratory_id = l.laboratory_id
WHERE l.laboratory_name = 'Arklay Research Lab'
GROUP BY l.laboratory_name;

-- Q6: Coste por muestra en cada experimento
SELECT
    f.experiment_id,
    f.experiment_cost,
    f.sample_count,
    ROUND(
        f.experiment_cost / NULLIF(f.sample_count, 0), 2
    ) AS coste_por_muestra
FROM experiment_fact AS f
ORDER BY f.experiment_id;

-- Q7: Comparativa de costes entre laborables y fines de semana
SELECT
    CASE
        WHEN d.is_weekend THEN 'Fin de semana'
        ELSE 'Dia laborable'
    END AS tipo_dia,
    COUNT(f.experiment_id) AS total_experimentos,
    SUM(f.experiment_cost) AS coste_total,
    ROUND(AVG(f.experiment_cost), 2) AS coste_medio
FROM experiment_fact AS f
JOIN date_dim AS d ON f.date_id = d.date_id
GROUP BY d.is_weekend
ORDER BY tipo_dia;
