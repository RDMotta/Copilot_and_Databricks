# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Projeto Hands-On: Camada Bronze (Ingestão)
# MAGIC
# MAGIC **Objetivo:** Construir a primeira camada de um projeto Lakehouse real.
# MAGIC A camada Bronze armazena dados brutos como chegam da fonte, sem transformações.
# MAGIC
# MAGIC **Duração estimada:** 20 minutos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Arquitetura do Projeto
# MAGIC
# MAGIC ```
# MAGIC   Fonte (CSV)  →  [BRONZE]  →  [SILVER]  →  [GOLD]
# MAGIC                   Raw data    Cleaned      Analytics
# MAGIC ```

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
)
from datetime import datetime

# Configuração de caminhos do projeto
PROJECT_NAME = "ecommerce_lakehouse"
BRONZE_PATH  = f"/FileStore/training/{PROJECT_NAME}/bronze"
SOURCE_PATH  = "/FileStore/training/raw"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 1: Configurar o Banco de Dados do Projeto
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie um banco de dados chamado ecommerce_lakehouse se não existir,
# MAGIC > e configure o path padrão para o DBFS"*

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS ecommerce_lakehouse
# MAGIC COMMENT 'Projeto Lakehouse de E-commerce - Treinamento Databricks + Copilot'
# MAGIC LOCATION '/FileStore/training/ecommerce_lakehouse/';
# MAGIC
# MAGIC USE ecommerce_lakehouse;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 2: Ingestão com Metadata de Auditoria
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função ingest_to_bronze que lê um arquivo CSV, adiciona colunas de auditoria
# MAGIC > (ingestion_timestamp, source_file, ingestion_date) e salva em Delta Lake na camada Bronze.
# MAGIC > Adicione também uma coluna _corrupt_record para capturar linhas com problema de parse"*

# COMMAND ----------

def ingest_to_bronze(
    source_path: str,
    bronze_path: str,
    table_name: str,
    schema: StructType,
) -> int:
    """
    Ingere dados brutos para a camada Bronze com metadados de auditoria.

    Args:
        source_path: Caminho do arquivo fonte no DBFS
        bronze_path: Caminho de destino na camada Bronze
        table_name: Nome da tabela Delta
        schema: Schema esperado (sem colunas de auditoria)

    Returns:
        Número de registros ingeridos
    """
    # TODO: Copilot vai completar a função. Inclua:
    # 1. Leitura com schema + opção PERMISSIVE para capturar erros
    # 2. Adição de colunas de auditoria:
    #    - _ingestion_timestamp (current_timestamp)
    #    - _source_file (input_file_name())
    #    - _ingestion_date (current_date)
    #    - _pipeline_version (literal "1.0.0")
    # 3. Escrita em Delta Lake com modo append
    # 4. Registro da tabela no Catálogo
    # 5. Retorno do count de registros ingeridos
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 3: Definir Schemas e Executar a Ingestão

# COMMAND ----------

orders_schema = StructType([
    StructField("order_id",         StringType(),  True),
    StructField("customer_id",      StringType(),  True),
    StructField("product_category", StringType(),  True),
    StructField("product_name",     StringType(),  True),
    StructField("quantity",         IntegerType(), True),
    StructField("unit_price",       DoubleType(),  True),
    StructField("order_date",       StringType(),  True),
    StructField("region",           StringType(),  True),
    StructField("status",           StringType(),  True),
])

customers_schema = StructType([
    StructField("customer_id",  StringType(), True),
    StructField("name",         StringType(), True),
    StructField("email",        StringType(), True),
    StructField("city",         StringType(), True),
    StructField("signup_date",  StringType(), True),
    StructField("segment",      StringType(), True),
])

# COMMAND ----------

# Execute a ingestão para ambas as tabelas
print("Iniciando ingestão Bronze...")

n_orders = ingest_to_bronze(
    source_path=f"{SOURCE_PATH}/orders.csv",
    bronze_path=f"{BRONZE_PATH}/orders",
    table_name="bronze_orders",
    schema=orders_schema,
)
print(f"✅ bronze_orders: {n_orders} registros")

n_customers = ingest_to_bronze(
    source_path=f"{SOURCE_PATH}/customers.csv",
    bronze_path=f"{BRONZE_PATH}/customers",
    table_name="bronze_customers",
    schema=customers_schema,
)
print(f"✅ bronze_customers: {n_customers} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 4: Validação da Camada Bronze
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Escreva queries SQL para validar a ingestão Bronze:
# MAGIC > 1) Contar total de registros e registros com _corrupt_record não nulo
# MAGIC > 2) Verificar o range de datas de order_date
# MAGIC > 3) Listar os arquivos fonte únicos"*

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Validação 1: Contagem e registros corrompidos
# MAGIC -- TODO: Copilot vai completar

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Validação 2: Range de datas
# MAGIC -- TODO: Copilot vai completar

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Validação 3: Ver metadados de auditoria
# MAGIC SELECT
# MAGIC     _source_file,
# MAGIC     _ingestion_date,
# MAGIC     _pipeline_version,
# MAGIC     COUNT(*) AS total_records
# MAGIC FROM ecommerce_lakehouse.bronze_orders
# MAGIC GROUP BY ALL
# MAGIC ORDER BY _ingestion_date DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Camada Bronze Concluída!
# MAGIC
# MAGIC A camada Bronze está pronta com:
# MAGIC - Dados brutos preservados (sem transformações)
# MAGIC - Metadados de auditoria em cada registro
# MAGIC - Captura de registros corrompidos
# MAGIC - Tabelas registradas no Catálogo Databricks
# MAGIC
# MAGIC **Próximo:** `02_silver_transform.py` — limpeza e validação de negócio
