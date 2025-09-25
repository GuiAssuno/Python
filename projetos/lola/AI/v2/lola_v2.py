import speech_recognition as sr
import pyttsx3
from comandos import COMANDOS

# Configurações de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Selecione a voz desejada
engine.setProperty('rate', 150)  # Velocidade da fala

recognizer = sr.Recognizer()

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

def processar_comando(comando):
    """Processa o comando e retorna a resposta apropriada"""
    for palavra_chave, funcao in COMANDOS.items():
        if palavra_chave in comando:
            return funcao()
    
    return "Desculpe, não entendi esse comando. Pode repetir?"

# Sistema de histórico simples
historico = []

def main():
    falar("Olá, eu sou a Lola. Como posso ajudar?")
    
    while True:
        comando = ouvir()
        
        if not comando:
            continue
            
        historico.append(comando)
        
        if "parar" in comando or "sair" in comando:
            falar("Até logo! Foi um prazer ajudar.")
            break
            
        resposta = processar_comando(comando)
        falar(resposta)
        
        # Mostrar histórico recente
        if "histórico" in comando or "o que falei" in comando:
            falar(f"Seus últimos comandos foram: {', '.join(historico[-3:])}")

if __name__ == "__main__":
    main()