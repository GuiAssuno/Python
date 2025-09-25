'''import json
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


        '''
import json
import os
from datetime import datetime
from usuarios import *

def carregar_historico(usuario=None):
    """Carrega o histórico de conversas de um usuário específico ou geral"""
    usuarios = carregar_usuarios()
    
    if usuario and usuario in usuarios:
        return usuarios[usuario].get("historico", [])
    
    # Histórico geral (todos os usuários)
    historico_geral = []
    for user_data in usuarios.values():
        historico_geral.extend(user_data.get("historico", []))
    
    # Ordena por timestamp
    historico_geral.sort(key=lambda x: x.get("timestamp", ""))
    return historico_geral

def salvar_no_historico(usuario, comando, resposta):
    """Salva uma interação no histórico do usuário"""
    usuarios = carregar_usuarios()
    
    if usuario in usuarios:
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "comando": comando,
            "resposta": resposta
        }
        
        usuarios[usuario]["historico"].append(entrada)
        
        # Mantém apenas os últimos 100 registros
        if len(usuarios[usuario]["historico"]) > 100:
            usuarios[usuario]["historico"] = usuarios[usuario]["historico"][-100:]
        
        salvar_usuarios(usuarios)