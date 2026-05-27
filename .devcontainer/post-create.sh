#!/usr/bin/env bash
# .devcontainer/post-create.sh — Executado após criação, com o repositório disponível
set -euo pipefail

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  post-create.sh — Configurando ambiente do treinamento"
echo "══════════════════════════════════════════════════════════════"
echo ""

# ── 1. Criar .env a partir do exemplo ─────────────────────────────────────────
if [ ! -f .env ]; then
  cp .env.example .env
  echo "📝 .env criado — preencha DATABRICKS_HOST e DATABRICKS_TOKEN"
else
  echo "✅ .env já existe."
fi

# ── 2. Instalar Databricks CLI (fallback se não veio no Dockerfile) ─────────────
if ! command -v databricks >/dev/null 2>&1; then
  echo "📥 Databricks CLI não encontrado — instalando em ~/bin..."
  mkdir -p ~/bin
  DATABRICKS_RUNTIME_VERSION=1 curl -fsSL \
    https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
  # Garante ~/bin no PATH da sessão atual
  export PATH="$HOME/bin:$PATH"
  # Persiste no bashrc para sessões futuras
  grep -qxF 'export PATH="$HOME/bin:$PATH"' ~/.bashrc \
    || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
  echo "✅ Databricks CLI instalado: $(databricks -v 2>&1 || true)"
else
  echo "✅ Databricks CLI já disponível: $(databricks -v 2>&1 || true)"
fi

# ── 3. Gerar dados de exemplo ─────────────────────────────────────────────────
echo ""
echo "📊 Gerando dados de exemplo..."
python scripts/generate_sample_data.py && echo "✅ Dados gerados em data/raw/" || \
  echo "⚠️  Falha ao gerar dados. Execute: python scripts/generate_sample_data.py"

# ── 4. Verificar PySpark + Delta Lake ────────────────────────────────────────
echo ""
python3 - <<'PYCHECK'
try:
    import pyspark, delta
    print(f"✅ PySpark {pyspark.__version__} + delta-spark {delta.__version__}")
except ImportError as e:
    print(f"⚠️  {e}")
PYCHECK

# ── 5. Resumo ─────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  🎉 Ambiente pronto! Próximos passos:"
echo ""
echo "  1. Preencha .env com suas credenciais Databricks"
echo "  2. make upload-data   → envia dados ao DBFS"
echo "  3. Abra os notebooks em notebooks/ e use Ctrl+Alt+I (Copilot)"
echo ""
echo "  Trilhas disponíveis (GitHub Actions → 01-training-start):"
echo "    🥇 track-2-handson      → Projeto Lakehouse (padrão)"
echo "    🥈 track-3-optimization → Pipeline de Otimização"
echo "    🥉 track-1-full         → Treinamento Completo"
echo "══════════════════════════════════════════════════════════════"
echo ""
