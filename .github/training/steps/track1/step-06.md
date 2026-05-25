> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[x] Etapa 4` `[x] Etapa 5` `[→] Etapa 6` `[ ] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🔍 Etapa 6 — Profiling: Encontrando os Gargalos

Agora que temos o baseline, vamos usar as ferramentas de diagnóstico do Databricks + Copilot para entender **por que** o pipeline está lento e **onde** está o maior ganho.

### 🎯 Objetivo
Usar `explain()`, Spark UI e análise de skew para gerar um diagnóstico completo de performance antes de otimizar.

### 📋 Tarefas

Abra `notebooks/03_pipeline_optimization/02_profiling.py` e execute cada seção:

#### Seção 1 — Explain Plan
- Execute `df_join.explain(True)` e identifique se o join é `SortMergeJoin` ou `BroadcastHashJoin`
- Abra o Copilot Chat e cole o output do explain plan pedindo análise

#### Seção 2 — Análise de Skew
- Complete o código de análise de distribuição por `customer_id`
- Calcule o coeficiente de variação (CV = desvio padrão / média)
- CV > 1.0 indica skew significativo

#### Seção 3 — Partições e Paralelismo
- Verifique o número atual de partições vs. cores disponíveis
- A regra geral: `shuffle.partitions` = 2 a 4x o número de cores

#### Seção 4 — Tamanho para Broadcast
- Calcule o tamanho estimado do DataFrame de clientes
- Se < 200MB → candidate a Broadcast Join

#### Seção 5 — Spark UI
- Acesse o **Spark UI** pelo link no painel do cluster
- Identifique o stage com maior duração
- Tire um screenshot e descreva o DAG no Copilot Chat

### 💡 Prompt Poderoso para o Copilot

```
Tenho um pipeline PySpark com as seguintes características:
- Dataset: 10.000 pedidos (CSV) + 500 clientes (CSV)
- Join: SortMergeJoin (shuffle.partitions = 200)
- 3 groupBy separados sem cache
- Escrita em CSV

Quais são as 5 otimizações de maior impacto que devo aplicar, em ordem de prioridade?
```

### ▶️ Como avançar

```bash
git add notebooks/03_pipeline_optimization/02_profiling.py
git commit -m "feat: etapa 6 concluída - profiling realizado"
git push origin main
```

> **Próximo notebook:** `notebooks/03_pipeline_optimization/03_optimized_pipeline.py`
> Este é o grande momento — vamos aplicar todas as otimizações! 🚀
