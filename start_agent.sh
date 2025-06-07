#!/bin/bash
# Start Agent - Iniciador principal del Agente NetHunter
# Sistema completo con TTY embebido, OCR, TTS y Núcleo Razonbilstro

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_NAME="NetHunter-Razonbilstro Agent"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Banner de arranque
show_startup_banner() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}${BOLD}                🚀 INICIANDO AGENTE NETHUNTER                    ${NC}${CYAN}║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC} ${PURPLE}🧠 Núcleo C.A- Razonbilstro${NC}     ${GREEN}🛡️ Seguridad NetHunter${NC}      ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC} ${YELLOW}📸 OCR Visual              ${BLUE}🗣️ TTS Inteligente${NC}       ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC} ${RED}⚡ TTY Embebido            ${GREEN}📊 Monitoreo Activo${NC}      ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Verificar dependencias
check_dependencies() {
    echo -e "${BLUE}🔍 Verificando dependencias del sistema...${NC}"
    
    local missing_deps=()
    local optional_deps=()
    
    # Dependencias críticas
    if ! command -v python3 &>/dev/null; then
        missing_deps+=("python3")
    fi
    
    if ! command -v bash &>/dev/null; then
        missing_deps+=("bash")
    fi
    
    # Dependencias opcionales
    if ! command -v tesseract &>/dev/null; then
        optional_deps+=("tesseract-ocr")
    fi
    
    if ! command -v import &>/dev/null; then
        optional_deps+=("imagemagick")
    fi
    
    if ! command -v tmux &>/dev/null; then
        optional_deps+=("tmux")
    fi
    
    if ! command -v screen &>/dev/null; then
        optional_deps+=("screen")
    fi
    
    # Reportar estado
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo -e "${RED}❌ Dependencias críticas faltantes:${NC}"
        for dep in "${missing_deps[@]}"; do
            echo -e "   • $dep"
        done
        echo -e "${YELLOW}💡 Instalar con: apt install ${missing_deps[*]}${NC}"
        return 1
    fi
    
    if [[ ${#optional_deps[@]} -gt 0 ]]; then
        echo -e "${YELLOW}⚠️ Dependencias opcionales faltantes:${NC}"
        for dep in "${optional_deps[@]}"; do
            echo -e "   • $dep"
        done
        echo -e "${YELLOW}💡 Para funcionalidad completa: apt install ${optional_deps[*]}${NC}"
    fi
    
    echo -e "${GREEN}✅ Verificación de dependencias completada${NC}"
    return 0
}

# Configurar entorno
setup_environment() {
    echo -e "${BLUE}⚙️ Configurando entorno del agente...${NC}"
    
    # Crear directorios necesarios
    mkdir -p "$SCRIPT_DIR"/{log,config,model,scripts,ocr,interface}
    
    # Hacer ejecutables los scripts
    chmod +x "$SCRIPT_DIR"/*.sh 2>/dev/null
    chmod +x "$SCRIPT_DIR"/scripts/*.sh 2>/dev/null
    chmod +x "$SCRIPT_DIR"/ocr/*.py 2>/dev/null
    
    # Verificar permisos TTY
    if [[ ! -t 0 ]]; then
        echo -e "${YELLOW}⚠️ No hay TTY disponible - funcionalidad limitada${NC}"
    fi
    
    echo -e "${GREEN}✅ Entorno configurado correctamente${NC}"
}

# Verificar integración con Núcleo Razonbilstro
check_nucleus_integration() {
    echo -e "${BLUE}🧠 Verificando integración con Núcleo C.A- Razonbilstro...${NC}"
    
    # Buscar núcleo en directorios padre
    local nucleus_paths=(
        "../../neural_model.py"
        "../../../neural_model.py" 
        "../../gym_razonbilstro"
        "../gym_razonbilstro"
    )
    
    local nucleus_found=false
    for path in "${nucleus_paths[@]}"; do
        if [[ -f "$SCRIPT_DIR/$path" ]] || [[ -d "$SCRIPT_DIR/$path" ]]; then
            echo -e "${GREEN}✅ Núcleo encontrado en: $path${NC}"
            nucleus_found=true
            break
        fi
    done
    
    if [[ "$nucleus_found" == false ]]; then
        echo -e "${YELLOW}⚠️ Núcleo no encontrado - funcionando en modo standalone${NC}"
        echo -e "${YELLOW}💡 Integración completa requiere acceso al proyecto principal${NC}"
    fi
}

# Iniciar servicios en background
start_background_services() {
    echo -e "${BLUE}🔄 Iniciando servicios en background...${NC}"
    
    # Iniciar watcher si está disponible
    if [[ -f "$SCRIPT_DIR/watcher.py" ]]; then
        echo -e "${CYAN}👁️ Iniciando monitor de logs...${NC}"
        python3 "$SCRIPT_DIR/watcher.py" "$SCRIPT_DIR" &
        echo $! > "$SCRIPT_DIR/log/watcher.pid"
        echo -e "${GREEN}✅ Monitor activo (PID: $!)${NC}"
    fi
    
    # Crear sesión tmux principal si está disponible
    if command -v tmux &>/dev/null; then
        tmux has-session -t "nethunter-agent" 2>/dev/null || {
            tmux new-session -d -s "nethunter-agent" -c "$SCRIPT_DIR"
            echo -e "${GREEN}✅ Sesión tmux creada: nethunter-agent${NC}"
        }
    fi
}

# Limpiar procesos al salir
cleanup_on_exit() {
    echo -e "\n${YELLOW}🛑 Deteniendo agente NetHunter...${NC}"
    
    # Matar watcher si existe
    if [[ -f "$SCRIPT_DIR/log/watcher.pid" ]]; then
        local pid=$(cat "$SCRIPT_DIR/log/watcher.pid" 2>/dev/null)
        if [[ -n "$pid" ]]; then
            kill "$pid" 2>/dev/null
            rm -f "$SCRIPT_DIR/log/watcher.pid"
            echo -e "${YELLOW}🔌 Monitor de logs detenido${NC}"
        fi
    fi
    
    echo -e "${GREEN}👋 ¡Agente NetHunter desconectado!${NC}"
    exit 0
}

# Capturar señales para limpieza
trap cleanup_on_exit SIGINT SIGTERM EXIT

# Mostrar información del sistema
show_system_info() {
    echo -e "${BLUE}📊 INFORMACIÓN DEL SISTEMA:${NC}"
    echo -e "   ${CYAN}Usuario:${NC} $(whoami)"
    echo -e "   ${CYAN}Host:${NC} $(hostname)"
    echo -e "   ${CYAN}SO:${NC} $(uname -o)"
    echo -e "   ${CYAN}Kernel:${NC} $(uname -r)"
    echo -e "   ${CYAN}Arquitectura:${NC} $(uname -m)"
    echo -e "   ${CYAN}Directorio:${NC} $SCRIPT_DIR"
    echo ""
}

# Test rápido de funcionalidades
quick_functionality_test() {
    echo -e "${BLUE}🧪 Test rápido de funcionalidades...${NC}"
    
    # Test brain.sh
    if [[ -f "$SCRIPT_DIR/brain.sh" ]]; then
        local test_result=$("$SCRIPT_DIR/brain.sh" "test system" "startup_test" 2>/dev/null)
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ Brain procesando correctamente${NC}"
        else
            echo -e "${YELLOW}⚠️ Brain con advertencias${NC}"
        fi
    fi
    
    # Test executor.sh
    if [[ -f "$SCRIPT_DIR/executor.sh" ]]; then
        "$SCRIPT_DIR/executor.sh" "echo 'test'" >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ Executor funcionando${NC}"
        else
            echo -e "${YELLOW}⚠️ Executor con advertencias${NC}"
        fi
    fi
    
    # Test OCR
    if [[ -f "$SCRIPT_DIR/ocr/ocr_enhanced.py" ]]; then
        python3 -c "import sys; sys.path.append('$SCRIPT_DIR'); from ocr.ocr_enhanced import EnhancedOCR; print('OCR OK')" 2>/dev/null
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ OCR disponible${NC}"
        else
            echo -e "${YELLOW}⚠️ OCR con dependencias faltantes${NC}"
        fi
    fi
    
    echo -e "${GREEN}✅ Tests completados${NC}"
    echo ""
}

# Función principal
main() {
    show_startup_banner
    
    echo -e "${PURPLE}🚀 Iniciando $AGENT_NAME...${NC}"
    echo ""
    
    # Verificaciones y setup
    if ! check_dependencies; then
        echo -e "${RED}❌ No se puede continuar sin dependencias críticas${NC}"
        exit 1
    fi
    
    setup_environment
    check_nucleus_integration
    show_system_info
    quick_functionality_test
    start_background_services
    
    echo -e "${GREEN}🎉 Agente NetHunter completamente inicializado${NC}"
    echo -e "${CYAN}💡 Transfiriendo control a interfaz interactiva...${NC}"
    echo ""
    
    # Transferir control a la interfaz principal
    if [[ -f "$SCRIPT_DIR/interface.sh" ]]; then
        exec "$SCRIPT_DIR/interface.sh"
    else
        echo -e "${RED}❌ interface.sh no encontrado${NC}"
        echo -e "${YELLOW}💡 Ejecutar manualmente: ./interface.sh${NC}"
        exit 1
    fi
}

# Verificar argumentos de línea de comandos
case "${1:-}" in
    "--help"|"-h")
        echo "Uso: $0 [opciones]"
        echo "Opciones:"
        echo "  --help, -h     Mostrar esta ayuda"
        echo "  --check-only   Solo verificar dependencias"
        echo "  --no-background No iniciar servicios en background"
        exit 0
        ;;
    "--check-only")
        check_dependencies
        exit $?
        ;;
    "--no-background")
        # Deshabilitar servicios en background
        start_background_services() { echo "Background services disabled"; }
        ;;
esac

# Ejecutar función principal
main "$@"