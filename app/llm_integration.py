import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_ai_analysis(asset_name, insights, asset_type='ativo'):
    """
    Gera uma análise em linguagem natural usando o modelo da Groq.
    
    Args:
        asset_name (str): Nome do ativo (ex: BTC, AAPL).
        insights (dict): Dicionário com os insights calculados.
        asset_type (str): Tipo do ativo ('criptomoeda' ou 'ação').
        
    Returns:
        str: Texto da análise gerada pela IA.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Erro: A chave da API da Groq não foi encontrada."

    client = Groq(api_key=api_key)
    
    prompt = f"""
    Você é um analista financeiro que explica dados de forma simples.
    Sua tarefa é analisar o desempenho recente do seguinte {asset_type}: {asset_name.upper()}.

    Use os dados abaixo:
    - Preço Atual: {insights['latest_price']}
    - Variação em 24 horas: {insights['price_change_24h']}
    - Variação em 7 dias: {insights['price_change_7d']}
    - Variação em 30 dias: {insights['price_change_30d']}
    
    Forneça uma análise curta (máximo de 3 parágrafos) sobre a tendência recente.
    Se houver um alerta, mencione-o de forma destacada.
    
    Alerta: {insights['alert'] if insights['alert'] else "Nenhum alerta significativo."}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=300,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar análise com a IA: {e}"