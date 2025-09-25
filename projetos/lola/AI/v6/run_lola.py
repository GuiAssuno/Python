import eventlet
eventlet.monkey_patch(os=True, select=True, socket=True, thread=True, time=True, psycopg=False)
from app import run_flask
import threading
import time

def main():
    print("Iniciando Lola Assistente Pessoal...")
    print("Servidor web disponível em: http://localhost:5000")
    print("Pressione Ctrl+C para parar o servidor")
    
    # Iniciar o servidor Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Manter o programa principal em execução
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nParando Lola...")

if __name__ == "__main__":
    main()