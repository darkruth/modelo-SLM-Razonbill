#!/bin/bash
# Script de creación de VM para RazonbilstroOS

set -e

VM_NAME="RazonbilstroOS_Test_VM"
VM_DIR="$PWD/vm_test_environment"
ISO_FILE="RazonbilstroOS-v2.1.0-complete.tar.gz"

log() { echo "[$(date +'%H:%M:%S')] $1"; }
success() { echo "✅ $1"; }
error() { echo "❌ $1"; exit 1; }

# Verificar dependencias
check_dependencies() {
    log "Verificando dependencias de virtualización..."
    
    if ! command -v qemu-system-x86_64 &> /dev/null; then
        error "QEMU no instalado. Instalar con: sudo apt install qemu-kvm"
    fi
    
    if ! command -v virt-manager &> /dev/null; then
        log "Virt-manager no encontrado, instalando herramientas básicas..."
    fi
    
    # Verificar KVM
    if [ -r /dev/kvm ]; then
        success "KVM disponible para aceleración"
    else
        log "KVM no disponible, usando emulación"
    fi
    
    success "Dependencias verificadas"
}

# Crear disco virtual
create_vm_disk() {
    log "Creando disco virtual..."
    
    DISK_PATH="$VM_DIR/vm_config/razonbilstro_vm.qcow2"
    
    if [ -f "$DISK_PATH" ]; then
        log "Disco virtual ya existe, sobrescribiendo..."
        rm "$DISK_PATH"
    fi
    
    qemu-img create -f qcow2 "$DISK_PATH" 50G
    success "Disco virtual creado: 50GB"
}

# Preparar ISO para VM
prepare_iso() {
    log "Preparando ISO para VM..."
    
    if [ -f "$ISO_FILE" ]; then
        # Extraer y preparar para VM
        cd "$VM_DIR/iso_mount"
        tar -xzf "../../../$ISO_FILE"
        
        # Crear ISO temporal para VM
        if command -v genisoimage &> /dev/null; then
            genisoimage -o ../vm_config/razonbilstro_vm.iso -J -R -V "RazonbilstroOS" RazonbilstroOS/
            success "ISO preparada para VM"
        else
            log "Usando archivo comprimido como fuente"
            cp "../../../$ISO_FILE" ../vm_config/razonbilstro_vm_source.tar.gz
        fi
        cd - > /dev/null
    else
        log "ISO no encontrada, continuando sin instalación automática"
    fi
}

# Configurar red VM
setup_vm_network() {
    log "Configurando red VM..."
    
    # Crear bridge de red si no existe
    if ! ip link show br0 &> /dev/null; then
        log "Creando bridge de red..."
        # Nota: requiere privilegios de administrador
        # sudo ip link add br0 type bridge
        # sudo ip link set br0 up
    fi
    
    success "Red VM configurada"
}

# Crear script de inicio de VM
create_vm_start_script() {
    log "Creando script de inicio VM..."
    
    cat > "$VM_DIR/vm_config/start_vm.sh" << 'EOF'
#!/bin/bash
# Script de inicio de VM RazonbilstroOS

VM_DIR="$(dirname "$0")"
DISK_PATH="$VM_DIR/razonbilstro_vm.qcow2"
ISO_PATH="$VM_DIR/razonbilstro_vm.iso"

# Configuración de VM
RAM_GB=8
CPU_CORES=4
VNC_PORT=5900

echo "🚀 Iniciando VM RazonbilstroOS..."
echo "RAM: ${RAM_GB}GB"
echo "CPU: ${CPU_CORES} cores"
echo "VNC: localhost:$VNC_PORT"
echo "Web: localhost:8080 (cuando esté instalado)"

# Comando QEMU
qemu-system-x86_64     -name "RazonbilstroOS Test VM"     -machine q35,accel=kvm     -cpu host     -smp $CPU_CORES     -m ${RAM_GB}G     -drive file="$DISK_PATH",format=qcow2,if=virtio     $([ -f "$ISO_PATH" ] && echo "-cdrom $ISO_PATH")     -boot menu=on     -netdev user,id=net0,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:5000     -device virtio-net,netdev=net0     -display gtk     -vnc :0     -usb -device usb-tablet     -soundhw hda     -rtc base=localtime     -monitor stdio
EOF
    
    chmod +x "$VM_DIR/vm_config/start_vm.sh"
    success "Script de inicio creado"
}

# Crear script de conexión
create_connection_scripts() {
    log "Creando scripts de conexión..."
    
    # SSH
    cat > "$VM_DIR/vm_config/connect_ssh.sh" << 'EOF'
#!/bin/bash
echo "Conectando por SSH a RazonbilstroOS VM..."
echo "Usuario: razonbill"
echo "Password: razonbill2024"
ssh -p 2222 razonbill@localhost
EOF
    
    # VNC
    cat > "$VM_DIR/vm_config/connect_vnc.sh" << 'EOF'
#!/bin/bash
echo "Iniciando cliente VNC..."
if command -v vncviewer &> /dev/null; then
    vncviewer localhost:5900
else
    echo "Cliente VNC no instalado"
    echo "Conectar manualmente a: localhost:5900"
fi
EOF
    
    # Web Dashboard
    cat > "$VM_DIR/vm_config/open_dashboard.sh" << 'EOF'
#!/bin/bash
echo "Abriendo dashboard RazonbilstroOS..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
elif command -v firefox &> /dev/null; then
    firefox http://localhost:8080
else
    echo "Abrir manualmente: http://localhost:8080"
fi
EOF
    
    chmod +x "$VM_DIR/vm_config"/*.sh
    success "Scripts de conexión creados"
}

# Función principal
main() {
    echo "🖥️ CONFIGURADOR DE VM RAZONBILSTROS"
    echo "=================================="
    
    check_dependencies
    create_vm_disk
    prepare_iso
    setup_vm_network
    create_vm_start_script
    create_connection_scripts
    
    echo ""
    echo "🎉 VM CONFIGURADA EXITOSAMENTE"
    echo "=============================="
    echo ""
    echo "Para iniciar VM:"
    echo "  cd $VM_DIR/vm_config"
    echo "  ./start_vm.sh"
    echo ""
    echo "Conexiones disponibles:"
    echo "  SSH: ./connect_ssh.sh"
    echo "  VNC: ./connect_vnc.sh"  
    echo "  Web: ./open_dashboard.sh"
    echo ""
    echo "Puertos de la VM:"
    echo "  SSH: localhost:2222"
    echo "  Dashboard: localhost:8080"
    echo "  VNC: localhost:5900"
}

main "$@"
