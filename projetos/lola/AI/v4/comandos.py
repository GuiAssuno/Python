'''def cumprimentar():
    return "Olá! É um prazer conversar com você!"

def como_esta():
    return "Estou funcionando perfeitamente, obrigada por perguntar!"

def horario_atual():
    from datetime import datetime
    agora = datetime.now()
    return f"Agora são {agora.hour} horas e {agora.minute} minutos"

def data_atual():
    from datetime import datetime
    agora = datetime.now()
    return f"Hoje é {agora.day} do {agora.month} de {agora.year}"

# Dicionário de comandos reconhecíveis
COMANDOS = {
    "olá": cumprimentar,
    "oi": cumprimentar,
    "como você está": como_esta,
    "que horas são": horario_atual,
    "qual é a hora": horario_atual,
    "que dia é hoje": data_atual,
    "qual é a data": data_atual
}



'''
'''
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

'''

import json
from datetime import datetime
from usuarios import carregar_usuarios
from Python.lola.AI.v4.clima import obter_previsao_tempo
from lembretes import adicionar_lembrete, listar_lembretes, marcar_lembrete_concluido
from Python.lola.AI.v4.sistema import abrir_programa, obter_informacoes_sistema
from Python.lola.AI.v4.pesquisa import pesquisar_wikipedia

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
    "qual é a data": data_atual,
    "previsão do tempo": obter_previsao_tempo,
    "adicionar lembrete": adicionar_lembrete,
    "listar lembretes": listar_lembretes,
    "concluir lembrete": marcar_lembrete_concluido,
    "abrir": abrir_programa,
    "informações do sistema": obter_informacoes_sistema,
    "pesquisar": pesquisar_wikipedia,
    "o que é": pesquisar_wikipedia
}