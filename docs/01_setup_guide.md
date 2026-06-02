# Guia de Setup: Databricks Community Edition + VS Code + Copilot

## 1. Criando sua Conta Gratuita no Databricks

### Passo 1 — Acesse o Databricks Community Edition

1. Acesse: https://community.cloud.databricks.com/login.html
2. Clique em **"Sign Up"** → **"Get started with Community Edition"**
3. Preencha nome, e-mail e senha
4. Confirme o e-mail e faça login

> **Limites do Community Edition:**
> - 1 cluster com até 15GB RAM
> - Armazenamento em DBFS (sem S3/ADLS externos)
> - Sem suporte a Unity Catalog
> - Suficiente para todos os exercícios deste treinamento

---

## 2. Configurando o Cluster

1. No Databricks, acesse **Compute → Create compute**
2. Configure:
   - **Cluster name:** `training-cluster`
   - **Cluster mode:** Single Node
   - **Databricks Runtime:** 14.x LTS (inclui Apache Spark 3.5, Scala 2.12)
   - **Node type:** (Community Edition usa configuração padrão)
3. Clique em **Create compute**
4. Aguarde o cluster iniciar (ícone verde)

---

## 3. Instalando o VS Code e Extensões

### VS Code
- Baixe em: https://code.visualstudio.com/

### Extensão Databricks
```
Ctrl+Shift+X → buscar "Databricks" → instalar "Databricks" (by Databricks)
```

### GitHub Copilot
```
Ctrl+Shift+X → buscar "GitHub Copilot" → instalar
```
Faça login com sua conta GitHub quando solicitado.

---

## 4. Conectando VS Code ao Databricks

### Método: Personal Access Token

1. No Databricks, acesse **Settings → Developer → Access Tokens**
2. Clique em **"Generate new token"**
   - Comment: `vscode-training`
   - Lifetime (days): 90
3. Copie e salve o token gerado (não será exibido novamente)

### Configurando a extensão no VS Code

1. Pressione `Ctrl+Shift+P` → digite **"Databricks: Configure workspace"**
2. Selecione **"Databricks Community Edition"**
3. Informe a URL do seu workspace: `https://community.cloud.databricks.com`
4. Cole o Personal Access Token gerado
5. Selecione o cluster criado anteriormente

### Verificando a conexão

No VS Code, o painel lateral da extensão Databricks deve mostrar:
- Status do cluster (Running/Terminated)
- Arquivos do DBFS
- Jobs disponíveis

---

## 5. Estrutura de Pastas no Databricks Workspace

Crie a estrutura no Databricks Workspace:
```
/Workspace/Users/{seu-email}/databricks-training/
├── 01_intro/
├── 02_copilot_integration/
├── 03_pipeline_optimization/
└── 04_project_hands_on/
```

---

## 6. Verificando o GitHub Copilot

1. Abra qualquer arquivo `.py` no VS Code
2. Comece a digitar um comentário: `# Crie uma função que lê um CSV`
3. O Copilot deve sugerir código automaticamente (texto acinzentado)
4. Pressione `Tab` para aceitar a sugestão

### Atalhos Principais do Copilot
| Ação | Atalho |
|------|--------|
| Aceitar sugestão | `Tab` |
| Rejeitar sugestão | `Esc` |
| Próxima sugestão | `Alt+]` |
| Sugestão anterior | `Alt+[` |
| Abrir painel de sugestões | `Ctrl+Enter` |
| Abrir Copilot Chat | `Ctrl+Alt+I` |

---

## 7. Checklist Final

- [ ] Conta Databricks Community Edition criada e funcionando
- [ ] Cluster criado e no status "Running"
- [ ] VS Code instalado
- [ ] Extensão Databricks instalada e conectada ao workspace
- [ ] GitHub Copilot instalado e ativo
- [ ] Teste de sugestão do Copilot funcionando

Você está pronto para o treinamento!
