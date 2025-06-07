#!/bin/bash
# Demo de la Interfaz Multi-Ventana NetHunter
# Muestra visualmente cómo se ve el layout completo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Función para simular la interfaz visualmente
show_interface_layout() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}${BOLD}                        🛡️ NETHUNTER WORKSPACE - LAYOUT DEMO                         ${NC}${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Ventana 0 - Principal (dividida en 3 paneles)
    echo -e "${BLUE}┌─ VENTANA 0: INTERFAZ PRINCIPAL ─────────────────────────────────────────────────────┐${NC}"
    echo -e "${BLUE}│${NC}"
    echo -e "${BLUE}│${NC} ${GREEN}📱 PANEL 0: AGENTE PRINCIPAL${NC}      ${YELLOW}│${NC} ${PURPLE}📊 PANEL 1: MONITOR${NC}"
    echo -e "${BLUE}│${NC} ┌─────────────────────────────────┐ ${YELLOW}│${NC} ┌─────────────────────┐"
    echo -e "${BLUE}│${NC} │ ${CYAN}🧠 Ruth Shell activada${NC}          │ ${YELLOW}│${NC} │ ${GREEN}CPU: 15.2%${NC}          │"
    echo -e "${BLUE}│${NC} │ ${WHITE}NetHunter> escanear 192.168.1.1${NC} │ ${YELLOW}│${NC} │ ${GREEN}RAM: 45.8%${NC}          │"
    echo -e "${BLUE}│${NC} │ ${CYAN}💡 Comando sugerido:${NC}             │ ${YELLOW}│${NC} │ ${GREEN}Red: ✓ Activa${NC}       │"
    echo -e "${BLUE}│${NC} │ ${GREEN}nmap -sS -O 192.168.1.1${NC}        │ ${YELLOW}│${NC} │ ${YELLOW}Procesos: 3${NC}         │"
    echo -e "${BLUE}│${NC} │ ${YELLOW}¿Ejecutar? (Y/n):${NC}               │ ${YELLOW}│${NC} └─────────────────────┘"
    echo -e "${BLUE}│${NC} │                                 │ ${YELLOW}│${NC}"
    echo -e "${BLUE}│${NC} │ ${DIM}Historial de comandos:${NC}          │ ${YELLOW}│${NC} ${RED}📋 PANEL 2: LOGS${NC}"
    echo -e "${BLUE}│${NC} │ ${DIM}• sqlmap -u target.com${NC}          │ ${YELLOW}│${NC} ┌─────────────────────┐"
    echo -e "${BLUE}│${NC} │ ${DIM}• john --wordlist hashes.txt${NC}    │ ${YELLOW}│${NC} │ ${DIM}[10:34] CMD: nmap${NC}   │"
    echo -e "${BLUE}│${NC} │ ${DIM}• hydra -l admin target${NC}         │ ${YELLOW}│${NC} │ ${DIM}[10:35] EXIT: 0${NC}     │"
    echo -e "${BLUE}│${NC} └─────────────────────────────────┘ ${YELLOW}│${NC} │ ${DIM}[10:36] OCR: text${NC}   │"
    echo -e "${BLUE}│${NC}                                     ${YELLOW}│${NC} │ ${GREEN}[10:37] SUCCESS${NC}     │"
    echo -e "${BLUE}│${NC}                                     ${YELLOW}│${NC} └─────────────────────┘"
    echo -e "${BLUE}└─────────────────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Ventana 1 - Monitor
    echo -e "${PURPLE}┌─ VENTANA 1: MONITOR AVANZADO ───────────────────────────────────────────────────────┐${NC}"
    echo -e "${PURPLE}│${NC}"
    echo -e "${PURPLE}│${NC} ${CYAN}👁️ PANEL 0: WATCHER INTELIGENTE${NC}              ${RED}🧠 PANEL 1: METACOGNICIÓN${NC}"
    echo -e "${PURPLE}│${NC} ┌─────────────────────────────────────────┐  ┌───────────────────────────────┐"
    echo -e "${PURPLE}│${NC} │ ${GREEN}🔍 Analizando logs en tiempo real...${NC}    │  │ ${BLUE}📊 Autoevaluación:${NC}         │"
    echo -e "${PURPLE}│${NC} │ ${YELLOW}🚨 Error detectado: network_error${NC}       │  │ ${GREEN}✓ Precisión: 0.95${NC}         │"
    echo -e "${PURPLE}│${NC} │ ${CYAN}💬 Respuesta: Verificando red...${NC}         │  │ ${GREEN}✓ Confianza: 0.87${NC}         │"
    echo -e "${PURPLE}│${NC} │ ${GREEN}🔧 Acción: ping 8.8.8.8${NC}                │  │ ${YELLOW}⚠️ CPU: Alto uso${NC}          │"
    echo -e "${PURPLE}│${NC} │ ${BLUE}💡 Sugerencia: Revisar firewall${NC}         │  │ ${PURPLE}🔄 Adaptación: Mínima${NC}     │"
    echo -e "${PURPLE}│${NC} │ ${DIM}Pattern: connection_refused x3${NC}          │  │ ${CYAN}📈 Progreso: +12%${NC}         │"
    echo -e "${PURPLE}│${NC} └─────────────────────────────────────────┘  └───────────────────────────────┘"
    echo -e "${PURPLE}└─────────────────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Ventana 2 - Herramientas (4 paneles)
    echo -e "${RED}┌─ VENTANA 2: HERRAMIENTAS NETHUNTER ─────────────────────────────────────────────────┐${NC}"
    echo -e "${RED}│${NC}"
    echo -e "${RED}│${NC} ${CYAN}🔍 NMAP${NC}              ${GREEN}💉 SQLMAP${NC}              ${YELLOW}🔐 JOHN/HASHCAT${NC}    ${PURPLE}⚡ HYDRA${NC}"
    echo -e "${RED}│${NC} ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ ┌──────────────┐"
    echo -e "${RED}│${NC} │ ${WHITE}Escaneando...${NC}    │  │ ${WHITE}Testing SQL...${NC}   │  │ ${WHITE}Cracking...${NC}      │ │ ${WHITE}Brute force${NC}  │"
    echo -e "${RED}│${NC} │ ${GREEN}Host: 192.168.1.5${NC} │  │ ${RED}Vulnerable!${NC}      │  │ ${GREEN}Progress: 45%${NC}    │ │ ${YELLOW}SSH: 22${NC}      │"
    echo -e "${RED}│${NC} │ ${GREEN}Port 22: Open${NC}    │  │ ${GREEN}DB: MySQL${NC}        │  │ ${CYAN}Speed: 1.2k/s${NC}   │ │ ${RED}Failed: 23${NC}   │"
    echo -e "${RED}│${NC} │ ${GREEN}Port 80: Open${NC}    │  │ ${YELLOW}Tables: 12${NC}       │  │ ${YELLOW}ETA: 2h 15m${NC}     │ │ ${GREEN}Valid: admin${NC} │"
    echo -e "${RED}│${NC} │ ${RED}Port 443: Filtered${NC}│  │ ${CYAN}Dumping...${NC}       │  │ ${PURPLE}Wordlist: rockyou${NC}│ │ ${GREEN}Pass: 123456${NC}│"
    echo -e "${RED}│${NC} └─────────────────┘  └─────────────────┘  └─────────────────┘ └──────────────┘"
    echo -e "${RED}└─────────────────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Ventana 3 - OCR Visual
    echo -e "${CYAN}┌─ VENTANA 3: INTERFAZ VISUAL ────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC}"
    echo -e "${CYAN}│${NC} ${GREEN}📸 PANEL 0: OCR EN TIEMPO REAL${NC}                 ${YELLOW}🧠 PANEL 1: ANÁLISIS VISUAL${NC}"
    echo -e "${CYAN}│${NC} ┌─────────────────────────────────────────┐  ┌───────────────────────────────┐"
    echo -e "${CYAN}│${NC} │ ${BLUE}🔍 Captura iniciada...${NC}                  │  │ ${PURPLE}💡 Núcleo procesando...${NC}   │"
    echo -e "${CYAN}│${NC} │ ${GREEN}📝 Texto extraído: 156 caracteres${NC}       │  │ ${CYAN}🎯 Intención: security_scan${NC}│"
    echo -e "${CYAN}│${NC} │ ${YELLOW}📄 \"nmap -sS target.com -p 80,443\"${NC}     │  │ ${GREEN}🎲 Confianza: 0.92${NC}        │"
    echo -e "${CYAN}│${NC} │ ${CYAN}🧠 Analizando con Razonbilstro...${NC}        │  │ ${YELLOW}💡 Comando sugerido:${NC}      │"
    echo -e "${CYAN}│${NC} │ ${GREEN}✅ Procesamiento completado${NC}              │  │ ${WHITE}nmap -sV -sC target.com${NC}   │"
    echo -e "${CYAN}│${NC} │ ${BLUE}🗣️ TTS: \"Escaneo de puertos sugerido\"${NC}   │  │ ${GREEN}🔊 Reproduciendo audio...${NC} │"
    echo -e "${CYAN}│${NC} └─────────────────────────────────────────┘  └───────────────────────────────┘"
    echo -e "${CYAN}└─────────────────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Barra de estado
    echo -e "${BOLD}${WHITE}🛡️ NetHunter                                                    🧠 Núcleo 10:42 27/05${NC}"
    echo ""
}

# Función para mostrar comandos de navegación
show_navigation_demo() {
    echo -e "${BOLD}🎮 NAVEGACIÓN ENTRE VENTANAS Y PANELES:${NC}"
    echo ""
    echo -e "${GREEN}📱 Cambiar ventanas:${NC}"
    echo -e "  • ${YELLOW}Ctrl+b 0${NC} → Interfaz Principal"
    echo -e "  • ${YELLOW}Ctrl+b 1${NC} → Monitor Avanzado" 
    echo -e "  • ${YELLOW}Ctrl+b 2${NC} → Herramientas NetHunter"
    echo -e "  • ${YELLOW}Ctrl+b 3${NC} → Interfaz Visual (OCR)"
    echo ""
    echo -e "${GREEN}🔄 Navegar paneles:${NC}"
    echo -e "  • ${YELLOW}Ctrl+b ←→↑↓${NC} → Mover entre paneles"
    echo -e "  • ${YELLOW}Ctrl+b q${NC} → Mostrar números de panel"
    echo -e "  • ${YELLOW}Ctrl+b z${NC} → Maximizar/minimizar panel actual"
    echo ""
    echo -e "${GREEN}⚡ Acciones rápidas:${NC}"
    echo -e "  • ${YELLOW}Ctrl+b [${NC} → Modo scroll (navegar historial)"
    echo -e "  • ${YELLOW}Ctrl+b c${NC} → Nueva ventana"
    echo -e "  • ${YELLOW}Ctrl+b d${NC} → Detach (mantener sesión activa)"
    echo ""
}

# Función principal del demo
main() {
    local mode="${1:-full}"
    
    case "$mode" in
        "layout")
            show_interface_layout
            ;;
        "nav")
            show_navigation_demo
            ;;
        *)
            show_interface_layout
            echo -e "${PURPLE}════════════════════════════════════════════════════════════════════════════════════════${NC}"
            show_navigation_demo
            
            echo -e "${BOLD}🚀 PARA EJECUTAR LA INTERFAZ REAL:${NC}"
            echo -e "  ${CYAN}./terminal_interface.sh${NC}     → Auto-detectar y configurar"
            echo -e "  ${CYAN}./terminal_interface.sh kitty${NC} → Optimizado para Kitty"
            echo -e "  ${CYAN}./terminal_interface.sh tmux${NC}  → Solo tmux estándar"
            echo ""
            ;;
    esac
}

# Verificar si se ejecuta directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi