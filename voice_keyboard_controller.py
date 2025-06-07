#!/usr/bin/env python3
"""
Voice & Keyboard Controller - Control de voz y teclado virtual
Sistema de gestión de entrada por voz y teclado virtual español
"""

import os
import json
import threading
import time
from datetime import datetime
from pathlib import Path

# Estado global del sistema
VOICE_STATE = {
    "enabled": True,
    "listening": False,
    "last_command": "",
    "mode": "voice"  # voice o keyboard
}

KEYBOARD_STATE = {
    "layout": "qwerty_es",
    "shift_pressed": False,
    "caps_lock": False,
    "current_input": ""
}

class VoiceKeyboardController:
    """Controlador de voz y teclado virtual"""
    
    def __init__(self, agent_dir):
        self.agent_dir = Path(agent_dir)
        self.log_dir = self.agent_dir / "log"
        self.voice_log = self.log_dir / "voice_commands.log"
        self.keyboard_log = self.log_dir / "keyboard_input.log"
        
        # Crear directorios
        self.log_dir.mkdir(exist_ok=True)
        
        print("🎤 Controlador de voz y teclado iniciado")
    
    def process_voice_command(self, command_text):
        """Procesar comando de voz específico"""
        command_lower = command_text.lower().strip()
        
        # Comandos de control del sistema
        if "mano a teclado" in command_lower:
            return self.switch_to_keyboard_mode()
        elif "voz a teclado" in command_lower:
            return self.switch_to_voice_mode()
        elif "activar voz" in command_lower:
            return self.enable_voice()
        elif "desactivar voz" in command_lower:
            return self.disable_voice()
        
        # Comandos de navegación
        elif "ventana principal" in command_lower:
            return self.send_tmux_command("select-window -t 0")
        elif "ventana monitor" in command_lower:
            return self.send_tmux_command("select-window -t 1")
        elif "ventana herramientas" in command_lower:
            return self.send_tmux_command("select-window -t 2")
        elif "ventana visual" in command_lower:
            return self.send_tmux_command("select-window -t 3")
        elif "mostrar teclado" in command_lower:
            return self.send_tmux_command("select-window -t keyboard")
        
        # Comandos de NetHunter
        elif "escanear red" in command_lower:
            return self.execute_nethunter_command("nmap -sn 192.168.1.0/24")
        elif "escanear puertos" in command_lower:
            return self.execute_nethunter_command("nmap -sS TARGET_IP")
        elif "buscar vulnerabilidades" in command_lower:
            return self.execute_nethunter_command("nmap --script vuln TARGET_IP")
        
        # Comando general - enviar al brain
        else:
            return self.send_to_brain(command_text)
    
    def switch_to_keyboard_mode(self):
        """Cambiar a modo teclado"""
        global VOICE_STATE
        VOICE_STATE["enabled"] = False
        VOICE_STATE["mode"] = "keyboard"
        
        self.log_action("voice_command", "Switched to keyboard mode")
        return {
            "action": "mode_switch",
            "mode": "keyboard",
            "message": "🖐️ Modo teclado activado - Entrada de voz desactivada",
            "tts_response": "Modo teclado activado"
        }
    
    def switch_to_voice_mode(self):
        """Cambiar a modo voz"""
        global VOICE_STATE
        VOICE_STATE["enabled"] = True
        VOICE_STATE["mode"] = "voice"
        
        self.log_action("voice_command", "Switched to voice mode")
        return {
            "action": "mode_switch", 
            "mode": "voice",
            "message": "🎤 Modo voz activado - Entrada de teclado desactivada",
            "tts_response": "Modo voz reactivado"
        }
    
    def enable_voice(self):
        """Activar sistema de voz"""
        global VOICE_STATE
        VOICE_STATE["enabled"] = True
        return {"action": "voice_enabled", "message": "🎤 Sistema de voz activado"}
    
    def disable_voice(self):
        """Desactivar sistema de voz"""
        global VOICE_STATE
        VOICE_STATE["enabled"] = False
        return {"action": "voice_disabled", "message": "🔇 Sistema de voz desactivado"}
    
    def send_tmux_command(self, tmux_cmd):
        """Enviar comando a tmux"""
        try:
            import subprocess
            session_name = "nethunter-enhanced"
            full_cmd = f"tmux {tmux_cmd} -t {session_name}"
            
            result = subprocess.run(full_cmd.split(), capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_action("tmux_command", tmux_cmd)
                return {"action": "tmux_success", "command": tmux_cmd}
            else:
                return {"action": "tmux_error", "error": result.stderr}
                
        except Exception as e:
            return {"action": "tmux_error", "error": str(e)}
    
    def execute_nethunter_command(self, command):
        """Ejecutar comando de NetHunter"""
        self.log_action("nethunter_command", command)
        
        # Enviar al brain para procesamiento
        brain_result = self.send_to_brain(f"ejecutar comando: {command}")
        
        return {
            "action": "nethunter_command",
            "command": command,
            "brain_response": brain_result,
            "message": f"🛡️ Ejecutando: {command}"
        }
    
    def send_to_brain(self, text):
        """Enviar texto al brain para procesamiento"""
        try:
            import subprocess
            brain_script = self.agent_dir / "brain.sh"
            
            if brain_script.exists():
                result = subprocess.run(
                    [str(brain_script), text, "voice_input"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.log_action("brain_processing", f"Input: {text}")
                    return {
                        "action": "brain_success",
                        "input": text,
                        "output": result.stdout.strip(),
                        "message": f"🧠 Procesado: {result.stdout.strip()}"
                    }
                else:
                    return {"action": "brain_error", "error": result.stderr}
            else:
                return {"action": "brain_error", "error": "brain.sh not found"}
                
        except Exception as e:
            return {"action": "brain_error", "error": str(e)}
    
    def process_keyboard_input(self, key_input):
        """Procesar entrada de teclado virtual"""
        global KEYBOARD_STATE
        
        # Teclas especiales
        if key_input == "SHIFT":
            KEYBOARD_STATE["shift_pressed"] = not KEYBOARD_STATE["shift_pressed"]
            return {"action": "key_modifier", "key": "shift", "state": KEYBOARD_STATE["shift_pressed"]}
        
        elif key_input == "CAPS":
            KEYBOARD_STATE["caps_lock"] = not KEYBOARD_STATE["caps_lock"]
            return {"action": "key_modifier", "key": "caps", "state": KEYBOARD_STATE["caps_lock"]}
        
        elif key_input == "BACKSPACE":
            if KEYBOARD_STATE["current_input"]:
                KEYBOARD_STATE["current_input"] = KEYBOARD_STATE["current_input"][:-1]
            return {"action": "key_backspace", "current_text": KEYBOARD_STATE["current_input"]}
        
        elif key_input == "ENTER":
            text = KEYBOARD_STATE["current_input"]
            KEYBOARD_STATE["current_input"] = ""
            
            # Procesar el texto como comando
            result = self.send_to_brain(text)
            self.log_action("keyboard_input", text)
            
            return {
                "action": "key_enter",
                "text_submitted": text,
                "brain_response": result
            }
        
        elif key_input == "SPACE":
            KEYBOARD_STATE["current_input"] += " "
            return {"action": "key_space", "current_text": KEYBOARD_STATE["current_input"]}
        
        # Caracteres normales
        else:
            # Aplicar modificadores
            char = key_input
            if KEYBOARD_STATE["shift_pressed"] or KEYBOARD_STATE["caps_lock"]:
                char = char.upper()
            
            KEYBOARD_STATE["current_input"] += char
            
            # Reset shift después de uso
            if KEYBOARD_STATE["shift_pressed"]:
                KEYBOARD_STATE["shift_pressed"] = False
            
            return {"action": "key_char", "char": char, "current_text": KEYBOARD_STATE["current_input"]}
    
    def get_spanish_keyboard_layout(self):
        """Obtener layout del teclado español"""
        return {
            "row_1": ["1!", "2\"", "3·", "4$", "5%", "6&", "7/", "8(", "9)", "0=", "'?", "¡¿"],
            "row_2": ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "`^", "+*"],
            "row_3": ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ñ", "´¨", "ç"],
            "row_4": ["z", "x", "c", "v", "b", "n", "m", ",;", ".:", "-_"],
            "symbols": ["→", "←", "↑", "↓", "⇒", "⇐", "⇑", "⇓", "∞", "≈", "≠", "≤", "≥", "±"],
            "emojis": ["😀", "😂", "🤔", "😎", "🔥", "💯", "⚡", "🚀", "🎯", "🛡️", "🔍", "💻", "📱", "🌐", "🔧", "⚙️"]
        }
    
    def log_action(self, action_type, details):
        """Registrar acción en log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"[{timestamp}] {action_type.upper()}: {details}\n"
        
        if action_type.startswith("voice"):
            log_file = self.voice_log
        else:
            log_file = self.keyboard_log
        
        try:
            with open(log_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️ Error logging: {e}")
    
    def get_system_status(self):
        """Obtener estado actual del sistema"""
        return {
            "voice_enabled": VOICE_STATE["enabled"],
            "current_mode": VOICE_STATE["mode"],
            "voice_listening": VOICE_STATE["listening"],
            "keyboard_layout": KEYBOARD_STATE["layout"],
            "caps_lock": KEYBOARD_STATE["caps_lock"],
            "current_input": KEYBOARD_STATE["current_input"],
            "timestamp": datetime.now().isoformat()
        }
    
    def create_keyboard_display(self):
        """Crear representación visual del teclado"""
        layout = self.get_spanish_keyboard_layout()
        
        keyboard_display = []
        keyboard_display.append("⌨️ TECLADO VIRTUAL ESPAÑOL - QWERTY")
        keyboard_display.append("═" * 60)
        
        # Fila numérica
        row1 = " ".join([f"[{key}]" for key in layout["row_1"]])
        keyboard_display.append(f"│ {row1} [⌫] │")
        
        # Fila QWERTY
        row2 = " ".join([f"[{key.upper()}]" for key in layout["row_2"]])
        keyboard_display.append(f"│ {row2} [⏎] │")
        
        # Fila ASDF
        row3 = " ".join([f"[{key.upper()}]" for key in layout["row_3"]])
        keyboard_display.append(f"│ [🔒] {row3}     │")
        
        # Fila ZXCV
        row4 = " ".join([f"[{key.upper()}]" for key in layout["row_4"]])
        keyboard_display.append(f"│ [⇧] {row4}   [⇧] │")
        
        # Barra espaciadora
        keyboard_display.append("│ [Ctrl] [🌐] [Alt]   [███ ESPACIO ███]   [Alt] [🌐] [Ctrl] │")
        keyboard_display.append("═" * 60)
        
        # Estado actual
        mode_indicator = "🎤 VOZ" if VOICE_STATE["enabled"] else "🖐️ TECLADO"
        caps_indicator = "🔒 CAPS" if KEYBOARD_STATE["caps_lock"] else ""
        
        keyboard_display.append(f"Estado: {mode_indicator} {caps_indicator}")
        keyboard_display.append(f"Entrada: {KEYBOARD_STATE['current_input']}")
        
        return "\n".join(keyboard_display)

def main():
    """Función principal para testing"""
    import sys
    
    agent_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)
    controller = VoiceKeyboardController(agent_dir)
    
    print("🎤 Controlador de voz y teclado iniciado")
    print("Comandos de prueba:")
    print("• 'mano a teclado' - Cambiar a modo teclado")
    print("• 'voz a teclado' - Cambiar a modo voz")
    print("• 'escanear red' - Comando NetHunter")
    print("• 'ventana principal' - Navegación")
    
    # Mostrar teclado virtual
    print("\n" + controller.create_keyboard_display())
    
    # Test de comandos
    test_commands = [
        "mano a teclado",
        "escanear red local", 
        "voz a teclado",
        "ventana monitor"
    ]
    
    for cmd in test_commands:
        print(f"\n🧪 Testing: {cmd}")
        result = controller.process_voice_command(cmd)
        print(f"   Resultado: {result}")

if __name__ == "__main__":
    main()