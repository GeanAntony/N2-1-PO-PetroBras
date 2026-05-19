# Backtest — Extração de Petróleo (Monte Carlo)

Modelo de extração de petróleo no Brasil com simulação Monte Carlo de ganhos em BRL (12 meses).

## Estrutura do projeto

```
Backtest_ex1/
├── config/
│   └── parametros.json          # Parâmetros e distribuições
├── src/
│   ├── paths.py                 # Caminhos centralizados
│   ├── distribuicoes.py         # Normal, lognormal, triangular
│   ├── gerar_dados.py           # Série mensal (valores reais simulados)
│   ├── monte_carlo.py           # Simulação anual + mensal
│   └── relatorios/
│       ├── utils.py
│       └── gerar_apresentacao_ganhos.py
├── data/
│   └── output/                  # CSVs gerados
├── reports/                     # Relatórios Markdown
├── scripts/                     # Pontos de entrada
│   ├── run_gerar_dados.py
│   ├── run_monte_carlo.py
│   ├── run_apresentacao.py
│   └── run_pipeline.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.10+
- Apenas biblioteca padrão (sem dependências externas obrigatórias)

## Uso

Na raiz do projeto:

```powershell
# Pipeline completo
python scripts/run_pipeline.py

# Ou passo a passo
python scripts/run_gerar_dados.py
python scripts/run_monte_carlo.py
python scripts/run_apresentacao.py
```

## Saídas

| Arquivo | Descrição |
|---------|-----------|
| `data/output/dados_extracao_petroleo.csv` | Série mensal (12 meses) |
| `data/output/resultado_monte_carlo.csv` | Resumo anual da simulação |
| `data/output/resultado_monte_carlo_mensal.csv` | Estatísticas por mês (100k cenários) |
| `data/output/distribuicao_ganhos_monte_carlo.csv` | 100k ganhos anuais (grande; no .gitignore) |
| `reports/APRESENTACAO_GANHOS.md` | Comparativo real vs simulação |

## Configuração

Edite `config/parametros.json` para ajustar produção, preço, câmbio, impostos e número de simulações (`monte_carlo.simulacoes`).

## Git

```powershell
git init
git add .
git commit -m "Estrutura inicial: modelo Monte Carlo extração petróleo"
```

O arquivo `distribuicao_ganhos_monte_carlo.csv` (~100k linhas) está no `.gitignore`; regenere com `run_monte_carlo.py`.
