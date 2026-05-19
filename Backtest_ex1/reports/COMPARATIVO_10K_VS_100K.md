# Comparativo Monte Carlo: 10.000 vs 100.000 simulações

**Empresa:** PetroBrasil Extração S.A.  
**Gerado em:** 18/05/2026 20:38  
**Modelo:** `parametros.json` + `distribuicoes.py` + `calcular_mes()`  
**Seed:** 42 (+ 1000 no MC)  
**Horizonte:** 12 meses por cenário

---

## 1. Objetivo

Este documento compara a **precisão e estabilidade** das estimativas obtidas com **10,000** e **100,000** simulações Monte Carlo, usando o mesmo modelo e a mesma seed de aleatoriedade.

---

## 2. Tabela comparativa

| Métrica | 10.000 sim. | 100.000 sim. | Variação |
|---------|-------------|--------------|----------|
| Simulações (N) | 10.000 | 100.000 | ×10 |
| Média | R$ 756.044.711,28 | R$ 756.052.476,06 | 0.00% |
| Mediana (P50) | R$ 754.575.261,31 | R$ 754.550.041,78 | 0.00% |
| Desvio padrão (σ) | R$ 58.038.972,86 | R$ 57.987.556,44 | 0.09% |
| Erro padrão da média (SEM) | R$ 580.389,73 | R$ 183.372,75 | −68.41% |
| Margem ±95% na média | R$ 1.137.563,87 | R$ 359.410,60 | −68.41% |
| IC 95% da média (inferior) | R$ 754.907.147,41 | R$ 755.693.065,46 | 0.10% |
| IC 95% da média (superior) | R$ 757.182.275,15 | R$ 756.411.886,66 | 0.10% |
| Mínimo | R$ 533.034.574,96 | R$ 533.034.574,96 | 0.00% |
| Máximo | R$ 1.001.966.588,54 | R$ 1.017.058.307,62 | 1.48% |
| Percentil 5 | R$ 663.865.414,57 | R$ 663.009.994,21 | 0.13% |
| Percentil 25 | R$ 716.019.014,41 | R$ 716.152.308,50 | 0.02% |
| Percentil 75 | R$ 794.637.855,15 | R$ 794.500.859,21 | 0.02% |
| Percentil 95 | R$ 854.521.212,01 | R$ 853.901.745,52 | 0.07% |
| Largura IC 90% (P95−P5) | R$ 190.655.797,44 | R$ 190.891.751,31 | 0.12% |

---

## 3. Precisão da estimativa da média

O **erro padrão da média (SEM)** quantifica a incerteza na estimativa do ganho líquido médio anual. Com mais simulações, o SEM diminui aproximadamente em **1/√N**.

| Indicador | 10.000 | 100.000 |
|-----------|--------|---------|
| SEM | R$ 580.389,73 | R$ 183.372,75 |
| Margem ±95% | ± R$ 1.137.563,87 | ± R$ 359.410,60 |
| IC 95% da média | [R$ 754.907.147,41 ; R$ 757.182.275,15] | [R$ 755.693.065,46 ; R$ 756.411.886,66] |

| Análise | Valor |
|---------|-------|
| Redução do SEM (observada) | **68.41%** |
| Redução teórica (1/√10) | **68.38%** |
| Redução da margem ±95% | **68.41%** |
| Diferença entre médias | **0.00%** |
| Sobreposição dos IC 95% da média | Sim ✅ |

---

## 4. Estabilidade dos percentis e da dispersão

| Métrica | Diferença relativa (10k → 100k) | Interpretação |
|---------|----------------------------------|---------------|
| Mediana (P50) | 0.00% | Estável |
| Desvio padrão (σ) | 0.09% | Estimativa da dispersão do modelo |
| Percentil 5 | 0.13% | Cauda inferior |
| Percentil 95 | 0.07% | Cauda superior |
| Largura IC 90% | 0.12% | Risco agregado 12 meses |

> Percentis e σ **não** devem mudar drasticamente ao aumentar N; o ganho principal de 100k simulações está na **precisão da média** (SEM).

---

## 5. Distribuição dos ganhos (histogramas)

### 10.000 simulações

| Faixa (12 meses) | Frequência | % do total | Gráfico |
|------------------|------------|------------|---------|
| R$ 533.034.574,96 – R$ 591.651.076,66 | 10 | 0.10% | `` |
| R$ 591.651.076,66 – R$ 650.267.578,36 | 276 | 2.76% | `██` |
| R$ 650.267.578,36 – R$ 708.884.080,05 | 1,833 | 18.33% | `██████████████` |
| R$ 708.884.080,05 – R$ 767.500.581,75 | 3,735 | 37.35% | `██████████████████████████████` |
| R$ 767.500.581,75 – R$ 826.117.083,45 | 2,990 | 29.90% | `████████████████████████` |
| R$ 826.117.083,45 – R$ 884.733.585,14 | 979 | 9.79% | `███████` |
| R$ 884.733.585,15 – R$ 943.350.086,84 | 168 | 1.68% | `█` |
| R$ 943.350.086,84 – R$ 1.001.966.588,54 | 9 | 0.09% | `` |

### 100.000 simulações

| Faixa (12 meses) | Frequência | % do total | Gráfico |
|------------------|------------|------------|---------|
| R$ 533.034.574,96 – R$ 593.537.541,54 | 125 | 0.12% | `` |
| R$ 593.537.541,54 – R$ 654.040.508,12 | 3,344 | 3.34% | `██` |
| R$ 654.040.508,12 – R$ 714.543.474,71 | 20,620 | 20.62% | `███████████████` |
| R$ 714.543.474,71 – R$ 775.046.441,29 | 39,452 | 39.45% | `██████████████████████████████` |
| R$ 775.046.441,29 – R$ 835.549.407,87 | 27,571 | 27.57% | `████████████████████` |
| R$ 835.549.407,87 – R$ 896.052.374,46 | 7,889 | 7.89% | `█████` |
| R$ 896.052.374,46 – R$ 956.555.341,04 | 929 | 0.93% | `` |
| R$ 956.555.341,04 – R$ 1.017.058.307,62 | 70 | 0.07% | `` |

---

## 6. Conclusão

| Critério | 10.000 simulações | 100.000 simulações |
|----------|-------------------|---------------------|
| Uso recomendado | Análises rápidas, protótipos | Decisões que exigem alta precisão na **média** |
| Precisão da média | SEM R$ 580.389,73 | SEM R$ 183.372,75 (**68.41% menor**) |
| Estabilidade P5–P95 | Referência | Diferença &lt; 0,2% nos percentis |
| Tempo de execução | ~2–5 s | ~20–25 s |

**Síntese:** Com **100.000** cenários, a média converge para **R$ 756.052.476,06** (vs R$ 756.044.711,28 em 10k), enquanto o intervalo de confiança da média estreita de ± R$ 1.137.563,87 para ± R$ 359.410,60. Para avaliar **risco** (P5, P95), **10.000** simulações já são suficientes; para **valor esperado** com margem estreita, prefira **100.000**.

---

*Arquivos relacionados: `distribuicao_ganhos_monte_carlo.csv` (100k), `resultado_monte_carlo.csv`, `RELATORIO_COMPARATIVO.md`*
