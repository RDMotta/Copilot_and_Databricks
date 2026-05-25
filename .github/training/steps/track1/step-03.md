> **📈 Progresso:** `[x] Etapa 1` `[x] Etapa 2` `[→] Etapa 3` `[ ] Etapa 4` `[ ] Etapa 5` `[ ] Etapa 6` `[ ] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## ⚡ Etapa 3 — PySpark com GitHub Copilot

Agora é hora de ver o Copilot brilhar em transformações PySpark reais! Você vai construir um pipeline completo de análise de vendas usando o Copilot para gerar cada função.

### 🎯 Objetivo
Usar prompts descritivos no Copilot para gerar código PySpark complexo — filtros, agregações, window functions e segmentação de clientes.

### 📋 Tarefas

Abra `notebooks/02_copilot_integration/01_pyspark_with_copilot.py` e complete os 5 exercícios:

| # | Exercício | Função a implementar | Técnica PySpark |
|---|-----------|---------------------|-----------------|
| 1 | Gerar dados de vendas | — (dados de exemplo) | `createDataFrame` |
| 2 | Limpeza e validação | `clean_orders()` | `filter`, `withColumn`, `dropDuplicates` |
| 3 | Métricas de negócio | `calculate_sales_metrics()` | `groupBy`, `agg`, `orderBy` |
| 4 | Análise temporal | `analyze_sales_by_period()` | `Window`, `lag()` |
| 5 | Segmentação de clientes | `segment_customers()` | `when/otherwise`, `ntile()` |

### 💡 Estratégia com o Copilot

**Para cada função**, siga este ritual:
1. Leia a docstring da função
2. Copie o prompt sugerido no comentário `# 💡 Prompt para o Copilot`
3. Cole no **Copilot Chat** (`Ctrl+Alt+I`)
4. Aceite a sugestão, revise e ajuste se necessário
5. Execute no Databricks e verifique o resultado

### 🧪 Experimento
Tente também abrir o Copilot Chat e perguntar:
> *"Esta função PySpark está correta? Existe uma forma mais eficiente de fazer isso?"*

### ▶️ Como avançar

```bash
git add notebooks/02_copilot_integration/01_pyspark_with_copilot.py
git commit -m "feat: etapa 3 concluída - pyspark com copilot"
git push origin main
```

> **Próximo notebook:** `notebooks/02_copilot_integration/02_sql_with_copilot.sql`
