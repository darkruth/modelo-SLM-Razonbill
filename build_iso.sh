#!/bin/bash
# Script de construcción de ISO para RazonbilstroOS
set -e

echo "🔧 Construyendo RazonbilstroOS-v2.1.0-amd64.iso..."

# Verificar dependencias
command -v debootstrap >/dev/null 2>&1 || { echo "Error: debootstrap no encontrado"; exit 1; }
command -v xorriso >/dev/null 2>&1 || { echo "Error: xorriso no encontrado"; exit 1; }

# Directorios
BUILD_DIR="razonbilstro_build"
ROOTFS_DIR="$BUILD_DIR/rootfs"
ISO_DIR="$BUILD_DIR/iso"
WORK_DIR="$BUILD_DIR/work"

# Crear estructura ISO
mkdir -p "$ISO_DIR/live"
mkdir -p "$WORK_DIR"

echo "📦 Creando sistema de archivos squashfs..."
mksquashfs "$ROOTFS_DIR" "$ISO_DIR/live/filesystem.squashfs" \
    -e boot -comp xz

echo "🚀 Configurando arranque..."
# Copiar kernel y initrd
cp "$ROOTFS_DIR/boot/vmlinuz-"* "$ISO_DIR/live/vmlinuz"
cp "$ROOTFS_DIR/boot/initrd.img-"* "$ISO_DIR/live/initrd"

# Crear configuración GRUB para ISO
cat > "$ISO_DIR/boot/grub/grub.cfg" << 'EOF'
set default=0
set timeout=10

menuentry "RazonbilstroOS 2.1.0 (Live)" {
    linux /live/vmlinuz boot=live components quiet splash
    initrd /live/initrd
}

menuentry "RazonbilstroOS 2.1.0 (Install)" {
    linux /live/vmlinuz boot=live components quiet splash razonbilstro-installer
    initrd /live/initrd
}
EOF

echo "💿 Generando ISO..."
xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "RAZONBILSTRO_2_1_0" \
    -eltorito-boot boot/grub/bios.img \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --eltorito-catalog boot/grub/boot.cat \
    --grub2-boot-info \
    --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
    -eltorito-alt-boot \
    -e EFI/BOOT/BOOTX64.EFI \
    -no-emul-boot \
    -append_partition 2 0xef isolinux/efiboot.img \
    -output "RazonbilstroOS-v2.1.0-amd64.iso" \
    -graft-points \
        "$ISO_DIR" \
        /boot/grub/bios.img=bios.img \
        /EFI/BOOT/BOOTX64.EFI=bootx64.efi

echo "✅ ISO creada: RazonbilstroOS-v2.1.0-amd64.iso"
echo "📊 Información de la ISO:"
ls -lh "RazonbilstroOS-v2.1.0-amd64.iso"

echo "🔍 Verificando ISO..."
file "RazonbilstroOS-v2.1.0-amd64.iso"

echo "🎉 ¡RazonbilstroOS ISO lista para bootear!"
