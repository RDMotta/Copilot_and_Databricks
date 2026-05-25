> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[x] Etapa 4` `[x] Etapa 5` `[x] Etapa 6` `[→] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🚀 Etapa 7 — Pipeline Otimizado com Copilot

Chegou a hora de aplicar todas as otimizações identificadas! Você vai reescrever o pipeline baseline usando as melhores práticas Spark + Delta Lake, com o Copilot acelerando a implementação.

### 🎯 Objetivo
Implementar 7 otimizações de performance e comparar os resultados com o baseline. O objetivo é reduzir o tempo total em pelo menos **40%**.

### 📋 Otimizações a Implementar

Abra `notebooks/03_pipeline_optimization/03_optimized_pipeline.py`:

| # | Otimização | Técnica | Ganho Esperado |
|---|-----------|---------|----------------|
| 1 | Configurar AQE e parâmetros Spark | `spark.conf.set` | Base para as demais |
| 2 | Schema explícito | `StructType` | Elimina scan duplo |
| 3 | Filter pushdown + cache | `.filter()` encadeado + `.cache()` | Evita re-leitura |
| 4 | Broadcast Join | `F.broadcast()` | Elimina shuffle de clientes |
| 5 | Aggregações sobre cache | — | 3 groupBy sem re-scan |
| 6 | Escrita em Delta Lake | `.format("delta")` | Columnar + compressão |
| 7 | OPTIMIZE + Z-Order | SQL `OPTIMIZE ... ZORDER BY` | Acelera queries futuras |

### 💡 Uso do Copilot em cada otimização

Para a otimização **Broadcast Join**, use o Copilot Chat:
> *"Explique a diferença entre SortMergeJoin e BroadcastHashJoin no Spark. Quando devo usar broadcast? Como forço o uso com a hint F.broadcast()?"*

Para a otimização **OPTIMIZE + Z-Order**:
> *"O que é Z-Ordering no Delta Lake? Como o ZORDER BY funciona internamente e quais colunas devo usar?"*

### 📊 Preencha a tabela comparativa

| Etapa | Baseline (s) | Otimizado (s) | Ganho % |
|-------|-------------|---------------|---------|
| Leitura | ___ | ___ | ___ |
| Limpeza | ___ | ___ | ___ |
| Join | ___ | ___ | ___ |
| Aggregações | ___ | ___ | ___ |
| Escrita | ___ | ___ | ___ |
| **Total** | **___** | **___** | **___** |

### ▶️ Como avançar

```bash
git add notebooks/03_pipeline_optimization/03_optimized_pipeline.py
git commit -m "feat: etapa 7 concluída - pipeline otimizado"
git push origin main
```

> **Próximo módulo:** Projeto Lakehouse Ponta a Ponta 🏗️
> **Próximo notebook:** `notebooks/04_project_hands_on/01_bronze_ingestion.py`
