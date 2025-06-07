#!/bin/bash
# Autostart Núcleo C.A- Razonbilstro en Kitty

# Esperar que el sistema esté listo
sleep 2

# Configurar variables de entorno
export NUCLEUS_HOME="$PWD"
export PYTHONPATH="$NUCLEUS_HOME:$PYTHONPATH"

# Verificar dependencias
echo "🔍 Verificando dependencias del núcleo..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 requerido"
    exit 1
fi

# Verificar módulos del núcleo
python3 -c "import gym_razonbilstro.neural_model" 2>/dev/null || {
    echo "❌ Módulos del núcleo no encontrados"
    exit 1
}

echo "✅ Dependencias verificadas"

# Lanzar Kitty con configuración del núcleo
if command -v kitty &> /dev/null; then
    echo "🚀 Lanzando interfaz Kitty-Núcleo..."
    kitty --config="$HOME/.config/kitty/kitty.conf" --session="$HOME/.config/kitty/nucleus_session.conf"
else
    echo "⚠️ Kitty no disponible, iniciando núcleo en terminal actual..."
    python3 gym_razonbilstro/neural_model.py
fi
