import json
import os

def carregar_historico():
    """Carrega o histórico de conversas"""
    if os.path.exists("historico.json"):
        with open("historico.json", "r") as f:
            return json.load(f)
    return []

def salvar_historico(historico):
    """Salva o histórico de conversas"""
    with open("historico.json", "w") as f:
        json.dump(historico[-50:], f)  # Salva apenas os últimos 50 comandos

def limpar_historico():
    """Limpa o histórico de conversas"""
    if os.path.exists("historico.json"):
        os.remove("historico.json")