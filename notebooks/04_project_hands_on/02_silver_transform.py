# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Projeto Hands-On: Camada Silver (Transformação)
# MAGIC
# MAGIC **Objetivo:** Transformar os dados brutos da Bronze em dados limpos, validados
# MAGIC e enriquecidos na camada Silver. Aplicar regras de qualidade de dados.
# MAGIC
# MAGIC **Duração estimada:** 25 minutos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## O que fazemos na Silver:
# MAGIC - Remoção de duplicatas
# MAGIC - Conversão e validação de tipos
# MAGIC - Padronização de strings (case, trim)
# MAGIC - Aplicação de regras de negócio
# MAGIC - Join com tabelas de referência
# MAGIC - Adição de colunas derivadas

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType, DoubleType
import re

# Caminhos do projeto
PROJECT_NAME = "ecommerce_lakehouse"
SILVER_PATH  = f"/FileStore/training/{PROJECT_NAME}/silver"

spark.sql("USE ecommerce_lakehouse")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 1: Ler da Camada Bronze

# COMMAND ----------

# Leitura das tabelas Bronze (já registradas no catálogo)
df_bronze_orders    = spark.table("bronze_orders")
df_bronze_customers = spark.table("bronze_customers")

print(f"Bronze orders:    {df_bronze_orders.count()} registros")
print(f"Bronze customers: {df_bronze_customers.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 2: Limpeza de Pedidos
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função clean_silver_orders que:
# MAGIC > 1) Exclui registros com _corrupt_record não nulo
# MAGIC > 2) Remove duplicatas por order_id mantendo o registro mais recente de _ingestion_timestamp
# MAGIC > 3) Converte order_date para TimestampType
# MAGIC > 4) Normaliza product_category e region para lower().trim()
# MAGIC > 5) Filtra pedidos com quantity entre 1 e 100 e unit_price entre 0.01 e 50000
# MAGIC > 6) Calcula total_amount e classifica em faixas de valor
# MAGIC > 7) Remove colunas de auditoria Bronze (prefixo _)"*

# COMMAND ----------

def clean_silver_orders(df: DataFrame) -> DataFrame:
    """
    Transforma pedidos da Bronze para Silver.
    Aplica limpeza, validação de tipos e regras de negócio.
    """
    # TODO: Copilot vai completar toda esta função
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 3: Limpeza de Clientes
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função clean_silver_customers que valida e normaliza dados de clientes:
# MAGIC > normalize email para lowercase, valide formato de email com regex,
# MAGIC > converta signup_date para DateType, adicione flag is_valid_email"*

# COMMAND ----------

# Regex para validação de email (padrão simples para exercício)
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"

def clean_silver_customers(df: DataFrame) -> DataFrame:
    """
    Transforma clientes da Bronze para Silver.
    Normaliza strings e valida campos críticos.
    """
    # TODO: Copilot vai completar — use F.regexp_extract ou F.rlike para validar email
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 4: Executar as Transformações

# COMMAND ----------

df_silver_orders    = clean_silver_orders(df_bronze_orders)
df_silver_customers = clean_silver_customers(df_bronze_customers)

# Exiba samples para validação visual
print("=== Silver Orders ===")
display(df_silver_orders.limit(5))
print(f"Total: {df_silver_orders.count()} registros")

print("\n=== Silver Customers ===")
display(df_silver_customers.limit(5))
print(f"Total: {df_silver_customers.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 5: Enriquecimento — Join Orders + Customers
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Junte os DataFrames silver_orders e silver_customers usando broadcast join,
# MAGIC > adicione as colunas do cliente e crie uma tabela silver_orders_enriched"*

# COMMAND ----------

# Enriquecimento com dados do cliente
df_silver_enriched = (
    df_silver_orders
    .join(
        F.broadcast(df_silver_customers.select("customer_id", "name", "city", "segment")),
        on="customer_id",
        how="left"
    )
    .withColumnRenamed("name", "customer_name")
    .withColumnRenamed("city", "customer_city")
    .withColumnRenamed("segment", "customer_segment")
)

display(df_silver_enriched.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 6: Salvar na Camada Silver
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Salve os DataFrames Silver em Delta Lake particionados por order_year,
# MAGIC > depois registre as tabelas no catálogo e execute OPTIMIZE"*

# COMMAND ----------

# Salvar pedidos limpos (particionado por ano)
(
    df_silver_enriched
    .write
    .format("delta")
    .mode("overwrite")
    .partitionBy("order_year")
    .option("overwriteSchema", "true")
    .save(f"{SILVER_PATH}/orders_enriched")
)

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS ecommerce_lakehouse.silver_orders_enriched
    USING DELTA
    LOCATION '{SILVER_PATH}/orders_enriched'
""")

# Salvar clientes limpos
(
    df_silver_customers
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(f"{SILVER_PATH}/customers")
)

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS ecommerce_lakehouse.silver_customers
    USING DELTA
    LOCATION '{SILVER_PATH}/customers'
""")

print("Camada Silver salva com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo 7: Data Quality Report
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie um relatório de qualidade de dados comparando Bronze vs Silver:
# MAGIC > total de registros, registros removidos por motivo (duplicatas, valores inválidos, etc.)
# MAGIC > e taxa de aproveitamento"*

# COMMAND ----------

# Relatório de qualidade: Bronze vs Silver
n_bronze_orders  = df_bronze_orders.count()
n_silver_orders  = df_silver_enriched.count()
n_removed        = n_bronze_orders - n_silver_orders
taxa_aproveitamento = (n_silver_orders / n_bronze_orders) * 100

print(f"{'='*50}")
print(f"RELATÓRIO DE QUALIDADE — PEDIDOS")
print(f"{'='*50}")
print(f"Bronze (entrada):    {n_bronze_orders:>8,}")
print(f"Silver (saída):      {n_silver_orders:>8,}")
print(f"Removidos:           {n_removed:>8,}")
print(f"Taxa aproveitamento: {taxa_aproveitamento:>7.1f}%")
print(f"{'='*50}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Camada Silver Concluída!
# MAGIC
# MAGIC A camada Silver está pronta com:
# MAGIC - Dados limpos e validados
# MAGIC - Tipos corretos (timestamps, decimais)
# MAGIC - Strings normalizadas
# MAGIC - Enriquecimento com dados de clientes
# MAGIC - Particionamento por ano
# MAGIC - Relatório de qualidade gerado
# MAGIC
# MAGIC **Próximo:** `03_gold_analytics.py` — camada analítica com KPIs
