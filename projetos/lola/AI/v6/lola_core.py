import json
import os
import random
from datetime import datetime
import requests
from config import OPENWEATHER_API_KEY

class LolaCore:
    def __init__(self):
        self.users_file = "users.json"
        self.history_file = "conversation_history.json"
        self.load_data()
        
    def load_data(self):
        # Carregar usuários
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            
        # Carregar histórico
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_data(self):
        # Salvar usuários
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
            
        # Salvar histórico (após processar comando)
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-100:], f, indent=4)  # Manter apenas os últimos 100
    
    def process_command(self, command, user_id="anonymous"):
        # Adicionar ao histórico
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_id,
            'command': command,
            'response': ''
        }
        
        # Processar o comando
        response = self._process_command_logic(command, user_id)
        entry['response'] = response
        
        # Adicionar ao histórico e salvar
        self.history.append(entry)
        self.save_data()
        
        return response
    
    def _process_command_logic(self, command, user_id):
        # Lógica de processamento de comandos
        command = command.lower()
        
        # Comandos básicos
        if any(word in command for word in ['olá', 'oi', 'ola', 'hello', 'hi']):
            greetings = [
                "Olá! Como posso ajudar?",
                "Oi! Em que posso ser útil?",
                "Olá! É um prazer conversar com você!",
                "Oi! Estou aqui para ajudar!"
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
                if user_id not in self.users:
                    self.users[user_id] = {"reminders": []}
                
                if 'reminders' not in self.users[user_id]:
                    self.users[user_id]['reminders'] = []
                
                self.users[user_id]['reminders'].append({
                    'text': reminder_text,
                    'created': datetime.now().isoformat()
                })
                self.save_data()
                return f"Lembrete adicionado: {reminder_text}"
            
            elif 'listar' in command or 'mostrar' in command:
                if user_id in self.users and 'reminders' in self.users[user_id] and self.users[user_id]['reminders']:
                    reminders = self.users[user_id]['reminders'][-5:]  # Últimos 5 lembretes
                    response = "Seus lembretes:\n"
                    for i, rem in enumerate(reminders, 1):
                        response += f"{i}. {rem['text']}\n"
                    return response
                return "Você não tem lembretes."
        
        # Comando de histórico
        elif 'histórico' in command:
            user_history = [h for h in self.history if h['user'] == user_id]
            if user_history:
                response = "Seu histórico recente:\n"
                for entry in user_history[-5:]:  # Últimas 5 entradas
                    response += f"- {entry['command']} → {entry['response'][:50]}...\n"
                return response
            return "Não há histórico de conversas."
        
        # Comando para identificar usuário
        elif any(word in command for word in ['chamo', 'sou o', 'sou a', 'meu nome']):
            # Extrair nome do comando
            name = None
            for word in command.split():
                if word not in ['me', 'chamo', 'sou', 'o', 'a', 'é', 'meu', 'nome']:
                    name = word
                    break
            
            if name:
                self.users[user_id] = {"name": name, "reminders": []}
                self.save_data()
                return f"Prazer em conhecê-lo, {name}! Agora vou me lembrar de você."
            return "Não entendi seu nome. Pode repetir?"
        
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