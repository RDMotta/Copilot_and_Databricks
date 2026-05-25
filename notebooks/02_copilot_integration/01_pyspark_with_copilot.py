# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — PySpark com GitHub Copilot
# MAGIC
# MAGIC **Objetivo:** Usar o GitHub Copilot para acelerar o desenvolvimento de pipelines PySpark reais.
# MAGIC
# MAGIC **Duração estimada:** 30 minutos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC > **Dinâmica:** Para cada bloco marcado com 💡, tente primeiro usar o Copilot
# MAGIC > para gerar o código, depois compare com a solução comentada abaixo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup: Importações e Dados de Exemplo

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType,
    DoubleType, TimestampType, ArrayType
)
from datetime import datetime

# COMMAND ----------

# Gere dados de vendas de e-commerce para os exercícios.
# Crie um DataFrame com as colunas:
# order_id (string), customer_id (string), product_category (string),
# product_name (string), quantity (int), unit_price (double),
# order_date (timestamp), region (string), status (string: completed/cancelled/pending)
# Gere pelo menos 20 registros variados para facilitar os exercícios de agregação

# TODO: Use o Copilot para gerar os dados de exemplo
# Dica: comece digitando "data = [" e o Copilot vai sugerir os registros


# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício 1: Limpeza e Validação de Dados
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função chamada clean_orders que recebe um DataFrame de pedidos e:
# MAGIC > 1) Remove duplicatas pela coluna order_id
# MAGIC > 2) Filtra apenas pedidos com status 'completed'
# MAGIC > 3) Remove pedidos com quantity <= 0 ou unit_price <= 0
# MAGIC > 4) Adiciona coluna total_amount = quantity * unit_price
# MAGIC > 5) Converte product_category para minúsculas"*

# COMMAND ----------

# Função de limpeza de pedidos conforme especificação acima
def clean_orders(df: DataFrame) -> DataFrame:
    # TODO: Copilot vai completar esta função
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício 2: Agregações e Métricas de Negócio
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função calculate_sales_metrics que recebe o DataFrame limpo e retorna
# MAGIC > um DataFrame com métricas por categoria: total de pedidos, receita total,
# MAGIC > ticket médio e quantidade média por pedido. Ordene por receita total decrescente."*

# COMMAND ----------

# Função para calcular métricas de vendas por categoria
def calculate_sales_metrics(df: DataFrame) -> DataFrame:
    # TODO: Copilot vai completar esta função
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício 3: Análise Temporal
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função analyze_sales_by_period que extrai ano e mês da order_date,
# MAGIC > agrupa por período e calcula receita total, variação percentual em relação
# MAGIC > ao período anterior usando window functions"*

# COMMAND ----------

# Análise temporal com window functions
def analyze_sales_by_period(df: DataFrame) -> DataFrame:
    # TODO: Copilot vai completar usando Window functions do PySpark
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício 4: Transformações Avançadas
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Crie uma função que classifica clientes em segmentos com base na receita total:
# MAGIC > 'VIP' (> 10000), 'Regular' (1000-10000), 'Ocasional' (< 1000).
# MAGIC > Use when/otherwise do PySpark e window functions para calcular o total por cliente"*

# COMMAND ----------

# Segmentação de clientes por receita
def segment_customers(df: DataFrame) -> DataFrame:
    # TODO: Copilot vai completar com when/otherwise e window functions
    pass


# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício 5: Pipeline Completo
# MAGIC
# MAGIC > 💡 **Exercício final:** Monte o pipeline completo chamando todas as funções criadas.
# MAGIC > Use o Copilot Chat para verificar se há algum problema no código.

# COMMAND ----------

# Monte o pipeline completo:
# 1. Aplique clean_orders no df_orders
# 2. Calcule as métricas de vendas
# 3. Faça a análise temporal
# 4. Segmente os clientes
# 5. Exiba os resultados de cada etapa com display()

# TODO: Copilot vai montar a orquestração do pipeline


# COMMAND ----------

# MAGIC %md
# MAGIC ## Salvar Resultados em Delta Lake
# MAGIC
# MAGIC > 💡 **Prompt para o Copilot:**
# MAGIC > *"Salve cada DataFrame resultado em Delta Lake no DBFS em /FileStore/training/results/,
# MAGIC > usando o nome da tabela como subpasta. Use modo overwrite."*

# COMMAND ----------

# Salve os resultados em Delta Lake
# Caminhos sugeridos:
# - /FileStore/training/results/sales_metrics/
# - /FileStore/training/results/sales_by_period/
# - /FileStore/training/results/customer_segments/

# TODO: Copilot vai completar o código de escrita


# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC
# MAGIC Neste notebook você praticou:
# MAGIC - Usar o Copilot para gerar funções PySpark complexas a partir de descrições
# MAGIC - Transformações: filter, withColumn, groupBy, agg
# MAGIC - Window functions: lag, rank, partitionBy
# MAGIC - Segmentação com when/otherwise
# MAGIC - Salvar resultados em Delta Lake
# MAGIC
# MAGIC **Próximo:** `02_sql_with_copilot.sql`
