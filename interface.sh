#!/bin/bash
# Interface.sh - CLI interactiva embebida en shell con TTY
# Interfaz principal de interacción con el agente NetHunter

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/log"
CONFIG_DIR="$SCRIPT_DIR/config"

# Colores y estilos
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Configuración de TTY
ORIGINAL_SETTINGS=$(stty -g)
INTERFACE_ACTIVE=false

# Banner del agente
show_banner() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}${BOLD}          🧠 AGENTE NETHUNTER + NÚCLEO RAZONBILSTRO           ${NC}${CYAN}║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC} ${GREEN}Sistema de IA Multi-Especializado para Seguridad${NC}             ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC} ${YELLOW}• 7 Dominios Especializados  • OCR/TTS Integrado${NC}            ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC} ${YELLOW}• Comandos Inteligentes      • Ejecución Segura${NC}             ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Configuración de TTY para input interactivo
setup_tty() {
    # Configurar TTY para input caracter por caracter
    stty -echo -icanon min 1 time 0
    INTERFACE_ACTIVE=true
}

# Restaurar configuración TTY
restore_tty() {
    stty "$ORIGINAL_SETTINGS"
    INTERFACE_ACTIVE=false
}

# Función de limpieza al salir
cleanup() {
    restore_tty
    echo -e "\n${YELLOW}👋 ¡Hasta luego! Agente NetHunter desconectado.${NC}"
    exit 0
}

# Capturar señales para limpieza
trap cleanup SIGINT SIGTERM EXIT

# Prompt personalizado con estado del sistema
show_prompt() {
    local timestamp=$(date '+%H:%M:%S')
    local user=$(whoami)
    local host=$(hostname)
    local pwd_short=$(basename "$PWD")
    
    # Estado de servicios críticos
    local services_status="🟢"
    if ! pgrep -f "watcher.py" > /dev/null; then
        services_status="🟡"
    fi
    
    echo -ne "\n${DIM}[$timestamp]${NC} "
    echo -ne "${PURPLE}$user${NC}@${BLUE}$host${NC}:"
    echo -ne "${GREEN}$pwd_short${NC} "
    echo -ne "$services_status "
    echo -ne "${BOLD}NetHunter>${NC} "
}

# Autocompletado inteligente
get_suggestions() {
    local input="$1"
    local suggestions=()
    
    # Comandos NetHunter comunes
    local nethunter_commands=(
        "nmap -sS"
        "nmap -sV -sC"
        "sqlmap -u"
        "john --wordlist"
        "hashcat -m"
        "hydra -l"
        "nikto -h"
        "dirb"
        "gobuster"
        "metasploit"
        "burpsuite"
    )
    
    # Comandos del sistema
    local system_commands=(
        "ls -la"
        "ps aux"
        "netstat -tulpn"
        "systemctl status"
        "journalctl -f"
        "find / -name"
        "grep -r"
        "chmod +x"
        "ssh -i"
        "scp -r"
    )
    
    # Buscar coincidencias
    for cmd in "${nethunter_commands[@]}" "${system_commands[@]}"; do
        if [[ "$cmd" == "$input"* ]]; then
            suggestions+=("$cmd")
        fi
    done
    
    # Mostrar sugerencias
    if [[ ${#suggestions[@]} -gt 0 && ${#suggestions[@]} -le 5 ]]; then
        echo -e "\n${DIM}Sugerencias:${NC}"
        for i in "${!suggestions[@]}"; do
            echo -e "  ${YELLOW}$((i+1)).${NC} ${suggestions[$i]}"
        done
    fi
}

# Procesamiento de comandos especiales
process_special_command() {
    local cmd="$1"
    
    case "$cmd" in
        "help"|"?")
            show_help
            return 0
            ;;
        "status")
            show_system_status
            return 0
            ;;
        "history")
            show_command_history
            return 0
            ;;
        "clear"|"cls")
            clear
            show_banner
            return 0
            ;;
        "ocr")
            trigger_ocr_capture
            return 0
            ;;
        "scan")
            start_network_scan
            return 0
            ;;
        "tools")
            show_available_tools
            return 0
            ;;
        "exit"|"quit"|"q")
            cleanup
            ;;
        *)
            return 1
            ;;
    esac
}

# Mostrar ayuda
show_help() {
    echo -e "\n${BOLD}🔧 COMANDOS ESPECIALES DEL AGENTE:${NC}"
    echo -e "  ${GREEN}help, ?${NC}      - Mostrar esta ayuda"
    echo -e "  ${GREEN}status${NC}       - Estado del sistema"
    echo -e "  ${GREEN}history${NC}      - Historial de comandos"
    echo -e "  ${GREEN}clear, cls${NC}   - Limpiar pantalla"
    echo -e "  ${GREEN}ocr${NC}          - Captura OCR de pantalla"
    echo -e "  ${GREEN}scan${NC}         - Escaneo de red rápido"
    echo -e "  ${GREEN}tools${NC}        - Herramientas disponibles"
    echo -e "  ${GREEN}exit, quit, q${NC} - Salir del agente"
    
    echo -e "\n${BOLD}🎯 EJEMPLOS DE USO:${NC}"
    echo -e "  ${CYAN}escanear 192.168.1.1${NC}     - Análisis inteligente de objetivo"
    echo -e "  ${CYAN}buscar vulnerabilidades${NC}  - Sugerir herramientas apropiadas"
    echo -e "  ${CYAN}analizar puerto 80${NC}       - Análisis específico de puerto"
    echo -e "  ${CYAN}compilar exploit.c${NC}       - Compilación con parámetros óptimos"
}

# Estado del sistema
show_system_status() {
    echo -e "\n${BOLD}📊 ESTADO DEL SISTEMA:${NC}"
    
    # Verificar procesos del agente
    if pgrep -f "watcher.py" > /dev/null; then
        echo -e "  ${GREEN}✓${NC} Monitor de logs activo"
    else
        echo -e "  ${RED}✗${NC} Monitor de logs inactivo"
    fi
    
    # Verificar logs
    if [[ -f "$LOG_DIR/execution_history.log" ]]; then
        local log_size=$(du -h "$LOG_DIR/execution_history.log" | cut -f1)
        echo -e "  ${GREEN}✓${NC} Log de ejecución: $log_size"
    fi
    
    # Verificar conectividad
    if ping -c 1 8.8.8.8 &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Conectividad de red OK"
    else
        echo -e "  ${RED}✗${NC} Problemas de conectividad"
    fi
    
    # Memoria y CPU
    local mem_usage=$(free | awk '/^Mem:/{printf "%.1f%%", $3/$2 * 100.0}')
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    
    echo -e "  ${BLUE}📊${NC} CPU: ${cpu_usage}% | RAM: $mem_usage"
}

# Historial de comandos
show_command_history() {
    if [[ -f "$LOG_DIR/execution_history.log" ]]; then
        echo -e "\n${BOLD}📋 ÚLTIMOS COMANDOS:${NC}"
        tail -10 "$LOG_DIR/execution_history.log" | while read line; do
            echo -e "  ${DIM}$line${NC}"
        done
    else
        echo -e "\n${YELLOW}⚠️ No hay historial disponible${NC}"
    fi
}

# Captura OCR
trigger_ocr_capture() {
    echo -e "\n${BLUE}📸 Iniciando captura OCR...${NC}"
    
    if command -v import &>/dev/null && command -v tesseract &>/dev/null; then
        # Captura de pantalla
        import -window root /tmp/agent_screen_capture.png 2>/dev/null
        
        # OCR
        local text=$(tesseract /tmp/agent_screen_capture.png stdout 2>/dev/null)
        
        if [[ -n "$text" ]]; then
            echo -e "${GREEN}📝 Texto detectado:${NC}"
            echo "$text" | head -5
            
            # Procesar con el brain
            echo -e "\n${YELLOW}🧠 Analizando con Núcleo Razonbilstro...${NC}"
            local result=$("$SCRIPT_DIR/brain.sh" "$text" "ocr_context")
            echo -e "${CYAN}💡 Sugerencia:${NC} $result"
        else
            echo -e "${RED}❌ No se detectó texto en la captura${NC}"
        fi
    else
        echo -e "${RED}❌ OCR no disponible (falta imagemagick o tesseract)${NC}"
    fi
}

# Escaneo rápido de red
start_network_scan() {
    echo -e "\n${BLUE}🔍 Iniciando escaneo rápido de red...${NC}"
    
    # Detectar interfaz de red activa
    local interface=$(ip route | grep default | awk '{print $5}' | head -1)
    local network=$(ip route | grep "$interface" | grep -v default | awk '{print $1}' | head -1)
    
    if [[ -n "$network" ]]; then
        echo -e "${GREEN}🌐 Red detectada:${NC} $network"
        echo -e "${YELLOW}⚡ Ejecutando nmap rápido...${NC}"
        
        # Ejecutar en background
        "$SCRIPT_DIR/executor.sh" "nmap -sn $network" "background"
    else
        echo -e "${RED}❌ No se pudo detectar la red local${NC}"
    fi
}

# Herramientas disponibles
show_available_tools() {
    echo -e "\n${BOLD}🛠️ HERRAMIENTAS NETHUNTER DISPONIBLES:${NC}"
    
    local tools=(
        "nmap:Escáner de puertos y red"
        "sqlmap:Testing de inyección SQL"
        "john:Cracker de contraseñas"
        "hashcat:Cracker de hashes"
        "hydra:Ataque de fuerza bruta"
        "nikto:Scanner web"
        "dirb:Enumeración de directorios"
        "metasploit:Framework de exploits"
    )
    
    for tool_info in "${tools[@]}"; do
        local tool=$(echo "$tool_info" | cut -d':' -f1)
        local desc=$(echo "$tool_info" | cut -d':' -f2)
        
        if command -v "$tool" &>/dev/null; then
            echo -e "  ${GREEN}✓${NC} ${BOLD}$tool${NC} - $desc"
        else
            echo -e "  ${RED}✗${NC} ${DIM}$tool - $desc (no instalado)${NC}"
        fi
    done
}

# Input loop principal con TTY embebido
main_loop() {
    show_banner
    
    # Iniciar watcher en background
    python3 "$SCRIPT_DIR/watcher.py" "$SCRIPT_DIR" &
    local watcher_pid=$!
    
    echo -e "${GREEN}🚀 Agente NetHunter activado${NC}"
    echo -e "${YELLOW}💡 Escribe 'help' para ver comandos disponibles${NC}"
    
    local input=""
    local char=""
    
    while true; do
        show_prompt
        input=""
        
        # Leer input caracter por caracter
        while true; do
            read -n 1 char
            
            case "$char" in
                $'\n'|$'\r')  # Enter
                    echo ""
                    break
                    ;;
                $'\177'|$'\b')  # Backspace
                    if [[ ${#input} -gt 0 ]]; then
                        input="${input%?}"
                        echo -ne "\b \b"
                    fi
                    ;;
                $'\t')  # Tab - autocompletado
                    get_suggestions "$input"
                    show_prompt
                    echo -n "$input"
                    ;;
                $'\x03')  # Ctrl+C
                    echo ""
                    cleanup
                    ;;
                *)
                    if [[ -n "$char" && "$char" != $'\x1b' ]]; then
                        input+="$char"
                        echo -n "$char"
                    fi
                    ;;
            esac
        done
        
        # Procesar comando si no está vacío
        if [[ -n "$input" ]]; then
            # Verificar comandos especiales primero
            if ! process_special_command "$input"; then
                # Procesar con brain y executor
                echo -e "${DIM}🤔 Procesando: $input${NC}"
                
                local brain_result=$("$SCRIPT_DIR/brain.sh" "$input" "interactive")
                
                if [[ -n "$brain_result" && "$brain_result" != "echo"* ]]; then
                    echo -e "${YELLOW}💡 Comando sugerido:${NC} $brain_result"
                    read -p "¿Ejecutar? (Y/n): " -n 1 confirm
                    echo ""
                    
                    if [[ "$confirm" =~ ^[Yy]$|^$ ]]; then
                        "$SCRIPT_DIR/executor.sh" "$brain_result"
                    fi
                else
                    echo -e "${RED}❓ No se pudo procesar el comando${NC}"
                fi
            fi
        fi
    done
}

# Función principal
main() {
    # Verificar dependencias
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}❌ Python3 no encontrado${NC}"
        exit 1
    fi
    
    # Setup TTY
    setup_tty
    
    # Iniciar loop principal
    main_loop
}

# Verificar si se ejecuta directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi