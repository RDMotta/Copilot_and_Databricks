> **📈 Progresso:** `[x] Etapa 1` `[→] Etapa 2` `[ ] Etapa 3` `[ ] Etapa 4` `[ ] Etapa 5` `[ ] Etapa 6` `[ ] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`
>
> ✅ **Commit detectado:** [`{{COMMIT_SHA}}`]({{COMMIT_URL}}) por @{{ACTOR}}

---

## 🧩 Etapa 2 — Hello Databricks

Ótimo trabalho no setup! Agora vamos colocar a mão na massa e explorar o ambiente Databricks pela primeira vez com o GitHub Copilot ativo.

### 🎯 Objetivo
Familiarizar-se com a interface do Databricks, criar DataFrames PySpark e usar o Copilot para gerar código automaticamente.

### 📋 Tarefas

Abra o notebook `notebooks/01_intro/01_hello_databricks.py` no VS Code e complete **todos** os exercícios marcados com `# TODO`:

| # | Exercício | Tecnologia |
|---|-----------|-----------|
| 1 | Verificar versão do Spark e Python | PySpark |
| 2 | Criar DataFrame de funcionários com o Copilot | PySpark |
| 3 | Filtrar e ordenar dados com sugestão do Copilot | PySpark |
| 4 | Registrar view temporária e rodar SQL | Spark SQL |
| 5 | Salvar e ler dados em Delta Lake | Delta Lake |

### 💡 Dica do Copilot
Para o exercício 2, tente digitar apenas o comentário descritivo e pressione `Tab` para aceitar a sugestão completa do Copilot. Compare a sugestão com o que você escreveria manualmente!

### 🔑 Conceitos que você vai praticar
- `spark.createDataFrame()` com schema
- `.filter()`, `.orderBy()`, `.select()`
- `createOrReplaceTempView()` + `%sql`
- `.write.format("delta").save()` e `.read.format("delta").load()`

### ▶️ Como avançar

Complete todos os `# TODO` no notebook, execute as células no Databricks e faça commit:

```bash
git add notebooks/01_intro/01_hello_databricks.py
git commit -m "feat: etapa 2 concluída - hello databricks"
git push origin main
```

> ⚡ O Actions vai detectar o commit em `notebooks/02_copilot_integration/` e liberar a **Etapa 3**.
>
> **Próximo notebook:** `notebooks/02_copilot_integration/01_pyspark_with_copilot.py`
