# app.py
import webview
import threading
import http.server
import socketserver
import os
import sys
from pathlib import Path

# Diretório base da aplicação
BASE_DIR = Path(__file__).parent.absolute()

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

def run_server(port=8000):
    with socketserver.TCPServer(("", port), HTTPHandler) as httpd:
        print(f"Servindo em http://localhost:{port}")
        httpd.serve_forever()

def create_window():
    # Inicia a janela com a interface web
    window = webview.create_window(
        'Minha Aplicação Python + Web', 
        'http://localhost:8000/index.html',
        width=1000,
        height=700,
        resizable=True
    )
    webview.start(http_server=False, gui='qt')  # Pode usar 'cef' ou 'qt'

if __name__ == '__main__':
    # Verifica se o arquivo HTML existe
    html_file = BASE_DIR / 'index.html'
    if not html_file.exists():
        # Cria o arquivo HTML padrão se não existir
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aplicação Desktop com Web</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 600px;
            padding: 30px;
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.2rem;
        }
        
        p {
            color: #666;
            margin-bottom: 25px;
            line-height: 1.6;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            border-color: #6e8efb;
            outline: none;
        }
        
        button {
            background: linear-gradient(to right, #6e8efb, #a777e3);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 10px 5px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        #resultado {
            margin-top: 25px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #6e8efb;
            text-align: left;
            min-height: 60px;
        }
        
        .status {
            margin-top: 15px;
            color: #28a745;
            font-weight: 500;
        }
        
        .error {
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Aplicação Desktop</h1>
        <p>Interface web integrada com Python</p>
        
        <div class="input-group">
            <input type="text" id="entrada" placeholder="Digite algo aqui...">
        </div>
        
        <div>
            <button id="btn-processar">Processar</button>
            <button id="btn-limpar">Limpar</button>
        </div>
        
        <div id="resultado"></div>
        
        <div class="status" id="status"></div>
    </div>

    <script>
        // Exemplo de comunicação com Python (via pywebview API)
        document.addEventListener('DOMContentLoaded', function() {
            const entrada = document.getElementById('entrada');
            const btnProcessar = document.getElementById('btn-processar');
            const btnLimpar = document.getElementById('btn-limpar');
            const resultado = document.getElementById('resultado');
            const status = document.getElementById('status');
            
            btnProcessar.addEventListener('click', function() {
                const texto = entrada.value.trim();
                
                if (!texto) {
                    status.textContent = 'Por favor, digite algo.';
                    status.className = 'status error';
                    return;
                }
                
                status.textContent = 'Processando...';
                status.className = 'status';
                
                // Simular processamento
                setTimeout(() => {
                    resultado.innerHTML = `<strong>Resultado:</strong> ${texto.toUpperCase()}`;
                    status.textContent = 'Processamento concluído!';
                }, 1000);
            });
            
            btnLimpar.addEventListener('click', function() {
                entrada.value = '';
                resultado.textContent = '';
                status.textContent = '';
            });
        });
    </script>
</body>
</html>''')
    
    # Inicia o servidor HTTP em uma thread separada
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Cria a janela da aplicação
    create_window()