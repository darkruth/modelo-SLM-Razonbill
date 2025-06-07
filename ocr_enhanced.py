#!/usr/bin/env python3
"""
OCR Enhanced - Sistema de captura y análisis visual integrado
Integración con Núcleo C.A- Razonbilstro para análisis inteligente
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Añadir directorio padre para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ pytesseract/PIL no disponibles - usando captura básica")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 no disponible - TTS deshabilitado")

class EnhancedOCR:
    """Sistema OCR mejorado con integración al Núcleo Razonbilstro"""
    
    def __init__(self, agent_dir):
        self.agent_dir = Path(agent_dir)
        self.log_dir = self.agent_dir / "log"
        self.config_dir = self.agent_dir / "config"
        self.ocr_log = self.log_dir / "ocr_analysis.log"
        
        # Crear directorios
        self.log_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        
        # Configurar TTS si está disponible
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.8)
            except Exception as e:
                print(f"⚠️ Error inicializando TTS: {e}")
                self.tts_engine = None
    
    def capture_screen(self, output_path="/tmp/agent_screen_capture.png"):
        """Capturar pantalla usando imagemagick"""
        try:
            # Usar import de ImageMagick para captura
            result = subprocess.run(
                ["import", "-window", "root", output_path],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return output_path
            else:
                print(f"❌ Error en captura: {result.stderr.decode()}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout en captura de pantalla")
            return None
        except FileNotFoundError:
            print("❌ ImageMagick no encontrado - instalar: apt install imagemagick")
            return None
        except Exception as e:
            print(f"❌ Error inesperado en captura: {e}")
            return None
    
    def extract_text(self, image_path):
        """Extraer texto de imagen usando OCR"""
        if not TESSERACT_AVAILABLE:
            print("❌ Tesseract no disponible - instalar: apt install tesseract-ocr python3-pytesseract")
            return None
        
        try:
            # Verificar que el archivo existe
            if not os.path.exists(image_path):
                print(f"❌ Archivo no encontrado: {image_path}")
                return None
            
            # Abrir imagen y extraer texto
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='eng+spa')
            
            return text.strip() if text else None
            
        except Exception as e:
            print(f"❌ Error en OCR: {e}")
            return None
    
    def analyze_with_nucleus(self, text):
        """Analizar texto con Núcleo C.A- Razonbilstro"""
        if not text:
            return None
        
        try:
            # Llamar al brain.sh para análisis
            brain_script = self.agent_dir / "brain.sh"
            
            if not brain_script.exists():
                print("❌ brain.sh no encontrado")
                return None
            
            result = subprocess.run(
                [str(brain_script), text, "ocr_visual_context"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"❌ Error en análisis: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout en análisis")
            return None
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            return None
    
    def speak_response(self, text):
        """Convertir texto a voz"""
        if not self.tts_engine or not text:
            return False
        
        try:
            # Limpiar texto para TTS (máximo 200 caracteres)
            clean_text = text[:200] if len(text) > 200 else text
            clean_text = clean_text.replace('\n', '. ')
            
            print(f"🗣️ TTS: {clean_text}")
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"❌ Error TTS: {e}")
            return False
    
    def log_analysis(self, image_path, extracted_text, nucleus_result):
        """Registrar análisis en log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = {
            "timestamp": timestamp,
            "image_path": str(image_path),
            "text_extracted": extracted_text[:100] if extracted_text else None,
            "nucleus_analysis": nucleus_result[:100] if nucleus_result else None,
            "text_length": len(extracted_text) if extracted_text else 0
        }
        
        try:
            with open(self.ocr_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Error logging: {e}")
    
    def process_visual_input(self, speak_result=True):
        """Proceso completo: captura → OCR → análisis → TTS"""
        print("📸 Iniciando análisis visual completo...")
        
        # 1. Capturar pantalla
        image_path = self.capture_screen()
        if not image_path:
            return None
        
        print(f"✅ Captura guardada: {image_path}")
        
        # 2. Extraer texto
        extracted_text = self.extract_text(image_path)
        if not extracted_text:
            print("❌ No se detectó texto en la imagen")
            return None
        
        print(f"📝 Texto extraído: {len(extracted_text)} caracteres")
        print(f"📄 Vista previa: {extracted_text[:100]}...")
        
        # 3. Analizar con Núcleo Razonbilstro
        print("🧠 Analizando con Núcleo C.A- Razonbilstro...")
        nucleus_result = self.analyze_with_nucleus(extracted_text)
        
        if nucleus_result:
            print(f"💡 Análisis del núcleo: {nucleus_result}")
            
            # 4. TTS si está habilitado
            if speak_result:
                self.speak_response(nucleus_result)
        else:
            print("❌ No se pudo analizar con el núcleo")
        
        # 5. Log del análisis
        self.log_analysis(image_path, extracted_text, nucleus_result)
        
        return {
            "image_path": image_path,
            "extracted_text": extracted_text,
            "nucleus_analysis": nucleus_result
        }
    
    def continuous_monitoring(self, interval=5):
        """Monitoreo continuo de cambios en pantalla"""
        print(f"👁️ Iniciando monitoreo continuo (cada {interval}s)")
        print("Presiona Ctrl+C para detener")
        
        import time
        previous_text = ""
        
        try:
            while True:
                result = self.process_visual_input(speak_result=False)
                
                if result and result["extracted_text"]:
                    current_text = result["extracted_text"]
                    
                    # Solo procesar si hay cambios significativos
                    if len(current_text) > 50 and current_text != previous_text:
                        print(f"🔄 Cambio detectado - analizando...")
                        if result["nucleus_analysis"]:
                            self.speak_response(result["nucleus_analysis"])
                        previous_text = current_text
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoreo detenido")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OCR Enhanced para NetHunter Agent")
    parser.add_argument("--mode", choices=["single", "monitor"], default="single",
                      help="Modo de operación")
    parser.add_argument("--interval", type=int, default=5,
                      help="Intervalo para monitoreo (segundos)")
    parser.add_argument("--no-tts", action="store_true",
                      help="Desactivar TTS")
    parser.add_argument("--agent-dir", default=None,
                      help="Directorio del agente")
    
    args = parser.parse_args()
    
    # Determinar directorio del agente
    if args.agent_dir:
        agent_dir = Path(args.agent_dir)
    else:
        agent_dir = Path(__file__).parent.parent
    
    # Crear instancia OCR
    ocr = EnhancedOCR(agent_dir)
    
    # Ejecutar según modo
    if args.mode == "single":
        result = ocr.process_visual_input(speak_result=not args.no_tts)
        if result:
            print("✅ Análisis completado")
        else:
            print("❌ Error en análisis")
    
    elif args.mode == "monitor":
        ocr.continuous_monitoring(interval=args.interval)

if __name__ == "__main__":
    main()