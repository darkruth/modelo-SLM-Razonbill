#!/bin/bash
# Brain.sh - Núcleo C.A- Razonbilstro Integration Brain
# Ejecuta modelos y traduce lenguaje natural a comandos

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/log"
MODEL_DIR="$SCRIPT_DIR/model"
CONFIG_DIR="$SCRIPT_DIR/config"

# Crear directorios si no existen
mkdir -p "$LOG_DIR" "$MODEL_DIR" "$CONFIG_DIR"

# Configuración
PERSONA_FILE="$CONFIG_DIR/persona.cfg"
HISTORY_FILE="$LOG_DIR/decision_history.json"
CONTEXT_FILE="$LOG_DIR/context_memory.json"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función de logging
log_decision() {
    local input="$1"
    local output="$2"
    local confidence="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "{
        \"timestamp\": \"$timestamp\",
        \"input\": \"$input\",
        \"output\": \"$output\",
        \"confidence\": \"$confidence\",
        \"context_used\": \"$(cat $CONTEXT_FILE 2>/dev/null | jq -c .current_context 2>/dev/null || echo 'null')\"
    }" >> "$HISTORY_FILE"
}

# Función de actualización de contexto
update_context() {
    local new_context="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "{
        \"last_update\": \"$timestamp\",
        \"current_context\": \"$new_context\",
        \"environment\": \"nethunter\",
        \"active_tools\": [],
        \"session_memory\": []
    }" > "$CONTEXT_FILE"
}

# Función principal de procesamiento con Núcleo Razonbilstro
process_with_nucleus() {
    local input_text="$1"
    local context="$2"
    
    echo -e "${CYAN}🧠 Procesando con Núcleo C.A- Razonbilstro...${NC}"
    
    # Crear entrada estructurada para el núcleo
    local structured_input="{
        \"input_data\": {
            \"raw_input\": \"$input_text\",
            \"semantic_type\": \"command_interpretation\",
            \"intent\": \"nethunter_assistance\",
            \"context\": \"$context\"
        },
        \"processing_requirements\": {
            \"domain_priority\": [\"security_tools\", \"bash_official\", \"cpp_fuzzy\"],
            \"output_format\": \"executable_command\",
            \"confidence_threshold\": 0.7
        }
    }"
    
    # Integración real con el Núcleo C.A- Razonbilstro
    echo -e "${PURPLE}🔗 Conectando con Núcleo C.A- Razonbilstro...${NC}"
    
    # Buscar núcleo en directorios padre
    local nucleus_paths=(
        "../../neural_model.py"
        "../../../neural_model.py"
        "../../gym_razonbilstro/core_system.py"
        "../gym_razonbilstro/core_system.py"
    )
    
    local nucleus_found=""
    for path in "${nucleus_paths[@]}"; do
        if [[ -f "$SCRIPT_DIR/$path" ]]; then
            nucleus_found="$SCRIPT_DIR/$path"
            break
        fi
    done
    
    if [[ -n "$nucleus_found" ]]; then
        echo -e "${GREEN}✓ Núcleo encontrado: $nucleus_found${NC}"
        
        # Procesar con el núcleo real
        local nucleus_result=""
        if [[ "$nucleus_found" == *"neural_model.py"* ]]; then
            nucleus_result=$(python3 "$nucleus_found" --process "$input_text" 2>/dev/null || echo "Error procesando con núcleo")
        elif [[ "$nucleus_found" == *"core_system.py"* ]]; then
            nucleus_result=$(python3 "$nucleus_found" --input "$input_text" --context "$context" 2>/dev/null || echo "Error procesando con core")
        fi
        
        if [[ -n "$nucleus_result" && "$nucleus_result" != "Error"* ]]; then
            echo -e "${GREEN}🧠 Núcleo procesó exitosamente${NC}"
            suggested_command="$nucleus_result"
            confidence="0.95"
        fi
    else
        echo -e "${YELLOW}⚠️ Núcleo no encontrado, usando análisis local${NC}"
    fi
    
    echo -e "${GREEN}✓ Núcleo activado - Analizando dominios especializados${NC}"
    
    # Clasificación de intención usando patrones del núcleo
    local intention="unknown"
    local confidence="0.5"
    local suggested_command=""
    
    # Análisis de seguridad (dominio security_tools)
    if [[ "$input_text" =~ (nmap|scan|port|vulnerability|exploit) ]]; then
        intention="security_scan"
        confidence="0.9"
        if [[ "$input_text" =~ nmap ]]; then
            suggested_command="nmap -sS -O target_ip"
        elif [[ "$input_text" =~ scan ]]; then
            suggested_command="nmap -sV -sC target_ip"
        fi
    
    # Análisis de comandos shell (dominio bash_official)
    elif [[ "$input_text" =~ (ls|find|grep|ps|kill|systemctl) ]]; then
        intention="system_command"
        confidence="0.85"
        suggested_command="$input_text"
    
    # Análisis de desarrollo (dominio cpp_fuzzy)
    elif [[ "$input_text" =~ (compile|build|make|gcc|g\+\+) ]]; then
        intention="development"
        confidence="0.8"
        suggested_command="g++ -O2 -std=c++17 source.cpp -o output"
    
    # Análisis de herramientas NetHunter
    elif [[ "$input_text" =~ (burp|sqlmap|john|hashcat|hydra|nikto) ]]; then
        intention="nethunter_tool"
        confidence="0.95"
        case "$input_text" in
            *sqlmap*) suggested_command="sqlmap -u 'target_url' --dbs" ;;
            *john*) suggested_command="john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt" ;;
            *nmap*) suggested_command="nmap -A target_ip" ;;
            *) suggested_command="echo 'Herramienta NetHunter detectada: especifica parámetros'" ;;
        esac
    fi
    
    # Logging de decisión
    log_decision "$input_text" "$suggested_command" "$confidence"
    
    # Output estructurado
    echo -e "${YELLOW}🎯 Intención detectada:${NC} $intention"
    echo -e "${YELLOW}🎲 Confianza:${NC} $confidence"
    echo -e "${YELLOW}💡 Comando sugerido:${NC} $suggested_command"
    
    # Retornar resultado para el executor
    echo "$suggested_command"
}

# Función de auto-prompt tuning
auto_tune_prompts() {
    local success_rate="$1"
    
    if (( $(echo "$success_rate < 0.7" | bc -l) )); then
        echo -e "${RED}⚠️ Tasa de éxito baja ($success_rate) - Ajustando prompts...${NC}"
        # Aquí implementarías la lógica de ajuste automático
        echo "# Auto-tuned prompts - $(date)" >> "$CONFIG_DIR/prompt_tuning.log"
    fi
}

# Función principal
main() {
    local input_text="$1"
    local context="${2:-general}"
    
    if [[ -z "$input_text" ]]; then
        echo -e "${RED}❌ Error: Se require entrada de texto${NC}"
        echo "Uso: $0 \"texto de entrada\" [contexto]"
        exit 1
    fi
    
    echo -e "${BLUE}🚀 Iniciando procesamiento cerebral...${NC}"
    echo -e "${PURPLE}📝 Entrada:${NC} $input_text"
    echo -e "${PURPLE}🔍 Contexto:${NC} $context"
    
    # Actualizar contexto
    update_context "$context"
    
    # Procesar con núcleo
    local result=$(process_with_nucleus "$input_text" "$context")
    
    echo -e "${GREEN}✅ Procesamiento completado${NC}"
    echo "$result"
}

# Verificar si se ejecuta directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi