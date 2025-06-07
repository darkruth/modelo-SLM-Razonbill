#!/usr/bin/env python3
"""
Interfaz Visual Razonbilstro - Réplica exacta del diseño de la imagen
Sistema de terminal que replica la experiencia visual original
"""

import os
import subprocess
from pathlib import Path

class RazonbilstroVisualInterface:
    """Interfaz visual que replica exactamente el diseño de la imagen"""
    
    def __init__(self):
        self.setup_environment()
        
    def setup_environment(self):
        """Configurar entorno visual según la imagen"""
        # Configurar prompt para replicar "user@razonbilstro-#"
        os.environ['PS1'] = r'\[\033[0;36m\]user@razonbilstro-#\[\033[0m\] '
        
        # Colores basados en la imagen
        self.colors = {
            'cyan': '\033[0;36m',
            'green': '\033[0;32m', 
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
    
    def create_directory_panel(self):
        """Crear panel Directory@Razonbilstro como en la imagen"""
        print(f"{self.colors['cyan']}Directory@Razonbilstro{self.colors['reset']}")
        
        directories = [
            "root/",
            "Storage/", 
            "home/",
            "usr/",
            "bin/",
            "lib/",
            "etc/",
            "shared/"
        ]
        
        for dir_name in directories:
            print(f"{self.colors['green']}{dir_name}{self.colors['reset']}")
    
    def create_agent_panel(self):
        """Crear panel Chat Agent como en la imagen"""
        print(f"\n{self.colors['cyan']}Chat Agent{self.colors['reset']}")
        print(f"{self.colors['green']}@user actualiza paqueterías e{self.colors['reset']}")
        print(f"{self.colors['green']}Eres un servidor de despliegue{self.colors['reset']}")
        print()
        print(f"{self.colors['green']}@agent ejecutando comandos de{self.colors['reset']}")
        print(f"{self.colors['green']}tarea{self.colors['reset']}")
    
    def setup_main_terminal(self):
        """Configurar terminal principal user@razonbilstro"""
        print(f"{self.colors['cyan']}user@razonbilstro-#{self.colors['reset']}")
        print(f"{self.colors['cyan']}user@razonbilstro-#{self.colors['green']}apt update &&{self.colors['reset']}")
        print(f"{self.colors['cyan']}user@razonbilstro-#{self.colors['reset']}")
        
    def launch_visual_kitty(self):
        """Lanzar Kitty con la configuración visual exacta"""
        # Regenerar configuración con el diseño actualizado
        from gym_razonbilstro.kitty_nucleus_interface import KittyNucleusInterface
        interface = KittyNucleusInterface()
        interface.setup_complete_interface()
        
        print(f"{self.colors['bold']}{self.colors['cyan']}🚀 LANZANDO INTERFAZ RAZONBILSTRO{self.colors['reset']}")
        print(f"{self.colors['green']}Diseño basado en imagen original del repositorio{self.colors['reset']}")
        
        # Intentar lanzar Kitty
        try:
            subprocess.run(['./launch_nucleus_kitty.sh'])
        except:
            print(f"{self.colors['cyan']}Usando configuración de terminal actual...{self.colors['reset']}")
            self.simulate_interface()
    
    def simulate_interface(self):
        """Simular la interfaz si Kitty no está disponible"""
        print("\n" + "="*80)
        print(f"{self.colors['bold']}{self.colors['cyan']}INTERFAZ RAZONBILSTRO - LAYOUT SIMULADO{self.colors['reset']}")
        print("="*80)
        
        # Panel izquierdo
        print(f"\n{self.colors['cyan']}┌─ PANEL IZQUIERDO ─────────┐{self.colors['reset']}")
        self.create_directory_panel()
        print(f"\n{self.colors['cyan']}├───────────────────────────┤{self.colors['reset']}")
        self.create_agent_panel()
        print(f"{self.colors['cyan']}└───────────────────────────┘{self.colors['reset']}")
        
        # Panel derecho
        print(f"\n{self.colors['cyan']}┌─ TERMINAL PRINCIPAL ──────────────────────────────┐{self.colors['reset']}")
        self.setup_main_terminal()
        print(f"{self.colors['cyan']}└───────────────────────────────────────────────────┘{self.colors['reset']}")

def main():
    """Lanzar interfaz visual Razonbilstro"""
    interface = RazonbilstroVisualInterface()
    interface.launch_visual_kitty()

if __name__ == "__main__":
    main()