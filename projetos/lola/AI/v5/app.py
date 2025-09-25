# app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

# Inicialize a aplicação Flask e o SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lola_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lola_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Simulação simples da Lola - em uma implementação real, importaríamos o módulo completo
class SimpleLola:
    def process_command(self, command, user="anonymous"):
        command = command.lower()
        if "olá" in command or "oi" in command:
            return "Olá! Como posso ajudar?"
        elif "hora" in command:
            from datetime import datetime
            now = datetime.now()
            return f"Agora são {now.hour} horas e {now.minute} minutos"
        elif "data" in command:
            from datetime import datetime
            now = datetime.now()
            return f"Hoje é {now.day}/{now.month}/{now.year}"
        else:
            return "Desculpe, não entendi. Pode repetir?"

lola = SimpleLola()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command', '')
    user = data.get('user', 'anonymous')
    
    if command:
        response = lola.process_command(command, user)
        return jsonify({'response': response})
    
    return jsonify({'error': 'No command provided'})

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    socketio.emit('response', {'text': 'Conectado à Lola. Como posso ajudar?'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

def run_flask():
    print("Servidor Flask iniciado")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_flask()