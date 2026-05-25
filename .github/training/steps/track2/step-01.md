> **🎓 Trilha:** Projeto Lakehouse — Mãos à Obra (Módulo 4)
> **Participante:** {{PARTICIPANT_NAME}}
> **Progresso:** `[→] Bronze` `[ ] Silver` `[ ] Gold` `[ ] Concluído`

---

## 🏗️ Bem-vindo ao Projeto Lakehouse!

Nesta trilha você vai construir um projeto de dados de **ponta a ponta** usando a arquitetura **Medallion** (Bronze → Silver → Gold) com Databricks e GitHub Copilot.

Não é preciso conhecer tudo de antemão — o Copilot vai te ajudar em cada etapa!

### O que você vai construir

```
CSV (fonte)
    ↓
[Bronze]  → Dados brutos com rastreabilidade (audit trail)
    ↓
[Silver]  → Dados limpos, validados e enriquecidos
    ↓
[Gold]    → KPIs analíticos prontos para BI (RFM, tendências, rankings)
```

---

## ✅ Setup (Faça isso primeiro)

### 1. Databricks Community Edition
- [ ] Acesse https://community.cloud.databricks.com/ e crie sua conta gratuita
- [ ] Crie um cluster: **Compute → Create compute → Single Node → Runtime 14.x LTS**
- [ ] Aguarde o cluster ficar verde ✅

### 2. Codespaces / VS Code
O ambiente já vem configurado! Abra o Codespaces deste repositório:
- [ ] GitHub Copilot ativo (Ctrl+Alt+I abre o Chat)
- [ ] Extensão Databricks conectada ao seu workspace

### 3. Gerar e enviar dados de exemplo
```bash
make generate-data   # gera data/raw/orders.csv e customers.csv
make upload-data     # envia para dbfs:/FileStore/training/raw/
```

---

## 🥉 Etapa 1 — Camada Bronze: Ingestão com Rastreabilidade

Abra `notebooks/04_project_hands_on/01_bronze_ingestion.py` e implemente a função `ingest_to_bronze()`.

A função deve:
- [ ] Ler o CSV com **schema explícito** e modo `PERMISSIVE` (captura linhas corrompidas em `_corrupt_record`)
- [ ] Adicionar colunas de auditoria: `_ingestion_timestamp`, `_source_file`, `_ingestion_date`, `_pipeline_version`
- [ ] Salvar em Delta Lake no caminho especificado (modo `append`)
- [ ] Registrar como tabela no Catálogo Databricks (`CREATE TABLE IF NOT EXISTS ... USING DELTA LOCATION`)
- [ ] Retornar o total de registros ingeridos

### 💡 Prompt Copilot sugerido

No Copilot Chat (`Ctrl+Alt+I`):
> *"Implemente em PySpark uma função ingest_to_bronze que lê um CSV com StructType definido usando PERMISSIVE mode, adiciona as colunas _ingestion_timestamp (current_timestamp), _source_file (input_file_name()), _ingestion_date (current_date), _pipeline_version (lit '1.0.0'), salva em Delta Lake com modo append e registra como tabela no catálogo."*

### ▶️ Como avançar

Execute o notebook completo no Databricks, valide as queries SQL de verificação e faça commit:

```bash
git add notebooks/04_project_hands_on/01_bronze_ingestion.py
git commit -m "feat: bronze layer implementada"
git push origin main
```

> ⚡ O Actions detecta o commit e posta as instruções da **Camada Silver** aqui!
