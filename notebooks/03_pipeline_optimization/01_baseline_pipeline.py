# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Pipeline Base (Sem Otimização)
# MAGIC
# MAGIC **Objetivo:** Executar o pipeline ingênuo e medir o tempo de execução como baseline.
# MAGIC
# MAGIC Este notebook serve como **ponto de partida** para o exercício de otimização.
# MAGIC Execute-o e anote os tempos de cada etapa antes de ir para `02_profiling.py`.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
import time

# Caminhos dos dados brutos (após upload via generate_sample_data.py)
RAW_ORDERS_PATH   = "/FileStore/training/raw/orders.csv"
RAW_CUSTOMERS_PATH = "/FileStore/training/raw/customers.csv"

OUTPUT_BASE = "/FileStore/training/baseline"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 1: Leitura dos Dados (Pipeline Ingênuo)
# MAGIC
# MAGIC > ⚠️ Problemas intencionais neste pipeline: sem particionamento, sem cache,
# MAGIC > joins ineficientes — identificaremos e corrigiremos no notebook de otimização.

# COMMAND ----------

t_start = time.time()

# Leitura sem schema definido (inferência é lenta em datasets grandes)
df_orders = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")   # ⚠️ Problemático em produção — scan duplo do arquivo
    .csv(RAW_ORDERS_PATH)
)

df_customers = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")   # ⚠️ Idem
    .csv(RAW_CUSTOMERS_PATH)
)

t_read = time.time()
print(f"Leitura: {t_read - t_start:.2f}s")
print(f"Pedidos: {df_orders.count()} registros")    # ⚠️ count() acionado cedo
print(f"Clientes: {df_customers.count()} registros") # ⚠️ idem

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 2: Limpeza (Ingênua)

# COMMAND ----------

# Limpeza sem cache — cada operação seguinte relê o CSV do início
df_orders_clean = df_orders.dropDuplicates(["order_id"])
df_orders_clean = df_orders_clean.filter(F.col("status") == "completed")
df_orders_clean = df_orders_clean.filter(F.col("quantity") > 0)
df_orders_clean = df_orders_clean.filter(F.col("unit_price") > 0)
df_orders_clean = df_orders_clean.withColumn(
    "total_amount", F.col("quantity") * F.col("unit_price")
)
df_orders_clean = df_orders_clean.withColumn(
    "product_category", F.lower(F.col("product_category"))
)
df_orders_clean = df_orders_clean.withColumn(
    "order_year", F.year(F.col("order_date").cast("timestamp"))
)
df_orders_clean = df_orders_clean.withColumn(
    "order_month", F.month(F.col("order_date").cast("timestamp"))
)

t_clean = time.time()
print(f"Limpeza: {t_clean - t_read:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 3: Join com Clientes (Ingênuo)

# COMMAND ----------

# ⚠️ Sort merge join em tabelas pequenas — broadcast seria mais eficiente
df_enriched = df_orders_clean.join(
    df_customers,
    on="customer_id",
    how="left"
)

t_join = time.time()
print(f"Join: {t_join - t_clean:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 4: Aggregações Múltiplas (Ingênuo)

# COMMAND ----------

# ⚠️ Três groupBy separados sem cache — Spark relê e reprocessa os dados 3x

# Métricas por categoria
df_by_category = (
    df_enriched
    .groupBy("product_category")
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum("total_amount").alias("total_revenue"),
        F.avg("total_amount").alias("avg_order_value"),
    )
    .orderBy(F.desc("total_revenue"))
)

# Métricas por região
df_by_region = (
    df_enriched
    .groupBy("region")
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum("total_amount").alias("total_revenue"),
    )
    .orderBy(F.desc("total_revenue"))
)

# Métricas por período
df_by_period = (
    df_enriched
    .groupBy("order_year", "order_month")
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum("total_amount").alias("total_revenue"),
    )
    .orderBy("order_year", "order_month")
)

t_agg = time.time()
print(f"Aggregações: {t_agg - t_join:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 5: Escrita dos Resultados (Ingênua)

# COMMAND ----------

# ⚠️ Escrevendo em CSV sem particionamento — dificulta leituras futuras
df_by_category.write.mode("overwrite").csv(f"{OUTPUT_BASE}/by_category")
df_by_region.write.mode("overwrite").csv(f"{OUTPUT_BASE}/by_region")
df_by_period.write.mode("overwrite").csv(f"{OUTPUT_BASE}/by_period")

t_write = time.time()
t_total = t_write - t_start

print(f"\nEscrita: {t_write - t_agg:.2f}s")
print(f"{'='*40}")
print(f"TEMPO TOTAL (baseline): {t_total:.2f}s")
print(f"{'='*40}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo do Baseline
# MAGIC
# MAGIC Anote os tempos abaixo antes de ir para o próximo notebook:
# MAGIC
# MAGIC | Etapa | Tempo (s) |
# MAGIC |-------|-----------|
# MAGIC | Leitura | ___ |
# MAGIC | Limpeza | ___ |
# MAGIC | Join | ___ |
# MAGIC | Aggregações | ___ |
# MAGIC | Escrita | ___ |
# MAGIC | **Total** | **___** |
# MAGIC
# MAGIC **Próximo:** `02_profiling.py` — vamos identificar os gargalos com Copilot!
