# 💳 Credit Recovery Analytics

Mini plataforma de dados que simula a área de **Recuperação de Crédito** de uma operação bancária, do dado bruto ao dashboard de negócio.

O objetivo do projeto é responder perguntas reais de negócio como:

- Quanto temos em carteira e quanto já foi recuperado?
- Qual a taxa de recuperação por região, faixa de atraso e estratégia de cobrança?
- Como a recuperação evolui mês a mês?
- Onde estão as maiores oportunidades de atuação?

## 🏗️ Arquitetura

```
Dados brutos (CSV)
        │
        ▼
   Python (geração + tratamento + validação)
        │
        ▼
   PostgreSQL (modelagem + SQL analítico)
        │
        ▼
   Power BI (dashboard executivo)
```

## 📁 Estrutura do repositório

```
credit-recovery-analytics/
├── python/
│   ├── db.py                  # conexão com o PostgreSQL (variáveis do .env)
│   ├── gerar_clientes.py      # geração de clientes sintéticos
│   ├── gerar_assessorias.py   # geração de assessorias de cobrança
│   ├── gerar_contratos.py     # geração de contratos (parcelas, vencimento, status)
│   ├── gerar_pagamentos.py    # pagamentos coerentes com o status do contrato
│   ├── gerar_interacoes.py    # interações de cobrança após o vencimento
│   └── main.py                # orquestra a geração e a carga no banco
├── sql/
│   ├── 01_schema.sql          # tabelas, constraints e view de faixa de atraso
│   └── 03_analysis.sql        # consultas de análise (em desenvolvimento)
├── powerbi/                   # dashboard (em desenvolvimento)
├── docs/                      # dicionário de dados e perguntas de negócio (em desenvolvimento)
├── .env.example               # modelo das variáveis de ambiente
├── .gitignore
├── README.md
└── requirements.txt
```

## 🧱 Modelo de dados

- `clientes`
- `contratos`
- `pagamentos`
- `interacoes_cobranca`
- `assessorias`

Volume simulado: ~50–100 mil contratos, gerados de forma sintética com Python.

## 🛠️ Stack

- **Python** — geração e tratamento de dados
- **PostgreSQL** — modelagem relacional e SQL analítico
- **Power BI** — dashboards e storytelling de negócio

## 🚧 Status do projeto

- [x] Definição do cenário de negócio
- [x] Geração da base sintética de dados
- [x] Validação e qualidade dos dados
- [ ] Modelagem no PostgreSQL
- [ ] Análises SQL de carteira e recuperação
- [ ] Dashboard executivo no Power BI
- [ ] Documentação de insights e recomendações de negócio

> Este projeto está em construção e evoluindo publicamente — os commits refletem o passo a passo do desenvolvimento.


**Júlia Titello**
[LinkedIn](https://linkedin.com/in/júlia-titello) · [GitHub](https://github.com/JuTitello)
