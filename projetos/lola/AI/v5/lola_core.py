import json
import os
from datetime import datetime

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
        # Lógica de processamento de comandos (similar à que já temos)
        command = command.lower()
        
        # Comandos básicos
        if any(word in command for word in ['olá', 'oi', 'ola', 'hello']):
            if user_id in self.users:
                return f"Olá {user_id}! Como posso ajudar?"
            return "Olá! Eu sou a Lola. Como posso ajudar?"
        
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
            # Lógica simplificada para lembrete
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
        
        return "Desculpe, não entendi esse comando. Pode reformular?"