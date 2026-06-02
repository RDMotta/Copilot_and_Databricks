> **📈 Progresso:** `[x] Setup` `[x] Extracao` `[→] Limpeza + ETL` `[ ] Concluido`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥇 Etapa 3 - Gold SQL e KPI Analitico

Com Silver pronta, crie uma camada Gold para consumo em BI.

Abra `notebooks/05_sql_warehouse_serverless/03_sql_gold_validation.sql`.

### 🎯 O que implementar

- [ ] Criar `gold_daily_kpis` com:
  - `order_date`
  - quantidade de pedidos
  - receita total
  - ticket medio
- [ ] Criar `gold_top_categories` com ranking por receita
- [ ] Criar query de validacao de qualidade dos dados:
  - nulos em chaves
  - pedidos sem cliente correspondente
  - percentual de emails invalidos

### 💡 Prompt Copilot sugerido

> "Gere SQL para tabela Gold com KPIs diarios (orders_count, revenue_total, avg_ticket) a partir de silver_orders_enriched, agrupando por date(order_date)."

### ▶️ Finalizar trilha

```bash
git add notebooks/05_sql_warehouse_serverless/03_sql_gold_validation.sql
git commit -m "feat: track4 etapa 3 - gold sql concluida"
git push origin main
```

> ⚡ O Actions detecta o commit e fecha a issue da trilha automaticamente.