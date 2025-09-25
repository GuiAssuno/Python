def cumprimentar():
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