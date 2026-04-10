# Crypto Dashboard — Análise de Criptomoedas em Tempo Real

📄 [English version](README_English.md)

 ## Descrição do Projeto

Este projeto consiste na construção de um `pipeline completo de dados (ETL)` automatizado para monitoramento de criptomoedas, desde a coleta até a visualização. Os dados são extraídos da `API pública da CoinGecko`, transformados e armazenados em um banco de dados `PostgreSQL na nuvem (Neon)`. A partir disso, um dashboard interativo foi desenvolvido com `Streamlit` para análise visual dos dados. Além disso, o pipeline foi automatizado com GitHub Actions, permitindo atualizações periódicas dos dados sem dependência de execução local.

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
- CSS (customização de layout)
- PostgreSQL (Neon - cloud)
- Git & GitHub
- GitHub Actions (automação / CI/CD)
- API CoinGecko

## Arquitetura do Projeto
A figura abaixo mostra como foi estruturada a arquitetura por trás desse projeto:  

![Pipeline](https://github.com/user-attachments/assets/22da660a-61a6-4900-9ca7-fce6753f6ad4)

## Pipeline de Dados (ETL)
### 🔹Extração
Dados abertos obtidos via API da [CoinGecko](https://docs.coingecko.com)
- Criptomoedas monitoradas: Bitcoin, Ethereum, Solana, Cardano, e Binance Coin
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
No topo da página, há um seletor suspenso por onde é possível escolher o idioma do dashboard, sendo que o usuário pode alternar entre português ou inglês. Logo abaixo do título e subtítulo, o dashboard conta um `card de insights automáticos`, que incluem informações da maior valorização no período, a maior queda e a criptomoeda mais volátil. Além disso, conta ainda com alguns cards de `indicadores de performance` das criptomoedas selecionadas, estando separados separados em diferentes abas por moeda, para a maior organização e apresentação.  

![dashboard1](https://github.com/user-attachments/assets/f26e6a4e-97ff-434e-8044-f322a02fc8f1)

Logo abaixo, encontram-se os gráficos, também divididos em pares por categoria ("Tendência e desempenho" e "Ranking e comparação").
- `Evolução do Preço (escala logarítmica):` mostra o histórico de preços das criptomoedas ao longo do tempo. A escala logarítimica aplicada nele permite comparar ativos com ordens de grandeza diferentes. Esse gráfico visa responder: Como os preços evoluíram ao longo do tempo e quais tendências podem ser observadas?
- `Variação Percentual (Base 100):` mostra o desempenho relativo das criptomoedas. Nele, todos os ativos começam em 100, de modo que as linhas revelam crescimento ou queda proporcional. Esse gráfico visa responder: Qual criptomoeda teve melhor desempenho no período analisado?

- `Ranking de Criptomoedas:` mostra o ranking das moedas por duas visualizações diferentes: preço atual e variação percentual. Esse gráfico visa responder:
Quais criptomoedas estão liderando em valor ou desempenho?

- `Distribuição de Preços (Volatilidade):` mostra a dispersão dos preços ao longo do tempo (boxplot), revelando estabilidade, presença de outliers e amplitude de variação. Esse gráfico visa responder: Quais criptomoedas são mais estáveis ou mais voláteis?

Ademais, há uma `barra lateral` do lado esquerdo, que conta com alguns `filtros` por onde o usuário pode interagir com esses gráficos.

## Paleta de Cores
![Paleta](https://github.com/user-attachments/assets/9813b82f-701c-45fa-a979-cd17008510bf)

## 🤖 Automação (GitHub Actions)
A fim de manter os dados sempre atualizados, foi criada uma automação para a execução automática do script de ingestão `todos os dias a cada 6 horas`, que roda na nuvem e, por isso, independente de máquina local.  
### Benefícios:
- Atualização contínua dos dados
- Pipeline totalmente automatizado
- Simulação de ambiente de produção

## Banco de Dados (Cloud)
- PostgreSQL hospedado no Neon
- Acesso remoto seguro via connection string
- Integração com scripts Python e Streamlit
- Nenhuma credencial exposta

## Possíveis Melhorias Futuras
- Monitoramento de falhas no pipeline
- Inclusão de mais ativos
- Criação de alertas automatizados
- Integração com ferramentas de BI

## Aprendizados
Este projeto permitiu consolidar conhecimentos em:
- Engenharia de dados (ETL)
- Consumo de APIs
- Modelagem e uso de banco relacional
- Visualização de dados
- Deploy de aplicações
- Automação de pipelines
- Versionamento com Git

## Atualizações
🔹 `Versão 1.1 (Publicada em 10 de abril de 2026):` Adicionado sistema de alternância entre idiomas para a visualização do dashboard (Português-BR e Inglês).

## Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Tags
`#analisededados` `#cienciadedados` `#engenhariadedados` `#etl` `#pipeline` `#dados` `#visualizacaodedados` `#dashboard` `#automacao` `#bancodedados` `#postgresql` `#cloud` `#dadosnuvem` `#python` `#streamlit` `#plotly` `#pandas` `#api` `#criptomoedas` `#dataproject` `#portfoliodedados` `#dataanalysis` `#datascience` `#dataengineering` `#datapipeline` `#etlprocess` `#datavisualization` `#dashboarding` `#automation` `#database` `#postgres` `#cloudcomputing` `#pythonproject` `#streamlitapp` `#plotlydash` `#pandaspython` `#apiconsumption` `#crypto` `#cryptodata` `#realtime` `#datadriven` `#analytics` `#businessintelligence` `#githubactions` `#cicd` `#clouddata` `#datastack` `#dataportfolio`
