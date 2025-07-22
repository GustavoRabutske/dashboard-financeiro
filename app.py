import streamlit as st
import pandas as pd
from app.data_fetcher import (
    get_crypto_list, get_crypto_historical_data,
    get_stock_list, get_stock_historical_data
)
from app.visualizer import create_price_chart
from app.insights_generator import calculate_insights_and_alerts
from app.llm_integration import generate_ai_analysis

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Funções de Cache ---
@st.cache_data(ttl=3600)
def cached_get_asset_list(asset_type):
    if asset_type == "Criptomoedas":
        return get_crypto_list()
    else:
        return get_stock_list()

@st.cache_data(ttl=300)
def cached_get_historical_data(asset_type, selected_id, days):
    if asset_type == "Criptomoedas":
        return get_crypto_historical_data(selected_id, str(days))
    else:
        return get_stock_historical_data(selected_id)

# --- Barra Lateral (Sidebar) ---
st.sidebar.title("🛠️ Configurações")

# Seleção do tipo de ativo
asset_type = st.sidebar.selectbox(
    "1. Escolha o tipo de ativo:",
    ["Criptomoedas", "Ações (Bolsa de Valores)"]
)

# Carrega a lista de ativos com base no tipo
asset_list = cached_get_asset_list(asset_type)
default_selection = 'BTC' if asset_type == "Criptomoedas" else 'AAPL'

selected_asset_symbol = st.sidebar.selectbox(
    "2. Escolha o ativo:",
    options=list(asset_list.keys()),
    index=list(asset_list.keys()).index(default_selection)
)
selected_asset_id = selected_asset_symbol if asset_type == "Ações (Bolsa de Valores)" else asset_list[selected_asset_symbol]

# Controles de período e alerta
days_to_load = st.sidebar.slider(
    "Selecione o período de análise (dias):",
    min_value=30, max_value=365, value=180, step=1,
    disabled=(asset_type == "Ações (Bolsa de Valores)") # AlphaVantage free tier traz dados 'full'
)
alert_percentage = st.sidebar.number_input(
    "Percentual para Alerta de Variação Diária (%)",
    min_value=0.5, max_value=20.0, value=5.0, step=0.5
)

# --- Corpo Principal do Dashboard ---
st.title(f"📊 Dashboard de Análise: {selected_asset_symbol}")

# --- NOVA SEÇÃO: DISCLAIMER E INFORMAÇÕES ---
with st.expander("ℹ️ Sobre esta Aplicação e Fontes de Dados", expanded=False):
    st.info(
        """
        **Bem-vindo ao Dashboard Financeiro para Portfólio!**

        Esta aplicação é um projeto de demonstração e **não deve ser usada para tomar decisões financeiras reais.** Os dados aqui apresentados podem ter imprecisões ou atrasos.
        
        **Fontes de Dados:**
        - **Criptomoedas:** Dados fornecidos pela API pública da [CoinGecko](https://www.coingecko.com/en/api).
        - **Ações:** Dados fornecidos pela API gratuita da [Alpha Vantage](https://www.alphavantage.co/).
        - **Análise por IA:** Textos gerados pela API da [Groq](https://groq.com/) com o modelo Llama 3.
        """
    )

# Carrega e exibe os dados
with st.spinner(f"Buscando dados para {selected_asset_symbol}..."):
    historical_data = cached_get_historical_data(asset_type, selected_asset_id, days_to_load)

if historical_data.empty:
    st.error(f"Não foi possível obter os dados para {selected_asset_symbol}. A API pode estar temporariamente indisponível ou o ativo ser inválido.")
else:
    # --- Métricas e Alertas ---
    st.header("🔍 Insights Rápidos")
    insights = calculate_insights_and_alerts(historical_data, alert_percentage)
    
    if insights["alert"]:
        st.warning(insights["alert"])
        
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Preço Atual (USD)", insights["latest_price"])
    col2.metric("Variação 24h", insights["price_change_24h"])
    col3.metric("Variação 7 dias", insights["price_change_7d"])
    col4.metric("Variação 30 dias", insights["price_change_30d"])
    
    st.markdown("---")

    # --- Gráfico Interativo ---
    st.header("📈 Gráfico de Preços")
    price_chart = create_price_chart(historical_data, selected_asset_symbol)
    st.plotly_chart(price_chart, use_container_width=True)

    st.markdown("---")

    # --- Análise com IA ---
    st.header("🤖 Análise por IA (Llama 3)")
    asset_type_for_ia = 'criptomoeda' if asset_type == "Criptomoedas" else 'ação'
    with st.spinner("Gerando análise com Inteligência Artificial..."):
        ai_analysis = generate_ai_analysis(selected_asset_symbol, insights, asset_type_for_ia)
        st.info(ai_analysis)

# --- Rodapé ---
st.sidebar.markdown("---")
st.sidebar.info("Este é um projeto de portfólio. Os dados são para fins de demonstração.")