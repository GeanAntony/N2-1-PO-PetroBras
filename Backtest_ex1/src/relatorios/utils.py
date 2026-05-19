"""Utilitários compartilhados para relatórios."""

from __future__ import annotations

import math
import statistics


def fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_num(v: float, dec: int = 2) -> str:
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(v: float) -> str:
    return f"{v:.2f}%"


def metricas(ganhos: list[float]) -> dict:
    g_sorted = sorted(ganhos)
    n = len(g_sorted)

    def pct_val(p: float) -> float:
        idx = int(round((p / 100) * (n - 1)))
        return g_sorted[idx]

    media = statistics.mean(ganhos)
    desvio = statistics.stdev(ganhos) if n > 1 else 0.0
    return {
        "n": n,
        "media": media,
        "desvio": desvio,
        "sem": desvio / math.sqrt(n) if n else 0.0,
        "margem_95_media": 1.96 * (desvio / math.sqrt(n)) if n else 0.0,
        "min": g_sorted[0],
        "max": g_sorted[-1],
        "p5": pct_val(5),
        "p25": pct_val(25),
        "p50": pct_val(50),
        "p75": pct_val(75),
        "p95": pct_val(95),
        "ic_90_largura": pct_val(95) - pct_val(5),
    }
