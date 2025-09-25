
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

            #entender esse trecho de codigo 

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
            
            # Verificar janela ativa com xdotool
            try:
                result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    window_name = result.stdout.strip()
                    if any(keyword in window_name.lower() for keyword in ['impress', 'libreoffice', 'apresentação']):
                        return True, window_name
            except (subprocess.TimeoutExpired, FileNotFoundError):
                logger.debug("xdotool não disponível")
            
            # Método alternativo: verificar se há janelas do LibreOffice com wmctrl
            try:
                result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if any(keyword in line.lower() for keyword in ['libreoffice', 'impress', 'apresentação']):
                            return True, line.split(None, 3)[-1] if len(line.split()) > 3 else "LibreOffice Impress"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                logger.debug("wmctrl não disponível")
            
            # Fallback: se há processos do Impress, assumir que está ativo
            if impress_processes:
                return True, "LibreOffice Impress (processo detectado)"
                
            return False, None
            
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
        """Extrai texto da imagem usando OCR com foco na área de conteúdo"""
        try:
            # Converter para escala de cinza
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Pegar apenas a região central (evitar menus e barras)
            h, w = gray.shape[:2]
            # Cortar bordas para evitar interface do sistema
            margin_top = int(h * 0.15)    # 15% do topo (barra de título/menu)
            margin_bottom = int(h * 0.10) # 10% da base (barra de status)
            margin_left = int(w * 0.05)   # 5% da esquerda
            margin_right = int(w * 0.05)  # 5% da direita
            
            cropped = gray[margin_top:h-margin_bottom, margin_left:w-margin_right]
            
            # Melhorar contraste com CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(cropped)
            
            # Aplicar threshold adaptativo
            thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Remover ruído com operações morfológicas
            kernel = np.ones((2,2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Salvar temporariamente para OCR
            temp_img = self.temp_dir / "temp_slide.png"
            cv2.imwrite(str(temp_img), cleaned)
            
            # Tentar usar tesseract com configurações otimizadas
            try:
                # Configurações do Tesseract para melhor reconhecimento
                config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüý0123456789.,!?:;()-\'" '
                
                result = subprocess.run(['tesseract', str(temp_img), 'stdout', '-l', 'por', config], 
                                      capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    raw_text = result.stdout.strip()
                    
                    # Filtrar e limpar o texto extraído
                    cleaned_text = self.clean_ocr_text(raw_text)
                    
                    if len(cleaned_text) > 15:  # Texto mínimo válido
                        return cleaned_text
                        
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
    
    def clean_ocr_text(self, text):
        """Limpa e filtra o texto extraído por OCR"""
        if not text:
            return ""
        
        # Lista de palavras/frases comuns da interface que devem ser removidas
        interface_words = [
            'arquivo', 'editar', 'seleção', 'ver', 'acessar', 'inserir', 'formatar',
            'slide', 'ferramentas', 'janela', 'ajuda', 'ctrl', 'alt', 'shift',
            'bd >', 'ds e', 'exp.oradcr', 'vscode', '.py', 'lola', 'pesquisa',
            'run', '—-', 'edodos', 'ind', '1426', 'orsa', 'esq', 'dir'
        ]
        
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) < 3:  # Ignorar linhas muito curtas
                continue
                
            # Converter para minúsculas para comparação
            line_lower = line.lower()
            
            # Verificar se a linha contém muitas palavras da interface
            interface_count = sum(1 for word in interface_words if word in line_lower)
            
            # Se mais de 30% da linha são palavras de interface, ignorar
            words_in_line = len(line.split())
            if words_in_line > 0 and (interface_count / words_in_line) > 0.3:
                continue
            
            # Filtrar linhas que são claramente elementos de interface
            if any(pattern in line_lower for pattern in [
                'à arquivo', 'editar seleção', 'vscode', '.py', 'bd >', 'exp.oradcr'
            ]):
                continue
            
            # Filtrar linhas com muitos caracteres especiais
            special_chars = sum(1 for c in line if c in '—-=+*&%$#@![]{}()<>|\\/')
            if len(line) > 0 and (special_chars / len(line)) > 0.4:
                continue
            
            filtered_lines.append(line)
        
        # Juntar linhas válidas
        cleaned_text = ' '.join(filtered_lines)
        
        # Limpeza final
        cleaned_text = ' '.join(cleaned_text.split())  # Normalizar espaços
        
        return cleaned_text

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
                logger.warning("Texto vazio, não gerando áudio")
                return None
            
            # Limpar texto
            clean_text = text.replace('\n', ' ').replace('\r', ' ')
            clean_text = ' '.join(clean_text.split())
            
            logger.info(f"Tentando gerar áudio para texto: '{clean_text[:100]}...'")
            
            if len(clean_text.strip()) < 3:
                logger.warning(f"Texto muito curto ({len(clean_text)} chars), não gerando áudio")
                return None
            
            # Método 1: Gerar áudio com gTTS (usando 'pt' para português)
            try:
                logger.info("Tentando gTTS...")
                tts = gTTS(text=clean_text, lang='pt', slow=False, tld='com.br')
                
                # Salvar em arquivo temporário
                audio_file = self.temp_dir / f"slide_audio_{int(time.time())}.mp3"
                logger.info(f"Salvando áudio gTTS em: {audio_file}")
                tts.save(str(audio_file))
                
                if audio_file.exists() and audio_file.stat().st_size > 0:
                    logger.info("✓ Áudio gTTS gerado com sucesso!")
                    return audio_file
                else:
                    logger.error("Arquivo de áudio gTTS vazio ou não criado")
                    
            except Exception as e:
                logger.error(f"Erro ao gerar áudio com gTTS: {e}")
            
            # Método 2: Fallback para espeak se gTTS falhar
            try:
                logger.info("Tentando espeak como fallback...")
                audio_file = self.temp_dir / f"slide_audio_espeak_{int(time.time())}.wav"
                
                # Usar diferentes variantes de português brasileiro no espeak
                espeak_variants = ['pt-br', 'pt+f3', 'pt']
                
                for variant in espeak_variants:
                    try:
                        logger.info(f"Tentando espeak com variante: {variant}")
                        cmd = ['espeak', '-v', variant, '-s', '150', '-w', str(audio_file), clean_text]
                        result = subprocess.run(cmd, check=True, timeout=15, 
                                              capture_output=True, text=True)
                        
                        if audio_file.exists() and audio_file.stat().st_size > 0:
                            logger.info(f"✓ Áudio espeak gerado com variante {variant}!")
                            return audio_file
                        else:
                            logger.warning(f"Arquivo espeak vazio com variante {variant}")
                            
                    except subprocess.CalledProcessError as e:
                        logger.warning(f"Espeak falhou com variante {variant}: {e}")
                        continue
                    except Exception as e:
                        logger.warning(f"Erro com espeak variante {variant}: {e}")
                        continue
                
                # Se todas as variantes falharam, tentar sem especificar idioma
                try:
                    logger.info("Tentando espeak sem especificar idioma...")
                    cmd = ['espeak', '-s', '150', '-w', str(audio_file), clean_text]
                    subprocess.run(cmd, check=True, timeout=15)
                    
                    if audio_file.exists() and audio_file.stat().st_size > 0:
                        logger.info("✓ Áudio espeak gerado sem idioma específico!")
                        return audio_file
                        
                except Exception as e:
                    logger.error(f"Espeak sem idioma também falhou: {e}")
                
            except Exception as e2:
                logger.error(f"Erro geral com espeak: {e2}")
            
            # Método 3: Último fallback - usar festival
            try:
                logger.info("Tentando festival como último recurso...")
                audio_file = self.temp_dir / f"slide_audio_festival_{int(time.time())}.wav"
                
                # Criar arquivo de texto temporário para o festival
                text_file = self.temp_dir / f"temp_text_{int(time.time())}.txt"
                text_file.write_text(clean_text)
                
                cmd = ['text2wave', str(text_file), '-o', str(audio_file)]
                subprocess.run(cmd, check=True, timeout=20)
                
                text_file.unlink()  # Limpar arquivo de texto
                
                if audio_file.exists() and audio_file.stat().st_size > 0:
                    logger.info("✓ Áudio festival gerado!")
                    return audio_file
                else:
                    logger.error("Arquivo festival vazio")
                    
            except Exception as e3:
                logger.error(f"Erro com festival: {e3}")
            
            # Se chegou até aqui, todos os métodos falharam
            logger.error("❌ TODOS os métodos de TTS falharam!")
            return None
            
        except Exception as e:
            logger.error(f"Erro geral ao gerar áudio: {e}")
            return None

    def play_audio(self, audio_file):
        """Reproduz o arquivo de áudio"""
        try:
            logger.info(f"Tentando reproduzir áudio: {audio_file}")
            
            if not audio_file.exists():
                logger.error(f"Arquivo de áudio não existe: {audio_file}")
                return
            
            file_size = audio_file.stat().st_size
            logger.info(f"Tamanho do arquivo: {file_size} bytes")
            
            if file_size == 0:
                logger.error("Arquivo de áudio vazio!")
                return
            
            # Método 1: Pygame
            try:
                logger.info("Tentando reproduzir com pygame...")
                pygame.mixer.music.load(str(audio_file))
                pygame.mixer.music.play()
                
                # Aguardar finalização
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                logger.info("✓ Áudio reproduzido com pygame!")
                return
                
            except Exception as e:
                logger.error(f"Erro com pygame: {e}")
            
            # Método 2: Fallback para aplay
            try:
                logger.info("Tentando reproduzir com aplay...")
                result = subprocess.run(['aplay', str(audio_file)], 
                                      check=True, timeout=30,
                                      capture_output=True, text=True)
                logger.info("✓ Áudio reproduzido com aplay!")
                return
                
            except subprocess.CalledProcessError as e:
                logger.error(f"Erro com aplay: {e}")
                if e.stderr:
                    logger.error(f"Stderr aplay: {e.stderr}")
            except FileNotFoundError:
                logger.error("aplay não encontrado")
            
            # Método 3: Fallback para paplay
            try:
                logger.info("Tentando reproduzir com paplay...")
                subprocess.run(['paplay', str(audio_file)], check=True, timeout=30)
                logger.info("✓ Áudio reproduzido com paplay!")
                return
                
            except subprocess.CalledProcessError as e:
                logger.error(f"Erro com paplay: {e}")
            except FileNotFoundError:
                logger.error("paplay não encontrado")
            
            # Método 4: Fallback para mpg123 (para MP3)
            if audio_file.suffix.lower() == '.mp3':
                try:
                    logger.info("Tentando reproduzir MP3 com mpg123...")
                    subprocess.run(['mpg123', str(audio_file)], check=True, timeout=30)
                    logger.info("✓ Áudio reproduzido com mpg123!")
                    return
                    
                except subprocess.CalledProcessError as e:
                    logger.error(f"Erro com mpg123: {e}")
                except FileNotFoundError:
                    logger.error("mpg123 não encontrado")
            
            logger.error("❌ Falha ao reproduzir áudio com todos os métodos!")
            
        except Exception as e:
            logger.error(f"Erro geral ao reproduzir áudio: {e}")
            import traceback
            logger.error(traceback.format_exc())

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

    def test_audio_system(self):
        """Testa se o sistema de áudio está funcionando"""
        logger.info("🔊 Testando sistema de áudio...")
        test_text = "Teste de áudio. Sistema funcionando."
        
        audio_file = self.generate_audio(test_text)
        if audio_file:
            logger.info("Teste de áudio gerado, reproduzindo...")
            self.play_audio(audio_file)
            
            # Limpeza
            try:
                audio_file.unlink()
            except:
                pass
            return True
        else:
            logger.error("Falha no teste de áudio")
            return False

    def start_monitoring(self):
        """Inicia o monitoramento"""
        logger.info("Iniciando monitoramento do LibreOffice Impress...")
        
        # Testar sistema de áudio primeiro
        if not self.test_audio_system():
            logger.error("Sistema de áudio não está funcionando. Verifique as dependências.")
            print("\n❌ ERRO: Sistema de áudio não funciona!")
            print("Tente instalar:")
            print("sudo apt install pulseaudio-utils alsa-utils mpg123")
            return
        
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
                        logger.info("Gerando áudio do conteúdo extraído...")
                        audio_file = self.generate_audio(content)
                        
                        if audio_file:
                            logger.info("Áudio gerado com sucesso, adicionando à fila...")
                            # Adicionar à fila de reprodução
                            self.audio_queue.put(audio_file)
                        else:
                            logger.error("❌ Não foi possível gerar áudio")
                            # Tentar áudio de teste para verificar se o sistema funciona
                            logger.info("Testando sistema de áudio com mensagem simples...")
                            test_audio = self.generate_audio("Novo slide detectado")
                            if test_audio:
                                logger.info("Sistema de áudio funcionando, problema pode ser com o texto extraído")
                                self.audio_queue.put(test_audio)
                
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
    required_tools = ['xdotool']  # Ferramentas essenciais
    optional_tools = ['wmctrl', 'xclip']  # Ferramentas opcionais
    
    missing_required = []
    missing_optional = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, timeout=3)
        except FileNotFoundError:
            missing_required.append(tool)
    
    for tool in optional_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, timeout=3)
        except FileNotFoundError:
            missing_optional.append(tool)
    
    if missing_required:
        print(f"❌ ERRO: Ferramentas obrigatórias não encontradas: {', '.join(missing_required)}")
        print("Instale com: sudo apt install xdotool")
        print("O script não funcionará sem essas ferramentas.")
        return
    
    if missing_optional:
        print(f"⚠️  AVISO: Ferramentas opcionais não encontradas: {', '.join(missing_optional)}")
        print("Instale com: sudo apt install wmctrl xclip")
        print("O script funcionará, mas com funcionalidade reduzida.")
        print()
    
    # Verificar se tesseract está disponível
    try:
        subprocess.run(['tesseract', '--version'], capture_output=True, timeout=3)
        print("✓ Tesseract OCR encontrado")
    except FileNotFoundError:
        print("⚠️  AVISO: Tesseract OCR não encontrado")
        print("Para melhor extração de texto, instale com:")
        print("sudo apt install tesseract-ocr tesseract-ocr-por")
        print()
    
    print("💡 DICAS DE USO:")
    print("1. Abra uma apresentação no LibreOffice Impress")
    print("2. Entre no modo apresentação (F5)")
    print("3. Para melhor extração de texto, você pode:")
    print("   - Deixar o script detectar automaticamente (OCR)")
    print("   - Ou selecionar todo o texto do slide (Ctrl+A) e copiar (Ctrl+C)")
    print()
    print("Pressione Ctrl+C para parar o monitoramento")
    print("=" * 60)
    
    monitor = ImpressMonitor()
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()