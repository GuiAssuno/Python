from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyaudio
import numpy as np
import threading
import time
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurações de áudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        
    def start_stream(self):
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        self.running = True
        
    def stop_stream(self):
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        
    def get_audio_data(self):
        if self.stream and self.running:
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Calcular FFT para obter frequências
                fft = np.fft.fft(audio_data)
                magnitude = np.abs(fft)[:CHUNK//2]
                
                # Normalizar dados
                if np.max(magnitude) > 0:
                    magnitude = magnitude / np.max(magnitude) * 100
                
                # Reduzir dados para otimizar transmissão (pegar apenas os primeiros 50 pontos)
                wave_data = magnitude[:50].tolist()
                
                return {
                    'waveform': audio_data[:100].tolist(),  # Forma de onda original
                    'spectrum': wave_data,                   # Espectro de frequência
                    'volume': float(np.max(np.abs(audio_data))) / 32768 * 100
                }
            except Exception as e:
                print(f"Erro ao capturar áudio: {e}")
                return None
        return None

audio_processor = AudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    emit('status', {'msg': 'Conectado ao servidor!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

@socketio.on('start_audio')
def handle_start_audio():
    print('Iniciando captura de áudio...')
    audio_processor.start_stream()
    # Iniciar thread para enviar dados de áudio
    threading.Thread(target=audio_loop, daemon=True).start()
    emit('audio_status', {'status': 'started'})

@socketio.on('stop_audio')
def handle_stop_audio():
    print('Parando captura de áudio...')
    audio_processor.stop_stream()
    emit('audio_status', {'status': 'stopped'})

def audio_loop():
    """Loop principal para capturar e enviar dados de áudio"""
    while audio_processor.running:
        audio_data = audio_processor.get_audio_data()
        if audio_data:
            socketio.emit('audio_data', audio_data)
        time.sleep(0.05)  # ~20 FPS

if __name__ == '__main__':
    print("=== Visualizador de Áudio do Sistema ===")
    print("Configuração para capturar áudio do sistema no Linux:")
    print("1. Certifique-se que o PulseAudio está rodando")
    print("2. Se necessário, instale: sudo apt install pulseaudio-utils")
    print("3. Para testar: pactl list short sources")
    print("\nIniciando servidor local...")
    print("Acesse: http://localhost:5000")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)