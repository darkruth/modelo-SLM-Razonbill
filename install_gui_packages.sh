#!/bin/bash
# Script de instalación de paquetes GUI Razonbilstro
set -e

echo "Actualizando repositorios..."
apt update

echo "Instalando paquetes del escritorio..."
apt install -y \
i3-wm i3status i3lock rofi polybar xorg lightdm gtk3 qt5 cairo pango pulseaudio alsa-utils pavucontrol audacity cava ffmpeg vlc mpv rhythmbox gimp kitty tmux zsh oh-my-zsh neofetch fonts-firacode fonts-noto papirus-icon-theme numix-icon-theme font-awesome \
build-essential \
cmake \
pkg-config \
libgtk-3-dev \
libcairo2-dev \
libpango1.0-dev \
libasound2-dev \
libpulse-dev \
xorg-dev \
libxrandr-dev \
libxinerama-dev \
libxcursor-dev \
libxi-dev

echo "Instalación completada"
