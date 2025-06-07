# Entorno de Pruebas VM - RazonbilstroOS

## 🖥️ Configuración de Máquina Virtual

### Especificaciones VM
- **Nombre**: RazonbilstroOS_Test_VM
- **Arquitectura**: x86_64
- **CPU**: 4 cores (host passthrough)
- **RAM**: 8 GB
- **Almacenamiento**: 50 GB (qcow2)
- **Red**: NAT con port forwarding

### Puertos de la VM
- **SSH**: localhost:2222 → VM:22
- **Dashboard**: localhost:8080 → VM:5000
- **VNC**: localhost:5900 → VM:5900

## 🚀 Inicio Rápido

### 1. Crear y configurar VM
```bash
cd vm_test_environment/vm_config
./create_vm.sh
```

### 2. Iniciar VM
```bash
./start_vm.sh
```

### 3. Conectar a la VM
```bash
# SSH
./connect_ssh.sh

# VNC
./connect_vnc.sh

# Dashboard web
./open_dashboard.sh
```

## 🔧 Configuración del Bootloader

### GRUB UEFI/BIOS
- Soporte dual UEFI y Legacy BIOS
- Menú personalizado RazonbilstroOS
- Opciones de arranque:
  - Normal
  - Modo seguro
  - Modo debug
  - Test de memoria
  - Recuperación

### Instalación del Bootloader
```bash
cd vm_test_environment/bootloader
sudo ./install_bootloader.sh
```

## 📊 Monitoreo de Hardware

### Monitor en Tiempo Real
```bash
cd vm_test_environment/hardware_monitor
python3 hardware_monitor.py --continuous 30
```

### Información Única
```bash
python3 hardware_monitor.py
```

### Métricas Monitoreadas
- **CPU**: Uso, cores, frecuencia
- **Memoria**: RAM, swap, cache
- **Almacenamiento**: Uso de discos
- **Red**: Tráfico de interfaces
- **Procesos**: Top procesos por CPU/memoria
- **RazonbilstroOS**: Estado del núcleo y servicios

## 🧪 Scripts de Pruebas

### Prueba de Instalación
```bash
cd vm_test_environment/test_scripts
./test_installation.sh
```

### Pruebas Incluidas
- Verificación de requisitos del sistema
- Comprobación de instalación
- Funcionalidad del núcleo
- Módulo de visión
- Benchmark de rendimiento

## 🔍 Comandos de Diagnóstico VM

### Estado del Sistema
```bash
# Información general
hostnamectl

# Uso de recursos
htop
free -h
df -h

# Procesos de RazonbilstroOS
ps aux | grep -E "(nucleus|vision|main.py)"

# Estado de servicios
systemctl status razonbilstro-nucleus
```

### Logs Importantes
```bash
# Logs del núcleo
tail -f /opt/razonbilstro/nucleus.log

# Logs del sistema
journalctl -f

# Logs de arranque
dmesg | grep -i error
```

## 🌐 Acceso Remoto

### Desde Host a VM
- **SSH**: `ssh -p 2222 razonbill@localhost`
- **Web**: `http://localhost:8080`
- **VNC**: Cliente VNC a `localhost:5900`

### Credenciales por Defecto
- **Usuario**: razonbill
- **Contraseña**: razonbill2024

## 🔧 Configuración de Red VM

### Port Forwarding Configurado
- SSH: 2222 → 22
- HTTP: 8080 → 5000
- VNC: 5900 → 5900

### Configuración de Red
```bash
# Ver configuración de red
ip addr show

# Verificar conectividad
ping google.com

# Puertos en uso
netstat -tlnp
```

## 📁 Estructura de Archivos VM

```
vm_test_environment/
├── vm_config/
│   ├── create_vm.sh         # Crear VM
│   ├── start_vm.sh          # Iniciar VM
│   ├── connect_ssh.sh       # Conectar SSH
│   ├── connect_vnc.sh       # Conectar VNC
│   └── vm_specs.json        # Especificaciones
├── bootloader/
│   ├── grub.cfg             # Configuración GRUB
│   ├── uefi_grub.cfg        # GRUB UEFI
│   └── install_bootloader.sh # Instalar bootloader
├── hardware_monitor/
│   └── hardware_monitor.py   # Monitor de hardware
├── test_scripts/
│   └── test_installation.sh  # Pruebas de instalación
└── logs/                     # Logs de monitoreo
```

## 🛠️ Solución de Problemas VM

### VM no inicia
```bash
# Verificar KVM
ls -la /dev/kvm

# Verificar QEMU
qemu-system-x86_64 --version

# Permisos de usuario
groups $USER | grep kvm
```

### Sin conectividad de red
```bash
# Verificar bridge
ip link show

# Reiniciar red en VM
sudo systemctl restart networking
```

### Dashboard no accesible
```bash
# Verificar puerto en VM
sudo netstat -tlnp | grep 5000

# Verificar servicio
systemctl status razonbilstro-nucleus

# Reiniciar núcleo
nucleus --restart
```

### Rendimiento lento
```bash
# Verificar recursos VM
python3 hardware_monitor.py

# Aumentar RAM en start_vm.sh
# Cambiar RAM_GB=8 a RAM_GB=16

# Habilitar KVM
# Verificar que -accel kvm esté en start_vm.sh
```

## 📊 Benchmarks Esperados

### Con 8GB RAM, 4 cores
- **Tiempo arranque VM**: 2-3 minutos
- **Tiempo arranque núcleo**: 15-30 segundos
- **Respuesta dashboard**: < 500ms
- **Uso RAM núcleo**: 1-2 GB
- **Uso CPU en reposo**: < 20%

### Optimizaciones VM
- KVM habilitado para aceleración
- Virtio para almacenamiento y red
- Cache writeback para mejor rendimiento
- CPU host passthrough

---

**Entorno de Pruebas VM RazonbilstroOS v2.1.0**
*Configuración completa para testing y desarrollo*
*QEMU/KVM con monitoreo de hardware integrado*

Generado: 2025-05-30 14:27:34
