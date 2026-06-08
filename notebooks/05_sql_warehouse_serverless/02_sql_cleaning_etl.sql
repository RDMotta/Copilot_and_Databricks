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
-- TODO: Copilot deve completar


-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Silver de clientes: normalizacao e validacao de email

-- COMMAND ----------

CREATE OR REPLACE TABLE silver_customers_clean AS
SELECT
  CAST(customer_id AS STRING) AS customer_id,
  TRIM(CAST(name AS STRING)) AS customer_name,
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
