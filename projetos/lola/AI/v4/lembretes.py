import json
import os
from datetime import datetime

LEMBRETES_FILE = "lembretes.json"

def carregar_lembretes():
    if os.path.exists(LEMBRETES_FILE):
        with open(LEMBRETES_FILE, "r") as f:
            return json.load(f)
    return []

def salvar_lembretes(lembretes):
    with open(LEMBRETES_FILE, "w") as f:
        json.dump(lembretes, f, indent=4)

def adicionar_lembrete(texto, usuario):
    lembretes = carregar_lembretes()
    
    novo_lembrete = {
        "id": len(lembretes) + 1,
        "usuario": usuario,
        "texto": texto,
        "data_criacao": datetime.now().isoformat(),
        "concluido": False
    }
    
    lembretes.append(novo_lembrete)
    salvar_lembretes(lembretes)
    return f"Lembrete adicionado: {texto}"

def listar_lembretes(usuario):
    lembretes = carregar_lembretes()
    lembretes_usuario = [l for l in lembretes if l["usuario"] == usuario and not l["concluido"]]
    
    if not lembretes_usuario:
        return "Você não tem lembretes pendentes."
    
    resposta = "Seus lembretes:\n"
    for lembrete in lembretes_usuario:
        resposta += f"- {lembrete['texto']}\n"
    
    return resposta

def marcar_lembrete_concluido(id_lembrete, usuario):
    lembretes = carregar_lembretes()
    
    for lembrete in lembretes:
        if lembrete["id"] == id_lembrete and lembrete["usuario"] == usuario:
            lembrete["concluido"] = True
            salvar_lembretes(lembretes)
            return f"Lembrete '{lembrete['texto']}' marcado como concluído."
    
    return "Não encontrei esse lembrete."