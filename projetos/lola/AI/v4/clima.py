import requests
from Python.lola.AI.v4.config import OPENWEATHER_API_KEY

def obter_previsao_tempo(cidade=None):
    if not cidade:
        return "Para qual cidade você gostaria da previsão do tempo?"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt_br"
        resposta = requests.get(url)
        dados = resposta.json()
        
        if dados['cod'] != 200:
            return "Não consegui encontrar essa cidade. Poderia repetir?"
        
        temperatura = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        umidade = dados['main']['humidity']
        vento = dados['wind']['speed']
        
        return f"Em {cidade}, está {descricao} com temperatura de {temperatura}°C. Umidade de {umidade}% e vento a {vento} km/h."
    
    except Exception as e:
        return "Desculpe, tive um problema ao acessar a previsão do tempo."