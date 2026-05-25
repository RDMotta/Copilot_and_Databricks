> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[x] Etapa 4` `[→] Etapa 5` `[ ] Etapa 6` `[ ] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🐢 Etapa 5 — Pipeline Baseline (Intencionalmente Lento)

Chegamos ao módulo de otimização! Nesta etapa você vai executar um pipeline **propositalmente ingênuo** e medir o tempo de cada etapa. Esses números serão seu ponto de comparação depois da otimização.

### 🎯 Objetivo
Executar o pipeline baseline, identificar os **6 problemas de performance** embutidos no código e anotar os tempos de execução.

### 📋 Tarefas

Abra `notebooks/03_pipeline_optimization/01_baseline_pipeline.py`:

1. **Execute o notebook completo** no Databricks e anote os tempos de cada etapa
2. **Identifique os problemas** — o código tem 6 anti-patterns intencionais marcados com `⚠️`:

| Anti-pattern | Linha | Impacto |
|-------------|-------|---------|
| `inferSchema=True` | Leitura | Scan duplo do arquivo |
| `count()` prematuro | Após leitura | Ação desnecessária antes do pipeline |
| Sem cache antes de múltiplos groupBy | Limpeza | Re-leitura do CSV 3 vezes |
| `SortMergeJoin` com tabela pequena | Join | Shuffle desnecessário |
| `shuffle.partitions = 200` (default) | Aggregações | Muitas partições pequenas |
| Escrita em CSV | Saída | Sem columnar storage, sem compressão |

3. **Preencha a tabela de tempos** no comentário `%md` no final do notebook

### 📊 Anote aqui seus tempos (antes de commitar)

| Etapa | Tempo (s) |
|-------|-----------|
| Leitura | ___ |
| Limpeza | ___ |
| Join | ___ |
| Aggregações (3x) | ___ |
| Escrita | ___ |
| **Total** | **___** |

### 💡 Dica do Copilot

Abra o Copilot Chat e cole o explain plan gerado pelo notebook:
> *"Analise este explain plan do Spark e liste os principais gargalos de performance em ordem de prioridade"*

### ▶️ Como avançar

```bash
git add notebooks/03_pipeline_optimization/01_baseline_pipeline.py
git commit -m "feat: etapa 5 concluída - baseline medido"
git push origin main
```

> **Próximo notebook:** `notebooks/03_pipeline_optimization/02_profiling.py`
