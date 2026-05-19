"""
Simulação Monte Carlo — ganhos anuais e mensais por cenário.
"""

from __future__ import annotations

import csv
import random
import statistics

from distribuicoes import amostrar_variaveis
from gerar_dados import _fator_sazonal, _periodo_mes, calcular_mes, carregar_parametros
from paths import (
    DISTRIBUICAO_MC_CSV,
    RESULTADO_MC_CSV,
    RESULTADO_MC_MENSAL_CSV,
    ensure_dirs,
)

OUTPUT_RESUMO = RESULTADO_MC_CSV
OUTPUT_HIST = DISTRIBUICAO_MC_CSV
OUTPUT_MENSAL = RESULTADO_MC_MENSAL_CSV


def _percentil(valores_ordenados: list[float], p: float) -> float:
    idx = int(round((p / 100) * (len(valores_ordenados) - 1)))
    return valores_ordenados[idx]


def _resumo_distribuicao(valores: list[float]) -> dict[str, float]:
    ordenado = sorted(valores)
    return {
        "media": statistics.mean(valores),
        "desvio": statistics.stdev(valores) if len(valores) > 1 else 0.0,
        "min": ordenado[0],
        "max": ordenado[-1],
        "p5": _percentil(ordenado, 5),
        "p25": _percentil(ordenado, 25),
        "p50": _percentil(ordenado, 50),
        "p75": _percentil(ordenado, 75),
        "p95": _percentil(ordenado, 95),
    }


def simular(params: dict) -> tuple[list[dict], list[float], list[dict]]:
    mc = params["monte_carlo"]
    base = params["parametros_base"]
    n = mc["simulacoes"]
    horizonte = mc["horizonte_meses"]
    dist = mc["distribuicoes"]
    dias = base["dias_uteis_mes"]
    impostos = base["impostos_receita_pct"]
    usa_sazonal = params.get("sazonalidade_producao", {}).get("ativo", False)

    rng = random.Random(params["fonte_uniforme"]["seed"] + 1000)
    ganhos_anuais: list[float] = []
    ganhos_por_mes: list[list[float]] = [[] for _ in range(horizonte)]

    for _ in range(n):
        total = 0.0
        for m in range(horizonte):
            saz = _fator_sazonal(params, m) if usa_sazonal else 1.0
            p, pr, c, cu = amostrar_variaveis(dist, rng, fator_sazonal=saz)
            ganho = calcular_mes(p, pr, c, cu, impostos, dias)["ganho_liquido_brl"]
            ganhos_por_mes[m].append(ganho)
            total += ganho
        ganhos_anuais.append(total)

    ordenado_anual = sorted(ganhos_anuais)
    percentis = [5, 10, 25, 50, 75, 90, 95]
    resumo = [
        ("ganho_liquido_12m_brl_media", statistics.mean(ganhos_anuais)),
        ("ganho_liquido_12m_brl_desvio", statistics.stdev(ganhos_anuais)),
        ("ganho_liquido_12m_brl_min", ordenado_anual[0]),
        ("ganho_liquido_12m_brl_max", ordenado_anual[-1]),
    ]
    for p in percentis:
        resumo.append((f"percentil_{p}", _percentil(ordenado_anual, p)))
    neg = sum(1 for g in ganhos_anuais if g < 0) / n
    resumo.append(("prob_ganho_negativo", neg))
    resumo_fmt = [{"metrica": m, "valor": round(v, 2)} for m, v in resumo]

    resumo_mensal: list[dict] = []
    for m in range(horizonte):
        stats = _resumo_distribuicao(ganhos_por_mes[m])
        resumo_mensal.append({
            "ano_mes": _periodo_mes(params["data_inicio"], m),
            "indice_mes": m + 1,
            "ganho_media": round(stats["media"], 2),
            "ganho_desvio": round(stats["desvio"], 2),
            "ganho_p5": round(stats["p5"], 2),
            "ganho_p25": round(stats["p25"], 2),
            "ganho_p50": round(stats["p50"], 2),
            "ganho_p75": round(stats["p75"], 2),
            "ganho_p95": round(stats["p95"], 2),
            "ganho_min": round(stats["min"], 2),
            "ganho_max": round(stats["max"], 2),
        })

    return resumo_fmt, ganhos_anuais, resumo_mensal


def salvar_resultados(
    resumo: list[dict],
    ganhos: list[float],
    resumo_mensal: list[dict] | None = None,
) -> None:
    ensure_dirs()
    with open(OUTPUT_RESUMO, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["metrica", "valor"], delimiter=";")
        w.writeheader()
        w.writerows(resumo)

    with open(OUTPUT_HIST, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["ganho_liquido_12m_brl"])
        for g in ganhos:
            w.writerow([f"{g:.2f}"])

    if resumo_mensal:
        colunas = [
            "ano_mes", "indice_mes", "ganho_media", "ganho_desvio",
            "ganho_p5", "ganho_p25", "ganho_p50", "ganho_p75", "ganho_p95",
            "ganho_min", "ganho_max",
        ]
        with open(OUTPUT_MENSAL, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=colunas, delimiter=";")
            w.writeheader()
            w.writerows(resumo_mensal)


def main() -> None:
    params = carregar_parametros()
    resumo, ganhos, mensal = simular(params)
    salvar_resultados(resumo, ganhos, mensal)
    print(f"Simulações: {params['monte_carlo']['simulacoes']:,}")
    print(f"Anual: {OUTPUT_RESUMO}")
    print(f"Mensal: {OUTPUT_MENSAL}")


if __name__ == "__main__":
    main()
