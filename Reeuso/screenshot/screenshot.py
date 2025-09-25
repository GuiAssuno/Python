import pyautogui
import pytesseract
from pynput import keyboard
import time
import sys
import subprocess

class ImpressScreenReader:
    def __init__(self):
        self.is_impress_running = False
        self.is_presentation_mode = False
        self.listener = None
    
    def Verifica(self):
        """olha se o Impress está sendo executado"""
        try:
            result = subprocess.run(['pgrep', '-f', 'soffice.*impress'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def print_tela(self):
        """Tira print da tela inteira"""
        try:
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            print(f" Erro ao capturar tela: {e}")
            return None                      
    
    def pega_texto(self, image):
        """Peguar texto da imagem usando OCR"""
        try:
            gray_image = image.convert('L')
            
            text = pytesseract.image_to_string(gray_image, lang='por')
            
            # Limpa o texto
            #clean_text = ' '.join(text.split())
            #return clean_text if clean_text else ""
            return text if text else "Não consegui, me desculpe oh mestre gui lorde das trevas o mais pika das galaxas o mais poderoso supremo magnânimo ser mais inteligente de todos os tempo. (estou beijando seus pés pedindo humildemente a magestosa gloriosa justa e linda misericordia do meu amo)"
            
        except Exception as e:
            print(f" Erro no OCR: {e}")
            return ""

    def process_current_slide(self):
        """Processa o slide atual: screenshot → OCR → TTS"""
        print(" Capturando tela...")
        
        # 1. Tira screenshot
        screenshot = self.print_tela()
        if not screenshot:
            return False
        
        # 2. Extrai texto da imagem
        print(" Extraindo texto...")
        text = self.pega_texto(screenshot)
        
        if text:
            print(f" Texto encontrado: {text[:100]}...")
            return True
        else:
            print(" Nenhum texto detectado na tela")
            return False
    
    def on_key_press(self, key):
        """Processa teclas pressionadas"""
        try:
            if key == keyboard.Key.f5:
                self.is_presentation_mode = True
                time.sleep(10)
                self.process_current_slide()

            elif key == keyboard.Key.right:
                if self.is_presentation_mode:
                    time.sleep(0.5) 
                self.process_current_slide()
            
            elif key == keyboard.Key.left:
                if self.is_presentation_mode:
                    time.sleep(0.5) 
                    self.process_current_slide()
            
            elif key == keyboard.Key.esc:
                self.stop()
                return False
                
        except Exception as e:
            pass

    def start(self):
        """Inicia o negocio do key event"""

        # Inicia o listener do teclado
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
        try:
            # Mantém o script rodando
            while self.listener.is_alive():
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Para o monitoramento"""
        if self.listener:
            self.listener.stop()
        print("=" * 12)
        print("\n   SAINDO   \n")
        print("=" * 12)
        sys.exit(0) 


def main():
    reader = ImpressScreenReader()
    reader.start()

if __name__ == "__main__":
    main()
