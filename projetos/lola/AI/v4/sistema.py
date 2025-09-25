import os
import platform
import subprocess

def abrir_programa(nome_programa):
    sistema = platform.system()
    
    try:
        if sistema == "Windows":
            if "chrome" in nome_programa.lower():
                os.system("start chrome")
            elif "notepad" in nome_programa.lower() or "bloco de notas" in nome_programa:
                os.system("notepad")
            else:
                return f"Desculpe, não sei como abrir {nome_programa} no Windows."
        
        elif sistema == "Darwin":  # macOS
            if "chrome" in nome_programa.lower():
                subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"])
            elif "safari" in nome_programa.lower():
                subprocess.Popen(["/Applications/Safari.app/Contents/MacOS/Safari"])
            else:
                return f"Desculpe, não sei como abrir {nome_programa} no macOS."
        
        elif sistema == "Linux":
            if "chrome" in nome_programa.lower():
                subprocess.Popen(["google-chrome"])
            elif "firefox" in nome_programa.lower():
                subprocess.Popen(["firefox"])
            else:
                return f"Desculpe, não sei como abrir {nome_programa} no Linux."
        
        return f"Abri o {nome_programa} para você."
    
    except Exception as e:
        return f"Desculpe, não consegui abrir {nome_programa}. Erro: {str(e)}"

def obter_informacoes_sistema():
    sistema = platform.system()
    versao = platform.version()
    arquitetura = platform.architecture()[0]
    
    return f"Sistema operacional: {sistema}, Versão: {versao}, Arquitetura: {arquitetura}"