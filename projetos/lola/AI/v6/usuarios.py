import json
import os

USUARIOS_FILE = "usuarios.json"

def carregar_usuarios():
    """Carrega os usuários do arquivo JSON"""
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    """Salva os usuários no arquivo JSON"""
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def identificar_usuario(comando_voz):
    """Identifica o usuário baseado em padrões de fala"""
    usuarios = carregar_usuarios()
    
    # Padrões de identificação simples
    if "sou o" in comando_voz or "sou a" in comando_voz:
        for nome in usuarios.keys():
            if nome.lower() in comando_voz:
                return nome
    
    # Se não identificou, pede para o usuário se identificar
    return None

def cadastrar_usuario(nome, comando_voz):
    """Cadastra um novo usuário"""
    usuarios = carregar_usuarios()
    
    if nome not in usuarios:
        usuarios[nome] = {
            "comando_cadastro": comando_voz,
            "preferencias": {},
            "historico": []
        }
        salvar_usuarios(usuarios)
        return True
    return False