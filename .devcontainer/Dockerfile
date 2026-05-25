# ── Base: Python 3.11 com ferramentas de desenvolvimento ─────────────────────
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# ── Variáveis de ambiente ─────────────────────────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive \
    JAVA_HOME=/usr/lib/jvm/default-java \
    PYSPARK_PYTHON=/usr/local/bin/python3 \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3 \
    SPARK_LOCAL_IP=127.0.0.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── 1. Java 11 (necessário para PySpark) ─────────────────────────────────────
# OpenJDK do Debian: mais rápido que baixar Temurin e suficiente para PySpark
RUN apt-get update && apt-get install -y --no-install-recommends \
        default-jdk-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── 2. Dependências Python ────────────────────────────────────────────────────
# pyspark + delta-spark já incluem os JARs — sem necessidade de Spark binário
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# ── 3. Databricks CLI ─────────────────────────────────────────────────────────
RUN curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh \
    | sh

# ── 4. Profile do usuário vscode ──────────────────────────────────────────────
USER vscode
WORKDIR /workspaces/databricks-treinner

RUN echo '' >> ~/.bashrc \
    && echo '# ── Databricks Training ──' >> ~/.bashrc \
    && echo 'export SPARK_LOCAL_IP=127.0.0.1' >> ~/.bashrc \
    && echo 'export PYSPARK_PYTHON=/usr/local/bin/python3' >> ~/.bashrc \
    && echo 'alias run-sample-data="python scripts/generate_sample_data.py"' >> ~/.bashrc \
    && echo 'alias dbx="databricks"' >> ~/.bashrc
