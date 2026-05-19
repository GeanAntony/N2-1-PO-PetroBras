"""Gera reports/APRESENTACAO_GANHOS.md."""

from __future__ import annotations

import csv
import copy
from datetime import datetime

from gerar_dados import carregar_parametros
from monte_carlo import OUTPUT_MENSAL, OUTPUT_RESUMO, salvar_resultados, simular
from paths import DADOS_EXTRACAO_CSV, REPORTS_DIR, ensure_dirs

OUTPUT_MD = REPORTS_DIR / "APRESENTACAO_GANHOS.md"


def _fmt(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _pct(obs: float, ref: float) -> str:
    if ref == 0:
        return "—"
    sinal = "+" if obs >= ref else ""
    return f"{sinal}{(obs - ref) / ref * 100:.1f}%"


def _dentro_faixa(real: float, p5: float, p95: float) -> str:
    return "Sim" if p5 <= real <= p95 else "Não"


def _garantir_simulacao_mensal() -> tuple[dict[str, float], list[dict]]:
    if OUTPUT_MENSAL.exists() and OUTPUT_RESUMO.exists():
        with open(OUTPUT_RESUMO, encoding="utf-8-sig") as f:
            mc = {r["metrica"]: float(r["valor"]) for r in csv.DictReader(f, delimiter=";")}
        with open(OUTPUT_MENSAL, encoding="utf-8-sig") as f:
            mensal = list(csv.DictReader(f, delimiter=";"))
        for row in mensal:
            for k in row:
                if k.startswith("ganho_"):
                    row[k] = float(row[k])
            row["indice_mes"] = int(row["indice_mes"])
        return mc, mensal

    params = carregar_parametros()
    if params["monte_carlo"]["simulacoes"] != 100_000:
        params = copy.deepcopy(params)
        params["monte_carlo"]["simulacoes"] = 100_000

    print("Gerando simulação (100.000 cenários)...")
    resumo, ganhos, mensal = simular(params)
    salvar_resultados(resumo, ganhos, mensal)
    return {r["metrica"]: float(r["valor"]) for r in resumo}, mensal


def main() -> None:
    ensure_dirs()
    with open(DADOS_EXTRACAO_CSV, encoding="utf-8-sig") as f:
        meses_real = {r["ano_mes"]: r for r in csv.DictReader(f, delimiter=";")}

    mc, mensal = _garantir_simulacao_mensal()
    ganhos_reais = [float(meses_real[m["ano_mes"]]["ganho_liquido_brl"]) for m in mensal]
    total_real = sum(ganhos_reais)
    total_mc_media = sum(float(m["ganho_media"]) for m in mensal)

    linhas_mensais = []
    for m, g_real in zip(mensal, ganhos_reais):
        media = float(m["ganho_media"])
        p5, p95 = float(m["ganho_p5"]), float(m["ganho_p95"])
        linhas_mensais.append(
            f"| {m['ano_mes']} | {_fmt(g_real)} | {_fmt(media)} | "
            f"{_fmt(p5)} | {_fmt(float(m['ganho_p50']))} | {_fmt(p95)} | "
            f"{_pct(g_real, media)} | {_dentro_faixa(g_real, p5, p95)} |"
        )

    md = f"""# Ganhos líquidos — Real vs Simulação

**PetroBrasil Extração S.A.** · **{mensal[0]['ano_mes']}** a **{mensal[-1]['ano_mes']}**  
**Simulação:** 100.000 cenários · estatísticas **por mês** · {datetime.now().strftime("%d/%m/%Y")}

---

## Resumo anual

| | Ganho líquido (12 meses) |
|---|--------------------------|
| **Valor real** | **{_fmt(total_real)}** |
| Simulação — soma das médias mensais | {_fmt(total_mc_media)} |
| Simulação — média anual (cenários) | {_fmt(mc['ganho_liquido_12m_brl_media'])} |
| Simulação — mediana anual (P50) | {_fmt(mc['percentil_50'])} |
| Simulação — P5 anual | {_fmt(mc['percentil_5'])} |
| Simulação — P95 anual | {_fmt(mc['percentil_95'])} |

| Comparativo anual | |
|-------------------|---|
| Real vs média anual simulada | **{_pct(total_real, mc['ganho_liquido_12m_brl_media'])}** |
| Real dentro de P5–P95 anual? | {_dentro_faixa(total_real, mc['percentil_5'], mc['percentil_95'])} |

---

## Ganhos mensais (modelo por mês)

| Mês | Ganho real | Sim. média | Sim. P5 | Sim. P50 | Sim. P95 | Dif. vs média | Real em P5–P95? |
|-----|------------|------------|---------|----------|----------|---------------|-----------------|
{chr(10).join(linhas_mensais)}
| **Total** | **{_fmt(total_real)}** | **{_fmt(total_mc_media)}** | — | — | — | **{_pct(total_real, total_mc_media)}** | — |

---

*Fontes: `data/output/dados_extracao_petroleo.csv` · `data/output/resultado_monte_carlo_mensal.csv`*
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"Gerado: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
