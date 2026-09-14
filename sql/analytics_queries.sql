-- RetailPulse Analytics: validated business questions
-- Source: data/processed/retail_sales_clean.csv

-- 1. Executive KPIs
SELECT
    SUM(Realized_Sales) AS total_sales,
    SUM(Realized_Profit) AS total_profit,
    ROUND(100.0 * SUM(Realized_Profit) / NULLIF(SUM(Realized_Sales),0), 2) AS profit_margin_pct,
    COUNT(DISTINCT CASE WHEN Order_Status = 'Completed' THEN Order_ID END) AS completed_orders,
    COUNT(DISTINCT Customer_ID) AS customers,
    ROUND(SUM(Realized_Sales) / NULLIF(COUNT(DISTINCT CASE WHEN Order_Status = 'Completed' THEN Order_ID END),0),2) AS avg_order_value
FROM FactSales;

-- 2. Monthly performance
SELECT Month,
       SUM(Realized_Sales) AS sales,
       SUM(Realized_Profit) AS profit,
       COUNT(DISTINCT CASE WHEN Order_Status='Completed' THEN Order_ID END) AS orders
FROM FactSales
GROUP BY Month ORDER BY Month;

-- 3. Region scorecard
SELECT Region,
       SUM(Realized_Sales) AS sales,
       SUM(Realized_Profit) AS profit,
       COUNT(DISTINCT CASE WHEN Order_Status='Completed' THEN Order_ID END) AS orders,
       ROUND(100.0*SUM(Realized_Profit)/NULLIF(SUM(Realized_Sales),0),2) AS margin_pct
FROM FactSales
GROUP BY Region ORDER BY sales DESC;

-- 4. Category profitability
SELECT Category,
       SUM(Realized_Sales) AS sales,
       SUM(Realized_Profit) AS profit,
       ROUND(100.0*SUM(Realized_Profit)/NULLIF(SUM(Realized_Sales),0),2) AS margin_pct,
       ROUND(AVG(Discount_Pct)*100,2) AS avg_discount_pct
FROM FactSales
WHERE Order_Status='Completed'
GROUP BY Category ORDER BY profit DESC;

-- 5. Customer segment economics
SELECT Customer_Segment,
       COUNT(DISTINCT CASE WHEN Order_Status='Completed' THEN Order_ID END) AS orders,
       SUM(Realized_Sales) AS sales,
       SUM(Realized_Profit) AS profit,
       ROUND(SUM(Realized_Sales)/NULLIF(COUNT(DISTINCT CASE WHEN Order_Status='Completed' THEN Order_ID END),0),2) AS aov
FROM FactSales
GROUP BY Customer_Segment ORDER BY sales DESC;

-- 6. Discount vs profitability bands
SELECT
  CASE WHEN Discount_Pct < 0.05 THEN '<5%'
       WHEN Discount_Pct < 0.10 THEN '5-10%'
       WHEN Discount_Pct < 0.15 THEN '10-15%'
       ELSE '15%+' END AS discount_band,
  COUNT(*) AS transactions,
  SUM(Realized_Sales) AS sales,
  ROUND(100.0*SUM(Realized_Profit)/NULLIF(SUM(Realized_Sales),0),2) AS margin_pct
FROM FactSales
WHERE Order_Status='Completed'
GROUP BY 1 ORDER BY 1;

-- 7. Product ranking
SELECT Product, Category,
       SUM(Realized_Sales) AS sales,
       SUM(Realized_Profit) AS profit,
       ROUND(100.0*SUM(Realized_Profit)/NULLIF(SUM(Realized_Sales),0),2) AS margin_pct
FROM FactSales
WHERE Order_Status='Completed'
GROUP BY Product, Category
ORDER BY sales DESC;

-- 8. Order-status operational view
SELECT Order_Status, COUNT(*) AS transactions,
       SUM(Sales) AS gross_value
FROM FactSales
GROUP BY Order_Status ORDER BY transactions DESC;
