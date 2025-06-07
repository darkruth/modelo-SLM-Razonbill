#!/bin/bash
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
