> **🎓 Treinamento:** Databricks + GitHub Copilot no Dia a Dia
> **Participante:** {{PARTICIPANT_NAME}}
> **Progresso:** `[ ] Etapa 1` `[ ] Etapa 2` `[ ] Etapa 3` `[ ] Etapa 4` `[ ] Etapa 5` `[ ] Etapa 6` `[ ] Etapa 7` `[ ] Etapa 8` `[ ] Etapa 9` `[ ] Etapa 10`

---

## 🚀 Etapa 1 — Setup do Ambiente

Bem-vindo ao treinamento! Antes de colocar a mão na massa, você precisa configurar seu ambiente de desenvolvimento. Esta etapa não tem código para commitar — siga o checklist abaixo.

### ✅ Checklist de Setup

#### 1. Databricks Community Edition
- [ ] Acesse https://community.cloud.databricks.com/login.html
- [ ] Clique em **"Sign Up"** → **"Get started with Community Edition"**
- [ ] Confirme o e-mail e faça login
- [ ] Crie um cluster: **Compute → Create compute**
  - Cluster name: `training-cluster`
  - Runtime: `14.x LTS`
  - Aguarde o cluster ficar verde ✅

#### 2. VS Code
- [ ] Instale o VS Code: https://code.visualstudio.com/
- [ ] Instale a extensão **Databricks** (`Ctrl+Shift+X` → buscar "Databricks")
- [ ] Instale a extensão **GitHub Copilot** (`Ctrl+Shift+X` → buscar "GitHub Copilot")

#### 3. Conectar VS Code ao Databricks
- [ ] No Databricks: **Settings → Developer → Access Tokens → Generate new token**
  - Comment: `vscode-training` | Lifetime: 90 dias
  - **Copie e salve o token!**
- [ ] No VS Code: `Ctrl+Shift+P` → **"Databricks: Configure workspace"**
  - URL: `https://community.cloud.databricks.com`
  - Cole o token gerado
  - Selecione o cluster `training-cluster`

#### 4. Clonar este repositório
```bash
git clone https://github.com/{{OWNER}}/{{REPO}}.git
cd {{REPO}}
```

#### 5. Gerar dados de exemplo
```bash
python scripts/generate_sample_data.py
```
Faça upload dos arquivos gerados para o Databricks DBFS:
- `data/raw/orders.csv` → `dbfs:/FileStore/training/raw/orders.csv`
- `data/raw/customers.csv` → `dbfs:/FileStore/training/raw/customers.csv`

---

### 📖 Leitura Recomendada
Antes de continuar, leia os documentos de referência:
- [`docs/01_setup_guide.md`](../blob/main/docs/01_setup_guide.md) — guia completo de setup
- [`docs/02_databricks_concepts.md`](../blob/main/docs/02_databricks_concepts.md) — conceitos Databricks
- [`docs/03_copilot_tips.md`](../blob/main/docs/03_copilot_tips.md) — dicas de uso do Copilot

---

### ▶️ Como avançar para a próxima etapa

Após concluir o setup, abra o notebook `notebooks/01_intro/01_hello_databricks.py` no VS Code, complete os exercícios e faça commit:

```bash
git add notebooks/01_intro/
git commit -m "feat: completo etapa 1 - hello databricks"
git push origin main
```

> ⚡ **O GitHub Actions detectará o commit e adicionará automaticamente as instruções da Etapa 2 nesta issue!**
