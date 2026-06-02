# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Pipeline Otimizado com GitHub Copilot
# MAGIC
# MAGIC **Objetivo:** Implementar todas as otimizações identificadas no profiling
# MAGIC usando o Copilot para acelerar o desenvolvimento. Comparar com o baseline.
# MAGIC
# MAGIC **Duração estimada:** 30 minutos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Otimizações que serão aplicadas:
# MAGIC 1. Schema explícito (elimina inferSchema)
# MAGIC 2. Broadcast Join para tabela pequena de clientes
# MAGIC 3. Cache estratégico antes de múltiplas agregações
# MAGIC 4. Ajuste de shuffle partitions
# MAGIC 5. Leitura/escrita em Delta Lake (formato colunar)
# MAGIC 6. Z-Ordering para acelerar filtros futuros
# MAGIC 7. Eliminação de count() prematuros

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
)
import time

RAW_ORDERS_PATH    = "/FileStore/training/raw/orders.csv"
RAW_CUSTOMERS_PATH = "/FileStore/training/raw/customers.csv"
DELTA_BASE         = "/FileStore/training/delta"
RESULTS_BASE       = "/FileStore/training/optimized"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 1: Configurações do Spark
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Configure o Spark para otimizar pipelines de dados:
# MAGIC > ajuste shuffle.partitions para 2x os cores disponíveis,
# MAGIC > habilite AQE (Adaptive Query Execution) e otimização de broadcast automático"*

# COMMAND ----------

# Configurações otimizadas do Spark
n_cores = sc.defaultParallelism
optimal_partitions = n_cores * 2

spark.conf.set("spark.sql.shuffle.partitions", str(optimal_partitions))
spark.conf.set("spark.sql.adaptive.enabled", "true")             # AQE
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")  # Consolida partições pequenas
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")   # Corrige skew automaticamente
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")   # Otimiza escrita Delta

print(f"Cores: {n_cores}")
print(f"Shuffle partitions ajustado para: {optimal_partitions}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 2: Schema Explícito + Leitura Eficiente
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Defina schemas StructType explícitos para as tabelas orders e customers,
# MAGIC > depois leia os CSVs com os schemas definidos para evitar inferSchema"*

# COMMAND ----------

# Schemas explícitos — evita o scan duplo do inferSchema
orders_schema = StructType([
    StructField("order_id",         StringType(),  False),
    StructField("customer_id",      StringType(),  False),
    StructField("product_category", StringType(),  True),
    StructField("product_name",     StringType(),  True),
    StructField("quantity",         IntegerType(), True),
    StructField("unit_price",       DoubleType(),  True),
    StructField("order_date",       StringType(),  True),
    StructField("region",           StringType(),  True),
    StructField("status",           StringType(),  True),
])

customers_schema = StructType([
    StructField("customer_id",  StringType(), False),
    StructField("name",         StringType(), True),
    StructField("email",        StringType(), True),
    StructField("city",         StringType(), True),
    StructField("signup_date",  StringType(), True),
    StructField("segment",      StringType(), True),
])

t_start = time.time()

df_orders    = spark.read.schema(orders_schema).option("header", "true").csv(RAW_ORDERS_PATH)
df_customers = spark.read.schema(customers_schema).option("header", "true").csv(RAW_CUSTOMERS_PATH)

t_read = time.time()
print(f"Leitura com schema explícito: {t_read - t_start:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 3: Limpeza com Pushdown e Cache Estratégico
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Reescreva a limpeza de dados usando filter pushdown (todos os filtros de uma vez),
# MAGIC > depois aplique .cache() antes das operações de join e aggregação"*

# COMMAND ----------

# Limpeza com todos os filtros encadeados (Spark os combina em um único scan)
df_orders_clean = (
    df_orders
    .dropDuplicates(["order_id"])
    .filter(
        (F.col("status") == "completed") &
        (F.col("quantity") > 0) &
        (F.col("unit_price") > 0)
    )
    .withColumn("total_amount",      F.round(F.col("quantity") * F.col("unit_price"), 2))
    .withColumn("product_category",  F.lower(F.col("product_category")))
    .withColumn("order_date",        F.col("order_date").cast(TimestampType()))
    .withColumn("order_year",        F.year("order_date"))
    .withColumn("order_month",       F.month("order_date"))
    .select(
        "order_id", "customer_id", "product_category", "product_name",
        "quantity", "unit_price", "total_amount",
        "order_date", "order_year", "order_month",
        "region", "status"
    )
    .cache()  # ← Cache estratégico: será usado em join + 3 aggregações
)

# Materialize o cache com uma ação (lazy evaluation)
n_orders = df_orders_clean.count()
t_clean = time.time()
print(f"Limpeza + Cache: {t_clean - t_read:.2f}s | Pedidos válidos: {n_orders}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 4: Broadcast Join para Tabela Pequena
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Aplique broadcast hint na tabela de clientes antes do join com pedidos,
# MAGIC > pois a tabela de clientes tem menos de 10MB e cabe na memória de todos os executors"*

# COMMAND ----------

# Broadcast Join — elimina o SortMergeJoin e o shuffle de clientes
df_enriched = (
    df_orders_clean
    .join(
        F.broadcast(df_customers),  # ← Força Broadcast Hash Join
        on="customer_id",
        how="left"
    )
    .cache()  # ← Cache do resultado do join para as 3 aggregações seguintes
)

# Materialize
n_enriched = df_enriched.count()
t_join = time.time()
print(f"Broadcast Join: {t_join - t_clean:.2f}s | Registros enriquecidos: {n_enriched}")

# Verifique o plano — deve mostrar BroadcastHashJoin, não SortMergeJoin
df_enriched.explain()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 5: Aggregações sobre Dados Cacheados
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Execute as três aggregações (por categoria, região e período) sobre o DataFrame
# MAGIC > já cacheado. Como as três leituras são do cache, o tempo deve ser muito menor"*

# COMMAND ----------

# As três aggregações agora leem do cache (sem rescan dos CSVs)
df_by_category = (
    df_enriched
    .groupBy("product_category")
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum("total_amount").alias("total_revenue"),
        F.avg("total_amount").alias("avg_order_value"),
        F.countDistinct("customer_id").alias("unique_customers"),
    )
    .orderBy(F.desc("total_revenue"))
)

df_by_region = (
    df_enriched
    .groupBy("region")
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum("total_amount").alias("total_revenue"),
        F.avg("total_amount").alias("avg_order_value"),
    )
    .orderBy(F.desc("total_revenue"))
)

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
print(f"Aggregações (3x): {t_agg - t_join:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 6: Escrita em Delta Lake com Z-Order
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Escreva os DataFrames em formato Delta Lake particionando por year/month onde fizer sentido,
# MAGIC > depois execute OPTIMIZE com ZORDER BY nas colunas mais usadas em filtros"*

# COMMAND ----------

# Escrita em Delta Lake (formato colunar com compressão e statistics)
df_by_category.write.format("delta").mode("overwrite").save(f"{RESULTS_BASE}/by_category")
df_by_region.write.format("delta").mode("overwrite").save(f"{RESULTS_BASE}/by_region")

# Tabela de períodos particionada por ano
df_by_period.write.format("delta").mode("overwrite").partitionBy("order_year").save(f"{RESULTS_BASE}/by_period")

# Dataset enriquecido completo — particionado por ano e categoria para queries futuras
(
    df_enriched
    .write
    .format("delta")
    .mode("overwrite")
    .partitionBy("order_year", "product_category")
    .save(f"{DELTA_BASE}/orders_enriched")
)

t_write = time.time()
print(f"Escrita Delta Lake: {t_write - t_agg:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Otimização 7: OPTIMIZE + Z-Order (Delta Lake)
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Execute OPTIMIZE no dataset principal com ZORDER BY nas colunas mais
# MAGIC > utilizadas em filtros: customer_id e order_date"*

# COMMAND ----------

# Registrar tabela Delta no Catálogo para usar SQL
spark.sql(f"CREATE TABLE IF NOT EXISTS training.orders_enriched USING DELTA LOCATION '{DELTA_BASE}/orders_enriched'")

# OPTIMIZE compacta arquivos pequenos em arquivos maiores
# ZORDER cria índice multidimensional para queries rápidas por customer_id e order_date
spark.sql("""
    OPTIMIZE training.orders_enriched
    ZORDER BY (customer_id, order_date)
""")

t_optimize = time.time()
print(f"OPTIMIZE + ZORDER: {t_optimize - t_write:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Liberar Cache
# MAGIC
# MAGIC > 💡 **Boa prática:** Sempre libere o cache ao final do pipeline para não pressionar a memória do cluster.

# COMMAND ----------

df_orders_clean.unpersist()
df_enriched.unpersist()
print("Cache liberado.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Comparação: Baseline vs Otimizado
# MAGIC
# MAGIC > 💡 **Exercício:** Complete a tabela com os tempos medidos.

# COMMAND ----------

t_total = t_optimize - t_start

print(f"\n{'='*50}")
print(f"RESUMO DA OTIMIZAÇÃO")
print(f"{'='*50}")
print(f"Leitura:       {t_read - t_start:.2f}s")
print(f"Limpeza+Cache: {t_clean - t_read:.2f}s")
print(f"Broadcast Join:{t_join - t_clean:.2f}s")
print(f"Aggregações:   {t_agg - t_join:.2f}s")
print(f"Escrita Delta: {t_write - t_agg:.2f}s")
print(f"OPTIMIZE:      {t_optimize - t_write:.2f}s")
print(f"{'='*50}")
print(f"TOTAL OTIMIZADO: {t_total:.2f}s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tabela Comparativa
# MAGIC
# MAGIC | Etapa | Baseline (s) | Otimizado (s) | Ganho |
# MAGIC |-------|-------------|---------------|-------|
# MAGIC | Leitura | ___ | ___ | ___% |
# MAGIC | Limpeza | ___ | ___ | ___% |
# MAGIC | Join | ___ | ___ | ___% |
# MAGIC | Aggregações | ___ | ___ | ___% |
# MAGIC | Escrita | ___ | ___ | ___% |
# MAGIC | **Total** | **___** | **___** | **___%** |
# MAGIC
# MAGIC ## O que aprendemos
# MAGIC
# MAGIC | Técnica | Quando usar |
# MAGIC |---------|-------------|
# MAGIC | Schema explícito | Sempre em produção |
# MAGIC | Broadcast Join | Tabela < 200MB |
# MAGIC | `.cache()` | Antes de múltiplas ações no mesmo DF |
# MAGIC | AQE | Habilitar sempre no Spark 3+ |
# MAGIC | Delta Lake | Substituir CSV/Parquet em produção |
# MAGIC | OPTIMIZE + ZORDER | Após carga de dados, colunas de filtro frequentes |
# MAGIC | Particionamento | Colunas usadas em filtros de range (data, ano) |
# MAGIC
# MAGIC **Parabéns!** Você concluiu o módulo de otimização de pipeline.
