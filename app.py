import streamlit as st
import pandas as pd
import plotly.express as px

# Cache para carregamento eficiente dos dados
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['landing_time'] = pd.to_datetime(df['landing_time'])
    df['ano'] = df['landing_time'].dt.year
    return df

# Título do dashboard
st.title("✈️ Dashboard de Tráfego AeroVision")

# Carrega os dados
data = load_data("data/sfo_landings.csv")

# Filtros na barra lateral
st.sidebar.header("Filtros")
ano_selecionado = st.sidebar.slider(
    "Selecione o Ano", int(data['ano'].min()), int(data['ano'].max()), int(data['ano'].max())
)
companhias_selecionadas = st.sidebar.multiselect(
    "Companhia(s) Aérea(s)", data['airline'].unique(), default=data['airline'].unique()
)
tipos_selecionados = st.sidebar.multiselect(
    "Tipo de Aeronave", data['aircraft_type'].unique(), default=data['aircraft_type'].unique()
)

# Filtra os dados
filtrado = data[
    (data['ano'] == ano_selecionado) &
    (data['airline'].isin(companhias_selecionadas)) &
    (data['aircraft_type'].isin(tipos_selecionados))
]

# Métricas principais
st.header(f"Visão Geral: {ano_selecionado}")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pousos", filtrado.shape[0])
col2.metric("Tipos de Aeronaves", filtrado['aircraft_type'].nunique())
col3.metric("Companhias Aéreas", filtrado['airline'].nunique())

# Gráfico de barras: Pousos por companhia
st.subheader("Pousos por Companhia Aérea")
fig1 = px.bar(
    filtrado.groupby('airline').size().reset_index(name='pousos'),
    x='airline', y='pousos', title='Número de Pousos por Companhia'
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de boxplot: Distribuição de peso por tipo
st.subheader("Distribuição de Peso Pousado por Tipo de Aeronave")
fig2 = px.box(
    filtrado, x='aircraft_type', y='weight_landed',
    title='Peso Pousado por Tipo'
)
st.plotly_chart(fig2, use_container_width=True)

# Visualização geoespacial
st.subheader("Visão Geoespacial dos Pousos")
fig3 = px.scatter_mapbox(
    filtrado, lat='lat', lon='lon', color='aircraft_type', size='weight_landed',
    zoom=10, mapbox_style='carto-positron', title='Localização dos Pousos'
)
st.plotly_chart(fig3, use_container_width=True)

# Instruções de deploy
st.sidebar.markdown("---")
st.sidebar.markdown("### Deploy no Streamlit Cloud")
st.sidebar.markdown(
    "1. Faça push do repositório no GitHub.\n"
    "2. Acesse https://streamlit.io/cloud e conecte sua conta GitHub.\n"
    "3. Selecione este repositório e clique em ‘Deploy’."
)
