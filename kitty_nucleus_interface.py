#!/usr/bin/env python3
"""
Interfaz CLI Multiventanas Kitty integrada con Núcleo C.A- Razonbilstro
Sistema de terminal avanzado con diseño Dracula Xeon
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

class KittyNucleusInterface:
    """Interfaz Kitty multiventanas integrada con el núcleo"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "kitty"
        self.nucleus_dir = Path("gym_razonbilstro")
        self.interface_active = False
        
        print("🖥️ Interfaz Kitty-Núcleo inicializándose")
        
    def setup_complete_interface(self):
        """Configurar interfaz completa Kitty con integración del núcleo"""
        print("\n🎨 CONFIGURANDO INTERFAZ KITTY MULTIVENTANAS")
        print("="*50)
        
        # Crear configuración base de Kitty
        self._create_kitty_config()
        
        # Crear scripts de integración con el núcleo
        self._create_nucleus_integration_scripts()
        
        # Configurar layouts multiventana
        self._setup_multiwindow_layouts()
        
        # Crear archivo de inicio automático
        self._create_autostart_script()
        
        print(f"\n✅ INTERFAZ KITTY CONFIGURADA COMPLETAMENTE")
        
    def _create_kitty_config(self):
        """Crear configuración principal de Kitty"""
        print("📝 Creando configuración principal de Kitty...")
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        kitty_config = """# Configuración Kitty - Núcleo C.A- Razonbilstro
# Tema Dracula Xeon optimizado para ciberseguridad

# === FUENTES Y TEXTO ===
font_family      FiraCode Nerd Font Mono
bold_font        FiraCode Nerd Font Mono Bold
italic_font      FiraCode Nerd Font Mono Italic
bold_italic_font FiraCode Nerd Font Mono Bold Italic
font_size 11.0

# === TEMA RAZONBILSTRO (BASADO EN IMAGEN ORIGINAL) ===
foreground            #00ffcc
background            #0a0a0a
selection_foreground  #000000
selection_background  #00ffcc
cursor                #00ffcc
cursor_text_color     #000000

# Colores basados en la imagen del diseño
color0  #000000
color1  #ff6b6b
color2  #00ffcc
color3  #ffcc00
color4  #6bcfff
color5  #cc00ff
color6  #00ffcc
color7  #cccccc

# Colores brillantes - esquema cyan/verde como en la imagen
color8  #333333
color9  #ff8888
color10 #33ffdd
color11 #ffdd33
color12 #88ddff
color13 #dd33ff
color14 #33ffdd
color15 #ffffff

# === CONFIGURACIÓN DE VENTANAS ===
window_padding_width 8
window_margin_width 2
single_window_margin_width 0
window_border_width 1pt
draw_minimal_borders yes
window_margin_width 0
single_window_margin_width -1

# === CONFIGURACIÓN DE PESTAÑAS (ESTILO RAZONBILSTRO) ===
tab_bar_edge bottom
tab_bar_style powerline
tab_powerline_style slanted
tab_title_template "🔸 {title} 🔸"
active_tab_foreground   #000000
active_tab_background   #00ffcc
inactive_tab_foreground #00ffcc
inactive_tab_background #1a1a1a
tab_bar_background      #0a0a0a

# === TRANSPARENCIA Y EFECTOS ===
background_opacity 0.95
dynamic_background_opacity yes

# === CONFIGURACIONES ADICIONALES ===
enable_audio_bell no
visual_bell_duration 0.0
confirm_os_window_close 0
shell_integration enabled
allow_remote_control yes
listen_on unix:/tmp/kitty

# === MAPEADO DE TECLAS PARA NÚCLEO ===
# Accesos rápidos al núcleo
map f1 launch --type=overlay python3 gym_razonbilstro/neural_model.py
map f2 launch --type=overlay python3 gym_razonbilstro/complete_system_integration.py
map f3 launch --type=overlay python3 gym_razonbilstro/pwnagotchi_ai_module.py
map f4 launch --type=tab --tab-title="Monitor" python3 gym_razonbilstro/monitoring_app.py

# Gestión de ventanas mejorada
map ctrl+shift+enter new_window_with_cwd
map ctrl+shift+t new_tab_with_cwd
map ctrl+shift+w close_window
map ctrl+shift+q close_tab

# Navegación rápida
map alt+left previous_tab
map alt+right next_tab
map ctrl+alt+left previous_window
map ctrl+alt+right next_window

# Control de opacidad
map ctrl+shift+a>m set_background_opacity +0.1
map ctrl+shift+a>l set_background_opacity -0.1
map ctrl+shift+a>1 set_background_opacity 1
map ctrl+shift+a>d set_background_opacity default

# === CONFIGURACIÓN DE INICIO ===
startup_session nucleus_session.conf
"""
        
        config_file = self.config_dir / "kitty.conf"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(kitty_config)
        
        print(f"   ✅ Configuración guardada: {config_file}")
    
    def _create_nucleus_integration_scripts(self):
        """Crear scripts de integración con el núcleo"""
        print("🔗 Creando scripts de integración con núcleo...")
        
        # Script principal de lanzamiento
        launcher_script = """#!/bin/bash
# Lanzador Kitty-Núcleo C.A- Razonbilstro

export TERM=xterm-256color
export NUCLEUS_PATH="$PWD/gym_razonbilstro"
export KITTY_CONFIG_DIRECTORY="$HOME/.config/kitty"

# Colores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
PURPLE='\\033[0;35m'
CYAN='\\033[0;36m'
NC='\\033[0m' # No Color

echo -e "${PURPLE}🚀 INICIANDO NÚCLEO C.A- RAZONBILSTRO${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Verificar núcleo
if [ -f "$NUCLEUS_PATH/neural_model.py" ]; then
    echo -e "${GREEN}✅ Núcleo encontrado y listo${NC}"
else
    echo -e "${RED}❌ Error: Núcleo no encontrado${NC}"
    exit 1
fi

# Verificar Kitty
if command -v kitty &> /dev/null; then
    echo -e "${GREEN}✅ Kitty terminal disponible${NC}"
else
    echo -e "${YELLOW}⚠️ Kitty no encontrado, usando terminal por defecto${NC}"
fi

# Lanzar interfaz
echo -e "${BLUE}🖥️ Iniciando interfaz multiventanas...${NC}"

if command -v kitty &> /dev/null; then
    kitty --session nucleus_session.conf
else
    # Fallback para terminales estándar
    python3 "$NUCLEUS_PATH/neural_model.py"
fi
"""
        
        launcher_file = Path("launch_nucleus_kitty.sh")
        with open(launcher_file, 'w', encoding='utf-8') as f:
            f.write(launcher_script)
        launcher_file.chmod(0o755)
        
        print(f"   ✅ Script lanzador: {launcher_file}")
    
    def _setup_multiwindow_layouts(self):
        """Configurar layouts multiventana"""
        print("🪟 Configurando layouts multiventana...")
        
        session_config = """# Sesión Kitty - Núcleo C.A- Razonbilstro
# Layout replicando diseño original de la imagen

new_tab Directory@Razonbilstro
layout splits
# Panel superior izquierdo - Navegador de archivos
launch --title="Directory@Razonbilstro" --cwd=. tree -C -L 3 .
# Panel inferior izquierdo - Chat Agent
launch --title="Chat Agent" python3 gym_razonbilstro/neural_model.py
# Panel derecho principal - Terminal user@razonbilstro
launch --title="user@razonbilstro" bash

# Redimensionar paneles para replicar el diseño de la imagen
resize_window narrower
resize_window narrower
focus_window left
resize_window wider

new_tab Pwnagotchi AI
layout horizontal
launch --title="🤖 Pwnagotchi AI" python3 gym_razonbilstro/pwnagotchi_ai_module.py
launch --title="📊 Monitor WiFi" python3 gym_razonbilstro/pwnagotchi_training_system.py

new_tab Sistema Completo
layout tall
launch --title="🧠 Núcleo Principal" python3 gym_razonbilstro/complete_system_integration.py
launch --title="⚡ Pruebas Sistema" python3 gym_razonbilstro/system_stress_test.py

new_tab Herramientas CLI
layout horizontal
launch --title="🛠️ Shell Avanzado" bash
launch --title="📋 Logs en Vivo" journalctl -f

new_tab Desarrollo
layout vertical
launch --title="📝 Editor Código" nano
launch --title="🔄 Git Workspace" git status
"""
        
        session_file = self.config_dir / "nucleus_session.conf"
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(session_config)
        
        print(f"   ✅ Configuración de sesión: {session_file}")
    
    def _create_autostart_script(self):
        """Crear script de inicio automático"""
        print("⚡ Creando script de inicio automático...")
        
        autostart_script = """#!/bin/bash
# Autostart Núcleo C.A- Razonbilstro en Kitty

# Esperar que el sistema esté listo
sleep 2

# Configurar variables de entorno
export NUCLEUS_HOME="$PWD"
export PYTHONPATH="$NUCLEUS_HOME:$PYTHONPATH"

# Verificar dependencias
echo "🔍 Verificando dependencias del núcleo..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 requerido"
    exit 1
fi

# Verificar módulos del núcleo
python3 -c "import gym_razonbilstro.neural_model" 2>/dev/null || {
    echo "❌ Módulos del núcleo no encontrados"
    exit 1
}

echo "✅ Dependencias verificadas"

# Lanzar Kitty con configuración del núcleo
if command -v kitty &> /dev/null; then
    echo "🚀 Lanzando interfaz Kitty-Núcleo..."
    kitty --config="$HOME/.config/kitty/kitty.conf" --session="$HOME/.config/kitty/nucleus_session.conf"
else
    echo "⚠️ Kitty no disponible, iniciando núcleo en terminal actual..."
    python3 gym_razonbilstro/neural_model.py
fi
"""
        
        autostart_file = Path("autostart_nucleus.sh")
        with open(autostart_file, 'w', encoding='utf-8') as f:
            f.write(autostart_script)
        autostart_file.chmod(0o755)
        
        print(f"   ✅ Script autostart: {autostart_file}")
    
    def create_shell_integration(self):
        """Crear integración completa con shell"""
        print("\n🐚 CONFIGURANDO INTEGRACIÓN SHELL")
        print("-" * 40)
        
        # Aliases para el núcleo
        shell_aliases = """# Aliases Núcleo C.A- Razonbilstro
alias nucleus='python3 gym_razonbilstro/neural_model.py'
alias pwn='python3 gym_razonbilstro/pwnagotchi_ai_module.py'
alias nstress='python3 gym_razonbilstro/system_stress_test.py'
alias nsystem='python3 gym_razonbilstro/complete_system_integration.py'
alias nmonitor='python3 gym_razonbilstro/monitoring_app.py'
alias nkitty='./launch_nucleus_kitty.sh'

# Función para consulta rápida al núcleo
nucleus_query() {
    if [ -z "$1" ]; then
        echo "Uso: nucleus_query 'tu consulta aquí'"
        return 1
    fi
    echo "🧠 Consultando núcleo: $1"
    python3 gym_razonbilstro/neural_model.py --query "$1"
}

# Función para activar Pwnagotchi AI
pwn_activate() {
    echo "🤖 Activando Pwnagotchi AI..."
    python3 gym_razonbilstro/pwnagotchi_ai_module.py --interactive
}

# Prompt personalizado con indicador del núcleo
export PS1='\\[\\033[35m\\]🧠\\[\\033[0m\\] \\[\\033[36m\\]\\u@nucleus\\[\\033[0m\\]:\\[\\033[33m\\]\\w\\[\\033[0m\\]\\$ '
"""
        
        # Guardar aliases
        bashrc_addon = Path(".nucleus_aliases")
        with open(bashrc_addon, 'w', encoding='utf-8') as f:
            f.write(shell_aliases)
        
        print(f"   ✅ Aliases creados: {bashrc_addon}")
        print("   💡 Ejecuta: source .nucleus_aliases")
        
        return bashrc_addon
    
    def launch_interface(self):
        """Lanzar la interfaz Kitty-Núcleo"""
        print("\n🚀 LANZANDO INTERFAZ KITTY-NÚCLEO")
        print("-" * 40)
        
        try:
            # Verificar si Kitty está disponible
            result = subprocess.run(['which', 'kitty'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Kitty encontrado, lanzando interfaz multiventanas...")
                
                # Lanzar Kitty con configuración del núcleo
                subprocess.run([
                    'kitty', 
                    '--config', str(self.config_dir / 'kitty.conf'),
                    '--session', str(self.config_dir / 'nucleus_session.conf')
                ])
                
                self.interface_active = True
                return True
                
            else:
                print("⚠️ Kitty no encontrado, usando terminal estándar...")
                self._launch_fallback_interface()
                return False
                
        except Exception as e:
            print(f"❌ Error lanzando interfaz: {e}")
            self._launch_fallback_interface()
            return False
    
    def _launch_fallback_interface(self):
        """Interfaz de respaldo sin Kitty"""
        print("🔄 Lanzando interfaz de respaldo...")
        
        # Lanzar núcleo en terminal actual
        subprocess.run(['python3', 'gym_razonbilstro/neural_model.py'])
    
    def status_report(self):
        """Generar reporte del estado de la interfaz"""
        return {
            "kitty_config_exists": (self.config_dir / "kitty.conf").exists(),
            "session_config_exists": (self.config_dir / "nucleus_session.conf").exists(),
            "launcher_script_exists": Path("launch_nucleus_kitty.sh").exists(),
            "autostart_script_exists": Path("autostart_nucleus.sh").exists(),
            "aliases_created": Path(".nucleus_aliases").exists(),
            "interface_active": self.interface_active,
            "integration_complete": True
        }

def main():
    """Configurar interfaz Kitty completa"""
    interface = KittyNucleusInterface()
    
    print("🎨 Configurando interfaz Kitty multiventanas para Núcleo C.A- Razonbilstro")
    
    # Configurar todo
    interface.setup_complete_interface()
    interface.create_shell_integration()
    
    # Mostrar estado
    status = interface.status_report()
    
    print(f"\n📊 ESTADO DE LA CONFIGURACIÓN:")
    print(f"   ✅ Configuración Kitty: {'Sí' if status['kitty_config_exists'] else 'No'}")
    print(f"   ✅ Sesión multiventana: {'Sí' if status['session_config_exists'] else 'No'}")
    print(f"   ✅ Script lanzador: {'Sí' if status['launcher_script_exists'] else 'No'}")
    print(f"   ✅ Integración shell: {'Sí' if status['aliases_created'] else 'No'}")
    print(f"   🎯 Integración completa: {'Sí' if status['integration_complete'] else 'No'}")
    
    print(f"\n🚀 PARA USAR LA INTERFAZ:")
    print(f"   1. Ejecuta: ./launch_nucleus_kitty.sh")
    print(f"   2. O usa: source .nucleus_aliases && nkitty")
    print(f"   3. Navega con F1-F4 para acceso rápido al núcleo")

if __name__ == "__main__":
    main()