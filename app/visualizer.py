import plotly.graph_objects as go

def create_price_chart(df, crypto_name):
    """
    Cria um gráfico de linha interativo para o histórico de preços.
    
    Args:
        df (pd.DataFrame): DataFrame com as colunas 'date' e 'price'.
        crypto_name (str): Nome da criptomoeda para o título do gráfico.
        
    Returns:
        go.Figure: Figura do Plotly.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['price'],
        mode='lines+markers',
        name='Preço (USD)',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title=f'Histórico de Preços para {crypto_name.upper()}',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1a", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        template='plotly_dark',
        height=500
    )
    
    return fig