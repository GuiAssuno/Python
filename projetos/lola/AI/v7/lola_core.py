import json
import os
import random
from datetime import datetime
import requests
from config import OPENWEATHER_API_KEY

class LolaCore:
    def __init__(self):
        # Diretório base para dados de usuários
        self.users_data_dir = "user_data"
        os.makedirs(self.users_data_dir, exist_ok=True)
        
    def get_user_file_path(self, username, filename):
        user_dir = os.path.join(self.users_data_dir, username)
        os.makedirs(user_dir, exist_ok=True)
        return os.path.join(user_dir, filename)
    
    def load_user_data(self, username):
        user_file = self.get_user_file_path(username, "data.json")
        
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                return json.load(f)
        
        # Dados padrão para novo usuário
        return {
            "preferences": {},
            "reminders": [],
            "conversation_history": []
        }
    
    def save_user_data(self, username, data):
        user_file = self.get_user_file_path(username, "data.json")
        
        with open(user_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def process_command(self, command, username):
        # Carregar dados do usuário
        user_data = self.load_user_data(username)
        
        # Processar o comando
        response = self._process_command_logic(command, username, user_data)
        
        # Adicionar ao histórico de conversas
        user_data["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "response": response
        })
        
        # Manter apenas os últimos 100 itens no histórico
        if len(user_data["conversation_history"]) > 100:
            user_data["conversation_history"] = user_data["conversation_history"][-100:]
        
        # Salvar dados do usuário
        self.save_user_data(username, user_data)
        
        return response
    
    def _process_command_logic(self, command, username, user_data):
        command = command.lower()
        
        # Comandos básicos
        if any(word in command for word in ['olá', 'oi', 'ola', 'hello', 'hi']):
            greetings = [
                f"Olá {username}! Como posso ajudar?",
                f"Oi {username}! Em que posso ser útil?",
                f"Olá {username}! É um prazer conversar com você!",
                f"Oi {username}! Estou aqui para ajudar!"
            ]
            return random.choice(greetings)
        
        elif 'hora' in command:
            now = datetime.now()
            return f"Agora são {now.hour} horas e {now.minute} minutos"
        
        elif 'data' in command or 'dia' in command:
            now = datetime.now()
            months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                     "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
            return f"Hoje é {now.day} de {months[now.month - 1]} de {now.year}"
        
        # Comando para adicionar lembrete
        elif 'lembrete' in command:
            if 'adicionar' in command or 'criar' in command:
                reminder_text = command.replace('adicionar', '').replace('lembrete', '').replace('criar', '').strip()
                
                user_data.setdefault("reminders", []).append({
                    'text': reminder_text,
                    'created': datetime.now().isoformat(),
                    'completed': False
                })
                
                self.save_user_data(username, user_data)
                return f"Lembrete adicionado: {reminder_text}"
            
            elif 'listar' in command or 'mostrar' in command:
                reminders = user_data.get("reminders", [])
                if reminders:
                    response = "Seus lembretes:\n"
                    for i, rem in enumerate(reminders[-5:], 1):  # Últimos 5 lembretes
                        status = "✓" if rem.get('completed', False) else "◯"
                        response += f"{i}. {status} {rem['text']}\n"
                    return response
                return "Você não tem lembretes."
            
            elif 'concluir' in command or 'completar' in command:
                try:
                    # Tentar extrair o número do lembrete
                    parts = command.split()
                    reminder_num = int(parts[-1]) - 1
                    
                    reminders = user_data.get("reminders", [])
                    if 0 <= reminder_num < len(reminders):
                        reminders[reminder_num]['completed'] = True
                        self.save_user_data(username, user_data)
                        return f"Lembrete '{reminders[reminder_num]['text']}' marcado como concluído."
                    else:
                        return "Número de lembrete inválido."
                except (ValueError, IndexError):
                    return "Por favor, especifique o número do lembrete a ser concluído."
        
        # Comando de histórico
        elif 'histórico' in command:
            history = user_data.get("conversation_history", [])
            if history:
                response = "Seu histórico recente:\n"
                for entry in history[-5:]:  # Últimas 5 entradas
                    response += f"- {entry['command']} → {entry['response'][:50]}...\n"
                return response
            return "Não há histórico de conversas."
        
        # Comando de previsão do tempo
        elif 'tempo' in command or 'clima' in command:
            # Extrair cidade do comando
            city = None
            if ' em ' in command:
                city = command.split(' em ')[-1].strip()
            elif ' para ' in command:
                city = command.split(' para ')[-1].strip()
            else:
                # Tentar encontrar um nome de cidade conhecido
                known_cities = ['são paulo', 'rio de janeiro', 'brasília', 'salvador', 'fortaleza', 
                               'belo horizonte', 'manaus', 'curitiba', 'recife', 'porto alegre']
                for known_city in known_cities:
                    if known_city in command:
                        city = known_city
                        break
            
            if city:
                return self.get_weather(city)
            return "Para qual cidade você gostaria da previsão do tempo?"
        
        # Comando de piada
        elif 'piada' in command or 'rir' in command or 'humor' in command:
            jokes = [
                "Por que o Python foi para a festa? Porque ele sabia ser snake!",
                "Qual é o café do programador? É o Java!",
                "Por que os desenvolvedores não gostam da natureza? Porque tem muitos bugs!",
                "Qual é o animal que mais sabe programar? O Python!",
                "Por que o computador foi ao médico? Porque tinha um vírus!"
            ]
            return random.choice(jokes)
        
        # Comando de ajuda
        elif 'ajuda' in command or 'comandos' in command or 'o que você pode fazer' in command:
            return """Posso ajudar com:
            - Dizer as horas e data
            - Adicionar e listar lembretes
            - Mostrar previsão do tempo
            - Contar piadas
            - Manter histórico das nossas conversas
            - E muito mais! Experimente me perguntar coisas."""
        
        # Comando para definir preferências
        elif 'preferência' in command or 'gosto' in command:
            if 'cor favorita' in command:
                if 'é' in command:
                    color = command.split('é')[-1].strip()
                    user_data.setdefault("preferences", {})["favorite_color"] = color
                    self.save_user_data(username, user_data)
                    return f"Entendido, vou lembrar que sua cor favorita é {color}"
                else:
                    color = user_data.get("preferences", {}).get("favorite_color")
                    if color:
                        return f"Sua cor favorita é {color}"
                    return "Ainda não sei qual é sua cor favorita"
        
        return "Desculpe, não entendi esse comando. Pode reformular?"
    
    def get_weather(self, city):
        """Obter previsão do tempo usando OpenWeatherMap API"""
        try:
            if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "sua_chave_aqui":
                return "A API de previsão do tempo não está configurada."
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt"
            response = requests.get(url)
            data = response.json()
            
            if data['cod'] != 200:
                return f"Não consegui obter a previsão para {city}."
            
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            
            return f"Em {city.title()}, está {description} com temperatura de {temp}°C e umidade de {humidity}%."
        
        except Exception as e:
            return f"Erro ao obter previsão do tempo: {str(e)}"