#!/bin/bash

# Script de Inicio Rápido - Núcleo C.A- Razonbilstro Avatar IA
# Lanza la aplicación web con avatar gesticulante

echo "🤖 Iniciando Núcleo C.A- Razonbilstro con Avatar IA..."
echo "=" * 60

# Verificar dependencias
echo "Verificando dependencias..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado"
    exit 1
fi

# Cambiar al directorio del proyecto
cd /home/runner/workspace

# Verificar que el video del avatar existe
if [ ! -f "static/avatar_video.mp4" ]; then
    echo "⚠️  Video del avatar no encontrado, copiando desde repositorio..."
    if [ -f "avatar_repo/tiktok-1748065341929.mp4" ]; then
        cp avatar_repo/tiktok-1748065341929.mp4 static/avatar_video.mp4
        echo "✅ Video del avatar copiado correctamente"
    else
        echo "❌ Error: No se encuentra el video del avatar"
        exit 1
    fi
fi

# Mostrar información del sistema
echo ""
echo "📋 Configuración del Sistema:"
echo "   • Avatar IA: Activo (40% de pantalla)"
echo "   • Gesticulación facial: Biométrica sincronizada"
echo "   • TTS/STT: Integrado con movimiento labial"
echo "   • Procesamiento URLs: Automático"
echo "   • PWA: Instalable en Android"
echo ""

# Iniciar servidor Flask
echo "🚀 Iniciando servidor Flask..."
python3 app.py &
SERVER_PID=$!

# Esperar a que el servidor inicie
echo "⏳ Esperando inicio del servidor..."
sleep 3

# Verificar que el servidor esté funcionando
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Servidor iniciado correctamente en http://localhost:5000"
    echo ""
    echo "🌐 Abriendo navegador..."
    
    # Abrir navegador según el sistema
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5000
    elif command -v open &> /dev/null; then
        open http://localhost:5000
    else
        echo "📱 Accede manualmente a: http://localhost:5000"
    fi
    
    echo ""
    echo "✨ ¡Avatar IA listo!"
    echo "   • Envía un mensaje para ver la gesticulación facial"
    echo "   • El avatar responde a emociones del texto"
    echo "   • Los labios se sincronizan con el audio TTS"
    echo ""
    echo "🛑 Presiona Ctrl+C para detener el servidor"
    
    # Mantener servidor activo
    wait $SERVER_PID
    
else
    echo "❌ Error: El servidor no pudo iniciarse"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi