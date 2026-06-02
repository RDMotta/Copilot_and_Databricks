> **📈 Progresso:** `[x] Baseline` `[→] Profiling` `[ ] Otimizado` `[ ] Concluído`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🔍 Etapa 2 — Profiling: Identificando os Gargalos

Você tem os tempos do baseline. Agora vamos usar as ferramentas de diagnóstico do Spark para entender **por que** está lento e **onde** está o maior potencial de melhoria.

### 🎯 O que você vai analisar

Abra `notebooks/03_pipeline_optimization/02_profiling.py` e execute cada seção:

#### Seção 1 — Explain Plan (mais importante!)
Execute `df_join.explain(True)` e procure no output:

| Se você ver... | Significa | Gravidade |
|---------------|-----------|-----------|
| `SortMergeJoin` | Join com shuffle dos dois lados | 🔴 Alto |
| `Exchange hashpartitioning(200)` | 200 partições no shuffle | 🟡 Médio |
| `FileScan csv` | Lendo linha a linha | 🔴 Alto |
| `BroadcastHashJoin` | ✅ Join eficiente sem shuffle | ✅ OK |

**Copie o output do explain plan e cole no Copilot Chat:**
> *"Analise este explain plan do Apache Spark e liste os gargalos de performance em ordem de prioridade com as soluções recomendadas."*

#### Seção 2 — Análise de Skew
- [ ] Complete o código de análise de skew por `customer_id`
- Calcule: `stddev / mean` — se resultado > 1.0, há skew significativo
- O Spark 3+ com AQE detecta e corrige skew automaticamente

#### Seção 3 — Diagnóstico de Partições
Anote os valores:
- `df_orders.rdd.getNumPartitions()` → ___
- `spark.sql.shuffle.partitions` → 200 (default — vamos mudar para `n_cores * 2`)
- `sc.defaultParallelism` (cores disponíveis) → ___

#### Seção 4 — Tamanho do DataFrame de Clientes
Se o DataFrame de clientes for **< 200MB**, podemos usar `F.broadcast()` e eliminar o SortMergeJoin.

#### Seção 5 — Spark UI
- Acesse o **Spark UI** pelo link no painel do cluster (ícone de gráfico)
- Vá em **Stages** e clique no stage com maior duração
- Veja o **DAG Visualization** e identifique os estágios com Exchange (shuffle)

### 💡 Diagnóstico com Copilot

```
Tenho um pipeline PySpark com estas características:
- Dataset: 10.000 pedidos (CSV) + 500 clientes (CSV, ~50KB)
- inferSchema=True na leitura
- 3 groupBy separados sem cache intermediário
- Join resulta em SortMergeJoin (shuffle de ambos os lados)
- spark.sql.shuffle.partitions=200 com 2 cores disponíveis
- Saída em CSV

Quais são as 5 otimizações de maior impacto, em ordem de prioridade?
Inclua o ganho esperado para cada uma.
```

### 📋 Preencha o diagnóstico antes de commitar

| Problema Identificado | Evidência | Solução |
|----------------------|-----------|---------|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

### ▶️ Como avançar

```bash
git add notebooks/03_pipeline_optimization/02_profiling.py
git commit -m "feat: profiling concluido - N gargalos identificados"
git push origin main
```

> ⚡ O Actions posta as instruções do **Pipeline Otimizado** aqui! 🚀
