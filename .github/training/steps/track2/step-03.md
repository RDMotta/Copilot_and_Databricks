> **📈 Progresso:** `[x] Bronze` `[x] Silver` `[→] Gold` `[ ] Concluído`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🥇 Camada Gold — KPIs Analíticos

Última etapa do projeto! A camada Gold transforma os dados Silver em **tabelas analíticas** prontas para dashboards de BI, relatórios executivos e modelos de ML.

### 🎯 O que você vai implementar

Abra `notebooks/04_project_hands_on/03_gold_analytics.py` e implemente as 5 funções Gold:

#### 1. `build_executive_kpis(df)` — Painel Executivo
- [ ] Receita total, número de pedidos, ticket médio
- [ ] Número de clientes únicos e receita por cliente
- [ ] Top categoria por receita (usando `first()` sobre window rankeada)
- Retorna **1 linha** com todos os indicadores globais

#### 2. `build_category_performance(df)` — Performance por Categoria
- [ ] Métricas por categoria: total de pedidos, receita, ticket médio
- [ ] Share percentual da receita total (usando `sum() over()` sem partição)
- [ ] Ranking por receita com `rank()` over window
- Ordenar por `revenue_rank`

#### 3. `build_monthly_trend(df)` — Tendência com MoM
- [ ] Agrupar por `order_year` e `order_month`
- [ ] Calcular receita e total de pedidos por período
- [ ] Variação MoM: `(atual - anterior) / anterior * 100` usando `lag()` over window temporal
- [ ] Média móvel de 3 meses: `avg() over rowsBetween(-2, 0)`

#### 4. `build_rfm_analysis(df)` — Segmentação de Clientes
- [ ] **Recency:** `datediff(current_date(), max(order_date))` — menor = mais recente = melhor
- [ ] **Frequency:** `count(order_id)` por cliente
- [ ] **Monetary:** `sum(total_amount)` por cliente
- [ ] Scores 1-5 usando `ntile(5)` — **atenção**: para Recency, inverter a ordem (mais recente = score 5)
- [ ] Classificar em: `Champions` (r≥4, f≥4, m≥4), `Loyal` (f≥3, m≥3), `At Risk` (r≤2, f≥2), `Lost` (r=1, f=1), `Others`

#### 5. `build_regional_summary(df)` — Análise Regional
- [ ] Métricas por região: receita, pedidos, ticket médio
- [ ] Top produto por receita em cada região (usando `first()` sobre window rankeada por região)

### 💡 Prompt Copilot — RFM Completo

```
Implemente análise RFM em PySpark:
1. Por customer_id: calcule Recency = datediff(current_date, max(order_date)),
   Frequency = count(order_id), Monetary = round(sum(total_amount), 2)
2. Scores com ntile(5): r_score ordena por recency ASC (menor dias = score 5),
   f_score e m_score ordenam ASC normalmente
3. Classifique com when/otherwise:
   - Champions: r_score>=4 AND f_score>=4 AND m_score>=4
   - Loyal: f_score>=3 AND m_score>=3
   - At Risk: r_score<=2 AND f_score>=2
   - Lost: r_score=1 AND f_score=1
   - Others: demais
```

### ▶️ Finalizar o projeto

```bash
git add notebooks/04_project_hands_on/03_gold_analytics.py
git commit -m "feat: gold layer implementada - projeto lakehouse concluido"
git push origin main
```

> ⚡ O Actions detecta o commit, posta a mensagem de conclusão e **fecha esta issue automaticamente!** 🏆
