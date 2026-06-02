# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Hello Databricks
# MAGIC
# MAGIC **Objetivo:** Familiarizar-se com o ambiente Databricks e testar o Copilot.
# MAGIC
# MAGIC **Duração estimada:** 15 minutos
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 1: Verificando o Ambiente

# COMMAND ----------

# Verifique a versão do Spark e do Python
print(f"Spark version: {spark.version}")
print(f"Python version: {spark.sparkContext.pythonVer}")
print(f"App Name: {spark.sparkContext.appName}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 2: Primeiro DataFrame
# MAGIC
# MAGIC > 💡 **Exercício Copilot:** Digite o comentário abaixo e deixe o Copilot completar o código.

# COMMAND ----------

# Crie um DataFrame com 5 registros de funcionários contendo:
# id (inteiro), nome (string), departamento (string) e salario (float)
# Use spark.createDataFrame com uma lista de tuplas e defina o schema

# TODO: Deixe o Copilot completar este código após digitar o comentário acima


# COMMAND ----------

# Exiba o DataFrame com display() e mostre o schema
# TODO: Copilot vai sugerir as chamadas display() e printSchema()


# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 3: Operações Básicas com PySpark
# MAGIC
# MAGIC > 💡 **Exercício Copilot:** Use o Copilot Chat (`Ctrl+Alt+I`) e peça:
# MAGIC > *"Escreva código PySpark para filtrar funcionários com salário acima de 5000 e ordenar por nome"*

# COMMAND ----------

# Filtre funcionários com salário acima de R$ 5.000 e ordene por nome alfabeticamente
# TODO: Use o Copilot para completar


# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 4: SQL no Databricks
# MAGIC
# MAGIC > 💡 **Exercício Copilot:** Digite `-- Calcule` e veja as sugestões do Copilot

# COMMAND ----------

# Registre o DataFrame como uma view temporária para usar SQL
# df_funcionarios.createOrReplaceTempView("funcionarios")
# TODO: Complete o código acima e use a view abaixo

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Calcule a média de salário por departamento e ordene do maior para o menor
# MAGIC -- TODO: Copilot vai completar a query SQL

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 5: Lendo e Escrevendo no DBFS
# MAGIC
# MAGIC > 💡 **Exercício Copilot:** Descreva o que você quer fazer e deixe o Copilot gerar o código

# COMMAND ----------

# Salve o DataFrame de funcionários no DBFS no formato Delta Lake
# Caminho: /FileStore/training/funcionarios/
# Modo: overwrite
# TODO: Copilot vai sugerir o código de escrita Delta

# COMMAND ----------

# Leia de volta os dados salvos em Delta Lake e exiba
# TODO: Complete com ajuda do Copilot

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC
# MAGIC Você completou o módulo introdutório! Você praticou:
# MAGIC - Criar DataFrames PySpark
# MAGIC - Operações básicas de transformação
# MAGIC - Consultas SQL no Databricks
# MAGIC - Leitura e escrita no Delta Lake
# MAGIC - Uso do GitHub Copilot para geração de código
