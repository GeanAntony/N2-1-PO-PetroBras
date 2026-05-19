"""
Amostragem unificada — usada por gerar_dados.py e monte_carlo.py.
"""

from __future__ import annotations

import math
import random


def amostrar_lognormal(media: float, desvio_pct: float, rng: random.Random) -> float:
    sigma = math.sqrt(math.log(1 + desvio_pct**2))
    mu = math.log(media) - 0.5 * sigma**2
    return rng.lognormvariate(mu, sigma)


def amostrar_variaveis(
    distribuicoes: dict,
    rng: random.Random,
    *,
    fator_sazonal: float = 1.0,
) -> tuple[float, float, float, float]:
    prod = distribuicoes["producao_diaria_bbl"]
    producao = max(prod["media"] * 0.5, rng.gauss(prod["media"], prod["desvio"])) * fator_sazonal

    preco_cfg = distribuicoes["preco_usd_bbl"]
    preco = amostrar_lognormal(preco_cfg["media"], preco_cfg["desvio_pct"], rng)

    cambio_cfg = distribuicoes["cambio_usd_brl"]
    cambio = min(8.0, max(3.5, rng.gauss(cambio_cfg["media"], cambio_cfg["desvio"])))

    custo_cfg = distribuicoes["custo_usd_bbl"]
    custo = rng.triangular(custo_cfg["min"], custo_cfg["max"], custo_cfg["moda"])

    return producao, preco, cambio, custo
