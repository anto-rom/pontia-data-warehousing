"""
Tests for Activity 02 : Normalization (1NF, 2NF, 3NF).
"""
import os
import pytest
import duckdb

SCRIPTS_DIR = os.environ.get("ACTIVITY_DIR", "02_normalization") + "/scripts"


def load_normalization():
    path = os.path.join(SCRIPTS_DIR, "normalization.py")
    if not os.path.exists(path):
        pytest.fail(f"Fichero no encontrado: {path}")
    con = duckdb.connect(":memory:")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace('con = duckdb.connect(":memory:")', '')
    exec(code, {"con": con, "duckdb": duckdb})
    return con


def get_tables(con):
    return [t[0] for t in con.execute("SHOW TABLES").fetchall()]


class TestNormalization:

    def test_file_exists(self):
        assert os.path.exists(os.path.join(SCRIPTS_DIR, "normalization.py"))

    def test_orders_raw_exists(self):
        con = load_normalization()
        tables = get_tables(con)
        assert "orders_raw" in tables, f"orders_raw no encontrada en {tables}"

    def test_orders_raw_has_7_rows(self):
        con = load_normalization()
        count = con.execute("SELECT COUNT(*) FROM orders_raw").fetchone()[0]
        assert count == 7, f"orders_raw debería tener 7 filas, tiene {count}"

    def test_1nf_table_exists(self):
        con = load_normalization()
        tables = get_tables(con)
        has_1nf = any("1nf" in t.lower() for t in tables)
        assert has_1nf, f"No se encontró ninguna tabla 1NF en {tables}"

    def test_1nf_has_composite_pk(self):
        con = load_normalization()
        tables = get_tables(con)
        t1nf = [t for t in tables if "1nf" in t.lower()][0]
        count = con.execute(f"SELECT COUNT(*) FROM {t1nf}").fetchone()[0]
        assert count == 7, f"La tabla 1NF debería tener 7 filas, tiene {count}"

    def test_2nf_orders_table(self):
        con = load_normalization()
        tables = get_tables(con)
        assert "orders" in tables, f"orders (2NF) no encontrada en {tables}"

    def test_2nf_products_table(self):
        con = load_normalization()
        tables = get_tables(con)
        assert "products" in tables, f"products (2NF) no encontrada en {tables}"

    def test_2nf_order_items_table(self):
        con = load_normalization()
        tables = get_tables(con)
        has_items = any("order_item" in t.lower() for t in tables)
        assert has_items, f"order_items (2NF) no encontrada en {tables}"

    def test_2nf_products_have_categories(self):
        con = load_normalization()
        result = con.execute("SELECT COUNT(DISTINCT product_category) FROM products").fetchone()[0]
        assert result >= 2, f"Se esperaban al menos 2 categorías, hay {result}"

    def test_3nf_customers_table(self):
        con = load_normalization()
        tables = get_tables(con)
        assert "customers" in tables, f"customers (3NF) no encontrada en {tables}"

    def test_3nf_orders_reference_customers(self):
        con = load_normalization()
        cols = [c[0] for c in con.execute("DESCRIBE orders_3nf").fetchall()]
        has_fk = "customer_id" in cols
        has_name = "customer_name" in cols
        assert has_fk, f"orders_3nf debería tener customer_id FK. Encontradas: {cols}"
        assert not has_name, f"orders_3nf NO debería tener customer_name (3NF). Encontradas: {cols}"

    def test_join_query_works(self):
        con = load_normalization()
        result = con.execute("""
            SELECT c.customer_name, c.customer_city,
                   oi.product_name, oi.quantity, p.product_category
            FROM orders_3nf o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_name = p.product_name
            ORDER BY o.order_id, oi.product_name
        """).fetchall()
        assert len(result) == 7, f"El JOIN debería devolver 7 filas, devuelve {len(result)}"

    def test_no_redundancy_in_3nf(self):
        con = load_normalization()
        result = con.execute("""
            SELECT customer_name, COUNT(*) as cnt
            FROM customers
            GROUP BY customer_name
            HAVING COUNT(*) > 1
        """).fetchall()
        assert len(result) == 0, f"Clientes duplicados encontrados: {result}"
