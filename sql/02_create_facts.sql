--------------------------------------------------
-- FACT SALES
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.fact_sales` AS
SELECT
    s.order_id,
    s.order_line_id,
    s.customer_id,
    s.product_id,
    s.order_date,
    s.sales_channel,
    s.region,

    -- Metrics
    s.quantity,
    s.unit_price,
    s.discount_pct,
    s.gross_revenue,
    s.net_revenue,
    s.shipping_fee,
    s.tax_amount,

    -- Cost and profit
    p.standard_cost,
    (s.quantity * p.standard_cost) AS total_cost,
    (s.net_revenue - (s.quantity * p.standard_cost)) AS gross_profit,

    -- Flags
    s.order_status,
    s.returned_flag

FROM `financial_ops_raw.sales_raw` s
LEFT JOIN `financial_ops_warehouse.dim_products` p
    ON s.product_id = p.product_id;


--------------------------------------------------
-- FACT COSTS
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.fact_costs` AS
SELECT
    cost_id,
    cost_date,
    region,
    department,
    cost_category,
    cost_type,
    amount,
    vendor_name,
    fixed_variable_flag
FROM `financial_ops_raw.costs_raw`;