-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 02 — SQL no Databricks com GitHub Copilot
-- MAGIC
-- MAGIC **Objetivo:** Usar o Copilot para escrever queries SQL analíticas no Databricks SQL.
-- MAGIC
-- MAGIC **Duração estimada:** 20 minutos
-- MAGIC
-- MAGIC ---

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Setup: Criando as Tabelas de Exemplo

-- COMMAND ----------

-- Crie um banco de dados para o treinamento
CREATE DATABASE IF NOT EXISTS training;
USE training;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Exercício 1: CTEs e Agregações
-- MAGIC
-- MAGIC > 💡 **Prompt para o Copilot:**
-- MAGIC > *"Escreva uma query SQL usando CTEs que calcula o ranking de produtos
-- MAGIC > por receita total dentro de cada categoria, mostrando apenas o top 3 por categoria"*

-- COMMAND ----------

-- Ranking de produtos por receita por categoria (top 3 por categoria)
-- Use WITH (CTE) e ROW_NUMBER() ou RANK()
-- TODO: Copilot vai completar a query

WITH sales_by_product AS (
    -- TODO: Copilot vai sugerir a agregação aqui
),
ranked_products AS (
    -- TODO: Copilot vai sugerir o window function aqui
)
-- TODO: SELECT final com filtro de top 3

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Exercício 2: Análise de Coorte
-- MAGIC
-- MAGIC > 💡 **Prompt para o Copilot:**
-- MAGIC > *"Crie uma query que analisa a coorte de clientes por mês de primeiro pedido,
-- MAGIC > mostrando a retenção mês a mês em formato de matriz"*

-- COMMAND ----------

-- Análise de coorte: retenção de clientes por mês
-- TODO: Copilot vai gerar a query de coorte

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Exercício 3: Detecção de Anomalias
-- MAGIC
-- MAGIC > 💡 **Prompt para o Copilot:**
-- MAGIC > *"Escreva uma query que identifica pedidos com valor anormalmente alto,
-- MAGIC > definindo anomalia como: total_amount > média + 2 * desvio padrão por categoria"*

-- COMMAND ----------

-- Detecção de pedidos anômalos usando estatística (z-score)
-- Retorne: order_id, category, total_amount, z_score, classificado como 'anomalia' ou 'normal'
-- TODO: Copilot vai usar funções de janela + estatística

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Exercício 4: Tabela Delta com Merge (Upsert)
-- MAGIC
-- MAGIC > 💡 **Prompt para o Copilot:**
-- MAGIC > *"Crie um MERGE INTO que atualiza a tabela de resumo de clientes.
-- MAGIC > Se o cliente já existe: atualiza total_orders, total_revenue e last_order_date.
-- MAGIC > Se não existe: insere o novo registro."*

-- COMMAND ----------

-- Upsert na tabela de resumo de clientes usando MERGE INTO (sintaxe Delta Lake)
-- TODO: Copilot vai gerar o MERGE INTO com MATCHED e NOT MATCHED

MERGE INTO training.customer_summary AS target
USING (
    -- TODO: Copilot vai sugerir a subquery de novos dados
) AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
    -- TODO: Copilot vai sugerir o UPDATE SET
WHEN NOT MATCHED THEN
    -- TODO: Copilot vai sugerir o INSERT

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Exercício 5: Time Travel no Delta Lake
-- MAGIC
-- MAGIC > 💡 **Prompt para o Copilot:**
-- MAGIC > *"Mostre como usar o Time Travel do Delta Lake para comparar o estado
-- MAGIC > da tabela entre duas versões e identificar registros que mudaram"*

-- COMMAND ----------

-- Ver histórico de versões da tabela
DESCRIBE HISTORY training.customer_summary;

-- COMMAND ----------

-- Comparar dados entre versão atual e versão anterior
-- TODO: Copilot vai usar VERSION AS OF ou TIMESTAMP AS OF

-- Dados na versão 0 (primeira versão)
-- SELECT * FROM training.customer_summary VERSION AS OF 0;

-- COMMAND ----------

-- Encontrar registros que mudaram entre versões
-- TODO: Copilot vai sugerir um EXCEPT ou JOIN entre as versões

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## ✅ Checkpoint
-- MAGIC
-- MAGIC Você praticou SQL avançado no Databricks com o Copilot:
-- MAGIC - CTEs e Window Functions
-- MAGIC - Análise de coorte
-- MAGIC - Detecção de anomalias com estatística
-- MAGIC - MERGE INTO (upsert) no Delta Lake
-- MAGIC - Time Travel para auditoria
-- MAGIC
-- MAGIC **Próximo:** Módulo de Otimização de Pipeline
