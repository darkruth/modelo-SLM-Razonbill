#!/bin/bash
# Terminal Multi-Ventana Interface - Kitty/tmux Integration
# Interfaz de terminal con múltiples paneles como la imagen de referencia

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
NC='\033[0m'

# Configuración de sesión tmux
SESSION_NAME="nethunter-workspace"
WINDOW_MAIN="main"
WINDOW_MONITOR="monitor"
WINDOW_TOOLS="tools"
WINDOW_OCR="visual"

# Verificar si estamos en Kitty
is_kitty_terminal() {
    [[ "$TERM" == "xterm-kitty" ]] || [[ -n "$KITTY_WINDOW_ID" ]]
}

# Configurar ventanas de Kitty si está disponible
setup_kitty_layout() {
    if is_kitty_terminal; then
        echo -e "${CYAN}🐱 Configurando layout optimizado para Kitty...${NC}"
        
        # Configurar tema oscuro para terminal
        if command -v kitty &>/dev/null; then
            # Crear configuración temporal de Kitty
            cat > "/tmp/kitty_nethunter.conf" << EOF
# NetHunter Kitty Configuration
background_opacity 0.95
background #1a1a1a
foreground #e6e6e6
cursor #ff6b35

# Colores para la interfaz
color0  #1a1a1a
color1  #ff6b35
color2  #7bc96f
color3  #eacd61
color4  #5aa7e4
color5  #c678dd
color6  #56d1dc
color7  #e6e6e6
color8  #5c6370
color9  #ff6b35
color10 #7bc96f
color11 #eacd61
color12 #5aa7e4
color13 #c678dd
color14 #56d1dc
color15 #ffffff

# Configuración de ventana
window_padding_width 8
tab_bar_style powerline
tab_powerline_style round
active_tab_background #ff6b35
inactive_tab_background #2d2d2d

# Font configuration
font_family JetBrains Mono
font_size 12.0
EOF
        fi
        return 0
    fi
    return 1
}

# Crear layout de tmux multi-ventana
create_tmux_layout() {
    echo -e "${BLUE}📊 Creando layout multi-ventana con tmux...${NC}"
    
    # Crear o conectar a sesión
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo -e "${YELLOW}♻️ Reconectando a sesión existente...${NC}"
        tmux attach-session -t "$SESSION_NAME"
        return 0
    fi
    
    # Crear nueva sesión tmux con layout complejo
    tmux new-session -d -s "$SESSION_NAME" -x 120 -y 40
    
    # Ventana principal (0) - Interfaz principal del agente
    tmux rename-window -t "$SESSION_NAME:0" "$WINDOW_MAIN"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN" "cd '$SCRIPT_DIR'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN" "clear" Enter
    
    # Dividir ventana principal horizontalmente 
    tmux split-window -t "$SESSION_NAME:$WINDOW_MAIN" -h -p 30
    
    # Dividir panel derecho verticalmente
    tmux split-window -t "$SESSION_NAME:$WINDOW_MAIN.1" -v -p 50
    
    # Panel 0: Interfaz principal del agente
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.0" "echo -e '${CYAN}🧠 AGENTE NETHUNTER - INTERFAZ PRINCIPAL${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.0" "./interface.sh" 
    
    # Panel 1: Monitor de sistema en tiempo real
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.1" "echo -e '${GREEN}📊 MONITOR DEL SISTEMA${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.1" "watch -n 2 'echo \"=== RECURSOS DEL SISTEMA ===\" && echo \"CPU: \$(top -bn1 | grep Cpu | cut -d\" \" -f2 | cut -d\"%\" -f1)%\" && echo \"RAM: \$(free | awk \"/^Mem:/{printf \\\"%.1f%%\\\", \$3/\$2 * 100.0}\")\" && echo \"=== PROCESOS NETHUNTER ===\" && ps aux | grep -E \"(nmap|sqlmap|john|hydra|metasploit)\" | grep -v grep | head -3'"
    
    # Panel 2: Log en tiempo real
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.2" "echo -e '${YELLOW}📋 LOGS EN TIEMPO REAL${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MAIN.2" "tail -f '$SCRIPT_DIR/log/execution_history.log' 2>/dev/null || echo 'Esperando logs...'"
    
    # Ventana 1 - Monitor avanzado con watcher
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_MONITOR"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR" "cd '$SCRIPT_DIR'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR" "echo -e '${PURPLE}👁️ MONITOR INTELIGENTE - WATCHER + METACOGNICION${NC}'" Enter
    
    # Dividir monitor en 2 paneles
    tmux split-window -t "$SESSION_NAME:$WINDOW_MONITOR" -v -p 50
    
    # Panel superior: Watcher
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR.0" "python3 watcher.py '$SCRIPT_DIR'"
    
    # Panel inferior: Metacognición
    tmux send-keys -t "$SESSION_NAME:$WINDOW_MONITOR.1" "python3 metacognition.py '$SCRIPT_DIR'"
    
    # Ventana 2 - Herramientas NetHunter
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_TOOLS"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS" "cd '$SCRIPT_DIR'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS" "echo -e '${RED}🛠️ HERRAMIENTAS NETHUNTER${NC}'" Enter
    
    # Crear sub-paneles para herramientas
    tmux split-window -t "$SESSION_NAME:$WINDOW_TOOLS" -h -p 50
    tmux split-window -t "$SESSION_NAME:$WINDOW_TOOLS.0" -v -p 50
    tmux split-window -t "$SESSION_NAME:$WINDOW_TOOLS.2" -v -p 50
    
    # Panel 0: Nmap
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.0" "echo -e '${CYAN}🔍 NMAP - SCANNER DE RED${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.0" "echo 'Ejemplos:'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.0" "echo '• nmap -sS 192.168.1.0/24'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.0" "echo '• nmap -sV -sC target.com'" Enter
    
    # Panel 1: SQLMap
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.1" "echo -e '${GREEN}💉 SQLMAP - INYECCION SQL${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.1" "echo 'Ejemplos:'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.1" "echo '• sqlmap -u \"http://target.com/page?id=1\"'" Enter
    
    # Panel 2: John/Hashcat
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.2" "echo -e '${YELLOW}🔐 JOHN/HASHCAT - CRACKING${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.2" "echo 'Ejemplos:'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.2" "echo '• john --wordlist=rockyou.txt hashes.txt'" Enter
    
    # Panel 3: Hydra
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.3" "echo -e '${PURPLE}⚡ HYDRA - FUERZA BRUTA${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.3" "echo 'Ejemplos:'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_TOOLS.3" "echo '• hydra -l admin -P passwords.txt ssh://target.com'" Enter
    
    # Ventana 3 - OCR Visual
    tmux new-window -t "$SESSION_NAME" -n "$WINDOW_OCR"
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR" "cd '$SCRIPT_DIR'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR" "echo -e '${CYAN}📸 INTERFAZ VISUAL - OCR + TTS${NC}'" Enter
    
    # Dividir ventana OCR
    tmux split-window -t "$SESSION_NAME:$WINDOW_OCR" -h -p 40
    
    # Panel izquierdo: OCR continuo
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR.0" "echo -e '${GREEN}🔍 OCR EN TIEMPO REAL${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR.0" "echo 'Comandos disponibles:'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR.0" "echo '• python3 ocr/ocr_enhanced.py --mode single'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR.0" "echo '• python3 ocr/ocr_enhanced.py --mode monitor'" Enter
    
    # Panel derecho: Análisis visual
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR.1" "echo -e '${YELLOW}🧠 ANÁLISIS VISUAL${NC}'" Enter
    tmux send-keys -t "$SESSION_NAME:$WINDOW_OCR.1" "echo 'Estado: Esperando captura...'" Enter
    
    # Configurar barra de estado personalizada
    tmux set-option -t "$SESSION_NAME" status-bg "#1a1a1a"
    tmux set-option -t "$SESSION_NAME" status-fg "#e6e6e6"
    tmux set-option -t "$SESSION_NAME" status-left "#[bg=#ff6b35,fg=#1a1a1a,bold] 🛡️ NetHunter #[bg=#1a1a1a,fg=#ff6b35]"
    tmux set-option -t "$SESSION_NAME" status-right "#[fg=#7bc96f]🧠 Núcleo #[fg=#5aa7e4]%H:%M #[fg=#c678dd]%d/%m"
    tmux set-option -t "$SESSION_NAME" status-left-length 20
    tmux set-option -t "$SESSION_NAME" status-right-length 30
    
    # Seleccionar ventana principal
    tmux select-window -t "$SESSION_NAME:$WINDOW_MAIN"
    tmux select-pane -t "$SESSION_NAME:$WINDOW_MAIN.0"
    
    echo -e "${GREEN}✅ Layout multi-ventana creado exitosamente${NC}"
    return 0
}

# Mostrar ayuda de navegación
show_navigation_help() {
    echo -e "${BOLD}🗺️ NAVEGACIÓN DEL WORKSPACE NETHUNTER:${NC}"
    echo ""
    echo -e "${CYAN}📱 VENTANAS DISPONIBLES:${NC}"
    echo -e "  ${GREEN}Ctrl+b 0${NC} - Interfaz Principal (Agente + Monitor + Logs)"
    echo -e "  ${GREEN}Ctrl+b 1${NC} - Monitor Avanzado (Watcher + Metacognición)"
    echo -e "  ${GREEN}Ctrl+b 2${NC} - Herramientas NetHunter (Nmap, SQLMap, etc.)"
    echo -e "  ${GREEN}Ctrl+b 3${NC} - Interfaz Visual (OCR + Análisis)"
    echo ""
    echo -e "${CYAN}🎮 COMANDOS TMUX ÚTILES:${NC}"
    echo -e "  ${YELLOW}Ctrl+b [${NC} - Modo scroll/copia"
    echo -e "  ${YELLOW}Ctrl+b z${NC} - Zoom/unzoom panel actual"
    echo -e "  ${YELLOW}Ctrl+b ;${NC} - Cambiar al panel anterior"
    echo -e "  ${YELLOW}Ctrl+b q${NC} - Mostrar números de panel"
    echo -e "  ${YELLOW}Ctrl+b w${NC} - Lista de ventanas"
    echo -e "  ${YELLOW}Ctrl+b d${NC} - Detach (mantener sesión activa)"
    echo ""
    echo -e "${CYAN}🔧 COMANDOS ESPECÍFICOS:${NC}"
    echo -e "  ${PURPLE}tmux attach -t $SESSION_NAME${NC} - Reconectar a sesión"
    echo -e "  ${PURPLE}tmux kill-session -t $SESSION_NAME${NC} - Cerrar sesión"
    echo ""
}

# Crear configuración de Kitty personalizada
create_kitty_config() {
    local kitty_config="$HOME/.config/kitty/nethunter.conf"
    mkdir -p "$(dirname "$kitty_config")"
    
    cat > "$kitty_config" << 'EOF'
# NetHunter Kitty Terminal Configuration
# Optimizado para el agente NetHunter multi-ventana

# Apariencia
background_opacity 0.95
background #1a1a1a
foreground #e6e6e6
cursor #ff6b35
cursor_text_color #1a1a1a

# Esquema de colores NetHunter
color0  #1a1a1a
color1  #ff6b35
color2  #7bc96f  
color3  #eacd61
color4  #5aa7e4
color5  #c678dd
color6  #56d1dc
color7  #e6e6e6
color8  #5c6370
color9  #ff6b35
color10 #7bc96f
color11 #eacd61
color12 #5aa7e4
color13 #c678dd
color14 #56d1dc
color15 #ffffff

# Ventana y tabs
window_padding_width 8
tab_bar_style powerline
tab_powerline_style round
active_tab_background #ff6b35
active_tab_foreground #1a1a1a
inactive_tab_background #2d2d2d
inactive_tab_foreground #999999

# Font
font_family JetBrains Mono
bold_font JetBrains Mono Bold
italic_font JetBrains Mono Italic
font_size 12.0

# Keyboard shortcuts para NetHunter
map ctrl+shift+t new_tab_with_cwd
map ctrl+shift+w close_tab
map ctrl+shift+n new_window
map ctrl+shift+enter new_window_with_cwd

# Layouts para multi-ventana
enabled_layouts tall,stack,grid
map ctrl+shift+l next_layout

# Configuración de rendimiento
sync_to_monitor yes
EOF

    echo -e "${GREEN}✅ Configuración de Kitty creada: $kitty_config${NC}"
    echo -e "${YELLOW}💡 Para usar: kitty --config=$kitty_config${NC}"
}

# Función principal
main() {
    local mode="${1:-auto}"
    
    case "$mode" in
        "kitty")
            echo -e "${CYAN}🐱 Configurando para terminal Kitty...${NC}"
            create_kitty_config
            setup_kitty_layout
            create_tmux_layout
            ;;
        "tmux")
            echo -e "${BLUE}📊 Configurando layout tmux estándar...${NC}"
            create_tmux_layout
            ;;
        "help")
            show_navigation_help
            ;;
        *)
            echo -e "${PURPLE}🚀 Detectando entorno y configurando automáticamente...${NC}"
            
            if ! command -v tmux &>/dev/null; then
                echo -e "${RED}❌ tmux no encontrado. Instalar: apt install tmux${NC}"
                exit 1
            fi
            
            if is_kitty_terminal; then
                echo -e "${CYAN}🐱 Terminal Kitty detectado${NC}"
                create_kitty_config
                setup_kitty_layout
            fi
            
            create_tmux_layout
            show_navigation_help
            
            # Conectar a la sesión
            echo -e "${GREEN}🔗 Conectando al workspace NetHunter...${NC}"
            tmux attach-session -t "$SESSION_NAME"
            ;;
    esac
}

# Verificar argumentos
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi