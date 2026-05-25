# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Profiling e Identificação de Gargalos
# MAGIC
# MAGIC **Objetivo:** Usar ferramentas do Databricks e o Copilot para identificar
# MAGIC gargalos de performance no pipeline baseline.
# MAGIC
# MAGIC **Duração estimada:** 20 minutos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC > 💡 **Dica:** Use o Copilot Chat para interpretar os resultados do profiling.
# MAGIC > Cole o explain plan e pergunte: *"O que este plano de execução Spark indica
# MAGIC > como possíveis gargalos de performance?"*

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
)

RAW_ORDERS_PATH    = "/FileStore/training/raw/orders.csv"
RAW_CUSTOMERS_PATH = "/FileStore/training/raw/customers.csv"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Analisando o Plano de Execução (Explain Plan)
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Mostre como usar df.explain(True) para analisar o plano físico de execução Spark
# MAGIC > e identifique as operações mais custosas"*

# COMMAND ----------

# Schema explícito — primeiro diagnóstico: o baseline usava inferSchema
orders_schema = StructType([
    StructField("order_id",          StringType(),  True),
    StructField("customer_id",       StringType(),  True),
    StructField("product_category",  StringType(),  True),
    StructField("product_name",      StringType(),  True),
    StructField("quantity",          IntegerType(), True),
    StructField("unit_price",        DoubleType(),  True),
    StructField("order_date",        StringType(),  True),
    StructField("region",            StringType(),  True),
    StructField("status",            StringType(),  True),
])

customers_schema = StructType([
    StructField("customer_id",   StringType(), True),
    StructField("name",          StringType(), True),
    StructField("email",         StringType(), True),
    StructField("city",          StringType(), True),
    StructField("signup_date",   StringType(), True),
    StructField("segment",       StringType(), True),
])

df_orders    = spark.read.schema(orders_schema).option("header", "true").csv(RAW_ORDERS_PATH)
df_customers = spark.read.schema(customers_schema).option("header", "true").csv(RAW_CUSTOMERS_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explain Plan do Join — Identifique o tipo de join usado

# COMMAND ----------

# Execute e analise o plano: o Spark está fazendo SortMergeJoin ou BroadcastHashJoin?
# Cole a saída no Copilot Chat e peça uma análise

df_join = df_orders.join(df_customers, on="customer_id", how="left")
df_join.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### O que procurar no Explain Plan:
# MAGIC
# MAGIC | Operação no Plan | O que significa | Ação |
# MAGIC |-----------------|-----------------|------|
# MAGIC | `SortMergeJoin` | Join custoso, ordena ambos os lados | Usar Broadcast se uma tabela for pequena |
# MAGIC | `HashAggregate → Exchange` | Shuffle de dados entre partições | Particionar por chave de agregação |
# MAGIC | `FileScan csv` | Leitura linha a linha | Converter para Parquet/Delta |
# MAGIC | `InMemoryTableScan` | Dados em cache | ✅ OK |
# MAGIC | `Exchange hashpartitioning` | Shuffle — dado movendo entre executors | Minimizar shuffles |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Análise de Skew (Desbalanceamento de Dados)
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Escreva código para detectar skew nos dados de pedidos verificando
# MAGIC > a distribuição de registros por customer_id e por region.
# MAGIC > Mostre as top 10 chaves com mais registros e calcule o coeficiente de variação"*

# COMMAND ----------

# Análise de skew por customer_id — detecta clientes com volume desproporcional
# TODO: Copilot vai completar a análise de skew


# COMMAND ----------

# Análise de distribuição por região
# TODO: Copilot vai completar


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Verificando Partições e Paralelismo

# COMMAND ----------

# Verifique o número de partições atual — ideal: 2-4x o número de cores do cluster
print(f"Partições do df_orders: {df_orders.rdd.getNumPartitions()}")
print(f"Partições do df_customers: {df_customers.rdd.getNumPartitions()}")
print(f"spark.sql.shuffle.partitions: {spark.conf.get('spark.sql.shuffle.partitions')}")
print(f"Cores disponíveis: {sc.defaultParallelism}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Tamanho do Dataset de Clientes
# MAGIC
# MAGIC Esta informação é crucial para decidir se devemos usar Broadcast Join.

# COMMAND ----------

# Calcule o tamanho estimado do DataFrame de clientes em MB
# Regra: se < 200MB, use broadcast join
# TODO: Copilot vai sugerir como calcular o tamanho estimado

# Dica: spark.sessionState.executePlan(df.queryExecution.logical).optimizedPlan.stats.sizeInBytes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Resumo dos Gargalos Identificados
# MAGIC
# MAGIC > 💡 **Exercício:** Preencha o quadro abaixo com base na análise acima.
# MAGIC > Use o Copilot Chat para ajudar a interpretar os resultados.

# COMMAND ----------

# MAGIC %md
# MAGIC | # | Problema Identificado | Evidência | Solução Proposta |
# MAGIC |---|----------------------|-----------|-----------------|
# MAGIC | 1 | inferSchema no CSV | Scan duplo do arquivo | Schema explícito |
# MAGIC | 2 | SortMergeJoin com tabela pequena | Explain Plan | Broadcast Join |
# MAGIC | 3 | Sem cache antes de múltiplos groupBy | 3 shuffles repetidos | .cache() ou Delta |
# MAGIC | 4 | shuffle.partitions = 200 (default) | Muitas partições pequenas | Ajustar para n_cores * 2 |
# MAGIC | 5 | Escrita em CSV | Sem columnar storage | Converter para Delta Lake |
# MAGIC | 6 | count() prematuros | Acionam jobs desnecessários | Remover ou agrupar |
# MAGIC
# MAGIC **Próximo:** `03_optimized_pipeline.py` — implementaremos todas as correções!

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark UI — Análise Visual
# MAGIC
# MAGIC > 💡 **Exercício:** Acesse o Spark UI (link no canto superior do cluster) e:
# MAGIC > 1. Vá em **Stages** e identifique o stage com maior duração
# MAGIC > 2. Clique no stage e veja o **DAG Visualization**
# MAGIC > 3. Abra o Copilot Chat e descreva o que você vê — peça sugestões de otimização
