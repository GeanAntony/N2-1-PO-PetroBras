# Relatório comparativo — modelo de extração de petróleo

**Empresa:** PetroBrasil Extração S.A.  
**Gerado em:** 18/05/2026 20:20  
**Fonte unificada:** `parametros.json` + `distribuicoes.py` + `calcular_mes()`  
**Simulações Monte Carlo:** **100,000** (comparativo de precisão vs. **10,000** simulações independentes, mesma seed)

---

## 1. Distribuições consolidadas

| Variável | Distribuição | Parâmetros |
|----------|--------------|------------|
| Produção diária | Normal (truncada ≥ 50% da média) | μ = 12,500 bbl/d, σ = 1,100 |
| Preço petróleo | Lognormal | média ≈ US$ 78.5, CV ≈ 15% |
| Câmbio USD/BRL | Normal (truncada 3,5–8,0) | μ = 5.12, σ = 0.28 |
| Custo operacional | Triangular | min 15.0 / moda 18.0 / máx 24.0 USD/bbl |
| Sazonalidade (produção) | Senoidal ±2% | Ativa na série e no MC |

---

## 2. Série observada (12 meses)

| Indicador | Valor |
|-----------|-------|
| Período | 2025-05 → 2026-04 |
| Produção total | 4.536.127 bbl |
| **Ganho líquido acumulado** | **R$ 802.388.872,37** |
| Ganho médio mensal | R$ 66.865.739,36 |

### Detalhamento mensal

| Mês | Produção (bbl) | Preço (USD) | Câmbio | Ganho líquido |
|-----|----------------|-------------|--------|---------------|
| 2025-05 | 370.245 | 72,09 | 5,0716 | R$ 51.354.309,41 |
| 2025-06 | 347.485 | 64,66 | 4,5906 | R$ 42.715.065,50 |
| 2025-07 | 389.294 | 84,46 | 5,4458 | R$ 81.202.781,88 |
| 2025-08 | 330.600 | 83,83 | 4,8488 | R$ 61.364.885,69 |
| 2025-09 | 410.817 | 97,16 | 5,0526 | R$ 89.989.354,86 |
| 2025-10 | 373.502 | 94,33 | 4,7757 | R$ 77.013.548,99 |
| 2025-11 | 396.921 | 96,64 | 4,7787 | R$ 83.030.920,05 |
| 2025-12 | 393.780 | 73,22 | 5,1772 | R$ 62.821.713,92 |
| 2026-01 | 389.582 | 81,99 | 5,2540 | R$ 73.579.159,90 |
| 2026-02 | 373.915 | 80,29 | 5,3336 | R$ 65.447.179,73 |
| 2026-03 | 384.904 | 81,30 | 5,3540 | R$ 67.125.901,80 |
| 2026-04 | 375.082 | 65,17 | 4,9207 | R$ 46.744.050,64 |

---

## 3. Monte Carlo — 100,000 simulações

| Métrica | Valor (BRL) |
|---------|-------------|
| Média | R$ 756.052.476,06 |
| Desvio padrão (σ) | R$ 57.987.556,44 |
| **Erro padrão da média (SEM)** | **R$ 183.372,75** |
| Margem ±95% na média | ± R$ 359.410,60 |
| Mínimo | R$ 533.034.574,96 |
| Máximo | R$ 1.017.058.307,62 |
| Percentil 5 | R$ 663.009.994,21 |
| Percentil 25 | R$ 716.152.308,50 |
| **Mediana (P50)** | **R$ 754.550.041,78** |
| Percentil 75 | R$ 794.500.859,21 |
| Percentil 95 | R$ 853.901.745,52 |
| Largura IC 90% (P95−P5) | R$ 190.891.751,31 |

### Histograma (100,000 cenários)

| Faixa de ganho (12m) | Frequência | Gráfico |
|----------------------|------------|---------|
| R$ 533.034.574,96 – R$ 581.436.948,23 | 57 | `` |
| R$ 581.436.948,23 – R$ 629.839.321,49 | 1,079 | `█` |
| R$ 629.839.321,49 – R$ 678.241.694,76 | 7,482 | `█████████` |
| R$ 678.241.694,76 – R$ 726.644.068,02 | 22,665 | `████████████████████████████` |
| R$ 726.644.068,02 – R$ 775.046.441,29 | 32,258 | `████████████████████████████████████████` |
| R$ 775.046.441,29 – R$ 823.448.814,56 | 24,009 | `█████████████████████████████` |
| R$ 823.448.814,56 – R$ 871.851.187,82 | 9,838 | `████████████` |
| R$ 871.851.187,82 – R$ 920.253.561,09 | 2,270 | `██` |
| R$ 920.253.561,09 – R$ 968.655.934,35 | 310 | `` |
| R$ 968.655.934,35 – R$ 1.017.058.307,62 | 32 | `` |

---

## 4. Precisão: 10,000 vs 100,000 simulações

Ambas as corridas usam a **mesma seed** (`seed + 1000`). Com **100,000** cenários, a estimativa da média converge (SEM ∝ 1/√N); percentis e σ tendem a estabilizar.

| Métrica | 10,000 simulações | 100,000 simulações | Diferença relativa |
|---------|----------------------|----------------------|-------------------|
| Média | R$ 756.044.711,28 | R$ 756.052.476,06 | 0.00% |
| Mediana (P50) | R$ 754.575.261,31 | R$ 754.550.041,78 | 0.00% |
| Desvio padrão (σ) | R$ 58.038.972,86 | R$ 57.987.556,44 | 0.09% |
| Erro padrão da média (SEM) | R$ 580.389,73 | R$ 183.372,75 | −68.41% |
| Margem ±95% na média | R$ 1.137.563,87 | R$ 359.410,60 | −68.41% |
| Percentil 5 | R$ 663.865.414,57 | R$ 663.009.994,21 | 0.13% |
| Percentil 95 | R$ 854.521.212,01 | R$ 853.901.745,52 | 0.07% |
| Largura IC 90% (P95−P5) | R$ 190.655.797,44 | R$ 190.891.751,31 | 0.12% |

### Interpretação da precisão

| Indicador | Resultado |
|-----------|-----------|
| SEM com 10,000 | R$ 580.389,73 |
| SEM com 100,000 | R$ 183.372,75 |
| Redução do SEM observada | **68.41%** (teórico ao 10× amostra: **68.38%**) |
| Diferença nas médias (10k vs 100k) | 0.00% |
| Diferença na mediana (10k vs 100k) | 0.00% |
| Diferença na largura IC 90% | 0.12% |

> **Nota:** O SEM da média diminui aproximadamente como **1/√N**. Percentis e σ da população simulada **estabilizam** com mais cenários; a média converge mais rápido que P5/P95.

---

## 5. Comparativo — eficiência do modelo (100,000 cenários)

| Critério | Observado | Monte Carlo | Avaliação |
|----------|-----------|-------------|-----------|
| Ganho 12 meses | R$ 802.388.872,37 | Média R$ 756.052.476,06 | Erro 6.13% |
| Ganho mensal médio | R$ 66.865.739,36 | R$ 63.004.373,01 | — |
| vs Mediana (P50) | — | R$ 754.550.041,78 | Desvio 6.34% |
| IC 90% (P5–P95) | — | [R$ 663.009.994,21 , R$ 853.901.745,52] | ✅ Dentro do IC 90% |
| IC 50% (P25–P75) | — | [R$ 716.152.308,50 , R$ 794.500.859,21] | ⚠️ |
| Z-score (observado) | 0.80 σ | — | Normal |

- **Erro vs média MC (100,000):** 6.13%
- **Z-score:** 0.80
- **Cobertura IC 90%:** observado dentro do intervalo
- **Eficiência vs mediana:** 6.34% — ✅ Próximo da mediana (≤10%)

| Parâmetro fixo | Valor |
|----------------|-------|
| Impostos sobre receita | 34% |
| Dias por mês | 30 |

---

## 6. Conclusão

Com **100,000** simulações, a estimativa da **média** ficou mais precisa (SEM 68.41% menor que com 10,000). Percentis e desvio-padrão apresentaram diferença relativa de **0.00%** (mediana) e **0.12%** (largura IC 90%) em relação à amostra de 10,000, indicando **maior estabilidade** dos quantis com o volume ampliado.

**Arquivos:** `dados_extracao_petroleo.csv`, `distribuicao_ganhos_monte_carlo.csv` (100,000 linhas), `resultado_monte_carlo.csv`
