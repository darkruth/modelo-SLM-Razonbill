#!/usr/bin/env python3
"""
Generador de Escritorio GUI Razonbilstro
Sistema desktop completo basado en el diseño de la imagen original
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

class RazonbilstroDesktopBuilder:
    """Constructor del escritorio GUI Razonbilstro"""
    
    def __init__(self):
        self.desktop_name = "RazonbilstroOS"
        self.version = "1.0.0"
        self.architecture = "x86_64"
        self.build_dir = Path("razonbilstro_desktop_build")
        self.build_dir.mkdir(exist_ok=True)
        
        # Librerías y paquetes reales necesarios
        self.gui_packages = {
            "window_manager": [
                "i3-wm",           # Gestor de ventanas tiling
                "i3status",        # Barra de estado
                "i3lock",          # Bloqueo de pantalla
                "rofi",            # Lanzador de aplicaciones
                "polybar"          # Barra personalizable
            ],
            "desktop_environment": [
                "xorg",            # Servidor X
                "lightdm",         # Display manager
                "gtk3",            # Toolkit GTK
                "qt5",             # Toolkit Qt
                "cairo",           # Renderizado de gráficos
                "pango"            # Renderizado de texto
            ],
            "audio_system": [
                "pulseaudio",      # Sistema de audio
                "alsa-utils",      # Utilidades ALSA
                "pavucontrol",     # Control de volumen
                "audacity",        # Editor de audio
                "cava"             # Visualizador de espectro
            ],
            "multimedia": [
                "ffmpeg",          # Codecs multimedia
                "vlc",             # Reproductor de video
                "mpv",             # Reproductor minimalista
                "rhythmbox",       # Reproductor de música
                "gimp"             # Editor de imágenes
            ],
            "terminal_enhanced": [
                "kitty",           # Terminal configurado
                "tmux",            # Multiplexor de terminal
                "zsh",             # Shell avanzado
                "oh-my-zsh",       # Framework para zsh
                "neofetch"         # Información del sistema
            ],
            "fonts_icons": [
                "fonts-firacode",  # Fuente FiraCode
                "fonts-noto",      # Fuentes Noto
                "papirus-icon-theme", # Iconos Papirus
                "numix-icon-theme",   # Iconos Numix
                "font-awesome"        # Iconos FontAwesome
            ]
        }
        
        print(f"Construyendo {self.desktop_name} v{self.version}")
        print(f"Arquitectura: {self.architecture}")
        
    def install_gui_packages(self):
        """Instalar paquetes GUI reales"""
        print("\nInstalando paquetes del sistema GUI...")
        
        all_packages = []
        for category, packages in self.gui_packages.items():
            print(f"\nCategoría: {category}")
            all_packages.extend(packages)
            for package in packages:
                print(f"  • {package}")
        
        # Comando para instalar todos los paquetes
        install_script = f"""#!/bin/bash
# Script de instalación de paquetes GUI Razonbilstro
set -e

echo "Actualizando repositorios..."
apt update

echo "Instalando paquetes del escritorio..."
apt install -y \\
{' '.join(all_packages)} \\
build-essential \\
cmake \\
pkg-config \\
libgtk-3-dev \\
libcairo2-dev \\
libpango1.0-dev \\
libasound2-dev \\
libpulse-dev \\
xorg-dev \\
libxrandr-dev \\
libxinerama-dev \\
libxcursor-dev \\
libxi-dev

echo "Instalación completada"
"""
        
        script_file = self.build_dir / "install_gui_packages.sh"
        with open(script_file, 'w') as f:
            f.write(install_script)
        script_file.chmod(0o755)
        
        print(f"Script de instalación creado: {script_file}")
        return script_file
    
    def create_desktop_environment_config(self):
        """Crear configuración del entorno de escritorio"""
        print("\nCreando configuración del entorno de escritorio...")
        
        # Configuración i3wm basada en el diseño de la imagen
        i3_config = """# Configuración i3wm - Razonbilstro Desktop
# Basado en el diseño de la imagen original

set $mod Mod4

# Fuente para títulos de ventanas
font pango:FiraCode Nerd Font 10

# Colores basados en la imagen (cyan/negro)
set $bg-color            #0a0a0a
set $inactive-bg-color   #1a1a1a
set $text-color          #00ffcc
set $inactive-text-color #6272a4
set $urgent-bg-color     #ff5555
set $indicator-color     #00ffcc

# Configuración de colores de ventanas
client.focused          $bg-color           $bg-color          $text-color          $indicator-color
client.unfocused        $inactive-bg-color  $inactive-bg-color $inactive-text-color $indicator-color
client.focused_inactive $inactive-bg-color  $inactive-bg-color $inactive-text-color $indicator-color
client.urgent           $urgent-bg-color    $urgent-bg-color   $text-color          $indicator-color

# Teclas de acceso
bindsym $mod+Return exec kitty
bindsym $mod+Shift+q kill
bindsym $mod+d exec rofi -show run -theme-str 'window {background-color: #0a0a0a; text-color: #00ffcc;}'

# Navegación de ventanas
bindsym $mod+j focus left
bindsym $mod+k focus down
bindsym $mod+l focus up
bindsym $mod+semicolon focus right

# Mover ventanas
bindsym $mod+Shift+j move left
bindsym $mod+Shift+k move down
bindsym $mod+Shift+l move up
bindsym $mod+Shift+semicolon move right

# División de ventanas
bindsym $mod+h split h
bindsym $mod+v split v

# Cambiar modo de contenedor
bindsym $mod+s layout stacking
bindsym $mod+w layout tabbed
bindsym $mod+e layout toggle split

# Pantalla completa
bindsym $mod+f fullscreen toggle

# Espacios de trabajo (como en la imagen)
set $ws1 "1: Directory@Razonbilstro"
set $ws2 "2: Chat Agent"
set $ws3 "3: Terminal"
set $ws4 "4: Audio"
set $ws5 "5: Monitor"

bindsym $mod+1 workspace $ws1
bindsym $mod+2 workspace $ws2
bindsym $mod+3 workspace $ws3
bindsym $mod+4 workspace $ws4
bindsym $mod+5 workspace $ws5

# Mover ventanas a espacios de trabajo
bindsym $mod+Shift+1 move container to workspace $ws1
bindsym $mod+Shift+2 move container to workspace $ws2
bindsym $mod+Shift+3 move container to workspace $ws3
bindsym $mod+Shift+4 move container to workspace $ws4
bindsym $mod+Shift+5 move container to workspace $ws5

# Reiniciar i3
bindsym $mod+Shift+r restart

# Salir de i3
bindsym $mod+Shift+e exec "i3-nagbar -t warning -m 'Salir?' -b 'Sí' 'i3-msg exit'"

# Configuración de la barra de estado
bar {
    status_command i3status
    position bottom
    colors {
        background $bg-color
        separator $text-color
        #                  border             background         text
        focused_workspace  $bg-color          $bg-color          $text-color
        inactive_workspace $inactive-bg-color $inactive-bg-color $inactive-text-color
        urgent_workspace   $urgent-bg-color   $urgent-bg-color   $text-color
    }
}

# Autostart del núcleo
exec --no-startup-id python3 /usr/local/bin/nucleus_autostart.py
exec --no-startup-id cava
"""
        
        config_dir = self.build_dir / "config" / "i3"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(config_dir / "config", 'w') as f:
            f.write(i3_config)
        
        print(f"Configuración i3wm creada: {config_dir}/config")
        
    def create_polybar_config(self):
        """Crear configuración de Polybar para la barra superior"""
        print("\nCreando configuración de Polybar...")
        
        polybar_config = """[colors]
; Colores basados en la imagen Razonbilstro
background = #0a0a0a
foreground = #00ffcc
primary = #00ffcc
secondary = #6272a4
alert = #ff5555

[bar/razonbilstro]
width = 100%
height = 30
background = ${colors.background}
foreground = ${colors.foreground}

line-size = 2
padding-left = 2
padding-right = 2
module-margin-left = 1
module-margin-right = 2

font-0 = FiraCode Nerd Font:pixelsize=10;1
font-1 = Font Awesome 5 Free:pixelsize=10;1
font-2 = Font Awesome 5 Brands:pixelsize=10;1

modules-left = i3
modules-center = date
modules-right = pulseaudio cpu memory network

tray-position = right
tray-padding = 2

[module/i3]
type = internal/i3
format = <label-state> <label-mode>
index-sort = true

label-mode-padding = 2
label-mode-foreground = ${colors.foreground}
label-mode-background = ${colors.background}

label-focused = %name%
label-focused-background = ${colors.primary}
label-focused-foreground = ${colors.background}
label-focused-padding = 2

label-unfocused = %name%
label-unfocused-padding = 2

label-visible = %name%
label-visible-background = ${colors.secondary}
label-visible-padding = 2

label-urgent = %name%
label-urgent-background = ${colors.alert}
label-urgent-padding = 2

[module/date]
type = internal/date
interval = 5
date = %Y-%m-%d
time = %H:%M
label = 🕒 %date% %time%

[module/pulseaudio]
type = internal/pulseaudio
format-volume = 🔊 <bar-volume>
label-volume = VOL %percentage%%
label-muted = 🔇 muted

bar-volume-width = 10
bar-volume-foreground-0 = ${colors.primary}
bar-volume-gradient = false
bar-volume-indicator = |
bar-volume-fill = ─
bar-volume-empty = ─
bar-volume-empty-foreground = ${colors.secondary}

[module/cpu]
type = internal/cpu
interval = 2
format-prefix = "💻 "
label = CPU %percentage:2%%

[module/memory]
type = internal/memory
interval = 2
format-prefix = "🧠 "
label = RAM %percentage_used%%

[module/network]
type = internal/network
interface = eth0
interval = 3
format-connected = 🌐 <label-connected>
label-connected = %downspeed:9%
format-disconnected = ❌ disconnected
"""
        
        polybar_dir = self.build_dir / "config" / "polybar"
        polybar_dir.mkdir(parents=True, exist_ok=True)
        
        with open(polybar_dir / "config", 'w') as f:
            f.write(polybar_config)
        
        print(f"Configuración Polybar creada: {polybar_dir}/config")
    
    def create_audio_visualizer_config(self):
        """Crear configuración del visualizador de audio (como en la imagen)"""
        print("\nCreando configuración del visualizador de audio...")
        
        cava_config = """[general]
# Configuración CAVA - Visualizador de espectro de audio
# Basado en el diseño de la imagen

bars = 50
bar_width = 2
bar_spacing = 1

[input]
method = pulse
source = auto

[output]
method = ncurses
channels = stereo
mono_option = average

[color]
# Colores cyan como en la imagen
gradient = 1
gradient_count = 2
gradient_color_1 = '#00ffcc'
gradient_color_2 = '#0080aa'

[smoothing]
integral = 60
monstercat = 1
waves = 0
gravity = 200
ignore = 0
"""
        
        cava_dir = self.build_dir / "config" / "cava"
        cava_dir.mkdir(parents=True, exist_ok=True)
        
        with open(cava_dir / "config", 'w') as f:
            f.write(cava_config)
        
        print(f"Configuración CAVA creada: {cava_dir}/config")
    
    def create_desktop_applications(self):
        """Crear aplicaciones de escritorio (.desktop files)"""
        print("\nCreando aplicaciones de escritorio...")
        
        applications = {
            "nucleus-terminal": {
                "name": "Núcleo Terminal",
                "comment": "Terminal del Núcleo C.A- Razonbilstro",
                "icon": "terminal",
                "exec": "kitty --config=/etc/razonbilstro/kitty.conf",
                "categories": "System;Terminal;"
            },
            "nucleus-pwnagotchi": {
                "name": "Pwnagotchi AI",
                "comment": "Sistema de auditoría WiFi",
                "icon": "network-wireless",
                "exec": "python3 /usr/local/bin/pwnagotchi_ai_module.py",
                "categories": "Network;Security;"
            },
            "nucleus-monitor": {
                "name": "Monitor del Sistema",
                "comment": "Monitor en tiempo real del núcleo",
                "icon": "utilities-system-monitor",
                "exec": "python3 /usr/local/bin/monitoring_app.py",
                "categories": "System;Monitor;"
            },
            "nucleus-audio": {
                "name": "Visualizador de Audio",
                "comment": "Ecualizador y visualizador de espectro",
                "icon": "multimedia-volume-control",
                "exec": "kitty --title='Audio Visualizer' -e cava",
                "categories": "AudioVideo;Audio;"
            }
        }
        
        desktop_dir = self.build_dir / "applications"
        desktop_dir.mkdir(exist_ok=True)
        
        for app_id, app_info in applications.items():
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_info['name']}
Comment={app_info['comment']}
Icon={app_info['icon']}
Exec={app_info['exec']}
Categories={app_info['categories']}
Terminal=false
StartupNotify=true
"""
            
            with open(desktop_dir / f"{app_id}.desktop", 'w') as f:
                f.write(desktop_content)
        
        print(f"Aplicaciones de escritorio creadas en: {desktop_dir}")
    
    def create_startup_scripts(self):
        """Crear scripts de inicio del sistema"""
        print("\nCreando scripts de inicio...")
        
        autostart_script = """#!/bin/bash
# Script de autostart Razonbilstro Desktop

# Configurar variables de entorno
export RAZONBILSTRO_HOME="/usr/local/razonbilstro"
export PATH="$RAZONBILSTRO_HOME/bin:$PATH"

# Iniciar servicios del núcleo
python3 $RAZONBILSTRO_HOME/nucleus_daemon.py &

# Configurar audio
pulseaudio --start

# Iniciar visualizador de audio en background
cava > /dev/null 2>&1 &

# Configurar fondos de pantalla
feh --bg-fill /usr/share/razonbilstro/wallpaper.png

# Iniciar polybar
polybar razonbilstro &

echo "Razonbilstro Desktop iniciado correctamente"
"""
        
        startup_dir = self.build_dir / "startup"
        startup_dir.mkdir(exist_ok=True)
        
        startup_file = startup_dir / "razonbilstro_autostart.sh"
        with open(startup_file, 'w') as f:
            f.write(autostart_script)
        startup_file.chmod(0o755)
        
        print(f"Script de autostart creado: {startup_file}")
    
    def create_iso_builder_script(self):
        """Crear script para construir ISO del sistema"""
        print("\nCreando constructor de ISO...")
        
        iso_script = f"""#!/bin/bash
# Constructor de ISO Razonbilstro Desktop
set -e

ISO_NAME="{self.desktop_name}-{self.version}-{self.architecture}.iso"
BUILD_ROOT="/tmp/razonbilstro_iso_build"
CHROOT_DIR="$BUILD_ROOT/chroot"

echo "Construyendo $ISO_NAME..."

# Crear estructura de directorios
mkdir -p "$BUILD_ROOT"
mkdir -p "$CHROOT_DIR"

# Instalar sistema base Ubuntu
debootstrap --arch=amd64 focal "$CHROOT_DIR" http://archive.ubuntu.com/ubuntu/

# Montar sistemas de archivos
mount --bind /dev "$CHROOT_DIR/dev"
mount --bind /proc "$CHROOT_DIR/proc"
mount --bind /sys "$CHROOT_DIR/sys"

# Configurar el chroot
cat > "$CHROOT_DIR/setup_razonbilstro.sh" << 'EOF'
#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Actualizar repositorios
apt update

# Instalar kernel y bootloader
apt install -y linux-image-generic grub-pc-bin grub-efi-amd64-bin

# Instalar paquetes GUI
{' '.join([pkg for category in self.gui_packages.values() for pkg in category])}

# Configurar usuario razonbilstro
useradd -m -s /bin/bash razonbilstro
echo "razonbilstro:razonbilstro" | chpasswd
usermod -aG sudo razonbilstro

# Instalar núcleo C.A- Razonbilstro
mkdir -p /usr/local/razonbilstro
cp -r /tmp/nucleus_files/* /usr/local/razonbilstro/

# Configurar escritorio
mkdir -p /home/razonbilstro/.config
cp -r /tmp/desktop_configs/* /home/razonbilstro/.config/
chown -R razonbilstro:razonbilstro /home/razonbilstro

# Configurar autostart
cp /tmp/startup/razonbilstro_autostart.sh /etc/profile.d/
chmod +x /etc/profile.d/razonbilstro_autostart.sh

# Configurar display manager
systemctl enable lightdm
systemctl set-default graphical.target

# Limpiar
apt autoremove -y
apt autoclean
EOF

chmod +x "$CHROOT_DIR/setup_razonbilstro.sh"

# Copiar archivos del núcleo
mkdir -p "$CHROOT_DIR/tmp/nucleus_files"
cp -r gym_razonbilstro/* "$CHROOT_DIR/tmp/nucleus_files/"

# Copiar configuraciones del escritorio
mkdir -p "$CHROOT_DIR/tmp/desktop_configs"
cp -r razonbilstro_desktop_build/config/* "$CHROOT_DIR/tmp/desktop_configs/"

# Copiar scripts de startup
mkdir -p "$CHROOT_DIR/tmp/startup"
cp -r razonbilstro_desktop_build/startup/* "$CHROOT_DIR/tmp/startup/"

# Ejecutar configuración en chroot
chroot "$CHROOT_DIR" /setup_razonbilstro.sh

# Desmontar sistemas de archivos
umount "$CHROOT_DIR/dev"
umount "$CHROOT_DIR/proc" 
umount "$CHROOT_DIR/sys"

# Crear filesystem squashfs
mksquashfs "$CHROOT_DIR" "$BUILD_ROOT/filesystem.squashfs" -comp xz

# Crear estructura ISO
mkdir -p "$BUILD_ROOT/iso/live"
cp "$BUILD_ROOT/filesystem.squashfs" "$BUILD_ROOT/iso/live/"

# Copiar kernel e initrd
cp "$CHROOT_DIR/boot/vmlinuz-"* "$BUILD_ROOT/iso/live/vmlinuz"
cp "$CHROOT_DIR/boot/initrd.img-"* "$BUILD_ROOT/iso/live/initrd"

# Crear grub.cfg
mkdir -p "$BUILD_ROOT/iso/boot/grub"
cat > "$BUILD_ROOT/iso/boot/grub/grub.cfg" << 'EOF'
set timeout=10
set default=0

menuentry "Razonbilstro Desktop Live" {{
    linux /live/vmlinuz boot=live live-config live-media-path=/live quiet splash
    initrd /live/initrd
}}

menuentry "Razonbilstro Desktop (Safe Mode)" {{
    linux /live/vmlinuz boot=live live-config live-media-path=/live nomodeset
    initrd /live/initrd
}}
EOF

# Crear ISO final
grub-mkrescue -o "$ISO_NAME" "$BUILD_ROOT/iso"

echo "ISO creada exitosamente: $ISO_NAME"
echo "Tamaño: $(du -h $ISO_NAME | cut -f1)"
"""
        
        iso_builder = self.build_dir / "build_iso.sh"
        with open(iso_builder, 'w') as f:
            f.write(iso_script)
        iso_builder.chmod(0o755)
        
        print(f"Constructor de ISO creado: {iso_builder}")
        
    def generate_build_report(self):
        """Generar informe de construcción"""
        report = {
            "desktop_name": self.desktop_name,
            "version": self.version,
            "architecture": self.architecture,
            "build_timestamp": datetime.now().isoformat(),
            "components": {
                "window_manager": "i3wm",
                "status_bar": "polybar",
                "audio_visualizer": "cava",
                "terminal": "kitty",
                "display_manager": "lightdm"
            },
            "packages_total": sum(len(packages) for packages in self.gui_packages.values()),
            "gui_packages": self.gui_packages,
            "features": [
                "Escritorio completo basado en imagen original",
                "Colores cyan/negro idénticos",
                "Visualizador de audio integrado",
                "Núcleo C.A- Razonbilstro preinstalado",
                "ISO booteable lista para distribución"
            ]
        }
        
        with open(self.build_dir / "build_report.json", 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report

def main():
    """Construir escritorio Razonbilstro completo"""
    builder = RazonbilstroDesktopBuilder()
    
    print("Iniciando construcción del escritorio GUI Razonbilstro...")
    
    # Crear todos los componentes
    builder.install_gui_packages()
    builder.create_desktop_environment_config()
    builder.create_polybar_config()
    builder.create_audio_visualizer_config()
    builder.create_desktop_applications()
    builder.create_startup_scripts()
    builder.create_iso_builder_script()
    
    # Generar informe
    report = builder.generate_build_report()
    
    print(f"\n🎉 ESCRITORIO RAZONBILSTRO CONSTRUIDO EXITOSAMENTE")
    print(f"📦 Paquetes incluidos: {report['packages_total']}")
    print(f"🖥️ Componentes: {len(report['components'])}")
    print(f"⚡ Características: {len(report['features'])}")
    
    print(f"\n📁 Archivos generados en: {builder.build_dir}")
    print(f"🔧 Para instalar paquetes: sudo ./razonbilstro_desktop_build/install_gui_packages.sh")
    print(f"💿 Para crear ISO: sudo ./razonbilstro_desktop_build/build_iso.sh")

if __name__ == "__main__":
    main()