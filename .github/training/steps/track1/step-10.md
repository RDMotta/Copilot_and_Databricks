> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[x] Etapa 3` `[x] Etapa 4` `[x] Etapa 5` `[x] Etapa 6` `[x] Etapa 7` `[x] Etapa 8` `[x] Etapa 9` `[→] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥇 Etapa 10 — Projeto Lakehouse: Camada Gold + Conclusão

**Última etapa!** A camada Gold é o produto final do seu pipeline — tabelas analíticas otimizadas para consumo por ferramentas de BI, dashboards executivos e relatórios de negócio.

### 🎯 Objetivo
Implementar as 5 tabelas Gold com KPIs de negócio, análise RFM de clientes e views para consumo por BI tools.

### 📋 Tarefas

Abra `notebooks/04_project_hands_on/03_gold_analytics.py`:

#### 1. `build_executive_kpis()` — KPIs Globais
- [ ] Receita total, número de pedidos, ticket médio
- [ ] Número de clientes únicos e receita por cliente
- [ ] Top categoria por receita

#### 2. `build_category_performance()` — Performance por Categoria
- [ ] Métricas por categoria + share percentual da receita total
- [ ] Ranking por receita usando `rank()` sobre window

#### 3. `build_monthly_trend()` — Tendência com MoM
- [ ] Receita e pedidos por mês/ano
- [ ] Variação MoM usando `lag()` → `(atual - anterior) / anterior * 100`
- [ ] Média móvel de 3 meses com `rowsBetween(-2, 0)`

#### 4. `build_rfm_analysis()` — Segmentação RFM
- [ ] **Recency:** dias desde o último pedido (menor = melhor)
- [ ] **Frequency:** número de pedidos por cliente
- [ ] **Monetary:** receita total por cliente
- [ ] Scores 1-5 usando `ntile(5)` para cada dimensão
- [ ] Classificação: Champions / Loyal / At Risk / Lost / Others

#### 5. `build_regional_summary()` — Análise Regional
- [ ] Receita, pedidos e ticket médio por região
- [ ] Top produto por receita em cada região

#### 6. Criar Views para BI
- [ ] `vw_executive_summary` combinando KPIs + regiões

### 💡 Prompt Copilot — Análise RFM

```
Implemente análise RFM em PySpark:
1. Calcule Recency (dias desde último pedido usando datediff e current_date), 
   Frequency (count de pedidos) e Monetary (sum de total_amount) por customer_id
2. Use ntile(5) sobre window sem partição e ordenado por cada métrica para 
   criar scores r_score, f_score, m_score (1 a 5)
3. Classifique: Champions (r>=4, f>=4, m>=4), Loyal (f>=3, m>=3), 
   At Risk (r<=2, f>=2), Lost (r=1, f=1), Others (demais)
```

### 📊 Tabelas que você vai criar

| Tabela Gold | Linhas Esperadas | Descrição |
|-------------|-----------------|-----------|
| `gold_executive_kpis` | 1 | KPIs globais |
| `gold_category_perf` | 6 (1 por categoria) | Performance por categoria |
| `gold_monthly_trend` | ~24 (meses 2023-2024) | Tendência mensal |
| `gold_rfm` | ~500 (1 por cliente) | Segmentação RFM |
| `gold_regional_summary` | 5 (1 por região) | Análise regional |

### ▶️ Como finalizar o treinamento

```bash
git add notebooks/04_project_hands_on/03_gold_analytics.py
git commit -m "feat: etapa 10 concluída - gold layer e projeto finalizado 🏆"
git push origin main
```

> ⚡ O Actions vai detectar este commit, publicar a mensagem de conclusão e **fechar esta issue automaticamente!**

---

## 🎉 Você está quase lá!

Este é o último notebook. Após o commit, esta issue será fechada como **concluída** e você terá construído:

- ✅ Pipeline de dados com arquitetura Medallion (Bronze → Silver → Gold)
- ✅ Integração Databricks + GitHub Copilot no fluxo de desenvolvimento
- ✅ Otimizações reais de performance com Delta Lake
- ✅ Análises avançadas: RFM, tendência MoM, detecção de anomalias

**Bom trabalho!** 🚀
