#!/usr/bin/env bash
# .devcontainer/post-start.sh — Executado a cada reabertura do Codespace
set -euo pipefail

if [ -f .env ]; then
  set -o allexport
  source <(grep -v '^\s*#' .env | grep -v '^\s*$')
  set +o allexport
fi

if [ -n "${DATABRICKS_HOST:-}" ] && [ -n "${DATABRICKS_TOKEN:-}" ]; then
  # Recover from older setup that created ~/.databrickscfg as a directory.
  if [ -d ~/.databrickscfg ]; then
    rm -rf ~/.databrickscfg
  fi
  cat > ~/.databrickscfg << DBCFG
[DEFAULT]
host  = ${DATABRICKS_HOST}
token = ${DATABRICKS_TOKEN}
DBCFG
fi

echo ""
echo "  🎓 Databricks + Copilot Training — Codespace pronto!"
echo "  📁 $(pwd)"
echo "  🐍 $(python3 --version)"
echo "  ☕ Java $(java -version 2>&1 | awk -F '"' '/version/ {print $2}')"
if [ -n "${DATABRICKS_HOST:-}" ]; then
  echo "  🔌 Databricks: ${DATABRICKS_HOST}"
else
  echo "  ⚠️  Databricks: configure o .env"
fi
echo ""
