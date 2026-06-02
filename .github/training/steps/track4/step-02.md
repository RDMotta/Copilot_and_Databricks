> **📈 Progresso:** `[x] Setup` `[→] Extracao` `[ ] Limpeza + ETL` `[ ] Concluido`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥈 Etapa 2 - Limpeza e Padronizacao (Silver SQL)

Agora que a Bronze esta pronta, transforme os dados em uma camada Silver confiavel.

Abra `notebooks/05_sql_warehouse_serverless/02_sql_cleaning_etl.sql`.

### 🎯 O que implementar

- [ ] Criar `silver_orders_clean` com:
  - cast de tipos
  - filtro de registros invalidos (`quantity`, `unit_price`, `status`)
  - remocao de duplicados por `order_id` com `row_number()`
  - `total_amount` calculado
- [ ] Criar `silver_customers_clean` com:
  - email normalizado (`lower(trim(email))`)
  - `is_valid_email` via regex
- [ ] Criar `silver_orders_enriched` com join entre pedidos e clientes

### 💡 Prompt Copilot sugerido

> "Escreva SQL com CTE para deduplicar pedidos por order_id usando row_number e manter o registro mais recente por order_date. Depois calcule total_amount e filtre quantity entre 1 e 100."

### ✅ Validacao esperada

- Tabela `silver_orders_clean` com menos linhas que Bronze (devido a deduplicacao e filtros)
- Tabela `silver_orders_enriched` com colunas de cliente preenchidas via join

### ▶️ Como avancar

```bash
git add notebooks/05_sql_warehouse_serverless/02_sql_cleaning_etl.sql
git commit -m "feat: track4 etapa 2 - silver sql etl"
git push origin main
```

> ⚡ O Actions vai postar a etapa de **Gold SQL + validacoes finais**.