import os
import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

load_dotenv()

# --- DADOS DE CRIPTOMOEDAS (COINGECKO) ---

# Lista pré-definida para simplificar a seleção
CURATED_CRYPTO_LIST = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'XRP': 'ripple',
    'DOGE': 'dogecoin',
    'ADA': 'cardano',
    'SHIB': 'shiba-inu',
    'AVAX': 'avalanche-2'
}

def get_crypto_list():
    """Retorna a lista de criptomoedas pré-definida."""
    return CURATED_CRYPTO_LIST

def get_crypto_historical_data(crypto_id, days='365'):
    """Busca o histórico de preços de uma criptomoeda específica da CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': days, 'interval': 'daily'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['prices']
        df = pd.DataFrame(data, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        return df[['date', 'price']].copy()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados da CoinGecko: {e}")
        return pd.DataFrame()

# --- DADOS DE AÇÕES (ALPHA VANTAGE) ---

# Lista de ações populares (EUA e Brasil)
CURATED_STOCK_LIST = {
    # EUA
    'AAPL': 'Apple Inc.',
    'GOOGL': 'Alphabet (Google)',
    'MSFT': 'Microsoft',
    'AMZN': 'Amazon',
    'TSLA': 'Tesla',
    'NVDA': 'NVIDIA',
    # Brasil (adicione .SA para B3)
    'PETR4.SA': 'Petrobras',
    'VALE3.SA': 'Vale',
    'ITUB4.SA': 'Itaú Unibanco',
    'MGLU3.SA': 'Magazine Luiza'
}

def get_stock_list():
    """Retorna a lista de ações pré-definida."""
    return CURATED_STOCK_LIST

def get_stock_historical_data(symbol):
    """Busca o histórico de preços de uma ação da Alpha Vantage."""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("Erro: Chave da API Alpha Vantage não encontrada.")
        return pd.DataFrame()

    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='full')
        
        # Renomeia e formata o DataFrame para ser compatível com o resto do app
        df = data[['4. close']].rename(columns={'4. close': 'price'})
        df.index = pd.to_datetime(df.index).date
        df.index.name = 'date'
        df = df.sort_index()
        return df.reset_index()
    except Exception as e:
        # A API da Alpha Vantage pode retornar erros específicos em texto
        print(f"Erro ao buscar dados da Alpha Vantage para {symbol}: {e}")
        return pd.DataFrame()