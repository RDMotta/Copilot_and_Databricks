> **🎓 Trilha:** SQL Warehouse Serverless (Conta Free)
> **Participante:** {{PARTICIPANT_NAME}}
> **Progresso:** `[→] Setup` `[ ] Extracao` `[ ] Limpeza + ETL` `[ ] Concluido`

---

## 🧭 Bem-vindo a Trilha SQL Serverless

Nesta trilha voce vai executar um mini pipeline de dados usando apenas **Databricks SQL Warehouse** em conta free:

```
CSV no Volume Unity Catalog
   ↓
[Bronze SQL] dados brutos + auditoria
   ↓
[Silver SQL] limpeza e padronizacao
   ↓
[Gold SQL] KPIs analiticos
```

---

## ✅ Setup e Integracao (faca primeiro)

### 1. Criar SQL Warehouse serverless 2X-Small
- [ ] Acesse seu workspace Databricks (conta free)
- [ ] Va em **SQL Warehouses**
- [ ] Clique em **Create SQL Warehouse**
- [ ] Configure:
  - **Type:** `Serverless`
  - **Size:** `2X-Small`
  - **Auto Stop:** 10 min
- [ ] Inicie o warehouse e aguarde status **Running**

### 2. Integrar VS Code com Databricks SQL
- [ ] No VS Code, confirme a extensao Databricks instalada
- [ ] Abra Command Palette: `Databricks: Add Connection`
- [ ] Informe `DATABRICKS_HOST` e token pessoal
- [ ] No seletor de compute da extensao, escolha o SQL Warehouse `Serverless 2X-Small`

### 3. Preparar dados de entrada
Execute no terminal do projeto:

```bash
make generate-data
make upload-data
```

Os arquivos serao enviados para:
- `dbfs:/Volumes/workspace/training_sql_serverless/raw_files/orders.csv`
- `dbfs:/Volumes/workspace/training_sql_serverless/raw_files/customers.csv`

---

## 🥉 Etapa 1 - Extracao SQL para Bronze

Abra `notebooks/05_sql_warehouse_serverless/01_sql_setup_and_extract.sql` e implemente os TODOs.

Objetivo desta etapa:
- [ ] Criar schema SQL da trilha
- [ ] Criar o Volume Unity Catalog para os arquivos de entrada
- [ ] Ler CSVs do Volume com `read_files`
- [ ] Criar tabelas Bronze com colunas de auditoria
- [ ] Validar contagem de registros

### 💡 Prompt Copilot sugerido

> "Gere SQL para criar uma tabela bronze_orders_raw a partir de read_files no caminho dbfs:/Volumes/workspace/training_sql_serverless/raw_files/orders.csv, adicionando colunas _ingestion_timestamp e _source_file."

### ▶️ Como avancar

```bash
git add notebooks/05_sql_warehouse_serverless/01_sql_setup_and_extract.sql
git commit -m "feat: track4 etapa 1 - extracao bronze sql"
git push origin main
```

> ⚡ O Actions vai postar a etapa de **Limpeza + ETL (Silver)**.