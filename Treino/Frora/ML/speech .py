import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# Inicializa o reconhecedor
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Fale algo:")
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("Você disse: {}".format(text))
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))