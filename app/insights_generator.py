import pandas as pd

def calculate_insights_and_alerts(df, alert_percentage=5.0):
    """
    Calcula insights e alertas com base nos dados mais recentes.
    
    Args:
        df (pd.DataFrame): DataFrame com histórico de preços.
        alert_percentage (float): Percentual para disparar um alerta.
        
    Returns:
        dict: Dicionário contendo insights e alertas.
    """
    if df.empty or len(df) < 2:
        return {
            "latest_price": "N/A",
            "price_change_24h": "N/A",
            "price_change_7d": "N/A",
            "price_change_30d": "N/A",
            "alert": None
        }

    # Preços
    latest_price = df['price'].iloc[-1]
    price_yesterday = df['price'].iloc[-2] if len(df) > 1 else latest_price
    price_7_days_ago = df['price'].iloc[-8] if len(df) > 7 else df['price'].iloc[0]
    price_30_days_ago = df['price'].iloc[-31] if len(df) > 30 else df['price'].iloc[0]

    # Variações percentuais
    change_24h = ((latest_price - price_yesterday) / price_yesterday) * 100
    change_7d = ((latest_price - price_7_days_ago) / price_7_days_ago) * 100
    change_30d = ((latest_price - price_30_days_ago) / price_30_days_ago) * 100

    # Alerta visual
    alert = None
    if abs(change_24h) > alert_percentage:
        direction = "aumento" if change_24h > 0 else "queda"
        alert = f"Alerta: {direction.capitalize()} significativo de {change_24h:.2f}% nas últimas 24 horas!"
    
    return {
        "latest_price": f"${latest_price:,.2f}",
        "price_change_24h": f"{change_24h:.2f}%",
        "price_change_7d": f"{change_7d:.2f}%",
        "price_change_30d": f"{change_30d:.2f}%",
        "alert": alert
    }