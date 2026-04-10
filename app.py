"""
Filename: app.py
Author: Luis Felipe Porto
Date: 10-04-2026
Version: 1.1
Description: Este script se conecta a um banco de dados PostgreSQL hospedado na nuvem via Neon, recupera dados de preços de criptomoedas e cria gráficos usando o Plotly em um dashboard do Streamlit. O painel permite que os usuários analisem o desempenho de cinco criptomoedas principais ao longo de diferentes períodos e com diferentes opções de visualização.
Contact: luisfelipeporto.lfp@gmail.com
"""

import psycopg2
import streamlit as st
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
df = pd.read_sql("SELECT * FROM precos_crypto", conn)

# Transformação dos nomes das moedas para exibição
nomes_moedas = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "binancecoin": "Binance Coin",
    "solana": "Solana",
    "cardano": "Cardano"
}

df["moeda"] = df["moeda"].map(nomes_moedas)

# Sistema de tradução do dashboard
from traducao import traducao

if "idioma" not in st.session_state:
    st.session_state.idioma = "pt"

def tr(key, **kwargs):
    texto = traducao.get(st.session_state.idioma, {}).get(key, key)
    try:
        return texto.format(**kwargs)
    except KeyError:
        return texto

# Configuração de cores para as moedas
color_discrete_map = {
    "Bitcoin": "#f7931a",
    "Ethereum": "#627eea",
    "Binance Coin": "#f3ba2f",
    "Solana": "#9945ff",
    "Cardano": "#0033ad"
}

# Formatação da data/hora para exibição
ultima_atualizacao = df["data_hora"].max()
ultima_atualizacao = ultima_atualizacao.strftime("%d/%m/%Y %H:%M")

# Barra lateral personalizada
# ==========================================================================
# Personalização da logo
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/5170/5170907.png" width="160">
    </div>
    """,
    unsafe_allow_html=True)

# Personalização do fundo da barra lateral
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #19194B;
    }
    </style>
""", unsafe_allow_html=True)

# Personalização da borda da barra lateral
st.markdown("""
<style>
section[data-testid="stSidebar"] {
border-right: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# Seletor de idioma
col1, col2 = st.columns([8, 2])  # ajusta proporção
with col2:
    idioma = st.selectbox(
        "🌐 Idioma / Language",
        options=["pt", "en"],
        format_func=lambda x: "Português" if x == "pt" else "English"
        )
    st.session_state.idioma = idioma

# Filtros na barra lateral
with st.sidebar:
    st.title(tr("filtros"))

    # Filtro de período
    periodo = st.sidebar.selectbox(
    tr("periodo"),
    [7, 30, 90, 180],
    index=1)
    # Configuração do período de análise
    hoje = pd.Timestamp.today()
    inicio = hoje - pd.Timedelta(days=periodo)
    df_periodo = df[
        (df["data_hora"] >= inicio) &
        (df["data_hora"] <= hoje)]

    # Filtro de moedas
    moedas_selecionadas = st.multiselect(
        tr("moedas"),
        options=df["moeda"].unique(),
        default=list(df["moeda"].unique())
    )

    # Tratamento de seleção vazia
    if not moedas_selecionadas:
        st.warning(tr("alerta"))
        st.stop()

    # Aplica o filtro somente se houver seleção
    df_filtrado = df_periodo[
        df_periodo["moeda"].isin(moedas_selecionadas)
    ]
    
    # Filtro de visualização (gráfico 1)
    visualizacao = st.sidebar.selectbox(
        tr("visualizacao"),
        ["Log", "Linear"])
    escala = "log" if visualizacao == "Log" else "linear"

    # Dataframe para ranking das moedas (gráfico 3)
    df_rank = df_filtrado.sort_values("data_hora").groupby("moeda").last().reset_index()

    tipo_ranking = st.sidebar.selectbox(
    tr("ranking_por"),
    [tr("preco"), tr("variacao_pct")])

    st.space("small")
    st.caption(f"{tr('atualizado')} {ultima_atualizacao}")
    linkedin = "https://www.linkedin.com/in/luis-felipe-porto/"
    st.caption(f"🔗 {tr('desenvolvido')} [Luis Felipe Porto]({linkedin})")
# ==========================================================================

# Título
st.markdown(
    f"<h1 style='color: #F09C49;'>{tr('titulo')}</h1>",
    unsafe_allow_html=True)
st.caption(f"{tr('descricao')}")
st.space("small")

# Configuração do card de alerta
# ==========================================================================
metricas = []

for moeda in df_filtrado["moeda"].unique():
    df_moeda = df_filtrado[df_filtrado["moeda"] == moeda].sort_values("data_hora")

    if len(df_moeda) < 2:
        continue

    # Variação no período
    preco_inicial = df_moeda["preco_usd"].iloc[0]
    preco_final = df_moeda["preco_usd"].iloc[-1]
    variacao = ((preco_final - preco_inicial) / preco_inicial) * 100

    # Volatilidade
    df_moeda["retorno"] = df_moeda["preco_usd"].pct_change()
    volatilidade = df_moeda["retorno"].std() * 100

    metricas.append((moeda, variacao, volatilidade))

df_metricas = pd.DataFrame(metricas, columns=["moeda", "variacao", "volatilidade"])

# Identificação de insights para o card de alerta
top_alta = df_metricas.loc[df_metricas["variacao"].idxmax()]
top_queda = df_metricas.loc[df_metricas["variacao"].idxmin()]
top_volatil = df_metricas.loc[df_metricas["volatilidade"].idxmax()]

st.markdown(f"""
<div style="
    background-color: #14143C;
    padding: 16px 18px;
    border-radius: 12px;
    color: white;
    font-size: 14px;
    margin-bottom: 10px;
">
    🚀 <b>{top_alta['moeda']}</b> {tr('insight_alta')} 
    (<span style="color:#5CD96E;">{top_alta['variacao']:.2f}%</span>)
    <span style="margin: 0 14px;">•</span>
    📉 <b>{top_queda['moeda']}</b> {tr('insight_queda')} 
    (<span style="color:#F44950;">{top_queda['variacao']:.2f}%</span>)
    <span style="margin: 0 14px;">•</span>
    ⚡ <b>{top_volatil['moeda']}</b> {tr('insight_vol')} 
    (<span style="color:#58A6FF;">{top_volatil['volatilidade']:.2f}%</span>)
</div>
""", unsafe_allow_html=True)
# ==========================================================================

st.subheader(tr("indicadores"))

def badge_variacao(valor):
    if valor >= 0:
        cor_fonte = "#5CD96E"
        cor_fundo = "#303A4B"
        texto = tr("tag1")
        seta = "🡩"
    else:
        cor_fonte = "#F44950"
        cor_fundo = "#58254B"
        texto = tr("tag2")
        seta = "🡫"

    return f"""
    <div style="
        margin-top: -20px;
        display: flex;
        justify-content: flex-start;
    ">
        <span style="
            background-color: {cor_fundo};
            color: {cor_fonte};
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 400;
            font-family: 'Inter', sans-serif;
        ">
            {seta} {abs(valor):.2f}% {texto}
        </span>
    </div>
    """

# Criação das abas para cada moeda
tab1, tab2, tab3, tab4, tab5= st.tabs(["Bitcoin", "Ethereum", "Binance Coin", "Solana", "Cardano"])

# Métricas principais para Bitcoin
# ==========================================================================
df_btc = df_periodo[df_periodo["moeda"] == "Bitcoin"].sort_values("data_hora")

# Preço atual (último valor)
preco_atual = df_btc["preco_usd"].iloc[-1]

# Preço 24h atrás (ou anterior)
preco_anterior = df_btc["preco_usd"].iloc[-2]

# Variação %
variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

# Máxima e mínima
maximo = df_btc["preco_usd"].max()
minimo = df_btc["preco_usd"].min()

# Mediana
mediana = df_btc["preco_usd"].median()

diff_max = ((maximo - mediana) / mediana) * 100
diff_min = ((minimo - mediana) / mediana) * 100

with tab1:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(tr("preco"), f"U$ {preco_atual:.2f}", f"{variacao:.2f}%")

    with col2:
        st.metric(tr("variacao"), f"{variacao:.2f}%")

    with col3:
        st.metric(tr("maxima"), f"U$ {maximo:.2f}")
        st.markdown(badge_variacao(diff_max), unsafe_allow_html=True)

    with col4:
        st.metric(tr("minima"), f"U$ {minimo:.2f}")
        st.markdown(badge_variacao(diff_min), unsafe_allow_html=True)
# ==========================================================================

# Métricas principais para Ethereum
# ==========================================================================
df_eth = df_periodo[df_periodo["moeda"] == "Ethereum"].sort_values("data_hora")

preco_atual = df_eth["preco_usd"].iloc[-1]
preco_anterior = df_eth["preco_usd"].iloc[-2]

variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

maximo = df_eth["preco_usd"].max()
minimo = df_eth["preco_usd"].min()

mediana = df_eth["preco_usd"].median()

diff_max = ((maximo - mediana) / mediana) * 100
diff_min = ((minimo - mediana) / mediana) * 100

with tab2:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(tr("preco"), f"U$ {preco_atual:.2f}", f"{variacao:.2f}%")

    with col2:
        st.metric(tr("variacao"), f"{variacao:.2f}%")

    with col3:
        st.metric(tr("maxima"), f"U$ {maximo:.2f}")
        st.markdown(badge_variacao(diff_max), unsafe_allow_html=True)

    with col4:
        st.metric(tr("minima"), f"U$ {minimo:.2f}")
        st.markdown(badge_variacao(diff_min), unsafe_allow_html=True)
# ==========================================================================

# Métricas principais para Binance Coin
# ==========================================================================
df_bnc = df_periodo[df_periodo["moeda"] == "Binance Coin"].sort_values("data_hora")

preco_atual = df_bnc["preco_usd"].iloc[-1]
preco_anterior = df_bnc["preco_usd"].iloc[-2]

variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

maximo = df_bnc["preco_usd"].max()
minimo = df_bnc["preco_usd"].min()

mediana = df_bnc["preco_usd"].median()

diff_max = ((maximo - mediana) / mediana) * 100
diff_min = ((minimo - mediana) / mediana) * 100

with tab3:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(tr("preco"), f"U$ {preco_atual:.2f}", f"{variacao:.2f}%")

    with col2:
        st.metric(tr("variacao"), f"{variacao:.2f}%")

    with col3:
        st.metric(tr("maxima"), f"U$ {maximo:.2f}")
        st.markdown(badge_variacao(diff_max), unsafe_allow_html=True)

    with col4:
        st.metric(tr("minima"), f"U$ {minimo:.2f}")
        st.markdown(badge_variacao(diff_min), unsafe_allow_html=True)
# ==========================================================================

# Métricas principais para Solana
# ==========================================================================
df_sol = df_periodo[df_periodo["moeda"] == "Solana"].sort_values("data_hora")

preco_atual = df_sol["preco_usd"].iloc[-1]
preco_anterior = df_sol["preco_usd"].iloc[-2]

variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

maximo = df_sol["preco_usd"].max()
minimo = df_sol["preco_usd"].min()

mediana = df_sol["preco_usd"].median()

diff_max = ((maximo - mediana) / mediana) * 100
diff_min = ((minimo - mediana) / mediana) * 100

with tab4:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(tr("preco"), f"U$ {preco_atual:.2f}", f"{variacao:.2f}%")

    with col2:
        st.metric(tr("variacao"), f"{variacao:.2f}%")

    with col3:
        st.metric(tr("maxima"), f"U$ {maximo:.2f}")
        st.markdown(badge_variacao(diff_max), unsafe_allow_html=True)

    with col4:
        st.metric(tr("minima"), f"U$ {minimo:.2f}")
        st.markdown(badge_variacao(diff_min), unsafe_allow_html=True)
# ==========================================================================

# Métricas principais para Cardano
# ==========================================================================
df_ada = df_periodo[df_periodo["moeda"] == "Cardano"].sort_values("data_hora")

preco_atual = df_ada["preco_usd"].iloc[-1]
preco_anterior = df_ada["preco_usd"].iloc[-2]

variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

maximo = df_ada["preco_usd"].max()
minimo = df_ada["preco_usd"].min()

mediana = df_ada["preco_usd"].median()

diff_max = ((maximo - mediana) / mediana) * 100
diff_min = ((minimo - mediana) / mediana) * 100

with tab5:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(tr("preco"), f"U$ {preco_atual:.2f}", f"{variacao:.2f}%")

    with col2:
        st.metric(tr("variacao"), f"{variacao:.2f}%")

    with col3:
        st.metric(tr("maxima"), f"U$ {maximo:.2f}")
        st.markdown(badge_variacao(diff_max), unsafe_allow_html=True)

    with col4:
        st.metric(tr("minima"), f"U$ {minimo:.2f}")
        st.markdown(badge_variacao(diff_min), unsafe_allow_html=True)
# ==========================================================================

# 1. Gráfico de linha sobre histórico de preços
# ==========================================================================
# Montagem do gráfico 1
fig = px.line(
    df_filtrado,
    x="data_hora",
    y="preco_usd",
    color="moeda",
    color_discrete_map=color_discrete_map,
    markers=True,
    labels={
        "preco_usd": tr('eixo_preco'),
        "moeda": tr('moeda_legenda')}
)

# Personalização do hover
fig.update_traces(
    hovertemplate=
    f"<b>{tr('Data')}: </b> %{{x}}<br>" +
    f"<b>{tr('eixo_preco')}: </b> U$ %{{y:.2f}}<br>" +
    f"<b>{tr('moeda_legenda2')}: </b> %{{fullData.name}}<extra></extra>",
    marker_size=4
)

# Personalização do layout
fig.update_layout(
    title=dict(
        text=tr('grafico1', periodo=periodo, escala=escala),
        font=dict(size=20),
        x=0.5,
        xanchor="center",
        yanchor="top"),
    xaxis_title=None,
    legend_title= tr('moeda_legenda'),
    legend=dict(
        y=0.5,
        yanchor="middle"),
    plot_bgcolor="#09091D",
    paper_bgcolor="#09091D"
)

# Configuração da escala do eixo y
if visualizacao == "Log":
    fig.update_yaxes(type="log")
else:
    fig.update_yaxes(type="linear")

fig.update_xaxes(range=[inicio, hoje])

# Destaque do máximo por moeda
for moeda in df_filtrado["moeda"].unique():
    df_moeda = df_filtrado[df_filtrado["moeda"] == moeda]

    if df_moeda.empty:
        continue

    max_row = df_moeda.loc[df_moeda["preco_usd"].idxmax()]

    fig.add_scatter(
        x=[max_row["data_hora"]],
        y=[max_row["preco_usd"]],
        mode="markers+text",
        marker=dict(
            size=10,
            color="white",
            line=dict(width=2)),
        text=[f"Max: U$ {max_row['preco_usd']:.2f}"],
        textfont=dict(size=10),
        textposition="top center",
        showlegend=False
    )
# ==========================================================================

# 2. Gráfico de linha com variação percentual (base 100)
# ==========================================================================
# Normalização dos preços para base 100
df_pct = df_filtrado.copy()
df_pct = df_pct.sort_values(["moeda", "data_hora"])
df_pct["preco_normalizado"] = df_pct.groupby("moeda")["preco_usd"]\
    .transform(lambda x: (x / x.iloc[0]) * 100)

# Montagem do gráfico 2
fig_pct = px.line(
    df_pct,
    x="data_hora",
    y="preco_normalizado",
    color="moeda",
    color_discrete_map=color_discrete_map,
    markers=True,
    labels={
        "preco_normalizado": "Base 100",
        "moeda": tr('moeda_legenda')
    }
)

# Personalização do hover
fig_pct.update_traces(
    hovertemplate=
    f"<b>{tr('Data')}: </b> %{{x}}<br>" +
    "<b>Base 100:</b> %{y:.2f}<br>" +
    f"<b>{tr('moeda_legenda2')}: </b> %{{fullData.name}}<extra></extra>"
)

# Personalização do layout
fig_pct.update_layout(
    title=dict(
        text=tr('grafico2', periodo=periodo),
        font=dict(size=20),
        x=0.5,
        xanchor="center",
        yanchor="top"),
    xaxis_title=None,
    legend=dict(
        y=0.5,
        yanchor="middle"),
    plot_bgcolor="#09091D",
    paper_bgcolor="#09091D"
)
fig_pct.update_xaxes(range=[inicio, hoje])
fig_pct.update_traces(marker_size=4)
# ==========================================================================

# 3. Gráfico de barras com o ranking das moedas
# ==========================================================================
# Estrutura para ranking das moedas (último preço)
df_inicio = df_filtrado.sort_values("data_hora").groupby("moeda").first().reset_index()
df_rank = df_rank.merge(df_inicio[["moeda", "preco_usd"]], on="moeda", suffixes=("_atual", "_inicio"))

# Variação %
df_rank["variacao_pct"] = (
    (df_rank["preco_usd_atual"] - df_rank["preco_usd_inicio"]) /
    df_rank["preco_usd_inicio"]
) * 100

if tipo_ranking == tr("preco"):
    df_rank = df_rank.sort_values("preco_usd_atual", ascending=False)
    eixo_x = "preco_usd_atual"
    titulo = "Ranking por Preço Atual (USD)"

else:
    df_rank = df_rank.sort_values("variacao_pct", ascending=False)
    eixo_x = "variacao_pct"
    titulo = "Ranking por Variação (%)"

text_col = eixo_x

# Montagem do gráfico 3
fig_rank = px.bar(
    df_rank,
    x=eixo_x,
    y="moeda",
    orientation="h",
    color="moeda",
    color_discrete_map=color_discrete_map,
    text=eixo_x,
    labels={
        "preco_usd_atual": tr('eixo_preco_atual'),
        "variacao_pct": tr('variacao_pct')
    }
)

# Personalização do layout
fig_rank.update_layout(
    title=dict(
        text=tr('grafico3', tipo=tr('preco') if tipo_ranking == "Preço atual" else tr('variacao_pct')),
        font=dict(size=20),
        x=0.5,
        xanchor="center",
        yanchor="top"),
    yaxis_title=None,
    legend_title=tr('moeda_legenda'),
    legend=dict(
        y=0.5,
        yanchor="middle"),
    plot_bgcolor="#09091D",
    paper_bgcolor="#09091D"
)

# Personalização dos rótulos dos dados
if tipo_ranking == "Preço atual":
    text_template = "U$ %{text:.2f}"
else:
    text_template = "%{text:.2f}%"

fig_rank.update_traces(
    texttemplate=text_template,
    textposition="outside",
    cliponaxis=False
)

# Personalização do hover
if tipo_ranking == tr("preco"):
    hovertemplate = (
        f"<b>{tr('moeda_legenda2')}: </b> %{{y}}<br>"
        f"<b>{tr('preco')}: </b> U$ %{{x:.2f}}<br>"
        "<extra></extra>"
    )

else:
    hovertemplate = (
        f"<b>{tr('moeda_legenda2')}: </b> %{{y}}<br>"
        f"<b>{tr('variacao_pct')}: </b> %{{x:.2f}}%<br>"
        "<extra></extra>"
    )

fig_rank.update_traces(hovertemplate=hovertemplate)
# ==========================================================================

# 4. Gráfico de boxplot para análise de volatilidade
# ==========================================================================
# Normalização dos preços para comparação de volatilidade
df_box = df_filtrado.copy()
df_box = df_box.sort_values(["moeda", "data_hora"])
df_box["preco_normalizado"] = df_box.groupby("moeda")["preco_usd"]\
    .transform(lambda x: x / x.iloc[0])

# Montagem do gráfico 4
fig_box = px.box(
    df_box,
    x="moeda",
    y="preco_usd",
    color="moeda",
    color_discrete_map=color_discrete_map,
    points="outliers"
)

# Personalização do layout
fig_box.update_layout(
    title=dict(
        text=tr('grafico4'),
        font=dict(size=20),
        x=0.5,
        xanchor="center",
        yanchor="top"),
    xaxis_title=None,
    yaxis_title=tr('eixo_preco'),
    legend_title=tr('moeda_legenda'),
    legend=dict(
        y=0.5,
        yanchor="middle"),
    plot_bgcolor="#09091D",
    paper_bgcolor="#09091D"
)
fig_box.update_traces(
    boxmean=True
)
# ==========================================================================

# Personalização do container das abas
st.markdown("""
<style>
/* Container geral das abas */
.stTabs [data-baseweb="tab-list"] {
    background-color: #19194B;
    border-radius: 8px;
    padding: 0px;
    border: 1px solid #30305D;
}
/* Abas individuais */
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px;
    padding: 8px 16px;
    margin-right: 5px;
    border: none;
}
/* Aba ativa */
.stTabs [aria-selected="true"] {
    background-color: #14143C;
}
/* Texto padrão */
.stTabs [data-baseweb="tab"] p {
    color: #B0B3C6;
    font-weight: 500;
}
/* Texto da aba ativa */
.stTabs [aria-selected="true"] p {
    color: #FFFFFF;
}
/* Hover */
.stTabs [data-baseweb="tab"]:hover p {
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

st.subheader(tr("aba_mercado"))

# Exibição dos gráficos
tab1, tab2 = st.tabs([tr("aba1"), tr("aba2")])
with tab1:
    st.plotly_chart(fig)
    st.divider()
    st.plotly_chart(fig_pct)
    st.caption(tr("caption1"))
with tab2:
    st.plotly_chart(fig_rank)
    st.divider()
    st.plotly_chart(fig_box)
    st.caption(tr("caption2"))

# Personalização do fundo
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/wkES8Wt.png");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuração da página
st.set_page_config(layout="wide")

conn.close()
