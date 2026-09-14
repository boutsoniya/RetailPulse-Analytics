-- Core RetailPulse KPIs

SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value,
    ROUND(SUM(profit) / NULLIF(SUM(revenue), 0) * 100, 2) AS profit_margin_pct
FROM sales;

-- Revenue and profit by month
SELECT
    DATE_TRUNC('month', order_date) AS month,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Top products by revenue
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(s.revenue), 2) AS revenue,
    ROUND(SUM(s.profit), 2) AS profit
FROM sales s
JOIN products p ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- Regional performance
SELECT
    c.region,
    ROUND(SUM(s.revenue), 2) AS revenue,
    ROUND(SUM(s.profit), 2) AS profit,
    COUNT(DISTINCT s.order_id) AS orders
FROM sales s
JOIN customers c ON c.customer_id = s.customer_id
GROUP BY c.region
ORDER BY revenue DESC;
