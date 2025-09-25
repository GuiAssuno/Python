import json
from datetime import datetime
from usuarios import carregar_usuarios

def cumprimentar(usuario=None):
    if usuario:
        usuarios = carregar_usuarios()
        if usuario in usuarios:
            preferencias = usuarios[usuario].get("preferencias", {})
            if "cor_favorita" in preferencias:
                return f"Olá {usuario}! Que bom te ver hoje. Sua cor favorita {preferencias['cor_favorita']} é linda!"
        return f"Olá {usuario}! É um prazer conversar com você!"
    return "Olá! É um prazer conversar com você!"

def como_esta():
    return "Estou funcionando perfeitamente, obrigada por perguntar!"

def horario_atual():
    agora = datetime.now()
    return f"Agora são {agora.hour} horas e {agora.minute} minutos"

def data_atual():
    agora = datetime.now()
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    return f"Hoje é {agora.day} de {meses[agora.month - 1]} de {agora.year}"

# Dicionário de comandos reconhecíveis
COMANDOS = {
    "olá": lambda usuario=None: cumprimentar(usuario),
    "oi": lambda usuario=None: cumprimentar(usuario),
    "como você está": como_esta,
    "que horas são": horario_atual,
    "qual é a hora": horario_atual,
    "que dia é hoje": data_atual,
    "qual é a data": data_atual
}