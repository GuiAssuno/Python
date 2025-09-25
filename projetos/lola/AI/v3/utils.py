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