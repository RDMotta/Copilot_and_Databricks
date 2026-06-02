-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 02 - Limpeza e ETL (Silver SQL)
-- MAGIC
-- MAGIC **Objetivo:** limpar pedidos/clientes e criar tabela enriquecida para analise.

-- COMMAND ----------

USE training_sql_serverless;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Silver de pedidos: padronizacao, filtros e deduplicacao

-- COMMAND ----------

CREATE OR REPLACE TABLE silver_orders_clean AS
WITH typed AS (
  SELECT
    CAST(order_id AS STRING) AS order_id,
    CAST(customer_id AS STRING) AS customer_id,
    LOWER(TRIM(CAST(product_category AS STRING))) AS product_category,
    TRIM(CAST(product_name AS STRING)) AS product_name,
    CAST(quantity AS INT) AS quantity,
    CAST(unit_price AS DOUBLE) AS unit_price,
    TO_TIMESTAMP(order_date) AS order_ts,
    LOWER(TRIM(CAST(region AS STRING))) AS region,
    LOWER(TRIM(CAST(status AS STRING))) AS status
  FROM bronze_orders_raw
),
filtered AS (
  SELECT *
  FROM typed
  WHERE quantity BETWEEN 1 AND 100
    AND unit_price BETWEEN 0.01 AND 50000
    AND status = 'completed'
),
dedup AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_ts DESC) AS rn
  FROM filtered
)
SELECT
  order_id,
  customer_id,
  product_category,
  product_name,
  quantity,
  unit_price,
  order_ts AS order_date,
  region,
  status,
  ROUND(quantity * unit_price, 2) AS total_amount
FROM dedup
WHERE rn = 1;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Silver de clientes: normalizacao e validacao de email

-- COMMAND ----------

CREATE OR REPLACE TABLE silver_customers_clean AS
SELECT
  CAST(customer_id AS STRING) AS customer_id,
  TRIM(CAST(customer_name AS STRING)) AS customer_name,
  LOWER(TRIM(CAST(email AS STRING))) AS email,
  LOWER(TRIM(CAST(city AS STRING))) AS city,
  TO_DATE(signup_date) AS signup_date,
  LOWER(TRIM(CAST(email AS STRING))) RLIKE '^[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}$' AS is_valid_email
FROM bronze_customers_raw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Enriquecimento Silver (join)

-- COMMAND ----------

CREATE OR REPLACE TABLE silver_orders_enriched AS
SELECT
  o.order_id,
  o.customer_id,
  o.product_category,
  o.product_name,
  o.quantity,
  o.unit_price,
  o.order_date,
  o.region,
  o.total_amount,
  c.customer_name,
  c.city AS customer_city,
  c.email,
  c.is_valid_email,
  c.signup_date
FROM silver_orders_clean o
LEFT JOIN silver_customers_clean c
  ON o.customer_id = c.customer_id;

-- COMMAND ----------

-- 1) Validacao de volume por camada
SELECT 'bronze_orders_raw' AS table_name, COUNT(*) AS row_count FROM bronze_orders_raw
UNION ALL
SELECT 'silver_orders_clean' AS table_name, COUNT(*) AS row_count FROM silver_orders_clean
UNION ALL
SELECT 'silver_orders_enriched' AS table_name, COUNT(*) AS row_count FROM silver_orders_enriched;

-- COMMAND ----------

-- 2) Validacao de qualidade
SELECT
  SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
  SUM(CASE WHEN total_amount <= 0 THEN 1 ELSE 0 END) AS invalid_total_amount,
  SUM(CASE WHEN is_valid_email = false THEN 1 ELSE 0 END) AS invalid_email_rows
FROM silver_orders_enriched;
