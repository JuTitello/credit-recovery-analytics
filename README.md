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
├── data/
│   ├── raw/
│   └── processed/
├── python/
│   ├── generate_data.py
│   └── data_quality.py
├── sql/
│   ├── 01_schema.sql
│   ├── 02_transformations.sql
│   └── 03_analysis.sql
├── powerbi/
│   └── dashboard.pbix
├── docs/
│   ├── data_dictionary.md
│   └── business_questions.md
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
- [ ] Geração da base sintética de dados
- [ ] Validação e qualidade dos dados
- [ ] Modelagem no PostgreSQL
- [ ] Análises SQL de carteira e recuperação
- [ ] Dashboard executivo no Power BI
- [ ] Documentação de insights e recomendações de negócio

> Este projeto está em construção e evoluindo publicamente — os commits refletem o passo a passo do desenvolvimento.

## 👩‍💻 Autora

**Júlia Titello**
[LinkedIn](https://linkedin.com/in/júlia-titello) · [GitHub](https://github.com/JuTitello)
