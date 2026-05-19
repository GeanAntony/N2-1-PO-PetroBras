"""
Gera 12 meses de extração e ganhos (BRL) — mesmas distribuições do Monte Carlo.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path

from distribuicoes import amostrar_variaveis
from paths import CONFIG_PATH, DADOS_EXTRACAO_CSV, ensure_dirs

OUTPUT_CSV = DADOS_EXTRACAO_CSV


def carregar_parametros() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def calcular_mes(
    producao_diaria_bbl: float,
    preco_usd_bbl: float,
    cambio_usd_brl: float,
    custo_usd_bbl: float,
    impostos_pct: float,
    dias_mes: int,
) -> dict:
    producao_mes_bbl = producao_diaria_bbl * dias_mes
    receita_bruta_brl = producao_mes_bbl * preco_usd_bbl * cambio_usd_brl
    custos_brl = producao_mes_bbl * custo_usd_bbl * cambio_usd_brl
    impostos_brl = receita_bruta_brl * impostos_pct
    ganho_liquido_brl = receita_bruta_brl - custos_brl - impostos_brl
    return {
        "producao_mes_bbl": round(producao_mes_bbl, 2),
        "producao_diaria_media_bbl": round(producao_diaria_bbl, 2),
        "preco_petroleo_usd_bbl": round(preco_usd_bbl, 2),
        "cambio_usd_brl": round(cambio_usd_brl, 4),
        "custo_usd_bbl": round(custo_usd_bbl, 2),
        "receita_bruta_brl": round(receita_bruta_brl, 2),
        "custos_operacionais_brl": round(custos_brl, 2),
        "impostos_brl": round(impostos_brl, 2),
        "ganho_liquido_brl": round(ganho_liquido_brl, 2),
    }


def _periodo_mes(data_inicio: str, offset: int) -> str:
    ano, mes = map(int, data_inicio.split("-"))
    mes += offset
    while mes > 12:
        mes -= 12
        ano += 1
    return f"{ano:04d}-{mes:02d}"


def _fator_sazonal(params: dict, indice_mes: int) -> float:
    saz = params.get("sazonalidade_producao", {})
    if not saz.get("ativo", False):
        return 1.0
    amp = saz.get("amplitude_pct", 0.02)
    return 1.0 + amp * math.sin(2 * math.pi * indice_mes / 12)


def gerar_serie_mensal(params: dict) -> list[dict]:
    base = params["parametros_base"]
    dist = params["monte_carlo"]["distribuicoes"]
    rng = random.Random(params["fonte_uniforme"]["seed"])

    linhas = []
    for i in range(params["periodo_meses"]):
        p, pr, c, cu = amostrar_variaveis(
            dist, rng, fator_sazonal=_fator_sazonal(params, i)
        )
        row = calcular_mes(
            p, pr, c, cu,
            base["impostos_receita_pct"],
            base["dias_uteis_mes"],
        )
        row["ano_mes"] = _periodo_mes(params["data_inicio"], i)
        linhas.append(row)
    return linhas


def salvar_csv(linhas: list[dict], path: Path | None = None) -> None:
    ensure_dirs()
    dest = path or OUTPUT_CSV
    colunas = [
        "ano_mes", "producao_diaria_media_bbl", "producao_mes_bbl",
        "preco_petroleo_usd_bbl", "cambio_usd_brl", "custo_usd_bbl",
        "receita_bruta_brl", "custos_operacionais_brl", "impostos_brl", "ganho_liquido_brl",
    ]
    with open(dest, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=colunas, delimiter=";")
        w.writeheader()
        w.writerows(linhas)


def main() -> None:
    params = carregar_parametros()
    linhas = gerar_serie_mensal(params)
    salvar_csv(linhas)

    print(f"Empresa: {params['empresa']}")
    print(f"Arquivo: {OUTPUT_CSV}")
    print(f"Período: {linhas[0]['ano_mes']} a {linhas[-1]['ano_mes']}")
    print(f"Ganho líquido: R$ {sum(r['ganho_liquido_brl'] for r in linhas):,.2f}")


if __name__ == "__main__":
    main()
