"""
Actividad 02 - Normalización de bases de datos.

Máster en Data Engineering - Pontia.

Objetivo:
Transformar una tabla desnormalizada en un modelo
relacional que cumpla 1NF, 2NF y 3NF.
"""

# La conexión 'con' es proporcionada por el entorno de ejecución.
# Ruff no puede inferir esta dependencia externa.
# ruff: noqa: F821 (undefined name 'con')


# ---------------------------------------------------------
# FASE 1 - DATOS ORIGINALES
# ---------------------------------------------------------

con.execute("""
    CREATE TABLE orders_raw (
        order_id INTEGER,
        customer_name VARCHAR,
        customer_city VARCHAR,
        product_name VARCHAR,
        quantity INTEGER,
        product_category VARCHAR
    );
""")

con.execute("""
    INSERT INTO orders_raw VALUES
    (1, 'Alice Garcia', 'Madrid', 'Laptop', 1, 'Electronics'),
    (1, 'Alice Garcia', 'Madrid', 'Mouse', 2, 'Electronics'),
    (2, 'Bob Smith', 'London', 'Keyboard', 1, 'Electronics'),
    (2, 'Bob Smith', 'London', 'Monitor', 1, 'Electronics'),
    (3, 'Alice Garcia', 'Madrid', 'Headphones', 1, 'Accessories'),
    (4, 'Carol White', 'Paris', 'Laptop', 2, 'Electronics'),
    (4, 'Carol White', 'Paris', 'USB Cable', 3, 'Accessories');
""")

# ---------------------------------------------------------
# FASE 2 - PRIMERA FORMA NORMAL (1NF)
# ---------------------------------------------------------

# Crear tabla con clave primaria compuesta
con.execute("""
    CREATE TABLE orders_1nf (
        order_id INTEGER,
        customer_name VARCHAR,
        customer_city VARCHAR,
        product_name VARCHAR,
        quantity INTEGER,
        product_category VARCHAR,

        PRIMARY KEY (order_id, product_name)
    );
""")

# Copiar los registros originales
con.execute("""
    INSERT INTO orders_1nf (
        order_id,
        customer_name,
        customer_city,
        product_name,
        quantity,
        product_category
    )
    SELECT
        order_id,
        customer_name,
        customer_city,
        product_name,
        quantity,
        product_category
    FROM orders_raw;
""")

print("1NF: tabla orders_1nf creada correctamente.")

# Validar los registros de 1NF
total_1nf = con.execute("""
    SELECT COUNT(*)
    FROM orders_1nf;
""").fetchone()[0]

assert total_1nf == 7, (
    f"Error en 1NF: se esperaban 7 registros y se encontraron {total_1nf}"
)

print(f"Validación 1NF correcta: {total_1nf} registros.")

# ---------------------------------------------------------
# FASE 3 - SEGUNDA FORMA NORMAL (2NF)
# ---------------------------------------------------------

# 1. Crear tabla de pedidos
con.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_name VARCHAR,
        customer_city VARCHAR
    );
""")

# Insertar los cuatro pedidos únicos
con.execute("""
    INSERT INTO orders (
        order_id,
        customer_name,
        customer_city
    )
    SELECT DISTINCT
        order_id,
        customer_name,
        customer_city
    FROM orders_1nf;
""")


# 2. Crear tabla de productos
con.execute("""
    CREATE TABLE products (
        product_name VARCHAR PRIMARY KEY,
        product_category VARCHAR
    );
""")

# Insertar los seis productos únicos
con.execute("""
    INSERT INTO products (
        product_name,
        product_category
    )
    SELECT DISTINCT
        product_name,
        product_category
    FROM orders_1nf;
""")


# 3. Crear tabla de líneas de pedido
con.execute("""
    CREATE TABLE order_items (
        order_id INTEGER,
        product_name VARCHAR,
        quantity INTEGER,

        PRIMARY KEY (order_id, product_name),

        FOREIGN KEY (order_id)
            REFERENCES orders(order_id),

        FOREIGN KEY (product_name)
            REFERENCES products(product_name)
    );
""")

# Insertar las siete líneas de pedido
con.execute("""
    INSERT INTO order_items (
        order_id,
        product_name,
        quantity
    )
    SELECT
        order_id,
        product_name,
        quantity
    FROM orders_1nf;
""")

print("2NF: tablas orders, products y order_items creadas correctamente.")

# ---------------------------------------------------------
# VALIDACIONES DE 2NF
# ---------------------------------------------------------

total_orders = con.execute("""
    SELECT COUNT(*) FROM orders;
""").fetchone()[0]

total_products = con.execute("""
    SELECT COUNT(*) FROM products;
""").fetchone()[0]

total_items = con.execute("""
    SELECT COUNT(*) FROM order_items;
""").fetchone()[0]

assert total_orders == 4, (
    f"Error: se esperaban 4 pedidos y se encontraron {total_orders}"
)

assert total_products == 6, (
    f"Error: se esperaban 6 productos y se encontraron {total_products}"
)

assert total_items == 7, (
    f"Error: se esperaban 7 líneas y se encontraron {total_items}"
)

print(
    f"Validación 2NF correcta: "
    f"{total_orders} pedidos, "
    f"{total_products} productos y "
    f"{total_items} líneas."
)

# ---------------------------------------------------------
# FASE 4 - TERCERA FORMA NORMAL (3NF)
# ---------------------------------------------------------

# 1. Crear tabla de clientes
con.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name VARCHAR NOT NULL UNIQUE,
        customer_city VARCHAR NOT NULL
    );
""")

# Insertar clientes únicos y asignar identificadores
con.execute("""
    INSERT INTO customers (
        customer_id,
        customer_name,
        customer_city
    )
    SELECT
        ROW_NUMBER() OVER (ORDER BY customer_name),
        customer_name,
        customer_city
    FROM (
        SELECT DISTINCT
            customer_name,
            customer_city
        FROM orders
    ) AS unique_customers;
""")


# 2. Crear tabla de pedidos normalizada
con.execute("""
    CREATE TABLE orders_3nf (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,

        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    );
""")

# Relacionar pedidos con clientes mediante customer_id
con.execute("""
    INSERT INTO orders_3nf (
        order_id,
        customer_id
    )
    SELECT
        o.order_id,
        c.customer_id
    FROM orders AS o
    JOIN customers AS c
        ON o.customer_name = c.customer_name;
""")

print("3NF: tablas customers y orders_3nf creadas correctamente.")

# ---------------------------------------------------------
# VALIDACIONES DE 3NF
# ---------------------------------------------------------

total_customers = con.execute("""
    SELECT COUNT(*) FROM customers;
""").fetchone()[0]

total_orders_3nf = con.execute("""
    SELECT COUNT(*) FROM orders_3nf;
""").fetchone()[0]

assert total_customers == 3, (
    f"Se esperaban 3 clientes y se encontraron {total_customers}"
)

assert total_orders_3nf == 4, (
    f"Se esperaban 4 pedidos y se encontraron {total_orders_3nf}"
)

# Reconstruir los registros originales mediante JOIN
total_reconstructed = con.execute("""
    SELECT COUNT(*)
    FROM orders_3nf AS o
    JOIN customers AS c
        ON o.customer_id = c.customer_id
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    JOIN products AS p
        ON oi.product_name = p.product_name;
""").fetchone()[0]

assert total_reconstructed == 7, (
    f"Se esperaban 7 registros reconstruidos y "
    f"se encontraron {total_reconstructed}"
)

print(
    f"Validación 3NF correcta: "
    f"{total_customers} clientes, "
    f"{total_orders_3nf} pedidos y "
    f"{total_reconstructed} registros reconstruidos."
)