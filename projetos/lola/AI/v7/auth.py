from flask import Flask, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import json
import os

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'

# Classe de usuário
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Arquivo de usuários
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username, password):
    users = load_users()
    
    if username in users:
        return False, "Usuário já existe"
    
    users[username] = {
        'password_hash': hash_password(password),
        'preferences': {}
    }
    
    save_users(users)
    return True, "Usuário criado com sucesso"

def verify_user(username, password):
    users = load_users()
    
    if username not in users:
        return False, "Usuário não encontrado"
    
    if not verify_password(password, users[username]['password_hash']):
        return False, "Senha incorreta"
    
    return True, "Login bem-sucedido"

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    if user_id in users:
        return User(user_id, user_id)
    return None