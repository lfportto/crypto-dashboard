# Crypto Dashboard — Pipeline ETL com Dashboard Interativo

📄 [English version](README_English.md)

 ## Descrição do Projeto

Este projeto consiste na construção de um pipeline completo de dados (ETL) automatizado para monitoramento de criptomoedas, desde a coleta até a visualização. Os dados são extraídos da API pública da CoinGecko, transformados e armazenados em um banco de dados PostgreSQL na nuvem (Neon). A partir disso, um dashboard interativo foi desenvolvido com Streamlit para análise visual dos dados. Além disso, o pipeline foi automatizado com GitHub Actions, permitindo atualizações periódicas dos dados sem dependência de execução local.

## 🎯 Objetivo
Este é um projeto pessoal desenvolvido com foco no aprimoramento de habilidades em análise de dados, incluindo:
- Construir um pipeline de dados ponta a ponta (ETL)
- Automatizar a ingestão de dados em ambiente cloud
- Desenvolver um dashboard interativo para análise exploratória
- Demonstrar boas práticas de versionamento, deploy e automação
- Criar um projeto de portfólio com aplicação real de engenharia e análise de dados

## Tecnologias Utilizadas
- Python
- Principais bibliotecas: Pandas, psycopg2, Plotly, Streamlit
- PostgreSQL (Neon - cloud)
- Git & GitHub
- GitHub Actions (automação / CI/CD)
- API CoinGecko

## Arquitetura do Projeto
A figura abaixo mostra como foi estruturada a arquitetura por trás desse projeto.

## Pipeline de Dados (ETL)
### 🔹Extração
Dados obtidos via API da CoinGecko
Criptomoedas monitoradas:
- Bitcoin
- Ethereum
- Solana
- Cardano
- Binance Coin
### 🔹Transformação
- Padronização dos dados
- Conversão de tipos
- Organização temporal (timestamp)
- Cálculo de métricas derivadas (ex: variação percentual)
### 🔹 Carregamento
- Armazenamento em banco PostgreSQL na nuvem (Neon)
- Estrutura relacional simples e eficiente
- Persistência histórica dos dados

## 🛢 Estratégia de Ingestão de Dados
- **Dados históricos ([historico.py](historico.py))**  
  Foi adotada uma estratégia híbrida para equilibrar a granularidade, o volume de dados e a performance:
  - `Últimos 30 dias:` coleta a cada 6 horas (4x ao dia)
  - `De 30 até 180 dias:` coleta diária

- **Ingestão contínua ([ingestao.py](ingestao.py))**
  - Execução automática 4x ao dia
  - 00h, 06h, 12h, 18h
  - Atualização incremental do banco

## Acesse o Dashboard
🔗 [Clique aqui para acessar o dashboard no Streamlit](https://crypto-dashboard-luisfelipeporto.streamlit.app)

## Dashboard Interativo
![dashboard1](https://github.com/user-attachments/assets/8118ab94-92d0-4257-9ec1-2ac6802d7365)

- No topo da página, o dashboard conta com alguns cards de indicadores de performance das criptomoedas selecionadas, estando separados separados em diferentes abas por moeda, para a maior organização e apresentação.
Logo abaixo, encontram-se os gráficos, também divididos em pares por categoria ("Tendência e desempenho" e "Ranking e comparação").
- Evolução do Preço (escala logarítmica): mostra o histórico de preços das criptomoedas ao longo do tempo. A escala logarítimica aplicada nele permite comparar ativos com ordens de grandeza diferentes. Esse gráfico visa responder: como os preços evoluíram ao longo do tempo e quais tendências podem ser observadas?

📊 2. Variação Percentual (Base 100)

O que mostra:

Desempenho relativo das criptomoedas

Como funciona:

Todos os ativos começam em 100
Mostra crescimento ou queda proporcional

Pergunta que responde:

Qual criptomoeda teve melhor desempenho no período analisado?

🏆 3. Ranking de Criptomoedas

O que mostra:

Ranking por:
preço atual
variação percentual

Pergunta que responde:

Quais criptomoedas estão liderando em valor ou desempenho?

📦 4. Distribuição de Preços (Volatilidade)

O que mostra:

Dispersão dos preços ao longo do tempo (boxplot)

Insights:

estabilidade
presença de outliers
amplitude de variação

Pergunta que responde:

Quais criptomoedas são mais estáveis ou mais voláteis?

⚡ Insights Automáticos

O dashboard inclui um destaque inicial com insights como:

Maior valorização no período
Maior queda
Criptomoeda mais volátil

👉 Objetivo: entregar valor imediato ao usuário

🤖 Automação (GitHub Actions)
Execução automática do script de ingestão
Frequência: a cada 6 horas
Independente de máquina local
Benefícios:
Atualização contínua dos dados
Pipeline totalmente automatizado
Simulação de ambiente de produção
☁️ Banco de Dados (Cloud)
PostgreSQL hospedado no Neon
Acesso remoto seguro via connection string
Integração com scripts Python e Streamlit
🚀 Deploy
Dashboard hospedado via Streamlit Cloud
Integração direta com repositório GitHub
Atualizações automáticas conforme versionamento
📁 Estrutura do Projeto
crypto_pipeline/
│
├── app.py                # Dashboard Streamlit
├── historico.py          # Ingestão de dados históricos
├── ingestao.py           # Ingestão contínua
├── requirements.txt
├── .env (não versionado)
│
├── .github/
│   └── workflows/
│       └── ingestao.yml  # Automação (GitHub Actions)
│
└── README.md
🔐 Segurança
Variáveis sensíveis armazenadas via:
GitHub Secrets
Streamlit Secrets
Nenhuma credencial exposta no código
📌 Possíveis Melhorias Futuras
Tratamento de duplicidade de dados
Monitoramento de falhas no pipeline
Inclusão de mais ativos
Criação de alertas automatizados
Integração com ferramentas de BI
Containerização com Docker
🧠 Aprendizados

Este projeto permitiu consolidar conhecimentos em:

Engenharia de dados (ETL)
Consumo de APIs
Modelagem e uso de banco relacional
Visualização de dados
Deploy de aplicações
Automação de pipelines
Versionamento com Git
