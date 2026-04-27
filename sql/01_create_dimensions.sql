-- Create dataset if not exists
CREATE SCHEMA IF NOT EXISTS `financial_ops_warehouse`;

--------------------------------------------------
-- DIM CUSTOMERS
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.dim_customers` AS
SELECT
    customer_id,
    customer_name,
    gender,
    age_group,
    region,
    city,
    acquisition_date,
    acquisition_channel,
    segment,
    loyalty_status,
    preferred_channel,
    is_active
FROM `financial_ops_raw.customers_raw`;


--------------------------------------------------
-- DIM PRODUCTS
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.dim_products` AS
SELECT
    product_id,
    product_name,
    category,
    subcategory,
    brand,
    supplier_name,
    standard_cost,
    list_price,
    launch_date,
    product_status
FROM `financial_ops_raw.products_raw`;


--------------------------------------------------
-- DIM DATE
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.dim_date` AS
SELECT
    date AS date_id,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    FORMAT_DATE('%B', date) AS month_name,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(DAY FROM date) AS day
FROM UNNEST(GENERATE_DATE_ARRAY('2024-01-01', '2025-12-31')) AS date;


--------------------------------------------------
-- DIM REGION
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.dim_region` AS
SELECT DISTINCT region
FROM `financial_ops_raw.sales_raw`;


--------------------------------------------------
-- DIM CHANNEL
--------------------------------------------------
CREATE OR REPLACE TABLE `financial_ops_warehouse.dim_channel` AS
SELECT DISTINCT sales_channel
FROM `financial_ops_raw.sales_raw`;