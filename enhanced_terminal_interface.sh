#!/bin/bash
# Enhanced Terminal Interface - Versión final con barra superior y teclado español
# Interfaz completa con reloj, monitoreo, chat natural y teclado virtual

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colores y estilos
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
SMALL='\033[2m'  # Texto pequeño para barra superior
NC='\033[0m'

# Estado del sistema de voz
VOICE_ENABLED=true
KEYBOARD_MODE=false

# Configuración de sesión tmux mejorada
SESSION_NAME="nethunter-enhanced"
WINDOW_STATUS="status"
WINDOW_MAIN="main"
WINDOW_MONITOR="monitor"
WINDOW_TOOLS="tools"
WINDOW_OCR="visual"

# Función para crear barra de estado superior compacta
create_status_bar() {
    local window_name="$1"
    
    # Configurar barra superior con información compacta
    tmux set-option -t "$SESSION_NAME:$window_name" status-position top
    tmux set-option -t "$SESSION_NAME:$window_name" status-style "bg=#1a1a1a,fg=#e6e6e6"
    tmux set-option -t "$SESSION_NAME:$window_name" status-left-length 80
    tmux set-option -t "$SESSION_NAME:$window_name" status-right-length 60
    
    # Lado izquierdo: Ubicación y estado
    tmux set-option -t "$SESSION_NAME:$window_name" status-left "#[bg=#ff6b35,fg=#1a1a1a,bold] 🛡️ #[bg=#2d2d2d,fg=#ff6b35] #S:#W #[bg=#1a1a1a,fg=#2d2d2d]#[fg=#7bc96f] 📍 #(pwd | sed 's|.*/||') "
    
    # Lado derecho: Reloj, CPU, RAM, Temp
    tmux set-option -t "$SESSION_NAME:$window_name" status-right "#[fg=#5aa7e4]🌡️#(sensors 2>/dev/null | grep 'Core 0' | awk '{print \$3}' | head -1 || echo '45°C') #[fg=#c678dd]💾#(free | awk '/^Mem:/{printf \"%.0f%%\", \$3/\$2 * 100.0}') #[fg=#7bc96f]🖥️#(top -bn1 | grep 'Cpu(s)' | awk '{print \$2}' | cut -d'%' -f1)% #[bg=#ff6b35,fg=#1a1a1a,bold] 🕐 %H:%M:%S "
    
    # Actualizar cada segundo
    tmux set-option -t "$SESSION_NAME:$window_name" status-interval 1
}

# Crear ventana de estado superior dedicada
create_status_window() {
    echo -e "${BLUE}📊 Creando ventana de estado superior...${NC}"
    
    # Crear ventana de estado muy pequeña
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_STATUS" -c "$SCRIPT_DIR"
    
    # Configurar ventana de estado como panel pequeño
    tmux send-keys -t "$SESSION_NAME:$WINDOW_STATUS" "clear" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_STATUS" "echo -e '${SMALL}${CYAN}╔══════════════════════════════════════════════════════════════════════════════════════╗${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_STATUS" "while true; do echo -ne '${SMALL}${CYAN}║${NC} ${SMALL}🕐 \$(date +\"%H:%M:%S\") ${BLUE}📍 \$(basename \$PWD) ${GREEN}🌡️ \$(sensors 2>/dev/null | grep \"Core 0\" | awk \"{print \\$3}\" | head -1 || echo \"45°C\") ${PURPLE}💾 \$(free | awk \"/^Mem:/{printf \\\"%.0f%%\\\", \\$3/\\$2 * 100.0}\") ${CYAN}🖥️ \$(top -bn1 | grep \"Cpu(s)\" | awk \"{print \\$2}\" | cut -d\"%\" -f1)% ${SMALL}${CYAN}║${NC}\\r'; sleep 1; done"
}

# Crear interfaz de chat natural mejorada
create_natural_chat_interface() {
    local window_name="$1"
    local panel_id="$2"
    
    # Panel de chat con entrada natural y respuesta contextual
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${CYAN}💬 CHAT NATURAL - NÚCLEO RAZONBILSTRO${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${GREEN}🎤 Modo: Voz Activa | 🎯 Estado: TTY/STL Habilitado${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${YELLOW}💡 Comandos de voz: \"mano a teclado\" | \"voz a teclado\"${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${DIM}════════════════════════════════════════════════════════${NC}'" Enter
    
    # Simular conversación natural
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${BLUE}👤 Usuario:${NC} Necesito escanear la red local'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${PURPLE}🧠 Ruth Shell:${NC} Analizado. Te sugiero nmap para descubrimiento.'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${GREEN}🎯 Contexto:${NC} Red doméstica, escaneo no intrusivo'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo ''" Enter
}

# Crear terminal de comandos separado
create_command_terminal() {
    local window_name="$1"
    local panel_id="$2"
    
    # Terminal dedicado para comandos y código
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${RED}⚡ TERMINAL DE COMANDOS${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${YELLOW}📝 Solo comandos y código - Respuestas técnicas${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo -e '${GREEN}✅ Comando sugerido:${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo 'nmap -sn 192.168.1.0/24  # Descubrir hosts activos'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo 'nmap -sV -sC 192.168.1.1  # Escaneo detallado del router'" Enter
    tmux send-keys -t "$SESSION_NAME:$window_name.$panel_id" "echo ''" Enter
}

# Crear teclado virtual español completo
create_virtual_keyboard() {
    local window_name="$1"
    
    tmux new-window -t "$SESSION_NAME" -n "keyboard" -c "$SCRIPT_DIR"
    
    # Teclado QWERTY español con símbolos y emojis
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${CYAN}⌨️ TECLADO VIRTUAL ESPAÑOL - QWERTY${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${YELLOW}🔤 Modo: Táctil | 🎤 Voz: $([[ $VOICE_ENABLED == true ]] && echo \"Activa\" || echo \"Inactiva\")${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo ''" Enter
    
    # Fila numérica con símbolos
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}┌─────────────────────────────────────────────────────────────────┐${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}│${NC} ${GREEN}1!${NC} ${GREEN}2\"${NC} ${GREEN}3·${NC} ${GREEN}4\$${NC} ${GREEN}5%${NC} ${GREEN}6&${NC} ${GREEN}7/${NC} ${GREEN}8(${NC} ${GREEN}9)${NC} ${GREEN}0=${NC} ${GREEN}'?${NC} ${GREEN}¡¿${NC} ${RED}⌫${NC} ${BOLD}│${NC}'" Enter
    
    # Fila QWERTY
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}├─────────────────────────────────────────────────────────────────┤${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}│${NC} ${BLUE}Q${NC} ${BLUE}W${NC} ${BLUE}E${NC} ${BLUE}R${NC} ${BLUE}T${NC} ${BLUE}Y${NC} ${BLUE}U${NC} ${BLUE}I${NC} ${BLUE}O${NC} ${BLUE}P${NC} ${PURPLE}\`^${NC} ${PURPLE}+*${NC} ${YELLOW}⏎${NC}    ${BOLD}│${NC}'" Enter
    
    # Fila ASDF
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}├─────────────────────────────────────────────────────────────────┤${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}│${NC} ${CYAN}🔒${NC} ${BLUE}A${NC} ${BLUE}S${NC} ${BLUE}D${NC} ${BLUE}F${NC} ${BLUE}G${NC} ${BLUE}H${NC} ${BLUE}J${NC} ${BLUE}K${NC} ${BLUE}L${NC} ${PURPLE}Ñ${NC} ${PURPLE}´¨${NC} ${PURPLE}Ç${NC}     ${BOLD}│${NC}'" Enter
    
    # Fila ZXCV
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}├─────────────────────────────────────────────────────────────────┤${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}│${NC} ${CYAN}⇧${NC}  ${BLUE}Z${NC} ${BLUE}X${NC} ${BLUE}C${NC} ${BLUE}V${NC} ${BLUE}B${NC} ${BLUE}N${NC} ${BLUE}M${NC} ${PURPLE},;${NC} ${PURPLE}.:${NC} ${PURPLE}-_${NC}    ${CYAN}⇧${NC}  ${BOLD}│${NC}'" Enter
    
    # Barra espaciadora y controles
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}├─────────────────────────────────────────────────────────────────┤${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}│${NC} ${YELLOW}Ctrl${NC} ${YELLOW}🌐${NC} ${YELLOW}Alt${NC}     ${RED}████ ESPACIO ████${NC}     ${YELLOW}Alt${NC} ${YELLOW}🌐${NC} ${YELLOW}Ctrl${NC} ${BOLD}│${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${BOLD}└─────────────────────────────────────────────────────────────────┘${NC}'" Enter
    
    # Panel de emojis y símbolos especiales
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo ''" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${CYAN}😀 EMOJIS RÁPIDOS:${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${YELLOW}😀😂🤔😎🔥💯⚡🚀🎯🛡️🔍💻📱🌐🔧⚙️${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo ''" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${PURPLE}⚡ SÍMBOLOS TÉCNICOS:${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${GREEN}→ ← ↑ ↓ ⇒ ⇐ ⇑ ⇓ ∞ ≈ ≠ ≤ ≥ ± × ÷ √ ∫ ∑ π α β γ δ${NC}'" Enter
    
    # Controles de voz
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo ''" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${RED}🎤 CONTROLES DE VOZ:${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${GREEN}▶️ \"mano a teclado\"${NC} - Desactivar voz, activar teclado'" Enter
    tmux send-keys -t "$SESSION_NAME:keyboard" "echo -e '${GREEN}▶️ \"voz a teclado\"${NC} - Reactivar entrada por voz'" Enter
}

# Función para alternar modo de voz
toggle_voice_mode() {
    if [[ "$VOICE_ENABLED" == true ]]; then
        VOICE_ENABLED=false
        KEYBOARD_MODE=true
        echo -e "${YELLOW}🖐️ Modo teclado activado - Voz desactivada${NC}"
    else
        VOICE_ENABLED=true
        KEYBOARD_MODE=false
        echo -e "${GREEN}🎤 Modo voz activado - Teclado desactivado${NC}"
    fi
}

# Crear layout principal mejorado
create_enhanced_layout() {
    echo -e "${BLUE}🚀 Creando interfaz NetHunter mejorada...${NC}"
    
    # Crear sesión principal
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo -e "${YELLOW}♻️ Reconectando a sesión mejorada...${NC}"
        tmux attach-session -t "$SESSION_NAME"
        return 0
    fi
    
    # Nueva sesión tmux
    tmux new-session -d -s "$SESSION_NAME" -x 140 -y 45
    
    # Ventana 0 - Interfaz principal mejorada
    tmux rename-window -t "$SESSION_NAME:0" "$WINDOW_MAIN"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN" "cd '$SCRIPT_DIR'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN" "clear" Enter
    
    # Dividir ventana principal en configuración específica
    # Panel superior: Chat natural (60% altura)
    tmux split-window -t "$SESSION_NAME:$WINDOW_MAIN" -v -p 40
    
    # Panel inferior: Dividir horizontalmente para comandos y teclado
    tmux split-window -t "$SESSION_NAME:$WINDOW_MAIN.1" -h -p 50
    
    # Panel derecho superior: Monitor compacto
    tmux split-window -t "$SESSION_NAME:$WINDOW_MAIN.0" -h -p 25
    
    # Configurar paneles
    # Panel 0: Chat natural (principal)
    create_natural_chat_interface "$WINDOW_MAIN" "0"
    
    # Panel 1: Monitor de estado compacto
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.1" "echo -e '${SMALL}${GREEN}📊 MONITOR COMPACTO${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.1" "watch -n 1 'echo \"${SMALL}💾 RAM: \$(free | awk \"/^Mem:/{printf \\\"%.0f%%\\\", \$3/\$2 * 100.0}\") 🖥️ CPU: \$(top -bn1 | grep \"Cpu(s)\" | awk \"{print \$2}\" | cut -d\"%\" -f1)% 🌡️ \$(sensors 2>/dev/null | grep \"Core 0\" | awk \"{print \$3}\" | head -1 || echo \"45°C\")\"'"
    
    # Panel 2: Terminal de comandos
    create_command_terminal "$WINDOW_MAIN" "2"
    
    # Panel 3: Teclado virtual integrado
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.3" "echo -e '${CYAN}⌨️ TECLADO VIRTUAL${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.3" "echo -e '${GREEN}Q W E R T Y U I O P${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.3" "echo -e '${GREEN}A S D F G H J K L Ñ${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.3" "echo -e '${GREEN}Z X C V B N M , . -${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.3" "echo -e '${YELLOW}🎤 Voz: Activa | 🖐️ Táctil: Disponible${NC}'" Enter
    
    # Ventana 1 - Monitor avanzado (igual que antes)
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_MONITOR"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR" "cd '$SCRIPT_DIR'" Enter
    tmux split-window -t "$SESSION_NAME:$WINDOW_MONITOR" -v -p 50
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR.0" "python3 watcher.py '$SCRIPT_DIR'"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR.1" "python3 metacognition.py '$SCRIPT_DIR'"
    
    # Ventana 2 - Herramientas (igual que antes)
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_TOOLS"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS" "cd '$SCRIPT_DIR'" Enter
    tmux split-window -t "$SESSION_NAME:$WINDOW_TOOLS" -h -p 50
    tmux split-window -t "$SESSION_NAME:$WINDOW_TOOLS.0" -v -p 50
    tmux split-window -t "$SESSION_NAME:$WINDOW_TOOLS.2" -v -p 50
    
    # Ventana 3 - OCR Visual (igual que antes)
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_OCR"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR" "cd '$SCRIPT_DIR'" Enter
    tmux split-window -t "$SESSION_NAME:$WINDOW_OCR" -h -p 40
    
    # Crear teclado virtual completo en ventana separada
    create_virtual_keyboard
    
    # Configurar barra de estado superior para todas las ventanas
    for window in "$WINDOW_MAIN" "$WINDOW_MONITOR" "$WINDOW_TOOLS" "$WINDOW_OCR" "keyboard"; do
        create_status_bar "$window"
    done
    
    # Seleccionar ventana principal
    tmux select-window -t "$SESSION_NAME:$WINDOW_MAIN"
    tmux select-pane -t "$SESSION_NAME:$WINDOW_MAIN.0"
    
    echo -e "${GREEN}✅ Interfaz NetHunter mejorada creada exitosamente${NC}"
}

# Función principal
main() {
    local mode="${1:-enhanced}"
    
    case "$mode" in
        "keyboard")
            create_virtual_keyboard
            ;;
        "voice-toggle")
            toggle_voice_mode
            ;;
        *)
            if ! command -v tmux &>/dev/null; then
                echo -e "${RED}❌ tmux no encontrado. Instalar: apt install tmux${NC}"
                exit 1
            fi
            
            create_enhanced_layout
            
            echo -e "${CYAN}🎯 INTERFAZ NETHUNTER MEJORADA${NC}"
            echo -e "${GREEN}📱 Ventanas: Main | Monitor | Tools | Visual | Keyboard${NC}"
            echo -e "${YELLOW}🎤 Comandos de voz: 'mano a teclado' | 'voz a teclado'${NC}"
            echo -e "${PURPLE}⌨️ Teclado: QWERTY español completo con emojis${NC}"
            echo ""
            
            # Conectar a la sesión
            tmux attach-session -t "$SESSION_NAME"
            ;;
    esac
}

# Ejecutar
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi