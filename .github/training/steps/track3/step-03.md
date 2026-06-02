> **📈 Progresso:** `[x] Baseline` `[x] Profiling` `[→] Otimizado` `[ ] Concluído`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## ⚡ Etapa 3 — Pipeline Otimizado

Você identificou os gargalos. Agora é hora de aplicar todas as otimizações e medir o ganho real!

### 🎯 As 7 Otimizações (implemente em ordem)

Abra `notebooks/03_pipeline_optimization/03_optimized_pipeline.py`:

#### Otimização 1 — Configurar AQE e parâmetros Spark
```python
n_cores = sc.defaultParallelism
spark.conf.set("spark.sql.shuffle.partitions", str(n_cores * 2))
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
```

#### Otimização 2 — Schema explícito (elimina inferSchema)
> 💡 Copilot Chat: *"Crie StructType explícito para um CSV de pedidos com as colunas: order_id (String), customer_id (String), product_category (String), product_name (String), quantity (Integer), unit_price (Double), order_date (String), region (String), status (String)"*

#### Otimização 3 — Filter pushdown + Cache estratégico
- [ ] Encadeie **todos** os filtros em uma única chamada `.filter(condição1 & condição2 & ...)`
- [ ] Aplique `.cache()` logo após as transformações
- [ ] Materialize com `.count()` antes das operações seguintes

#### Otimização 4 — Broadcast Join
```python
df_enriched = df_orders_clean.join(
    F.broadcast(df_customers),  # ← elimina SortMergeJoin
    on="customer_id",
    how="left"
)
```
Verifique no explain que apareceu `BroadcastHashJoin` em vez de `SortMergeJoin`.

#### Otimização 5 — Aggregações sobre cache
- [ ] Com o DF cacheado, as 3 aggregações leem do cache (sem re-scan do CSV)
- [ ] Encadeie as 3 chamadas de groupBy na sequência

#### Otimização 6 — Escrita em Delta Lake
```python
df.write.format("delta").mode("overwrite").partitionBy("order_year").save(path)
```

#### Otimização 7 — OPTIMIZE + Z-Order
```sql
OPTIMIZE training.orders_enriched ZORDER BY (customer_id, order_date)
```

### 📊 Preencha a tabela comparativa (objetivo: ≥40% de ganho total)

| Etapa | Baseline (s) | Otimizado (s) | Ganho % |
|-------|-------------|---------------|---------|
| Leitura | ___ | ___ | ___ |
| Limpeza | ___ | ___ | ___ |
| Join | ___ | ___ | ___ |
| Aggregações | ___ | ___ | ___ |
| Escrita | ___ | ___ | ___ |
| **Total** | **___** | **___** | **___** |

### 💡 Prompt Copilot — Revisão Final

Após implementar todas as otimizações, peça ao Copilot Chat uma revisão:
> *"Revise este pipeline PySpark otimizado e verifique se há alguma otimização adicional que eu possa aplicar, considerando que estou usando Delta Lake e AQE habilitado."*

### ▶️ Finalizar a trilha

Adicione a tabela comparativa como comentário no notebook e faça commit:

```bash
git add notebooks/03_pipeline_optimization/03_optimized_pipeline.py
git commit -m "feat: pipeline otimizado - ganho de XX% no tempo total"
git push origin main
```

> ⚡ O Actions detecta o commit, posta a mensagem de conclusão e **fecha esta issue automaticamente!** 🏆
