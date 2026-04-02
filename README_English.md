# Crypto Dashboard — Real-Time Cryptocurrency Analysis

📄 [Versão em português](README.md)

## Project Description

This project consists of building a `complete automated data pipeline (ETL)` for monitoring cryptocurrencies, from data collection to visualization. The data is extracted from the `CoinGecko public API`, transformed, and stored in a `PostgreSQL cloud database (Neon)`. From this, an interactive dashboard was developed using `Streamlit` for visual data analysis. Additionally, the pipeline was automated with GitHub Actions, allowing periodic data updates without relying on local execution.

## 🎯 Objective
This is a personal project developed with a focus on improving data analysis skills, including:
- Building an end-to-end data pipeline (ETL)
- Automating data ingestion in a cloud environment
- Developing an interactive dashboard for exploratory analysis
- Demonstrating best practices in versioning, deployment, and automation
- Creating a portfolio project with real-world application in data engineering and analysis

## Technologies Used
- Python
- Main libraries: Pandas, psycopg2, Plotly, Streamlit
- CSS (layout customization)
- PostgreSQL (Neon - cloud)
- Git & GitHub
- GitHub Actions (automation / CI/CD)
- CoinGecko API

## Project Architecture
The figure below shows how the architecture behind this project was structured:  
![Pipeline](https://github.com/user-attachments/assets/22da660a-61a6-4900-9ca7-fce6753f6ad4)

## Data Pipeline (ETL)
### 🔹 Extraction
Open data obtained via the [CoinGecko API](https://docs.coingecko.com)
- Monitored cryptocurrencies: Bitcoin, Ethereum, Solana, Cardano, and Binance Coin

### 🔹 Transformation
- Data standardization
- Type conversion
- Temporal organization (timestamp)
- Calculation of derived metrics (e.g., percentage variation)

### 🔹 Loading
- Storage in a PostgreSQL cloud database (Neon)
- Simple and efficient relational structure
- Historical data persistence

## 🛢 Data Ingestion Strategy
- **Historical data ([historico.py](historico.py))**  
  A hybrid strategy was adopted to balance granularity, data volume, and performance:
  - `Last 30 days:` data collected every 6 hours (4 times per day)
  - `From 30 up to 180 days:` daily data collection

- **Continuous ingestion ([ingestao.py](ingestao.py))**
  - Automatic execution 4 times per day
  - 00h, 06h, 12h, 18h
  - Incremental database updates

## Access the Dashboard
🔗 [Click here to access the dashboard on Streamlit](https://crypto-dashboard-luisfelipeporto.streamlit.app)

## Interactive Dashboard
At the top of the page, the dashboard includes an `automatic insights card`, highlighting information such as the highest gain in the period, the biggest drop, and the most volatile cryptocurrency. In addition, it features `key performance indicator cards` for the selected cryptocurrencies, organized into separate tabs by asset for better structure and presentation.

![dashboard1](https://github.com/user-attachments/assets/8118ab94-92d0-4257-9ec1-2ac6802d7365)

Below that, the charts are displayed, also grouped in pairs by category ("Trend and Performance" and "Ranking and Comparison"):
- `Price Evolution (logarithmic scale):` shows the historical price trends of cryptocurrencies over time. The logarithmic scale allows comparison between assets with different orders of magnitude. This chart answers: How have prices evolved over time and what trends can be observed?
- `Percentage Variation (Base 100):` shows the relative performance of cryptocurrencies. All assets start at 100, so the lines reveal proportional growth or decline. This chart answers: Which cryptocurrency performed best during the analyzed period?

- `Cryptocurrency Ranking:` shows the ranking of assets based on two views: current price and percentage variation. This chart answers:
Which cryptocurrencies are leading in value or performance?

- `Price Distribution (Volatility):` shows the dispersion of prices over time (boxplot), revealing stability, presence of outliers, and variation range. This chart answers: Which cryptocurrencies are more stable or more volatile?

Additionally, there is a `sidebar` on the left containing `filters` that allow users to interact with the charts.

## Color Palette
![Paleta](https://github.com/user-attachments/assets/03aaa1d3-e16d-4d34-b881-ac62b8300285)

## 🤖 Automation (GitHub Actions)
To keep the data always up to date, an automation was created to run the ingestion script automatically `every day every 6 hours`. It runs in the cloud and is therefore independent of a local machine.

### Benefits:
- Continuous data updates
- Fully automated pipeline
- Simulation of a production environment

## Cloud Database
- PostgreSQL hosted on Neon
- Secure remote access via connection string
- Integration with Python scripts and Streamlit
- No credentials exposed

## Possible Future Improvements
- Pipeline failure monitoring
- Inclusion of more assets
- Creation of automated alerts
- Integration with BI tools

## Learnings
This project helped consolidate knowledge in:
- Data engineering (ETL)
- API consumption
- Relational database modeling and usage
- Data visualization
- Application deployment
- Pipeline automation
- Version control with Git

## License
This project is licensed under the [MIT License](LICENSE).

## Tags
`#analisededados` `#cienciadedados` `#engenhariadedados` `#etl` `#pipeline` `#dados` `#visualizacaodedados` `#dashboard` `#automacao` `#bancodedados` `#postgresql` `#cloud` `#dadosnuvem` `#python` `#streamlit` `#plotly` `#pandas` `#api` `#criptomoedas` `#dataproject` `#portfoliodedados` `#dataanalysis` `#datascience` `#dataengineering` `#datapipeline` `#etlprocess` `#datavisualization` `#dashboarding` `#automation` `#database` `#postgres` `#cloudcomputing` `#pythonproject` `#streamlitapp` `#plotlydash` `#pandaspython` `#apiconsumption` `#crypto` `#cryptodata` `#realtime` `#datadriven` `#analytics` `#businessintelligence` `#githubactions` `#cicd` `#clouddata` `#datastack` `#dataportfolio`
