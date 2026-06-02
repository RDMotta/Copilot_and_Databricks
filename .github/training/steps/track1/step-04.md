> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[→] Etapa 4` `[ ] Etapa 5` `[ ] Etapa 6` `[ ] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🗄️ Etapa 4 — SQL Analítico com GitHub Copilot

Hora de explorar o poder do Databricks SQL! O Copilot é excelente para gerar queries analíticas complexas — CTEs, window functions, análises estatísticas e operações Delta Lake.

### 🎯 Objetivo
Usar o Copilot para escrever queries SQL avançadas no Databricks, incluindo upsert com `MERGE INTO` e consultas de auditoria com Time Travel.

### 📋 Tarefas

Abra `notebooks/02_copilot_integration/02_sql_with_copilot.sql` e complete os 5 exercícios:

| # | Exercício | Técnica SQL |
|---|-----------|------------|
| 1 | Ranking de produtos por categoria (top 3) | CTE + `ROW_NUMBER()` / `RANK()` |
| 2 | Análise de coorte de clientes | Self-join + `DATE_TRUNC` |
| 3 | Detecção de anomalias por z-score | `STDDEV`, `AVG` em window |
| 4 | Upsert com `MERGE INTO` (Delta Lake) | `WHEN MATCHED` / `NOT MATCHED` |
| 5 | Time Travel — comparar versões da tabela | `VERSION AS OF` |

### 💡 Dica do Copilot para SQL

No arquivo `.sql`, o Copilot responde bem a comentários `--`:
```sql
-- Calcule a receita acumulada por mês usando SUM() OVER com ROWS UNBOUNDED PRECEDING
```
Digite o comentário, pressione `Enter` e aguarde a sugestão aparecer!

### ⭐ Desafio Extra
Após completar os 5 exercícios, abra o Copilot Chat e peça:
> *"Otimize esta query SQL para rodar mais rápido no Databricks, considerando Delta Lake e particionamento"*

Avalie as sugestões e aplique pelo menos uma otimização.

### ▶️ Como avançar

```bash
git add notebooks/02_copilot_integration/02_sql_with_copilot.sql
git commit -m "feat: etapa 4 concluída - sql com copilot"
git push origin main
```

> **Próximo módulo:** Otimização de Pipeline 🚀
> **Próximo notebook:** `notebooks/03_pipeline_optimization/01_baseline_pipeline.py`
