#!/bin/bash
# Script de pruebas de instalación RazonbilstroOS

set -e

log() { echo "[$(date +'%H:%M:%S')] $1"; }
success() { echo "✅ $1"; }
error() { echo "❌ $1"; }

test_system_requirements() {
    log "Probando requisitos del sistema..."
    
    # Verificar RAM
    RAM_MB=$(free -m | awk 'NR==2{print $2}')
    if [ "$RAM_MB" -ge 4000 ]; then
        success "RAM: ${RAM_MB}MB (suficiente)"
    else
        error "RAM insuficiente: ${RAM_MB}MB (mínimo 4GB)"
    fi
    
    # Verificar CPU
    CPU_CORES=$(nproc)
    if [ "$CPU_CORES" -ge 2 ]; then
        success "CPU: ${CPU_CORES} cores (suficiente)"
    else
        error "CPU insuficiente: ${CPU_CORES} cores (mínimo 2)"
    fi
    
    # Verificar almacenamiento
    DISK_GB=$(df / | awk 'NR==2{print int($4/1024/1024)}')
    if [ "$DISK_GB" -ge 20 ]; then
        success "Almacenamiento: ${DISK_GB}GB disponibles"
    else
        error "Almacenamiento insuficiente: ${DISK_GB}GB (mínimo 20GB)"
    fi
}

test_installation() {
    log "Probando instalación de RazonbilstroOS..."
    
    # Verificar directorios
    if [ -d "/opt/razonbilstro" ]; then
        success "Directorio de instalación encontrado"
    else
        error "Directorio de instalación no encontrado"
    fi
    
    # Verificar comandos
    if command -v nucleus &> /dev/null; then
        success "Comando 'nucleus' disponible"
    else
        error "Comando 'nucleus' no encontrado"
    fi
    
    # Verificar base de datos
    if systemctl is-active postgresql &> /dev/null; then
        success "PostgreSQL activo"
    else
        log "PostgreSQL no activo (puede ser normal)"
    fi
}

test_nucleus_functionality() {
    log "Probando funcionalidad del núcleo..."
    
    # Verificar estado
    if nucleus --status &> /dev/null; then
        success "Comando nucleus --status funcional"
    else
        error "Comando nucleus --status falló"
    fi
    
    # Intentar iniciar núcleo
    log "Intentando iniciar núcleo..."
    if nucleus --start; then
        sleep 5
        if curl -s http://localhost:5000 &> /dev/null; then
            success "Núcleo iniciado y dashboard accesible"
            nucleus --stop
        else
            error "Dashboard no accesible en puerto 5000"
        fi
    else
        error "Error al iniciar núcleo"
    fi
}

test_vision_module() {
    log "Probando módulo de visión..."
    
    if command -v vision &> /dev/null; then
        if vision --status &> /dev/null; then
            success "Módulo de visión disponible"
        else
            log "Módulo de visión disponible pero con errores (puede ser normal sin cámara)"
        fi
    else
        error "Comando 'vision' no encontrado"
    fi
}

benchmark_performance() {
    log "Ejecutando benchmark de rendimiento..."
    
    # CPU benchmark
    echo "CPU Benchmark:"
    time python3 -c "
import time
start = time.time()
for i in range(1000000):
    _ = i ** 2
print(f'CPU test completed in {time.time() - start:.2f} seconds')
"
    
    # Memoria benchmark
    echo "Memory Benchmark:"
    python3 -c "
import psutil
mem = psutil.virtual_memory()
print(f'RAM Total: {mem.total / 1024**3:.1f} GB')
print(f'RAM Usado: {mem.used / 1024**3:.1f} GB')
print(f'RAM Libre: {mem.available / 1024**3:.1f} GB')
"
    
    # Disco benchmark
    echo "Disk Benchmark:"
    time dd if=/dev/zero of=/tmp/benchmark bs=1M count=100 2>/dev/null
    rm -f /tmp/benchmark
}

main() {
    echo "🧪 PRUEBAS DE INSTALACIÓN RAZONBILSTROS"
    echo "====================================="
    
    test_system_requirements
    test_installation
    test_nucleus_functionality
    test_vision_module
    benchmark_performance
    
    echo ""
    echo "🎉 PRUEBAS COMPLETADAS"
    echo "====================="
    echo ""
    echo "Ver logs detallados en /var/log/razonbilstro/"
}

main "$@"
