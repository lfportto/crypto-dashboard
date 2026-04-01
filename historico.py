"""
Filename: historico.py
Author: Luis Felipe Porto
Date: 27-03-2026
Version: 2.0
Description: Este script realiza um backfill híbrido dos dados de preços de criptomoedas, combinando dados de alta granularidade (6 horas) dos últimos 30 dias com dados diários dos últimos 180 dias. O script inclui tratamento de rate limit, validação de resposta e granularidade dinâmica (6h + diário).
"""

import requests
import pandas as pd
import psycopg2
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Moedas a serem coletadas
MOEDAS = ["bitcoin", "ethereum", "binancecoin", "solana", "cardano"]

# Função para fazer requisições com tratamento de rate limit e validação de resposta
def fazer_requisicao(url, params, tentativas=5):
    for i in range(tentativas):
        try:
            response = requests.get(url, params=params)
            response.encoding = "utf-8"

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 429:
                espera = 5 * (i + 1)
                print(f"Rate limit atingido. Tentando novamente em {espera}s...")
                time.sleep(espera)

            else:
                print(f"Erro {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"Erro na requisição: {e}")
            time.sleep(5)

    return None

# Conexão com o banco de dados
conn = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = conn.cursor()

# Limpar tabela antes do backfill
cursor.execute("TRUNCATE TABLE precos_crypto RESTART IDENTITY")
conn.commit()

for moeda in MOEDAS:
    try:
        print(f"Coletando dados de {moeda}...")

        url = f"https://api.coingecko.com/api/v3/coins/{moeda}/market_chart"

        # Coleta de dados dos últimos 30 dias com granularidade de 6 horas
        params_30 = {"vs_currency": "usd", "days": 30}
        data_30 = fazer_requisicao(url, params_30)

        if not data_30 or "prices" not in data_30:
            print(f"Erro nos dados (30 dias) para {moeda}: {data_30}")
            continue

        df_30 = pd.DataFrame(data_30["prices"], columns=["timestamp", "preco_usd"])
        df_30["data_hora"] = pd.to_datetime(df_30["timestamp"], unit="ms")
        df_30.set_index("data_hora", inplace=True)

        df_30 = df_30.resample("6h").last().dropna()

        time.sleep(3)

        # Coleta de dados dos últimos 180 dias com granularidade diária
        params_180 = {"vs_currency": "usd", "days": 180}
        data_180 = fazer_requisicao(url, params_180)

        if not data_180 or "prices" not in data_180:
            print(f"Erro nos dados (180 dias) para {moeda}: {data_180}")
            continue

        df_180 = pd.DataFrame(data_180["prices"], columns=["timestamp", "preco_usd"])
        df_180["data_hora"] = pd.to_datetime(df_180["timestamp"], unit="ms")
        df_180.set_index("data_hora", inplace=True)

        df_180 = df_180.resample("1D").last().dropna()

        limite = pd.Timestamp.today() - pd.Timedelta(days=30)
        df_180 = df_180[df_180.index < limite]

        df_final = pd.concat([df_180, df_30])
        df_final = df_final.sort_index()
        df_final.reset_index(inplace=True)

        registros_inseridos = 0

        # Inserção dos dados no banco de dados com tratamento de duplicatas
        for _, row in df_final.iterrows():
            cursor.execute(
                """
                INSERT INTO precos_crypto (moeda, preco_usd, data_hora, fonte)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (moeda, data_hora) DO NOTHING;
                """,
                (moeda, row["preco_usd"], row["data_hora"], "backfill")
            )
            registros_inseridos += 1

        print(f"{registros_inseridos} registros inseridos para {moeda}")

        time.sleep(3)

    except Exception as e:
        print(f"Erro ao processar {moeda}: {e}")

conn.commit()
cursor.close()
conn.close()

print("Backfill híbrido concluído!")