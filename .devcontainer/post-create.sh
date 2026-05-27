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

# ── 2. Configurar Databricks CLI ──────────────────────────────────────────────
if [ -n "${DATABRICKS_HOST:-}" ] && [ -n "${DATABRICKS_TOKEN:-}" ]; then
  echo "🔧 Configurando Databricks CLI..."
  # Recover from older setup that created ~/.databrickscfg as a directory.
  if [ -d ~/.databrickscfg ]; then
    rm -rf ~/.databrickscfg
  fi
  cat > ~/.databrickscfg << DBCFG
[DEFAULT]
host  = ${DATABRICKS_HOST}
token = ${DATABRICKS_TOKEN}
DBCFG
  echo "✅ Databricks CLI configurado → ${DATABRICKS_HOST}"
else
  echo "⚠️  DATABRICKS_HOST/TOKEN não definidos."
  echo "   Configure em: repo → Settings → Secrets and variables → Codespaces"
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
