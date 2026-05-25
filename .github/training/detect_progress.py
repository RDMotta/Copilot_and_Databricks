#!/usr/bin/env python3
"""
detect_progress.py

Dada uma lista de arquivos alterados e uma trilha, retorna a próxima etapa.

Uso:
    python3 .github/training/detect_progress.py <track> "arquivo1 arquivo2"

Exemplo:
    python3 .github/training/detect_progress.py track-2-handson \
        "notebooks/04_project_hands_on/01_bronze_ingestion.py"

Saída:
    next_step=02   (próxima etapa) ou next_step=none
"""

import sys

# Mapeamento: trilha → [(padrão de arquivo, próxima etapa)]
TRACK_TRIGGERS: dict[str, list[tuple[str, str]]] = {
    "track-1-full": [
        ("notebooks/01_intro/",                                       "02"),
        ("notebooks/02_copilot_integration/01_pyspark_with_copilot",  "03"),
        ("notebooks/02_copilot_integration/02_sql_with_copilot",      "04"),
        ("notebooks/03_pipeline_optimization/01_baseline_pipeline",   "05"),
        ("notebooks/03_pipeline_optimization/02_profiling",           "06"),
        ("notebooks/03_pipeline_optimization/03_optimized_pipeline",  "07"),
        ("notebooks/04_project_hands_on/01_bronze_ingestion",         "08"),
        ("notebooks/04_project_hands_on/02_silver_transform",         "09"),
        ("notebooks/04_project_hands_on/03_gold_analytics",           "10"),
    ],
    "track-2-handson": [
        ("notebooks/04_project_hands_on/01_bronze_ingestion", "02"),
        ("notebooks/04_project_hands_on/02_silver_transform", "03"),
        ("notebooks/04_project_hands_on/03_gold_analytics",   "04"),
    ],
    "track-3-optimization": [
        ("notebooks/03_pipeline_optimization/01_baseline_pipeline",  "02"),
        ("notebooks/03_pipeline_optimization/02_profiling",          "03"),
        ("notebooks/03_pipeline_optimization/03_optimized_pipeline", "04"),
    ],
}


def detect_next_step(track: str, changed_files: list[str]) -> str:
    triggers = TRACK_TRIGGERS.get(track, [])
    for pattern, next_step in triggers:
        if any(pattern in f for f in changed_files):
            return next_step
    return "none"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("next_step=none")
        sys.exit(0)

    track = sys.argv[1]
    files = sys.argv[2].split()
    result = detect_next_step(track, files)
    print(f"next_step={result}")
