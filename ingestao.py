"""
Filename: ingestao.py
Author: Luis Felipe Porto
Date: 28-03-2026
Version: 1.0
Description: Este script se conecta a um banco de dados PostgreSQL, recupera dados de preços atuais de criptomoedas da API do CoinGecko e os insere no banco de dados. O script foi projetado para ser executado a cada 6 horas para manter o banco de dados atualizado com os preços mais recentes.
Contact: luisfelipeporto.lfp@gmail.com
"""

import requests
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
conn = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = conn.cursor()

# Coleta de preços atuais das criptomoedas via API CoinGecko
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum,solana,cardano,binancecoin",
    "vs_currencies": "usd"
}

data = requests.get(url, params=params).json()

# Inserção dos dados
for moeda, valores in data.items():
    preco = valores["usd"]
    agora = datetime.now()

    cursor.execute(
        """
        INSERT INTO precos_crypto (moeda, preco_usd, data_hora, fonte)
        VALUES (%s, %s, %s, %s)
        """,
        (moeda, preco, agora, "api")
    )

conn.commit()
cursor.close()
conn.close()

print("Ingestão concluída com sucesso!")