#!/usr/bin/env python3
"""
Monitor LibreOffice Impress - Text-to-Speech para Slides
Monitora apresentações do LibreOffice Impress e converte o conteúdo dos slides em áudio PT-BR

Dependências:
pip install psutil gtts pygame pillow python-xlib opencv-python

Para instalar dependências do sistema (Ubuntu 24):
sudo apt install python3-pip espeak espeak-data-pt-br festival festvox-kallpc16k
"""

import os
import sys
import time
import psutil
import subprocess
import hashlib
import tempfile
from pathlib import Path
import threading
import queue
import logging

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageGrab
    import pygame
    from gtts import gTTS
    import Xlib.display
    from Xlib import X
except ImportError as e:
    print(f"Erro ao importar dependências: {e}")
    print("Execute: pip install psutil gtts pygame pillow python-xlib opencv-python")
    sys.exit(1)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImpressMonitor:
    def __init__(self):
        self.current_slide_hash = None
        self.current_slide_content = ""
        self.is_monitoring = False
        self.temp_dir = Path(tempfile.gettempdir()) / "impress_tts"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Inicializar pygame mixer para áudio
        pygame.mixer.init()
        
        # Configurações
        self.check_interval = 2.0  # segundos
        self.audio_queue = queue.Queue()
        self.audio_thread = None
        
        # Display X11 para captura de tela
        try:
            self.display = Xlib.display.Display()
        except Exception as e:
            logger.error(f"Erro ao conectar com X11: {e}")
            self.display = None

    def is_impress_active(self):
        """Verifica se o LibreOffice Impress está rodando e ativo"""
        try:
            # Verificar se o processo existe
            impress_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'soffice' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline'] or []
                        if any('impress' in arg.lower() for arg in cmdline):
                            impress_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not impress_processes:
                return False, None
            
            # Verificar janela ativa
            try:
                result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    window_name = result.stdout.strip()
                    if 'impress' in window_name.lower() or 'libreoffice' in window_name.lower():
                        return True, window_name
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            # Método alternativo: verificar se há janelas do LibreOffice
            try:
                result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'libreoffice' in line.lower() or 'impress' in line.lower():
                            return True, line.split()[-1] if line.split() else "LibreOffice Impress"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
                
            return len(impress_processes) > 0, "LibreOffice Impress"
            
        except Exception as e:
            logger.error(f"Erro ao verificar Impress ativo: {e}")
            return False, None

    def capture_screen_region(self):
        """Captura a região da tela onde está o Impress"""
        try:
            # Capturar tela inteira primeiro
            screenshot = ImageGrab.grab()
            return np.array(screenshot)
        except Exception as e:
            logger.error(f"Erro ao capturar tela: {e}")
            return None

    def extract_text_from_clipboard(self):
        """Tenta extrair texto do clipboard (útil se o usuário copiar o slide)"""
        try:
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return ""

    def extract_text_ocr(self, image):
        """Extrai texto da imagem usando OCR básico (implementação simples)"""
        try:
            # Converter para escala de cinza
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Aplicar threshold para melhorar o contraste
            _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
            
            # Salvar temporariamente para OCR
            temp_img = self.temp_dir / "temp_slide.png"
            cv2.imwrite(str(temp_img), thresh)
            
            # Tentar usar tesseract se disponível
            try:
                result = subprocess.run(['tesseract', str(temp_img), 'stdout', '-l', 'por'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    text = result.stdout.strip()
                    if len(text) > 10:  # Filtrar resultados muito pequenos
                        return text
            except FileNotFoundError:
                logger.warning("Tesseract não encontrado. Instale com: sudo apt install tesseract-ocr tesseract-ocr-por")
            except subprocess.TimeoutExpired:
                logger.warning("OCR timeout")
            
            # Limpeza
            if temp_img.exists():
                temp_img.unlink()
                
        except Exception as e:
            logger.error(f"Erro no OCR: {e}")
        
        return ""

    def get_slide_content_via_uno(self):
        """Tenta obter conteúdo do slide via UNO API"""
        try:
            script = """
import uno
import sys

def get_slide_text():
    try:
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)
        ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        
        docs = desktop.getComponents()
        enum = docs.createEnumeration()
        
        while enum.hasMoreElements():
            doc = enum.nextElement()
            if hasattr(doc, 'getDrawPages'):
                controller = doc.getCurrentController()
                if hasattr(controller, 'getCurrentPage'):
                    slide = controller.getCurrentPage()
                    text = ""
                    for i in range(slide.getCount()):
                        shape = slide.getByIndex(i)
                        if hasattr(shape, 'getString'):
                            text += shape.getString() + " "
                    return text.strip()
        return ""
    except:
        return ""

print(get_slide_text())
"""
            
            temp_script = self.temp_dir / "get_slide.py"
            temp_script.write_text(script)
            
            result = subprocess.run([sys.executable, str(temp_script)], 
                                  capture_output=True, text=True, timeout=10)
            
            temp_script.unlink()
            
            if result.returncode == 0:
                return result.stdout.strip()
                
        except Exception as e:
            logger.error(f"Erro ao usar UNO API: {e}")
        
        return ""

    def detect_slide_change(self):
        """Detecta se houve mudança no slide atual"""
        try:
            # Método 1: Capturar e comparar screenshot
            screenshot = self.capture_screen_region()
            if screenshot is not None:
                # Calcular hash da região central (onde geralmente está o conteúdo)
                h, w = screenshot.shape[:2]
                center_region = screenshot[h//4:3*h//4, w//4:3*w//4]
                current_hash = hashlib.md5(center_region.tobytes()).hexdigest()
                
                if self.current_slide_hash != current_hash:
                    self.current_slide_hash = current_hash
                    
                    # Tentar extrair texto por diferentes métodos
                    text_content = ""
                    
                    # Método 1: UNO API
                    uno_text = self.get_slide_content_via_uno()
                    if len(uno_text) > 10:
                        text_content = uno_text
                    
                    # Método 2: OCR se UNO falhar
                    if not text_content:
                        ocr_text = self.extract_text_ocr(screenshot)
                        if len(ocr_text) > 10:
                            text_content = ocr_text
                    
                    # Método 3: Clipboard como fallback
                    if not text_content:
                        clipboard_text = self.extract_text_from_clipboard()
                        if len(clipboard_text) > 10:
                            text_content = clipboard_text
                    
                    # Se não conseguiu texto, usar texto padrão
                    if not text_content:
                        text_content = "Novo slide detectado. Conteúdo não pôde ser extraído automaticamente."
                    
                    return True, text_content
            
            return False, ""
            
        except Exception as e:
            logger.error(f"Erro ao detectar mudança de slide: {e}")
            return False, ""

    def generate_audio(self, text):
        """Gera áudio a partir do texto usando gTTS"""
        try:
            if not text.strip():
                return None
            
            # Limpar texto
            clean_text = text.replace('\n', ' ').replace('\r', ' ')
            clean_text = ' '.join(clean_text.split())
            
            if len(clean_text.strip()) < 3:
                return None
            
            # Gerar áudio com gTTS
            tts = gTTS(text=clean_text, lang='pt-br', slow=False)
            
            # Salvar em arquivo temporário
            audio_file = self.temp_dir / f"slide_audio_{int(time.time())}.mp3"
            tts.save(str(audio_file))
            
            return audio_file
            
        except Exception as e:
            logger.error(f"Erro ao gerar áudio: {e}")
            # Fallback para espeak se gTTS falhar
            try:
                audio_file = self.temp_dir / f"slide_audio_espeak_{int(time.time())}.wav"
                subprocess.run(['espeak', '-v', 'pt-br', '-s', '150', '-w', str(audio_file), text], 
                             check=True, timeout=10)
                return audio_file
            except Exception as e2:
                logger.error(f"Erro com espeak também: {e2}")
                return None

    def play_audio(self, audio_file):
        """Reproduz o arquivo de áudio"""
        try:
            pygame.mixer.music.load(str(audio_file))
            pygame.mixer.music.play()
            
            # Aguardar finalização
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Erro ao reproduzir áudio: {e}")
            # Fallback para player externo
            try:
                subprocess.run(['aplay', str(audio_file)], check=True, timeout=30)
            except Exception as e2:
                logger.error(f"Erro com aplay: {e2}")

    def audio_worker(self):
        """Worker thread para processar áudio"""
        while self.is_monitoring:
            try:
                audio_file = self.audio_queue.get(timeout=1)
                if audio_file is None:  # Sinal para parar
                    break
                
                logger.info("Reproduzindo áudio do slide...")
                self.play_audio(audio_file)
                
                # Limpeza
                try:
                    audio_file.unlink()
                except:
                    pass
                    
                self.audio_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no worker de áudio: {e}")

    def start_monitoring(self):
        """Inicia o monitoramento"""
        logger.info("Iniciando monitoramento do LibreOffice Impress...")
        self.is_monitoring = True
        
        # Iniciar thread de áudio
        self.audio_thread = threading.Thread(target=self.audio_worker, daemon=True)
        self.audio_thread.start()
        
        try:
            while self.is_monitoring:
                is_active, window_name = self.is_impress_active()
                
                if is_active:
                    logger.debug(f"Impress ativo: {window_name}")
                    
                    slide_changed, content = self.detect_slide_change()
                    
                    if slide_changed and content:
                        logger.info("Mudança de slide detectada!")
                        logger.info(f"Conteúdo: {content[:100]}...")
                        
                        # Gerar áudio
                        audio_file = self.generate_audio(content)
                        if audio_file:
                            # Adicionar à fila de reprodução
                            self.audio_queue.put(audio_file)
                        else:
                            logger.warning("Não foi possível gerar áudio")
                
                else:
                    logger.debug("LibreOffice Impress não está ativo")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário")
        finally:
            self.stop_monitoring()

    def stop_monitoring(self):
        """Para o monitoramento"""
        logger.info("Parando monitoramento...")
        self.is_monitoring = False
        
        # Sinalizar thread de áudio para parar
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_queue.put(None)
            self.audio_thread.join(timeout=3)
        
        # Limpeza de arquivos temporários
        try:
            for file in self.temp_dir.glob("slide_audio_*"):
                file.unlink()
        except Exception as e:
            logger.error(f"Erro na limpeza: {e}")

def main():
    print("=== Monitor LibreOffice Impress - TTS ===")
    print("Este script monitora apresentações do LibreOffice Impress")
    print("e converte o conteúdo dos slides em áudio PT-BR")
    print()
    
    # Verificar dependências do sistema
    required_tools = ['xdotool', 'wmctrl', 'xclip']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, timeout=3)
        except FileNotFoundError:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"AVISO: Ferramentas não encontradas: {', '.join(missing_tools)}")
        print("Instale com: sudo apt install xdotool wmctrl xclip")
        print("O script funcionará com funcionalidade limitada.")
        print()
    
    # Verificar se tesseract está disponível
    try:
        subprocess.run(['tesseract', '--version'], capture_output=True, timeout=3)
        print("✓ Tesseract OCR encontrado")
    except FileNotFoundError:
        print("AVISO: Tesseract OCR não encontrado")
        print("Para melhor extração de texto, instale com:")
        print("sudo apt install tesseract-ocr tesseract-ocr-por")
        print()
    
    print("Pressione Ctrl+C para parar o monitoramento")
    print("=" * 50)
    
    monitor = ImpressMonitor()
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()