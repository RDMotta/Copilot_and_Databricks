# Treinamento: Databricks + GitHub Copilot no Dia a Dia

## Visão Geral

Este treinamento apresenta a integração entre **Databricks** e **GitHub Copilot**, com foco prático em como essas ferramentas podem acelerar o desenvolvimento de pipelines de dados, otimizar código e aumentar a produtividade dos times de engenharia de dados.

---

## Agenda

### Módulo 1 — Introdução e Conceitos (30 min)
- O que é Databricks e por que usar?
- O que é GitHub Copilot e como ele funciona?
- Por que usar Databricks + Copilot juntos?
- Arquitetura Databricks: Clusters, Notebooks, Delta Lake, Unity Catalog

### Módulo 2 — Setup do Ambiente (20 min)
- Criando conta gratuita no Databricks Community Edition
- Configurando o VS Code com extensão Databricks
- Instalando e configurando o GitHub Copilot no VS Code
- Conectando VS Code ao workspace Databricks

### Módulo 3 — GitHub Copilot no Databricks: Dia a Dia (40 min)
- Usando Copilot para gerar código PySpark
- Copilot para escrever queries SQL no Databricks SQL
- Copilot para documentar notebooks
- Copilot Chat para entender código legado
- Dicas e atalhos de produtividade

### Módulo 4 — Hands-On: Construindo um Projeto de Ponta a Ponta (60 min)
- Criando a estrutura do projeto no Databricks
- Ingestão de dados brutos (Bronze Layer)
- Transformação e limpeza (Silver Layer)
- Camada analítica (Gold Layer)
- Usando Copilot em cada etapa

### Módulo 5 — Hands-On: Pipeline de Otimização de Dataset (60 min)
- Identificando gargalos de performance em um dataset
- Técnicas de otimização com Delta Lake (Z-Order, Particionamento, Vacuum)
- Usando Copilot para sugerir e implementar otimizações
- Comparando performance antes e depois
- Monitoramento e observabilidade

### Módulo 6 — Boas Práticas e Próximos Passos (20 min)
- Boas práticas com Copilot em projetos de dados
- Padrões de projeto no Databricks
- Recursos para continuar aprendendo

---

## Estrutura do Repositório

```
databricks-treinner/
├── README.md                          # Este arquivo
├── docs/
│   ├── 01_setup_guide.md              # Guia de setup do ambiente
│   ├── 02_databricks_concepts.md      # Conceitos chave do Databricks
│   └── 03_copilot_tips.md             # Dicas de uso do Copilot
├── notebooks/
│   ├── 01_intro/
│   │   └── 01_hello_databricks.py     # Primeiro notebook
│   ├── 02_copilot_integration/
│   │   ├── 01_pyspark_with_copilot.py # PySpark com Copilot
│   │   └── 02_sql_with_copilot.sql    # SQL com Copilot
│   ├── 03_pipeline_optimization/
│   │   ├── 01_baseline_pipeline.py    # Pipeline base (sem otimização)
│   │   ├── 02_profiling.py            # Análise de performance
│   │   └── 03_optimized_pipeline.py   # Pipeline otimizado
│   └── 04_project_hands_on/
│       ├── 01_bronze_ingestion.py     # Ingestão Bronze
│       ├── 02_silver_transform.py     # Transformação Silver
│       └── 03_gold_analytics.py      # Camada Gold
├── data/
│   ├── raw/                           # Dados brutos de exemplo
│   └── processed/                     # Dados processados
└── scripts/
    └── generate_sample_data.py        # Script para gerar dados de exemplo
```

---

## ▶️ Escolha sua Trilha e Comece Agora

> **Como funciona:** clique em **"Abrir Codespace"** para preparar o ambiente, depois clique em **"Iniciar Trilha"** para criar a Issue com os steps guiados. Cada commit nos notebooks avança automaticamente a Issue para a próxima etapa.

> ⚠️ Substitua `OWNER/REPO` pela URL do seu repositório antes de compartilhar.

---

### 🏗️ Trilha 2 — Hands-On Lakehouse *(Recomendada para iniciantes)*
> Construa um projeto de ponta a ponta: Bronze → Silver → Gold com Delta Lake. **4 etapas — Módulo 4.**

<p>
  <a href="https://codespaces.new/OWNER/REPO?quickstart=1">
    <img src="https://github.com/codespaces/badge.svg" alt="Abrir Codespace"/>
  </a>
  &nbsp;
  <a href="https://github.com/OWNER/REPO/actions/workflows/start-track2.yml">
    <img src="https://img.shields.io/badge/🏗️_Iniciar_Trilha_2-Hands--On_Lakehouse-0075ca?style=for-the-badge" alt="Iniciar Trilha 2"/>
  </a>
</p>

---

### ⚡ Trilha 3 — Otimização de Pipeline
> Identifique gargalos, aplique 7 otimizações e compare a performance. **4 etapas — Módulo 5.**

<p>
  <a href="https://codespaces.new/OWNER/REPO?quickstart=1">
    <img src="https://github.com/codespaces/badge.svg" alt="Abrir Codespace"/>
  </a>
  &nbsp;
  <a href="https://github.com/OWNER/REPO/actions/workflows/start-track3.yml">
    <img src="https://img.shields.io/badge/⚡_Iniciar_Trilha_3-Otimização_de_Pipeline-e11d48?style=for-the-badge" alt="Iniciar Trilha 3"/>
  </a>
</p>

---

### 🎓 Trilha 1 — Treinamento Completo
> Percurso completo pelos 6 módulos: conceitos, Copilot no dia a dia, otimização e projeto hands-on. **10 etapas.**

<p>
  <a href="https://codespaces.new/OWNER/REPO?quickstart=1">
    <img src="https://github.com/codespaces/badge.svg" alt="Abrir Codespace"/>
  </a>
  &nbsp;
  <a href="https://github.com/OWNER/REPO/actions/workflows/start-track1.yml">
    <img src="https://img.shields.io/badge/🎓_Iniciar_Trilha_1-Treinamento_Completo-6e40c9?style=for-the-badge" alt="Iniciar Trilha 1"/>
  </a>
</p>

---

O Codespace já vem pré-configurado com:
- ☕ Java 11 + PySpark 3.5.1 + Delta Lake (via pip, sem download de binário)
- 🐍 Python 3.11
- 🔧 Databricks CLI
- ⚡ GitHub Copilot + Copilot Chat
- 🗄️ Extensão Databricks para VS Code
- 📊 Jupyter Notebook support

### Configurar Credenciais no Codespaces

Antes de abrir o Codespace, configure os secrets em:
**github.com → Settings → Codespaces → New secret**

| Secret | Valor |
|--------|-------|
| `DATABRICKS_HOST` | `https://community.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | Token gerado em Settings → Developer → Access Tokens |
| `DATABRICKS_CLUSTER_ID` | ID do cluster criado no Databricks |

---

## Pré-requisitos (Instalação Local)

Se preferir rodar localmente em vez do Codespaces:

- Conta gratuita no [Databricks Community Edition](https://community.cloud.databricks.com/login.html)
- VS Code instalado
- Extensão [Databricks para VS Code](https://marketplace.visualstudio.com/items?itemName=databricks.databricks)
- GitHub Copilot (licença ativa ou trial)
- Python 3.9+ e Java 11+

---

## Como Usar Este Repositório

### Via Codespaces (Recomendado)
1. Abra o repositório no GitHub Codespaces (botão acima)
2. Configure os secrets `DATABRICKS_HOST` e `DATABRICKS_TOKEN`
3. O ambiente será configurado automaticamente
4. Execute `make generate-data && make upload-data` para preparar os dados
5. Siga o treinamento guiado pela Issue criada pelo workflow `01-training-start`

### Via Instalação Local
1. Siga o [Guia de Setup](docs/01_setup_guide.md) para configurar seu ambiente
2. Copie `.env.example` para `.env` e preencha com suas credenciais
3. Execute `make setup && make generate-data`
4. Importe os notebooks na ordem indicada pelos módulos
5. Execute cada célula e pratique com o Copilot ativado

---

## Links Úteis

- [Databricks Community Edition](https://community.cloud.databricks.com/)
- [Documentação Databricks](https://docs.databricks.com/)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Extensão Databricks VS Code](https://docs.databricks.com/dev-tools/vs-code-ext.html)
- [Delta Lake](https://delta.io/)
