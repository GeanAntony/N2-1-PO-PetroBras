"""Caminhos centralizados do projeto."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "parametros.json"
DATA_OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

DADOS_EXTRACAO_CSV = DATA_OUTPUT_DIR / "dados_extracao_petroleo.csv"
RESULTADO_MC_CSV = DATA_OUTPUT_DIR / "resultado_monte_carlo.csv"
RESULTADO_MC_MENSAL_CSV = DATA_OUTPUT_DIR / "resultado_monte_carlo_mensal.csv"
DISTRIBUICAO_MC_CSV = DATA_OUTPUT_DIR / "distribuicao_ganhos_monte_carlo.csv"


def ensure_dirs() -> None:
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
