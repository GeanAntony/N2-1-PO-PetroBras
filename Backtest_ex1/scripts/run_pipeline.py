#!/usr/bin/env python3
"""Executa o pipeline completo a partir da raiz do projeto."""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gerar_dados import main as gerar_dados
from monte_carlo import main as monte_carlo
from relatorios.gerar_apresentacao_ganhos import main as apresentacao


def main() -> None:
    print("=== 1/3 Série real (12 meses) ===")
    gerar_dados()
    print("\n=== 2/3 Monte Carlo ===")
    monte_carlo()
    print("\n=== 3/3 Relatório de apresentação ===")
    apresentacao()
    print("\nConcluído.")


if __name__ == "__main__":
    main()
