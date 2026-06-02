> **📈 Progresso:** `[x] Bronze` `[→] Silver` `[ ] Gold` `[ ] Concluído`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥈 Camada Silver — Limpeza, Validação e Enriquecimento

A Bronze está pronta com os dados brutos rastreados. Agora vamos transformá-los em dados **limpos e confiáveis** — essa é a responsabilidade da camada Silver.

### 🎯 O que você vai implementar

Abra `notebooks/04_project_hands_on/02_silver_transform.py`:

#### Função `clean_silver_orders(df)`
- [ ] Excluir registros com `_corrupt_record` não nulo
- [ ] Remover duplicatas por `order_id` (manter o mais recente por `_ingestion_timestamp`)
- [ ] Converter `order_date` para `TimestampType`
- [ ] Normalizar `product_category` e `region`: `F.lower(F.trim(...))`
- [ ] Filtrar registros válidos: `1 ≤ quantity ≤ 100` e `0.01 ≤ unit_price ≤ 50000`
- [ ] Calcular `total_amount = quantity * unit_price`
- [ ] Adicionar coluna `order_value_tier` (faixas: "low" < 200, "medium" < 1000, "high" ≥ 1000)
- [ ] Remover colunas de auditoria Bronze (prefixo `_`)

#### Função `clean_silver_customers(df)`
- [ ] Normalizar `email` para lowercase
- [ ] Adicionar `is_valid_email` (boolean) usando `F.col("email").rlike(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")`
- [ ] Converter `signup_date` para `DateType`

#### Enriquecimento Silver
- [ ] Join de pedidos limpos + clientes com `F.broadcast()` (tabela de clientes é pequena)
- [ ] Adicionar: `customer_name`, `customer_city`, `customer_segment`

#### Salvar + Relatório de Qualidade
- [ ] Salvar em Delta Lake particionado por `order_year`
- [ ] Gerar relatório: quantos registros entraram vs. saíram (taxa de aproveitamento)

### 💡 Prompt Copilot sugerido

```
Implemente a função clean_silver_orders em PySpark que:
1. Filtra registros onde _corrupt_record é nulo
2. Remove duplicatas por order_id mantendo o mais recente por _ingestion_timestamp usando Window
3. Converte order_date para TimestampType
4. Aplica lower e trim em product_category e region
5. Filtra quantity entre 1 e 100 e unit_price entre 0.01 e 50000
6. Calcula total_amount = round(quantity * unit_price, 2)
7. Adiciona order_value_tier com when/otherwise (low/medium/high)
8. Remove colunas que começam com underscore usando select com list comprehension
```

### 📊 Métricas esperadas após limpeza

Com os dados do `generate_sample_data.py`:
- Pedidos Bronze → ~10.100 registros (com duplicatas e negativos)
- Pedidos Silver → ~7.400 registros (apenas `completed` + válidos + sem dup)
- Taxa de aproveitamento: ~73%

### ▶️ Como avançar

```bash
git add notebooks/04_project_hands_on/02_silver_transform.py
git commit -m "feat: silver layer implementada"
git push origin main
```

> ⚡ O Actions posta as instruções da **Camada Gold** aqui! Você está quase lá 🏆
