#!/bin/bash
# Constructor de ISO Razonbilstro Desktop
set -e

ISO_NAME="RazonbilstroOS-1.0.0-x86_64.iso"
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
i3-wm i3status i3lock rofi polybar xorg lightdm gtk3 qt5 cairo pango pulseaudio alsa-utils pavucontrol audacity cava ffmpeg vlc mpv rhythmbox gimp kitty tmux zsh oh-my-zsh neofetch fonts-firacode fonts-noto papirus-icon-theme numix-icon-theme font-awesome

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

menuentry "Razonbilstro Desktop Live" {
    linux /live/vmlinuz boot=live live-config live-media-path=/live quiet splash
    initrd /live/initrd
}

menuentry "Razonbilstro Desktop (Safe Mode)" {
    linux /live/vmlinuz boot=live live-config live-media-path=/live nomodeset
    initrd /live/initrd
}
EOF

# Crear ISO final
grub-mkrescue -o "$ISO_NAME" "$BUILD_ROOT/iso"

echo "ISO creada exitosamente: $ISO_NAME"
echo "Tamaño: $(du -h $ISO_NAME | cut -f1)"
