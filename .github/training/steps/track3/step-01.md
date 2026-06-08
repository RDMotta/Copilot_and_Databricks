> **🎓 Trilha:** Otimização de Pipeline (Módulo 5)
> **Participante:** {{PARTICIPANT_NAME}}
> **Progresso:** `[→] Baseline` `[ ] Profiling` `[ ] Otimizado` `[ ] Concluído`

---

## 🚀 Bem-vindo à Trilha de Otimização de Pipeline!

Nesta trilha você vai aprender a **identificar e corrigir gargalos de performance** em pipelines PySpark usando ferramentas de diagnóstico do Databricks e o GitHub Copilot para implementar as soluções.

### O ciclo da otimização

```
[Baseline]  →  [Profiling]  →  [Otimizado]
 (medir)        (diagnosticar)   (corrigir + comparar)
```

---

## ✅ Setup (Faça isso primeiro)

### 1. Databricks Free Edition
- [ ] Acesse https://login.databricks.com/?dbx_source=docs&intent=CE_SIGN_UP e crie sua conta gratuita no Databricks Free Edition
- [ ] Crie um compute serverless disponível na Free Edition

### 2. Criar o Volume da trilha
Antes de começar o baseline, crie a pasta de entrada no Unity Catalog:

```sql
CREATE SCHEMA IF NOT EXISTS main.training_sql_serverless;
CREATE VOLUME IF NOT EXISTS main.training_sql_serverless.raw_files;
```

### 3. Gerar e enviar dados de exemplo
```bash
make generate-data   # gera data/raw/orders.csv e customers.csv
make upload-data     # envia para /Volumes/workspace/training_sql_serverless/raw_files/
```

---

## 🐢 Etapa 1 — Pipeline Baseline

Abra `notebooks/03_pipeline_optimization/01_baseline_pipeline.py` e **execute o notebook completo** no Databricks sem modificar nenhuma linha.

O pipeline tem **6 anti-patterns** intencionais marcados com `⚠️`:

| # | Anti-pattern | Localização | Impacto |
|---|-------------|-------------|---------|
| 1 | `inferSchema=True` | Leitura | Scan duplo do CSV |
| 2 | `count()` prematuro | Após leitura | Ação desnecessária |
| 3 | Sem `.cache()` antes de 3 groupBy | Pós-limpeza | Re-leitura 3x dos dados |
| 4 | `SortMergeJoin` com tabela pequena | Join | Shuffle desnecessário |
| 5 | `shuffle.partitions = 200` (default) | Aggregações | Partições excessivas |
| 6 | Escrita em CSV | Saída | Sem columnar storage |

### 📊 Anote os tempos abaixo (você vai comparar depois)

| Etapa | Tempo (s) |
|-------|-----------|
| Leitura | ___ |
| Limpeza | ___ |
| Join | ___ |
| Aggregações (3x) | ___ |
| Escrita | ___ |
| **Total** | **___** |

### 💡 Dica do Copilot

Após executar o baseline, abra o Copilot Chat e pergunte:
> *"Este código PySpark tem 6 anti-patterns de performance. Identifique-os e sugira otimizações em ordem de impacto."*

Cole os primeiros 30 linhas do código para dar contexto.

### ▶️ Como avançar

Adicione os tempos medidos como comentário no final do notebook e faça commit:

```bash
git add notebooks/03_pipeline_optimization/01_baseline_pipeline.py
git commit -m "feat: baseline medido - total XXs"
git push origin main
```

> ⚡ O Actions posta as instruções de **Profiling** aqui!
