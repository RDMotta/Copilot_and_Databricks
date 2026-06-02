> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[x] Etapa 4` `[x] Etapa 5` `[x] Etapa 6` `[x] Etapa 7` `[→] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥉 Etapa 8 — Projeto Lakehouse: Camada Bronze

Parabéns por concluir o módulo de otimização! Agora começa o projeto final: você vai construir um **Lakehouse de E-commerce** completo com arquitetura Medallion (Bronze → Silver → Gold).

A camada **Bronze** é a fundação — armazena os dados brutos exatamente como chegam da fonte, com metadados de auditoria.

### 🎯 Objetivo
Implementar a função `ingest_to_bronze()` que ingere dados CSV para o Delta Lake com rastreabilidade completa.

### 📋 Tarefas

Abra `notebooks/04_project_hands_on/01_bronze_ingestion.py`:

#### 1. Implementar `ingest_to_bronze()`
A função deve:
- [ ] Ler o CSV com schema definido e modo `PERMISSIVE` (captura erros em `_corrupt_record`)
- [ ] Adicionar colunas de auditoria:
  - `_ingestion_timestamp` → `F.current_timestamp()`
  - `_source_file` → `F.input_file_name()`
  - `_ingestion_date` → `F.current_date()`
  - `_pipeline_version` → `F.lit("1.0.0")`
- [ ] Salvar em Delta Lake com modo `append`
- [ ] Registrar a tabela no Catálogo Databricks
- [ ] Retornar o total de registros ingeridos

#### 2. Executar a ingestão
- [ ] Ingeste `orders.csv` → `bronze_orders`
- [ ] Ingeste `customers.csv` → `bronze_customers`

#### 3. Validar os dados ingeridos
- [ ] Contar registros vs. registros corrompidos (`_corrupt_record` não nulo)
- [ ] Verificar range de datas
- [ ] Confirmar metadados de auditoria

### 💡 Prompt para o Copilot

```
Implemente uma função Python/PySpark chamada ingest_to_bronze que:
1. Lê um CSV com schema StructType usando modo PERMISSIVE
2. Adiciona as colunas: _ingestion_timestamp (current_timestamp), 
   _source_file (input_file_name()), _ingestion_date (current_date),
   _pipeline_version (literal string "1.0.0")
3. Salva em Delta Lake no caminho especificado com modo append
4. Registra como tabela no catálogo com CREATE TABLE IF NOT EXISTS ... USING DELTA LOCATION
5. Retorna o count de registros ingeridos
```

### 🏗️ Arquitetura que você está construindo

```
CSV (FileStore)
     ↓
 bronze_orders          ← você está aqui
 bronze_customers
     ↓
 [silver_orders_enriched]   (próxima etapa)
 [silver_customers]
     ↓
 [gold_executive_kpis]      (etapa final)
 [gold_category_perf]
 [gold_rfm]
```

### ▶️ Como avançar

```bash
git add notebooks/04_project_hands_on/01_bronze_ingestion.py
git commit -m "feat: etapa 8 concluída - bronze layer implementada"
git push origin main
```

> **Próximo notebook:** `notebooks/04_project_hands_on/02_silver_transform.py`
