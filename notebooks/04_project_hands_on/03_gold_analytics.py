# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Projeto Hands-On: Camada Gold (Analytics)
# MAGIC
# MAGIC **Objetivo:** Construir a camada analítica com KPIs de negócio prontos para consumo
# MAGIC por ferramentas de BI, dashboards e relatórios executivos.
# MAGIC
# MAGIC **Duração estimada:** 25 minutos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## O que fazemos na Gold:
# MAGIC - KPIs agregados por diferentes dimensões
# MAGIC - Métricas de negócio calculadas
# MAGIC - Tabelas desnormalizadas para performance de leitura
# MAGIC - Views para consumo por BI tools

# COMMAND ----------

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

GOLD_PATH = "/FileStore/training/ecommerce_lakehouse/gold"
spark.sql("USE ecommerce_lakehouse")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup: Ler da Camada Silver

# COMMAND ----------

df_silver = spark.table("silver_orders_enriched")
df_customers = spark.table("silver_customers")

display(df_silver.limit(3))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 1: Dashboard Executivo (KPIs Gerais)
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma tabela gold_executive_kpis com as seguintes métricas calculadas:
# MAGIC > receita total, número de pedidos, ticket médio, número de clientes únicos,
# MAGIC > receita por cliente, e top categoria por receita. Retorne uma única linha de KPIs."*

# COMMAND ----------

def build_executive_kpis(df: DataFrame) -> DataFrame:
    """Constrói tabela de KPIs executivos — uma linha com todos os indicadores globais."""
    # TODO: Copilot vai completar — use agg() com múltiplas métricas
    pass


df_gold_kpis = build_executive_kpis(df_silver)
display(df_gold_kpis)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 2: Performance por Categoria
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma tabela gold_category_performance com: receita total, quantidade de pedidos,
# MAGIC > ticket médio, participação percentual na receita total, e ranking por receita.
# MAGIC > Use window functions para calcular percentual e ranking."*

# COMMAND ----------

def build_category_performance(df: DataFrame) -> DataFrame:
    """
    KPIs por categoria de produto com share de receita e ranking.
    """
    # TODO: Copilot vai usar window functions para pct e rank
    pass


df_gold_category = build_category_performance(df_silver)
display(df_gold_category)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 3: Tendência Mensal de Vendas (com Variação MoM)
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma tabela gold_monthly_trend com receita e pedidos por mês/ano,
# MAGIC > variação percentual da receita em relação ao mês anterior (MoM) usando lag(),
# MAGIC > e média móvel de 3 meses."*

# COMMAND ----------

def build_monthly_trend(df: DataFrame) -> DataFrame:
    """
    Tendência mensal com variação MoM e média móvel.
    """
    w_time = Window.orderBy("order_year", "order_month")
    w_rolling = Window.orderBy("order_year", "order_month").rowsBetween(-2, 0)

    # TODO: Copilot vai completar com lag() e avg() sobre window
    pass


df_gold_monthly = build_monthly_trend(df_silver)
display(df_gold_monthly)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 4: Análise de Clientes (RFM)
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Implemente uma análise RFM (Recency, Frequency, Monetary) para segmentação de clientes:
# MAGIC > - Recency: dias desde o último pedido
# MAGIC > - Frequency: número de pedidos
# MAGIC > - Monetary: receita total
# MAGIC > Calcule scores de 1 a 5 para cada dimensão usando ntile(5) e classifique em segmentos:
# MAGIC > Champions, Loyal, At Risk, Lost"*

# COMMAND ----------

def build_rfm_analysis(df: DataFrame) -> DataFrame:
    """
    Segmentação RFM de clientes com scores e classificação.
    """
    from pyspark.sql.functions import datediff, current_date, ntile, when

    # Calcular métricas RFM base
    # TODO: Copilot vai completar o cálculo de R, F, M e scores

    # Regras de classificação (exemplos):
    # Champions:    R>=4, F>=4, M>=4
    # Loyal:        F>=3, M>=3
    # At Risk:      R<=2, F>=2
    # Lost:         R=1, F=1
    # Others:       demais
    pass


df_gold_rfm = build_rfm_analysis(df_silver)
display(df_gold_rfm)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold 5: Tabela Regional
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie a tabela gold_regional_summary com receita, pedidos e ticket médio por região,
# MAGIC > incluindo o top produto por receita em cada região usando first() sobre window"*

# COMMAND ----------

# TODO: Copilot vai completar esta função
def build_regional_summary(df: DataFrame) -> DataFrame:
    pass


df_gold_regional = build_regional_summary(df_silver)
display(df_gold_regional)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Salvar Camada Gold

# COMMAND ----------

gold_tables = {
    "gold_executive_kpis":    (df_gold_kpis,     None),
    "gold_category_perf":     (df_gold_category,  None),
    "gold_monthly_trend":     (df_gold_monthly,   None),
    "gold_rfm":               (df_gold_rfm,        None),
    "gold_regional_summary":  (df_gold_regional,  None),
}

for table_name, (df, partition_col) in gold_tables.items():
    if df is None:
        print(f"⏭ {table_name}: função não implementada ainda")
        continue

    path = f"{GOLD_PATH}/{table_name}"
    writer = df.write.format("delta").mode("overwrite").option("overwriteSchema", "true")

    if partition_col:
        writer = writer.partitionBy(partition_col)

    writer.save(path)

    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS ecommerce_lakehouse.{table_name}
        USING DELTA LOCATION '{path}'
    """)
    print(f"✅ {table_name} salva")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Criar Views para Consumo por BI
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie views SQL que combinam as tabelas Gold para dashboards de BI:
# MAGIC > uma view de resumo executivo e uma view de performance detalhada por categoria e período"*

# COMMAND ----------

# MAGIC %sql
# MAGIC -- View de resumo executivo para o dashboard principal
# MAGIC CREATE OR REPLACE VIEW ecommerce_lakehouse.vw_executive_summary AS
# MAGIC SELECT
# MAGIC     k.*,
# MAGIC     r.region,
# MAGIC     r.total_revenue AS regional_revenue
# MAGIC FROM ecommerce_lakehouse.gold_executive_kpis k
# MAGIC CROSS JOIN ecommerce_lakehouse.gold_regional_summary r
# MAGIC ORDER BY r.total_revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Listagem final de todas as tabelas do projeto
# MAGIC SHOW TABLES IN ecommerce_lakehouse;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Projeto Lakehouse Completo!
# MAGIC
# MAGIC ### O que você construiu:
# MAGIC
# MAGIC | Camada | Tabelas | Descrição |
# MAGIC |--------|---------|-----------|
# MAGIC | Bronze | `bronze_orders`, `bronze_customers` | Dados brutos com auditoria |
# MAGIC | Silver | `silver_orders_enriched`, `silver_customers` | Dados limpos e enriquecidos |
# MAGIC | Gold | `gold_executive_kpis`, `gold_category_perf`, `gold_monthly_trend`, `gold_rfm`, `gold_regional_summary` | KPIs analíticos |
# MAGIC
# MAGIC ### Tecnologias utilizadas:
# MAGIC - Apache Spark (PySpark + SQL)
# MAGIC - Delta Lake (ACID, Time Travel, OPTIMIZE, Z-Order)
# MAGIC - GitHub Copilot (geração de código, sugestões, chat)
# MAGIC - Databricks Catalog (governança de tabelas)
# MAGIC
# MAGIC ### Próximos passos:
# MAGIC - Conectar Databricks SQL ao Power BI ou Tableau
# MAGIC - Agendar o pipeline como um Databricks Job
# MAGIC - Adicionar monitoramento com Delta Live Tables
# MAGIC - Explorar Unity Catalog para governança avançada
