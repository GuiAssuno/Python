from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO
from flask_login import current_user, login_required
import eventlet
eventlet.monkey_patch()

from auth import login_manager, register_user, verify_user, load_user, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lola_secret_key_muito_segura_aqui'  # Em produção, use uma chave secreta forte e aleatória
app.config['SESSION_PROTECTION'] = 'strong'

# Inicializar o LoginManager
login_manager.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Importar a Lola completa
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lola_core import LolaCore

lola = LolaCore()

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message = verify_user(username, password)
        
        if success:
            user = User(username, username)
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('As senhas não coincidem', 'error')
        else:
            success, message = register_user(username, password)
            if success:
                flash(message, 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'error')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('login'))

# Rota principal - requer autenticação
@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

# API de comandos - requer autenticação
@app.route('/api/command', methods=['POST'])
@login_required
def handle_command():
    data = request.json
    command = data.get('command', '')
    
    if command:
        response = lola.process_command(command, current_user.username)
        
        # Enviar resposta via SocketIO também
        socketio.emit('response', {'text': response}, room=current_user.username)
        
        return jsonify({'response': response})
    
    return jsonify({'error': 'No command provided'})

@socketio.on('connect')
@login_required
def handle_connect():
    print(f'Cliente conectado: {current_user.username}')
    # Associar o socket à sala do usuário
    socketio.emit('response', {'text': 'Conectado à Lola. Como posso ajudar?'}, room=current_user.username)

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

def run_flask():
    print("Servidor Flask iniciado")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_flask()