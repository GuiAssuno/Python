import speech_recognition as sr
import pyttsx3
from comandos import COMANDOS
from usuarios import identificar_usuario, cadastrar_usuario, carregar_usuarios
from utils import salvar_no_historico, carregar_historico

# Configurações de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

recognizer = sr.Recognizer()
usuario_atual = None

def falar(texto):
    """Fala um texto usando síntese de voz"""
    print(f"Lola: {texto}")
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    """Ouve e reconhece a fala"""
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
    try:
        print("Reconhecendo...")
        comando = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Erro no serviço de reconhecimento de voz")
        return ""
    except sr.WaitTimeoutError:
        return ""

def processar_comando(comando, usuario):
    """Processa o comando e retorna a resposta apropriada"""
    # Comandos de sistema
    if "quem sou eu" in comando:
        if usuario:
            return f"Você é {usuario}"
        return "Ainda não sei quem você é. Diga 'Eu sou [seu nome]'"
    
    if "me chamo" in comando or "sou o" in comando or "sou a" in comando:
        for palavra in comando.split():
            if palavra not in ["me", "chamo", "sou", "o", "a"]:
                if cadastrar_usuario(palavra, comando):
                    global usuario_atual
                    usuario_atual = palavra
                    return f"Prazer em conhecê-lo, {palavra}! Agora vou me lembrar de você."
                else:
                    return f"Já conheço alguém chamado {palavra}."
    
    # Comandos personalizados por usuário
    usuarios = carregar_usuarios()
    if usuario and usuario in usuarios:
        preferencias = usuarios[usuario].get("preferencias", {})
        
        if "cor favorita" in comando:
            if "minha cor favorita é" in comando:
                cor = comando.split("é")[-1].strip()
                preferencias["cor_favorita"] = cor
                usuarios[usuario]["preferencias"] = preferencias
                from usuarios import salvar_usuarios
                salvar_usuarios(usuarios)
                return f"Entendido, vou lembrar que sua cor favorita é {cor}"
            elif "cor favorita" in comando:
                if "cor_favorita" in preferencias:
                    return f"Sua cor favorita é {preferencias['cor_favorita']}"
                return "Ainda não sei qual é sua cor favorita"
    
    # Comandos normais
    for palavra_chave, funcao in COMANDOS.items():
        if palavra_chave in comando:
            return funcao()
    
    return "Desculpe, não entendi esse comando. Pode repetir?"

def main():
    global usuario_atual
    falar("Olá, eu sou a Lola. Como posso ajudar?")
    
    while True:
        comando = ouvir()
        
        if not comando:
            continue
            
        # Tenta identificar o usuário
        if not usuario_atual:
            usuario_atual = identificar_usuario(comando)
        
        resposta = processar_comando(comando, usuario_atual)
        
        # Salva no histórico
        if usuario_atual:
            salvar_no_historico(usuario_atual, comando, resposta)
        
        falar(resposta)
        
        if "parar" in comando or "sair" in comando:
            falar("Até logo! Foi um prazer ajudar.")
            break
            
        # Mostrar histórico do usuário
        if "histórico" in comando or "o que falei" in comando:
            historico = carregar_historico(usuario_atual)
            ultimos = [f"'{item['comando']}'" for item in historico[-3:]]
            falar(f"Seus últimos comandos foram: {', '.join(ultimos)}")

if __name__ == "__main__":
    main()