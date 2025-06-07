#!/bin/bash
# Lanzador Kitty-Núcleo C.A- Razonbilstro

export TERM=xterm-256color
export NUCLEUS_PATH="$PWD/gym_razonbilstro"
export KITTY_CONFIG_DIRECTORY="$HOME/.config/kitty"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🚀 INICIANDO NÚCLEO C.A- RAZONBILSTRO${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Verificar núcleo
if [ -f "$NUCLEUS_PATH/neural_model.py" ]; then
    echo -e "${GREEN}✅ Núcleo encontrado y listo${NC}"
else
    echo -e "${RED}❌ Error: Núcleo no encontrado${NC}"
    exit 1
fi

# Verificar Kitty
if command -v kitty &> /dev/null; then
    echo -e "${GREEN}✅ Kitty terminal disponible${NC}"
else
    echo -e "${YELLOW}⚠️ Kitty no encontrado, usando terminal por defecto${NC}"
fi

# Lanzar interfaz
echo -e "${BLUE}🖥️ Iniciando interfaz multiventanas...${NC}"

if command -v kitty &> /dev/null; then
    kitty --session nucleus_session.conf
else
    # Fallback para terminales estándar
    python3 "$NUCLEUS_PATH/neural_model.py"
fi
