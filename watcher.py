#!/usr/bin/env python3
"""
Watcher.py - Monitor inteligente de logs y respuesta automática a errores
Analiza logs en tiempo real y proporciona feedback automático
"""

import os
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path
import threading
import queue
import re

class LogWatcher:
    """Monitor inteligente de logs con análisis de patrones"""
    
    def __init__(self, script_dir):
        self.script_dir = Path(script_dir)
        self.log_dir = self.script_dir / "log"
        self.config_dir = self.script_dir / "config"
        
        # Archivos de monitoreo
        self.execution_log = self.log_dir / "execution_history.log"
        self.decision_log = self.log_dir / "decision_history.json"
        self.context_log = self.log_dir / "context_memory.json"
        self.error_patterns_file = self.config_dir / "error_patterns.json"
        self.feedback_log = self.log_dir / "feedback_responses.log"
        
        # Crear directorios
        self.log_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        
        # Queue para comunicación entre threads
        self.feedback_queue = queue.Queue()
        
        # Patrones de error comunes
        self.setup_error_patterns()
        
        print("🔍 Monitor de logs inicializado")
    
    def setup_error_patterns(self):
        """Configurar patrones de error y respuestas automáticas"""
        error_patterns = {
            "network_errors": {
                "patterns": [
                    r"Network is unreachable",
                    r"Connection refused",
                    r"No route to host",
                    r"Timeout"
                ],
                "response": "Error de conectividad detectado. Verificando configuración de red...",
                "auto_action": "network_check"
            },
            "permission_errors": {
                "patterns": [
                    r"Permission denied",
                    r"Operation not permitted",
                    r"Access denied"
                ],
                "response": "Error de permisos. Considerando elevación de privilegios...",
                "auto_action": "permission_fix"
            },
            "command_not_found": {
                "patterns": [
                    r"command not found",
                    r"No such file or directory",
                    r"not found in PATH"
                ],
                "response": "Comando no encontrado. Buscando alternativas...",
                "auto_action": "command_suggest"
            },
            "service_errors": {
                "patterns": [
                    r"Failed to start",
                    r"Service unavailable",
                    r"Connection to .* failed"
                ],
                "response": "Error de servicio detectado. Analizando estado del sistema...",
                "auto_action": "service_check"
            },
            "syntax_errors": {
                "patterns": [
                    r"Syntax error",
                    r"Invalid syntax",
                    r"Parse error"
                ],
                "response": "Error de sintaxis detectado. Sugiriendo corrección...",
                "auto_action": "syntax_help"
            }
        }
        
        with open(self.error_patterns_file, 'w') as f:
            json.dump(error_patterns, f, indent=2)
    
    def analyze_log_entry(self, log_line):
        """Analizar entrada de log para detectar patrones"""
        with open(self.error_patterns_file, 'r') as f:
            patterns = json.load(f)
        
        for error_type, config in patterns.items():
            for pattern in config["patterns"]:
                if re.search(pattern, log_line, re.IGNORECASE):
                    return {
                        "error_type": error_type,
                        "response": config["response"],
                        "auto_action": config["auto_action"],
                        "matched_pattern": pattern
                    }
        
        return None
    
    def execute_auto_action(self, action_type, context):
        """Ejecutar acción automática basada en el error detectado"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        actions = {
            "network_check": [
                "ping -c 3 8.8.8.8",
                "ip route show",
                "systemctl status NetworkManager"
            ],
            "permission_fix": [
                "whoami",
                "id",
                "ls -la"
            ],
            "command_suggest": [
                "which python3 python pip3 pip",
                "apt list --installed | grep -i tool",
                "dpkg -l | grep -i security"
            ],
            "service_check": [
                "systemctl --failed",
                "systemctl status",
                "journalctl -n 10"
            ],
            "syntax_help": [
                "echo 'Verificando sintaxis de comando anterior'"
            ]
        }
        
        if action_type in actions:
            print(f"🔧 Ejecutando acción automática: {action_type}")
            
            for cmd in actions[action_type]:
                try:
                    result = subprocess.run(
                        cmd, 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=30
                    )
                    
                    self.log_feedback(timestamp, action_type, cmd, result.returncode, result.stdout)
                    
                except subprocess.TimeoutExpired:
                    self.log_feedback(timestamp, action_type, cmd, -1, "Timeout")
                except Exception as e:
                    self.log_feedback(timestamp, action_type, cmd, -1, str(e))
    
    def log_feedback(self, timestamp, action_type, command, exit_code, output):
        """Registrar feedback de acciones automáticas"""
        feedback_entry = f"[{timestamp}] ACTION: {action_type} | CMD: {command} | EXIT: {exit_code}\n"
        
        with open(self.feedback_log, 'a') as f:
            f.write(feedback_entry)
            if output:
                f.write(f"[{timestamp}] OUTPUT: {output[:200]}...\n")
    
    def provide_intelligent_suggestion(self, error_analysis, log_context):
        """Proporcionar sugerencias inteligentes basadas en contexto"""
        suggestions = {
            "network_errors": [
                "Verificar conectividad: ping 8.8.8.8",
                "Revisar configuración de red: ip addr show",
                "Comprobar firewall: iptables -L"
            ],
            "permission_errors": [
                "Ejecutar con sudo si es necesario",
                "Verificar permisos del directorio: ls -la",
                "Cambiar propietario si corresponde: chown"
            ],
            "command_not_found": [
                "Instalar herramienta: apt install <tool>",
                "Verificar PATH: echo $PATH",
                "Buscar alternativas: apt search <keyword>"
            ]
        }
        
        error_type = error_analysis["error_type"]
        if error_type in suggestions:
            print(f"💡 Sugerencias para {error_type}:")
            for suggestion in suggestions[error_type]:
                print(f"   • {suggestion}")
    
    def monitor_execution_log(self):
        """Monitorear archivo de log de ejecución en tiempo real"""
        print("👁️ Iniciando monitoreo de logs de ejecución...")
        
        if not self.execution_log.exists():
            self.execution_log.touch()
        
        # Seguir el archivo como tail -f
        with open(self.execution_log, 'r') as f:
            # Ir al final del archivo
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    # Analizar nueva línea de log
                    analysis = self.analyze_log_entry(line)
                    if analysis:
                        print(f"🚨 Error detectado: {analysis['error_type']}")
                        print(f"💬 Respuesta: {analysis['response']}")
                        
                        # Ejecutar acción automática
                        self.execute_auto_action(analysis['auto_action'], line)
                        
                        # Proporcionar sugerencias
                        self.provide_intelligent_suggestion(analysis, line)
                        
                        # Enviar a queue para TTS si está habilitado
                        self.feedback_queue.put(analysis['response'])
                else:
                    time.sleep(0.1)
    
    def tts_feedback_worker(self):
        """Worker thread para feedback TTS"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # Velocidad de habla
            
            print("🔊 TTS feedback habilitado")
            
            while True:
                try:
                    message = self.feedback_queue.get(timeout=1)
                    if message:
                        print(f"🗣️ TTS: {message}")
                        engine.say(message)
                        engine.runAndWait()
                    self.feedback_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"❌ Error TTS: {e}")
                    
        except ImportError:
            print("⚠️ pyttsx3 no disponible - TTS deshabilitado")
    
    def start_monitoring(self, enable_tts=True):
        """Iniciar monitoreo completo"""
        print("🚀 Iniciando sistema de monitoreo inteligente...")
        
        # Thread para monitoreo de logs
        log_thread = threading.Thread(target=self.monitor_execution_log, daemon=True)
        log_thread.start()
        
        # Thread para TTS feedback si está habilitado
        if enable_tts:
            tts_thread = threading.Thread(target=self.tts_feedback_worker, daemon=True)
            tts_thread.start()
        
        try:
            # Mantener el programa ejecutándose
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo monitoreo...")

def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) > 1:
        script_dir = sys.argv[1]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Crear e iniciar watcher
    watcher = LogWatcher(script_dir)
    
    # Iniciar monitoreo
    watcher.start_monitoring(enable_tts=True)

if __name__ == "__main__":
    main()