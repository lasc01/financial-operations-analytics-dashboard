CREATE SCHEMA IF NOT EXISTS `financial_ops_reporting`;

CREATE OR REPLACE VIEW `financial_ops_reporting.vw_executive_summary` AS
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(total_cost), 2) AS total_product_cost,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(SAFE_DIVIDE(SUM(gross_profit), SUM(net_revenue)) * 100, 2) AS profit_margin_pct,
    ROUND(SAFE_DIVIDE(SUM(net_revenue), COUNT(DISTINCT order_id)), 2) AS average_order_value
FROM `financial_ops_warehouse.fact_sales`
WHERE order_status = 'Completed';


CREATE OR REPLACE VIEW `financial_ops_reporting.vw_monthly_financial_performance` AS
SELECT
    DATE_TRUNC(order_date, MONTH) AS month,
    FORMAT_DATE('%Y %m', DATE_TRUNC(order_date, MONTH)) AS month_label,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(SUM(total_cost), 2) AS product_cost,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(SAFE_DIVIDE(SUM(gross_profit), SUM(net_revenue)) * 100, 2) AS profit_margin_pct,
    ROUND(SAFE_DIVIDE(SUM(net_revenue), COUNT(DISTINCT order_id)), 2) AS average_order_value
FROM `financial_ops_warehouse.fact_sales`
WHERE order_status = 'Completed'
GROUP BY month, month_label
ORDER BY month;


CREATE OR REPLACE VIEW `financial_ops_reporting.vw_revenue_by_region_channel` AS
SELECT
    region,
    sales_channel,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(SAFE_DIVIDE(SUM(gross_profit), SUM(net_revenue)) * 100, 2) AS profit_margin_pct
FROM `financial_ops_warehouse.fact_sales`
WHERE order_status = 'Completed'
GROUP BY region, sales_channel
ORDER BY revenue DESC;


CREATE OR REPLACE VIEW `financial_ops_reporting.vw_product_profitability` AS
SELECT
    p.category,
    p.subcategory,
    p.product_name,
    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS units_sold,
    ROUND(SUM(s.net_revenue), 2) AS revenue,
    ROUND(SUM(s.total_cost), 2) AS product_cost,
    ROUND(SUM(s.gross_profit), 2) AS gross_profit,
    ROUND(SAFE_DIVIDE(SUM(s.gross_profit), SUM(s.net_revenue)) * 100, 2) AS profit_margin_pct
FROM `financial_ops_warehouse.fact_sales` s
LEFT JOIN `financial_ops_warehouse.dim_products` p
    ON s.product_id = p.product_id
WHERE s.order_status = 'Completed'
GROUP BY p.category, p.subcategory, p.product_name
ORDER BY gross_profit DESC;


CREATE OR REPLACE VIEW `financial_ops_reporting.vw_cost_analysis` AS
SELECT
    DATE_TRUNC(cost_date, MONTH) AS month,
    FORMAT_DATE('%Y %m', DATE_TRUNC(cost_date, MONTH)) AS month_label,
    region,
    department,
    cost_category,
    fixed_variable_flag,
    COUNT(cost_id) AS total_cost_records,
    ROUND(SUM(amount), 2) AS total_operating_cost
FROM `financial_ops_warehouse.fact_costs`
GROUP BY month, month_label, region, department, cost_category, fixed_variable_flag
ORDER BY month;


CREATE OR REPLACE VIEW `financial_ops_reporting.vw_profit_after_operating_cost` AS
WITH sales_monthly AS (
    SELECT
        DATE_TRUNC(order_date, MONTH) AS month,
        region,
        ROUND(SUM(net_revenue), 2) AS revenue,
        ROUND(SUM(total_cost), 2) AS product_cost,
        ROUND(SUM(gross_profit), 2) AS gross_profit
    FROM `financial_ops_warehouse.fact_sales`
    WHERE order_status = 'Completed'
    GROUP BY month, region
),

cost_monthly AS (
    SELECT
        DATE_TRUNC(cost_date, MONTH) AS month,
        region,
        ROUND(SUM(amount), 2) AS operating_cost
    FROM `financial_ops_warehouse.fact_costs`
    GROUP BY month, region
)

SELECT
    s.month,
    FORMAT_DATE('%Y %m', s.month) AS month_label,
    s.region,
    s.revenue,
    s.product_cost,
    s.gross_profit,
    COALESCE(c.operating_cost, 0) AS operating_cost,
    ROUND(s.gross_profit - COALESCE(c.operating_cost, 0), 2) AS net_profit,
    ROUND(SAFE_DIVIDE(s.gross_profit - COALESCE(c.operating_cost, 0), s.revenue) * 100, 2) AS net_profit_margin_pct
FROM sales_monthly s
LEFT JOIN cost_monthly c
    ON s.month = c.month
    AND s.region = c.region
ORDER BY s.month, s.region;


CREATE OR REPLACE VIEW `financial_ops_reporting.vw_customer_lifetime_value` AS
SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    c.loyalty_status,
    c.region,
    c.acquisition_channel,
    COUNT(DISTINCT s.order_id) AS total_orders,
    ROUND(SUM(s.net_revenue), 2) AS lifetime_revenue,
    ROUND(SUM(s.gross_profit), 2) AS lifetime_gross_profit,
    ROUND(SAFE_DIVIDE(SUM(s.net_revenue), COUNT(DISTINCT s.order_id)), 2) AS average_order_value,
    MIN(s.order_date) AS first_order_date,
    MAX(s.order_date) AS last_order_date,
    CASE
        WHEN COUNT(DISTINCT s.order_id) > 1 THEN TRUE
        ELSE FALSE
    END AS repeat_customer_flag
FROM `financial_ops_warehouse.fact_sales` s
LEFT JOIN `financial_ops_warehouse.dim_customers` c
    ON s.customer_id = c.customer_id
WHERE s.order_status = 'Completed'
GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment,
    c.loyalty_status,
    c.region,
    c.acquisition_channel
ORDER BY lifetime_revenue DESC;