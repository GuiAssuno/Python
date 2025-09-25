from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lola_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Importar a Lola completa
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lola_core import LolaCore

lola = LolaCore()

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
        
        # Enviar resposta via SocketIO também
        socketio.emit('response', {'text': response})
        
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