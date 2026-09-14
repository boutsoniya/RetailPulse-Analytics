-- RetailPulse analytical schema
-- Compatible with PostgreSQL-style SQL. Adapt SERIAL/DATE syntax as needed for other engines.

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    age INTEGER,
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(20)
);

CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    unit_price DECIMAL(12,2),
    unit_cost DECIMAL(12,2)
);

CREATE TABLE sales (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    channel VARCHAR(30),
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    quantity INTEGER,
    discount_pct DECIMAL(6,2),
    revenue DECIMAL(14,2),
    cost DECIMAL(14,2),
    profit DECIMAL(14,2),
    payment_method VARCHAR(40)
);

CREATE INDEX idx_sales_order_date ON sales(order_date);
CREATE INDEX idx_sales_customer ON sales(customer_id);
CREATE INDEX idx_sales_product ON sales(product_id);
