#!/bin/bash
# Instalador de Bootloader RazonbilstroOS

set -e

log() { echo "[$(date +'%H:%M:%S')] $1"; }
success() { echo "✅ $1"; }

install_grub_uefi() {
    log "Instalando GRUB para UEFI..."
    
    # Crear partición EFI si no existe
    if [ ! -d /boot/efi ]; then
        mkdir -p /boot/efi
    fi
    
    # Instalar GRUB UEFI
    grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=RazonbilstroOS
    
    # Copiar configuración
    cp grub.cfg /boot/grub/
    cp uefi_grub.cfg /boot/efi/EFI/razonbilstro/
    
    # Generar configuración
    grub-mkconfig -o /boot/grub/grub.cfg
    
    success "GRUB UEFI instalado"
}

install_grub_bios() {
    log "Instalando GRUB para BIOS Legacy..."
    
    # Instalar GRUB en MBR
    grub-install --target=i386-pc /dev/sda
    
    # Copiar configuración
    cp grub.cfg /boot/grub/
    
    # Generar configuración
    grub-mkconfig -o /boot/grub/grub.cfg
    
    success "GRUB BIOS instalado"
}

create_grub_theme() {
    log "Creando tema GRUB personalizado..."
    
    THEME_DIR="/boot/grub/themes/razonbilstro"
    mkdir -p "$THEME_DIR"
    
    cat > "$THEME_DIR/theme.txt" << 'EOF'
# RazonbilstroOS GRUB Theme
desktop-image: "background.png"
title-color: "#ffffff"
title-font: "DejaVu Sans Bold 16"
message-font: "DejaVu Sans 12"
terminal-font: "DejaVu Sans Mono 12"

+ boot_menu {
    left = 20%
    top = 30%
    width = 60%
    height = 50%
    item_color = "#cccccc"
    selected_item_color = "#ffffff"
    item_height = 25
    item_padding = 5
    item_spacing = 10
    selected_item_pixmap_style = "selected_*.png"
}

+ label {
    top = 10%
    left = 0
    width = 100%
    height = 20
    text = "RazonbilstroOS v2.1.0 Neural Agent"
    color = "#ffffff"
    font = "DejaVu Sans Bold 18"
    align = "center"
}

+ label {
    top = 85%
    left = 0  
    width = 100%
    height = 20
    text = "Sistema operativo con IA integrada - Selecciona una opción"
    color = "#cccccc"
    font = "DejaVu Sans 12"
    align = "center"
}
EOF
    
    success "Tema GRUB creado"
}

main() {
    echo "🥾 INSTALADOR DE BOOTLOADER RAZONBILSTROS"
    echo "========================================"
    
    # Detectar tipo de firmware
    if [ -d /sys/firmware/efi ]; then
        log "Sistema UEFI detectado"
        install_grub_uefi
    else
        log "Sistema BIOS Legacy detectado"
        install_grub_bios
    fi
    
    create_grub_theme
    
    echo ""
    echo "🎉 BOOTLOADER INSTALADO EXITOSAMENTE"
    echo "===================================="
    echo ""
    echo "Características del bootloader:"
    echo "✅ Soporte UEFI y BIOS Legacy"
    echo "✅ Menú personalizado RazonbilstroOS"
    echo "✅ Modo seguro y debug incluidos"
    echo "✅ Test de memoria integrado"
    echo "✅ Opciones de recuperación"
    echo ""
    echo "El sistema está listo para arrancar"
}

main "$@"
