#!/bin/bash
# Executor.sh - Ejecutor de comandos con validación y logging
# Corre comandos reales con seguridad y monitoreo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/log"
CONFIG_DIR="$SCRIPT_DIR/config"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuración de seguridad
SAFE_COMMANDS_FILE="$CONFIG_DIR/safe_commands.list"
DANGEROUS_COMMANDS_FILE="$CONFIG_DIR/dangerous_commands.list"
EXECUTION_LOG="$LOG_DIR/execution_history.log"

# Crear archivos de configuración si no existen
setup_security_config() {
    mkdir -p "$CONFIG_DIR"
    
    if [[ ! -f "$SAFE_COMMANDS_FILE" ]]; then
        cat > "$SAFE_COMMANDS_FILE" << EOF
# Comandos seguros para ejecución automática
ls
pwd
whoami
id
uname
date
ps
top
htop
netstat
ss
df
free
cat
grep
find
locate
which
whereis
nmap
nikto
dirb
gobuster
sqlmap
john
hashcat
hydra
metasploit
EOF
    fi
    
    if [[ ! -f "$DANGEROUS_COMMANDS_FILE" ]]; then
        cat > "$DANGEROUS_COMMANDS_FILE" << EOF
# Comandos que requieren confirmación
rm
rmdir
dd
mkfs
fdisk
parted
halt
shutdown
reboot
init
kill
killall
pkill
chmod
chown
mount
umount
iptables
ufw
systemctl
service
EOF
    fi
}

# Función de logging de ejecución
log_execution() {
    local command="$1"
    local exit_code="$2"
    local output="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] CMD: $command | EXIT: $exit_code" >> "$EXECUTION_LOG"
    if [[ $exit_code -ne 0 ]]; then
        echo "[$timestamp] ERROR: $output" >> "$EXECUTION_LOG"
    fi
}

# Validación de seguridad
validate_command() {
    local command="$1"
    local base_cmd=$(echo "$command" | awk '{print $1}')
    
    # Verificar si está en lista de comandos seguros
    if grep -q "^$base_cmd$" "$SAFE_COMMANDS_FILE" 2>/dev/null; then
        return 0  # Comando seguro
    fi
    
    # Verificar si está en lista de comandos peligrosos
    if grep -q "^$base_cmd$" "$DANGEROUS_COMMANDS_FILE" 2>/dev/null; then
        return 2  # Comando peligroso, requiere confirmación
    fi
    
    return 1  # Comando desconocido
}

# Ejecución con monitoreo
execute_command() {
    local command="$1"
    local force_execute="$2"
    
    echo -e "${BLUE}🔍 Validando comando:${NC} $command"
    
    validate_command "$command"
    local validation_result=$?
    
    case $validation_result in
        0)
            echo -e "${GREEN}✅ Comando seguro - Ejecutando...${NC}"
            ;;
        1)
            echo -e "${YELLOW}⚠️ Comando desconocido${NC}"
            if [[ "$force_execute" != "force" ]]; then
                echo -e "${RED}❌ Ejecución cancelada por seguridad${NC}"
                return 1
            fi
            ;;
        2)
            echo -e "${RED}⚠️ Comando potencialmente peligroso${NC}"
            if [[ "$force_execute" != "force" ]]; then
                read -p "¿Continuar? (y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    echo -e "${RED}❌ Ejecución cancelada por el usuario${NC}"
                    return 1
                fi
            fi
            ;;
    esac
    
    # Ejecutar comando con timeout y captura de output
    echo -e "${CYAN}⚡ Ejecutando:${NC} $command"
    local start_time=$(date +%s)
    
    # Crear sesión tmux para el comando si es complejo
    if [[ "$command" =~ (nmap|sqlmap|john|hashcat|hydra|metasploit) ]]; then
        local session_name="exec_$(date +%s)"
        tmux new-session -d -s "$session_name" "$command"
        echo -e "${YELLOW}📺 Comando ejecutado en sesión tmux: $session_name${NC}"
        echo -e "${YELLOW}💡 Usa 'tmux attach -t $session_name' para ver progreso${NC}"
        return 0
    fi
    
    # Ejecución normal con timeout
    local output
    local exit_code
    
    output=$(timeout 300 bash -c "$command" 2>&1)
    exit_code=$?
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # Logging
    log_execution "$command" "$exit_code" "$output"
    
    # Mostrar resultados
    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}✅ Comando ejecutado exitosamente (${duration}s)${NC}"
        echo "$output"
    elif [[ $exit_code -eq 124 ]]; then
        echo -e "${RED}⏰ Comando cancelado por timeout (5min)${NC}"
    else
        echo -e "${RED}❌ Error en ejecución (código: $exit_code)${NC}"
        echo "$output"
    fi
    
    return $exit_code
}

# Función de ejecución en background para herramientas de larga duración
execute_background() {
    local command="$1"
    local session_name="bg_$(date +%s)"
    
    echo -e "${BLUE}🔄 Ejecutando en background:${NC} $command"
    
    # Crear sesión screen persistente
    screen -dmS "$session_name" bash -c "
        echo 'Iniciando: $command'
        $command
        echo 'Comando completado. Presiona cualquier tecla para salir.'
        read
    "
    
    echo -e "${GREEN}✅ Sesión creada:${NC} $session_name"
    echo -e "${YELLOW}💡 Usa 'screen -r $session_name' para ver progreso${NC}"
    
    return 0
}

# Función principal
main() {
    local command="$1"
    local execution_mode="$2"  # normal, force, background
    
    if [[ -z "$command" ]]; then
        echo -e "${RED}❌ Error: Se requiere un comando${NC}"
        echo "Uso: $0 \"comando\" [normal|force|background]"
        exit 1
    fi
    
    # Setup inicial
    setup_security_config
    
    echo -e "${BLUE}🚀 Iniciando executor...${NC}"
    echo -e "${CYAN}📝 Comando:${NC} $command"
    echo -e "${CYAN}🔧 Modo:${NC} ${execution_mode:-normal}"
    
    # Ejecutar según modo
    case "${execution_mode:-normal}" in
        "background"|"bg")
            execute_background "$command"
            ;;
        "force")
            execute_command "$command" "force"
            ;;
        *)
            execute_command "$command"
            ;;
    esac
}

# Verificar si se ejecuta directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi