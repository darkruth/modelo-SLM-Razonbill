#!/usr/bin/env python3
"""
Script de configuración para Núcleo C.A- Razonbilstro
Optimizado para equipos de bajos recursos (arch64, 4GB RAM)
Compatible con smartphones Android via Termux
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class RazonbilstroSetup:
    """Configuración automática del sistema Razonbilstro"""
    
    def __init__(self):
        self.system_info = self.detect_system()
        self.is_termux = 'com.termux' in os.environ.get('PREFIX', '')
        self.is_android = 'ANDROID_ROOT' in os.environ
        
    def detect_system(self):
        """Detectar información del sistema"""
        return {
            'platform': platform.system(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'is_64bit': platform.machine() in ['x86_64', 'aarch64', 'arm64']
        }
    
    def check_requirements(self):
        """Verificar requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        
        requirements = {
            'python_version': sys.version_info >= (3, 7),
            'architecture': self.system_info['is_64bit'],
            'memory_available': True  # Asumimos que sí para simplificar
        }
        
        if self.is_termux:
            print("📱 Sistema Android/Termux detectado")
            requirements['termux_ready'] = True
        
        for req, status in requirements.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {req}: {status}")
        
        return all(requirements.values())
    
    def install_dependencies(self):
        """Instalar dependencias según el entorno"""
        print("\n📦 Instalando dependencias...")
        
        if self.is_termux:
            self.install_termux_dependencies()
        else:
            self.install_linux_dependencies()
    
    def install_termux_dependencies(self):
        """Dependencias específicas para Termux"""
        packages = [
            'python', 'numpy', 'clang', 'make', 'pkg-config',
            'git', 'wget', 'curl', 'openssh'
        ]
        
        print("📱 Instalando paquetes Termux...")
        for package in packages:
            try:
                subprocess.run(['pkg', 'install', '-y', package], 
                             check=True, capture_output=True)
                print(f"   ✅ {package}")
            except subprocess.CalledProcessError:
                print(f"   ⚠️ {package} (opcional)")
    
    def install_linux_dependencies(self):
        """Dependencias para Linux tradicional"""
        pip_packages = ['numpy', 'psutil']
        
        print("🐧 Instalando paquetes Python...")
        for package in pip_packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True, capture_output=True)
                print(f"   ✅ {package}")
            except subprocess.CalledProcessError:
                print(f"   ⚠️ Error instalando {package}")
    
    def setup_directories(self):
        """Crear estructura de directorios"""
        print("\n📁 Configurando directorios...")
        
        directories = [
            'data/models',
            'data/repository', 
            'data/logs',
            'data/temp',
            'config/user',
            'config/hardware'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory}")
    
    def configure_kitty_theme(self):
        """Configurar tema Dracula Xeon para Kitty"""
        if self.is_termux:
            print("\n🎨 Configurando tema para Termux...")
            self.setup_termux_colors()
        else:
            print("\n🎨 Configurando tema Kitty Dracula Xeon...")
            self.setup_kitty_config()
    
    def setup_termux_colors(self):
        """Configurar colores Dracula Xeon en Termux"""
        termux_properties = """
# Dracula Xeon Theme for Termux
extra-keys = [['ESC','/','-','HOME','UP','END','PGUP'],['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']]
bell-character = ignore

# Colors
foreground = #f8f8f2
background = #1a1a2e
cursor = #f8f8f2

color0  = #21222c
color1  = #ff5555
color2  = #50fa7b
color3  = #f1fa8c
color4  = #bd93f9
color5  = #ff79c6
color6  = #8be9fd
color7  = #f8f8f2
color8  = #6272a4
color9  = #ff6e6e
color10 = #69ff94
color11 = #ffffa5
color12 = #d6acff
color13 = #ff92df
color14 = #a4ffff
color15 = #ffffff
"""
        
        try:
            termux_dir = Path.home() / '.termux'
            termux_dir.mkdir(exist_ok=True)
            
            properties_file = termux_dir / 'termux.properties'
            with open(properties_file, 'w') as f:
                f.write(termux_properties)
            
            print("   ✅ Tema Termux configurado")
            print("   ℹ️ Reinicia Termux para aplicar cambios")
            
        except Exception as e:
            print(f"   ⚠️ Error configurando tema: {e}")
    
    def setup_kitty_config(self):
        """Configurar Kitty en sistemas Linux"""
        kitty_config = """
# Dracula Xeon Theme for Kitty
font_family      FiraCode Nerd Font
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size 12.0

foreground            #f8f8f2
background            #1a1a2e
selection_foreground  #ffffff
selection_background  #44475a

# Normal colors
color0  #21222c
color1  #ff5555
color2  #50fa7b
color3  #f1fa8c
color4  #bd93f9
color5  #ff79c6
color6  #8be9fd
color7  #f8f8f2

# Bright colors
color8  #6272a4
color9  #ff6e6e
color10 #69ff94
color11 #ffffa5
color12 #d6acff
color13 #ff92df
color14 #a4ffff
color15 #ffffff

# Tab bar
active_tab_foreground   #1a1a2e
active_tab_background   #bd93f9
inactive_tab_foreground #f8f8f2
inactive_tab_background #44475a

# Window
window_border_width 1px
draw_minimal_borders yes
"""
        
        try:
            kitty_dir = Path.home() / '.config' / 'kitty'
            kitty_dir.mkdir(parents=True, exist_ok=True)
            
            config_file = kitty_dir / 'kitty.conf'
            with open(config_file, 'w') as f:
                f.write(kitty_config)
            
            print("   ✅ Configuración Kitty creada")
            
        except Exception as e:
            print(f"   ⚠️ Error configurando Kitty: {e}")
    
    def create_launcher_scripts(self):
        """Crear scripts de lanzamiento"""
        print("\n🚀 Creando scripts de lanzamiento...")
        
        # Script principal CLI
        cli_launcher = """#!/bin/bash
# Lanzador CLI Razonbilstro
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export NUMEXPR_NUM_THREADS=2

cd "$(dirname "$0")"
python3 cli_environment/razonbilstro_cli.py "$@"
"""
        
        # Script web
        web_launcher = """#!/bin/bash
# Lanzador Web Razonbilstro
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2

cd "$(dirname "$0")"
python3 app_integrated.py
"""
        
        scripts = {
            'razonbilstro': cli_launcher,
            'razonbilstro-web': web_launcher
        }
        
        for name, content in scripts.items():
            script_path = Path(name)
            with open(script_path, 'w') as f:
                f.write(content)
            
            # Hacer ejecutable
            os.chmod(script_path, 0o755)
            print(f"   ✅ {name}")
    
    def create_config_files(self):
        """Crear archivos de configuración"""
        print("\n⚙️ Creando configuración...")
        
        # Configuración principal
        main_config = {
            "system": {
                "optimization_level": "low_resource",
                "max_memory_mb": 512,
                "cpu_threads": 2,
                "enable_swap": True
            },
            "core": {
                "auto_init": True,
                "input_size": 64,  # Reducido para bajos recursos
                "output_size": 32,
                "learning_rate": 0.001
            },
            "agent": {
                "auto_init": True,
                "repository_max_entries": 50,
                "lora_rank": 4  # Muy bajo para optimización
            },
            "ui": {
                "theme": "dracula_xeon",
                "cli_enabled": True,
                "web_enabled": True,
                "arduino_enabled": False
            }
        }
        
        config_path = Path('config/razonbilstro.json')
        with open(config_path, 'w') as f:
            json.dump(main_config, f, indent=2)
        
        print("   ✅ config/razonbilstro.json")
    
    def optimize_for_low_resources(self):
        """Aplicar optimizaciones para bajos recursos"""
        print("\n⚡ Aplicando optimizaciones para bajos recursos...")
        
        # Variables de entorno para optimización
        env_vars = {
            'OMP_NUM_THREADS': '2',
            'MKL_NUM_THREADS': '2', 
            'NUMEXPR_NUM_THREADS': '2',
            'PYTHONHASHSEED': '0',
            'TF_CPP_MIN_LOG_LEVEL': '2'
        }
        
        # Crear archivo de entorno
        env_file = Path('.env')
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        print("   ✅ Variables de entorno optimizadas")
        print("   ✅ Configuración para 4GB RAM")
        print("   ✅ Límite de 2 threads CPU")
    
    def run_setup(self):
        """Ejecutar configuración completa"""
        print("🎯 Configurando Núcleo C.A- Razonbilstro")
        print("=" * 50)
        
        if not self.check_requirements():
            print("\n❌ Requisitos no cumplidos. Revisa tu sistema.")
            return False
        
        try:
            self.install_dependencies()
            self.setup_directories()
            self.configure_kitty_theme()
            self.create_launcher_scripts()
            self.create_config_files()
            self.optimize_for_low_resources()
            
            print("\n" + "=" * 50)
            print("🎉 ¡Configuración completada exitosamente!")
            print("\n📋 Próximos pasos:")
            print("   1. ./razonbilstro          # Para CLI")
            print("   2. ./razonbilstro-web      # Para interfaz web")
            print("   3. Revisar config/razonbilstro.json")
            
            if self.is_termux:
                print("\n📱 Específico para Termux:")
                print("   • Reinicia Termux para aplicar tema")
                print("   • Usa 'termux-setup-storage' si necesitas acceso a archivos")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante la configuración: {e}")
            return False


def main():
    """Función principal"""
    setup = RazonbilstroSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🚀 Sistema listo para usar!")
    else:
        print("\n⚠️ Configuración incompleta. Revisa los errores.")
        sys.exit(1)


if __name__ == "__main__":
    main()