
# 🧠 RazonbilstroOS v2.1.0 - Guía de Instalación

## 📋 Información del Sistema
- **Nombre**: RazonbilstroOS 
- **Versión**: 2.1.0 (Neural Agent)
- **Arquitectura**: amd64 (64-bit)
- **Núcleo**: Linux 6.2.16
- **Base**: Ubuntu 22.04 LTS

## 🎯 Hardware Optimizado
- **Laptop**: Lenovo ThinkPad T480
- **Procesador**: Intel Core i7 (8ª generación)
- **RAM**: 16GB DDR4
- **Almacenamiento**: 500GB SSD
- **Arranque**: UEFI exclusivamente

## 🔧 Características Principales
- 🧠 **Núcleo C.A- Razonbilstro**: IA con 94.18% de precisión
- 🎥 **Vision Cam Module**: Reconocimiento biométrico (91.2% precisión)
- 🤖 **Pwnagotchi AI**: Módulo WiFi inteligente (Nivel 4)
- 🔒 **27 Herramientas de Seguridad**: Integradas y optimizadas
- 🎨 **Blue Theme Desktop**: Interfaz moderna y funcional
- 🔊 **Saludo por Voz**: Razonbill asistente personal

## 📦 Requisitos del Sistema
- **CPU**: Intel Core i5 o superior (recomendado i7)
- **RAM**: Mínimo 8GB (recomendado 16GB)
- **Almacenamiento**: Mínimo 100GB (recomendado 500GB SSD)
- **UEFI**: Obligatorio (no soporta BIOS legacy)
- **Conectividad**: WiFi 802.11n/ac

## 🚀 Preparación del USB de Instalación

### 1. Descargar la ISO
```bash
wget https://releases.razonbilstro.ai/v2.1.0/RazonbilstroOS-v2.1.0-amd64.iso
```

### 2. Verificar Integridad (Recomendado)
```bash
sha256sum RazonbilstroOS-v2.1.0-amd64.iso
# Comparar con: [HASH_SHA256_AQUÍ]
```

### 3. Crear USB Booteable

#### En Linux:
```bash
sudo dd if=RazonbilstroOS-v2.1.0-amd64.iso of=/dev/sdX bs=4M status=progress && sync
# Reemplazar /dev/sdX con su dispositivo USB
```

#### En Windows:
- Usar **Rufus** o **Etcher**
- Seleccionar RazonbilstroOS-v2.1.0-amd64.iso
- Configurar como UEFI
- Escribir al USB

#### En macOS:
```bash
sudo dd if=RazonbilstroOS-v2.1.0-amd64.iso of=/dev/diskX bs=4m && sync
# Reemplazar /dev/diskX con su dispositivo USB
```

## 💻 Proceso de Instalación

### 1. Preparar la Laptop ThinkPad T480
- ✅ Acceder a BIOS/UEFI (F1 al encender)
- ✅ Habilitar arranque desde USB
- ✅ Deshabilitar Secure Boot (temporalmente)
- ✅ Configurar UEFI como modo de arranque
- ✅ Guardar configuración y reiniciar

### 2. Arrancar desde USB
- 🔌 Conectar USB booteable
- ⚡ Reiniciar laptop
- 🔑 Presionar F12 para menú de arranque
- 📀 Seleccionar USB UEFI

### 3. Menú de Arranque RazonbilstroOS
```
┌─────────────────────────────────────────┐
│    🧠 RazonbilstroOS v2.1.0        │
├─────────────────────────────────────────┤
│ ➤ RazonbilstroOS (Live)                │
│   RazonbilstroOS (Install)             │
│   Memory Test                           │
│   Boot from Hard Disk                  │
└─────────────────────────────────────────┘
```

### 4. Configuración del Sistema

#### A. Selección de Idioma
- 🇲🇽 **Español (México)** - Predeterminado
- 🇺🇸 Inglés (Estados Unidos) - Alternativo

#### B. Configuración de Teclado
- ⌨️ **Español (México)** - Incluye tecla "ñ"
- 🔄 Alternar con Alt+Shift para inglés US

#### C. Configuración de Red
- 📶 **WiFi**: Totalplay-2.4G-bd28
- 🔐 **Contraseña**: cJnQTuwJ9nWhuLAN
- 🌐 **Banda**: 2.4GHz optimizada

### 5. Particionado del Disco (500GB SSD)

```
📊 Esquema de Particiones Recomendado:
┌─────────────────────────────────────────┐
│ /boot/efi  │ 512MB  │ vfat   │ EFI    │
│ /boot      │ 1GB    │ ext4   │ Boot   │ 
│ /          │ 60GB   │ ext4   │ Root   │
│ /opt/razonbilstro │ 20GB │ ext4 │ IA   │
│ /home      │ 395GB  │ ext4   │ User   │
│ swap       │ 16GB   │ swap   │ Swap   │
└─────────────────────────────────────────┘
```

#### Particionado Automático:
1. 🎯 Seleccionar "Usar disco completo"
2. ✅ Confirmar esquema optimizado
3. 🚀 Proceder con instalación

#### Particionado Manual (Avanzado):
1. 🛠️ Seleccionar "Configurar manualmente"
2. 📝 Crear particiones según esquema
3. 🎯 Asignar puntos de montaje
4. ✅ Confirmar cambios

### 6. Configuración de Usuario

```
👤 Datos del Usuario:
Nombre completo: [Su nombre]
Nombre de usuario: razonbill (recomendado)
Contraseña: [Contraseña segura]
Hostname: razonbilstro-t480
```

### 7. Instalación del Sistema
- ⏱️ **Tiempo estimado**: 15-30 minutos
- 📊 **Progreso mostrado** en tiempo real
- 🧠 **Configuración automática** del núcleo IA

## ✅ Post-Instalación

### 1. Primer Arranque
- 🔊 **Saludo por voz**: "¡Buen día! Es un placer poder asistirle..."
- 🎨 **Desktop Blue Theme** cargado automáticamente
- 🧠 **Núcleo C.A-** iniciando en segundo plano

### 2. Verificación del Sistema
```bash
# Verificar núcleo IA
nucleus --status

# Verificar módulo de visión  
vision --status

# Verificar Pwnagotchi
pwn --status

# Verificar herramientas
tools --list
```

### 3. Configuración WiFi (Si no se configuró)
```bash
# Conectar a Totalplay
sudo nmcli dev wifi connect "Totalplay-2.4G-bd28" password "cJnQTuwJ9nWhuLAN"
```

### 4. Actualizaciones del Sistema
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade

# Verificar estado del núcleo
nucleus --full-scan
```

## 🎮 Comandos Principales

### Núcleo C.A- Razonbilstro
```bash
nucleus --status          # Estado completo
nucleus --dashboard       # Abrir interfaz web
nucleus --restart         # Reiniciar núcleo
nucleus --full-scan       # Escaneo completo
```

### Vision Cam Module
```bash
vision --scan            # Escaneo biométrico
vision --objects         # Detección de objetos
vision --analyze "texto" # Análisis contextual
vision --status          # Estado del módulo
```

### Pwnagotchi AI
```bash
pwn --scan              # Escaneo WiFi agresivo
pwn --status            # Estado del AI
```

### Herramientas del Sistema
```bash
tools --list            # Lista completa
tools --security        # Herramientas de seguridad
tools --system          # Herramientas de sistema
```

## 🌐 Acceso Web Dashboard
- **URL**: http://localhost:5000
- **Funciones**: Monitoreo neuronal, estadísticas, configuración
- **Acceso**: Automático desde navegador local

## 🔧 Solución de Problemas

### Problema: Sistema no arranca
```bash
# Verificar UEFI en BIOS
# Confirmar USB booteable correcto
# Probar con otro puerto USB
```

### Problema: WiFi no conecta
```bash
# Verificar SSID y contraseña
sudo nmcli dev wifi rescan
sudo systemctl restart NetworkManager
```

### Problema: Núcleo no responde
```bash
# Reiniciar servicios
sudo systemctl restart razonbilstro-nucleus
sudo systemctl restart postgresql
```

## 📞 Soporte
- **Documentación**: https://docs.razonbilstro.ai
- **Issues**: https://github.com/razonbilstro/os/issues
- **Email**: soporte@razonbilstro.ai

---

## 🎯 ¡Listo para Usar!

Una vez completada la instalación, tendrás:
- 🧠 IA con 94.18% precisión operativa
- 🎥 Reconocimiento biométrico funcional
- 🤖 Asistente Razonbill activo
- 🔒 27 herramientas de seguridad
- 🎨 Interfaz Blue Theme optimizada
- 📊 Dashboard web completo

**¡Bienvenido a RazonbilstroOS!** 🚀

---
*RazonbilstroOS v2.1.0 - Neural Agent Distribution*
*Optimizado para Lenovo ThinkPad T480 | Intel Core i7 | 16GB RAM | 500GB SSD*
