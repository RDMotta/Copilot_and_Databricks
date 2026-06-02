-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 01 - Setup e Extracao (Bronze SQL)
-- MAGIC
-- MAGIC **Objetivo:** usar SQL Warehouse Serverless (2X-Small) para ler CSVs no DBFS e criar tabelas Bronze.

-- COMMAND ----------

-- 1) Criar schema da trilha
CREATE SCHEMA IF NOT EXISTS training_sql_serverless;
USE training_sql_serverless;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Extracao de pedidos (Bronze)

-- COMMAND ----------

CREATE OR REPLACE TABLE bronze_orders_raw AS
SELECT
  order_id,
  customer_id,
  product_category,
  product_name,
  quantity,
  unit_price,
  order_date,
  region,
  status,
  current_timestamp() AS _ingestion_timestamp,
  'dbfs:/FileStore/training/raw/orders.csv' AS _source_file
FROM read_files(
  'dbfs:/FileStore/training/raw/orders.csv',
  format => 'csv',
  header => true,
  inferSchema => true
);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Extracao de clientes (Bronze)

-- COMMAND ----------

CREATE OR REPLACE TABLE bronze_customers_raw AS
SELECT
  customer_id,
  customer_name,
  email,
  city,
  signup_date,
  current_timestamp() AS _ingestion_timestamp,
  'dbfs:/FileStore/training/raw/customers.csv' AS _source_file
FROM read_files(
  'dbfs:/FileStore/training/raw/customers.csv',
  format => 'csv',
  header => true,
  inferSchema => true
);

-- COMMAND ----------

-- 2) Validacoes basicas
SELECT 'bronze_orders_raw' AS table_name, COUNT(*) AS row_count FROM bronze_orders_raw
UNION ALL
SELECT 'bronze_customers_raw' AS table_name, COUNT(*) AS row_count FROM bronze_customers_raw;

-- COMMAND ----------

-- 3) Amostra dos dados
SELECT * FROM bronze_orders_raw LIMIT 20;

-- COMMAND ----------

SELECT * FROM bronze_customers_raw LIMIT 20;
