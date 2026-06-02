> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[x] Etapa 4` `[x] Etapa 5` `[x] Etapa 6` `[x] Etapa 7` `[x] Etapa 8` `[→] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥈 Etapa 9 — Projeto Lakehouse: Camada Silver

A Bronze está pronta — agora vamos transformar os dados brutos em dados limpos, validados e prontos para análise. A camada **Silver** é onde aplicamos regras de qualidade de dados e lógica de negócio.

### 🎯 Objetivo
Implementar as funções de limpeza e enriquecimento que transformam Bronze → Silver, aplicando validações de dados e gerando um relatório de qualidade.

### 📋 Tarefas

Abra `notebooks/04_project_hands_on/02_silver_transform.py`:

#### 1. Implementar `clean_silver_orders()`
- [ ] Excluir registros com `_corrupt_record` não nulo
- [ ] Remover duplicatas por `order_id` (manter o mais recente por `_ingestion_timestamp`)
- [ ] Converter `order_date` para `TimestampType`
- [ ] Normalizar `product_category` e `region` com `lower().trim()`
- [ ] Filtrar: `1 ≤ quantity ≤ 100` e `0.01 ≤ unit_price ≤ 50.000`
- [ ] Adicionar `total_amount` e `order_value_tier` (faixas de valor)
- [ ] Remover colunas de auditoria Bronze (prefixo `_`)

#### 2. Implementar `clean_silver_customers()`
- [ ] Normalizar `email` para lowercase
- [ ] Validar formato de email com regex → adicionar `is_valid_email` (boolean)
- [ ] Converter `signup_date` para `DateType`

#### 3. Enriquecimento Silver
- [ ] Join de pedidos + clientes com Broadcast Join
- [ ] Colunas do cliente: `customer_name`, `customer_city`, `customer_segment`

#### 4. Salvar e gerar relatório de qualidade
- [ ] Salvar em Delta Lake particionado por `order_year`
- [ ] Gerar relatório: Bronze count vs. Silver count vs. taxa de aproveitamento

### 💡 Prompt Copilot — Validação de Email

```
Usando PySpark, adicione uma coluna booleana is_valid_email ao DataFrame.
Use F.col("email").rlike() com o padrão regex para validar e-mails:
^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$
```

### 📊 Métricas de Qualidade Esperadas

Com os dados gerados pelo script de exemplo, a taxa de aproveitamento esperada é:
- **Pedidos:** ~75% (status completed) − duplicatas − valores inválidos
- **Clientes:** ~95% (todos válidos, sem corrompidos)

Se seus números estiverem muito fora disso, revise os filtros aplicados.

### ▶️ Como avançar

```bash
git add notebooks/04_project_hands_on/02_silver_transform.py
git commit -m "feat: etapa 9 concluída - silver layer implementada"
git push origin main
```

> **Última etapa:** `notebooks/04_project_hands_on/03_gold_analytics.py` 🏆
> Você está quase lá! A camada Gold fecha o projeto com KPIs e análise RFM.
