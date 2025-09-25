import speech_recognition as sr
import pyttsx3

# Inicializar o reconhecedor de voz e o sintetizador
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def falar(texto):
    """Fala um texto usando síntese de voz"""
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    """Ouve e reconhece a fala"""
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Reconhecendo...")
        comando = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        print("Não entendi o que você disse")
        return ""
    except sr.RequestError:
        print("Erro no serviço de reconhecimento de voz")
        return ""

# Teste inicial
if __name__ == "__main__":
    falar("Olá, eu sou a Lola. Como posso ajudar?")
    
    while True:
        comando = ouvir()
        
        if "parar" in comando:
            falar("Até logo!")
            break
        elif "olá" in comando:
            falar("Olá! É um prazer conversar com você!")
        elif "como você está" in comando:
            falar("Estou funcionando perfeitamente, obrigada por perguntar!")