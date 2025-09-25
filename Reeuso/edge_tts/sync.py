import edge_tts
import asyncio

async def reproduzir_voz(texto):
    voice = "pt-BR-AntonioNeural"  
    communicate = edge_tts.Communicate(texto, voice)
    await communicate.save("audio.mp3")
    import playsound
    playsound.playsound("audio.mp3")

if __name__ == "__main__":
    asyncio.run(reproduzir_voz("Olá, eu sou a voz do Microsoft Edge."))
