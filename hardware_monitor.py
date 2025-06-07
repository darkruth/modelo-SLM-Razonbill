#!/usr/bin/env python3
"""
Monitor de Hardware RazonbilstroOS VM
Monitoreo en tiempo real de recursos del sistema
"""

import psutil
import time
import json
import subprocess
from datetime import datetime

class HardwareMonitor:
    """Monitor de hardware para VM"""
    
    def __init__(self):
        self.monitoring = True
        self.log_file = "hardware_monitor.log"
        
    def get_cpu_info(self):
        """Información del CPU"""
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            "per_core_usage": psutil.cpu_percent(percpu=True),
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else []
        }
    
    def get_memory_info(self):
        """Información de memoria"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "ram": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent_used": memory.percent,
                "cached_gb": round(memory.cached / (1024**3), 2) if hasattr(memory, 'cached') else 0
            },
            "swap": {
                "total_gb": round(swap.total / (1024**3), 2),
                "used_gb": round(swap.used / (1024**3), 2),
                "percent_used": swap.percent
            }
        }
    
    def get_disk_info(self):
        """Información de almacenamiento"""
        disks = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent_used": round((usage.used / usage.total) * 100, 1)
                })
            except PermissionError:
                continue
        
        return disks
    
    def get_network_info(self):
        """Información de red"""
        network = psutil.net_io_counters()
        interfaces = []
        
        for interface, stats in psutil.net_io_counters(pernic=True).items():
            interfaces.append({
                "interface": interface,
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv
            })
        
        return {
            "total": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            "interfaces": interfaces
        }
    
    def get_process_info(self):
        """Información de procesos"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if proc.info['cpu_percent'] > 1.0 or proc.info['memory_percent'] > 1.0:
                    processes.append(proc.info)
            except psutil.NoSuchProcess:
                continue
        
        # Ordenar por uso de CPU
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:10]  # Top 10 procesos
    
    def get_system_info(self):
        """Información general del sistema"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            "hostname": subprocess.getoutput("hostname"),
            "kernel": subprocess.getoutput("uname -r"),
            "architecture": subprocess.getoutput("uname -m"),
            "boot_time": boot_time.isoformat(),
            "uptime_hours": round(uptime.total_seconds() / 3600, 1),
            "users_connected": len(psutil.users()),
            "python_version": subprocess.getoutput("python3 --version")
        }
    
    def check_razonbilstro_status(self):
        """Verificar estado de RazonbilstroOS"""
        try:
            # Buscar procesos relacionados
            nucleus_running = False
            vision_running = False
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'main.py' in cmdline or 'nucleus' in cmdline.lower():
                        nucleus_running = True
                    if 'vision' in cmdline.lower():
                        vision_running = True
                except:
                    continue
            
            return {
                "nucleus_active": nucleus_running,
                "vision_active": vision_running,
                "web_port_5000": self.check_port(5000),
                "installation_detected": self.check_installation()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_port(self, port):
        """Verificar si un puerto está en uso"""
        try:
            connections = psutil.net_connections()
            for conn in connections:
                if conn.laddr.port == port and conn.status == 'LISTEN':
                    return True
            return False
        except:
            return False
    
    def check_installation(self):
        """Verificar instalación de RazonbilstroOS"""
        import os
        installation_paths = [
            "/opt/razonbilstro",
            "/home/razonbill",
            "/usr/local/bin/nucleus"
        ]
        
        for path in installation_paths:
            if os.path.exists(path):
                return True
        return False
    
    def collect_all_data(self):
        """Recopilar toda la información del hardware"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "processes": self.get_process_info(),
            "razonbilstro": self.check_razonbilstro_status()
        }
    
    def display_summary(self, data):
        """Mostrar resumen en consola"""
        print(f"\n🖥️ MONITOR DE HARDWARE - {data['timestamp'][:19]}")
        print("=" * 60)
        
        # Sistema
        sys_info = data['system']
        print(f"🖥️ Sistema: {sys_info['hostname']} ({sys_info['architecture']})")
        print(f"⏱️ Uptime: {sys_info['uptime_hours']} horas")
        
        # CPU
        cpu_info = data['cpu']
        print(f"🔄 CPU: {cpu_info['usage_percent']}% ({cpu_info['cores_logical']} cores)")
        
        # Memoria
        mem_info = data['memory']
        ram = mem_info['ram']
        print(f"🧠 RAM: {ram['used_gb']:.1f}GB / {ram['total_gb']:.1f}GB ({ram['percent_used']:.1f}%)")
        
        # Disco
        disk_info = data['disk']
        if disk_info:
            main_disk = disk_info[0]
            print(f"💾 Disco: {main_disk['used_gb']:.1f}GB / {main_disk['total_gb']:.1f}GB ({main_disk['percent_used']:.1f}%)")
        
        # RazonbilstroOS
        razon_info = data['razonbilstro']
        if not razon_info.get('error'):
            nucleus_status = "ACTIVO" if razon_info['nucleus_active'] else "INACTIVO"
            web_status = "DISPONIBLE" if razon_info['web_port_5000'] else "NO DISPONIBLE"
            print(f"🧠 Núcleo: {nucleus_status}")
            print(f"🌐 Dashboard: {web_status} (puerto 5000)")
        
        print("-" * 60)
    
    def save_to_log(self, data):
        """Guardar datos en log"""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(data) + "\n")
    
    def monitor_continuous(self, interval=30):
        """Monitoreo continuo"""
        print("🔍 Iniciando monitor de hardware continuo...")
        print(f"Intervalo: {interval} segundos")
        print("Presiona Ctrl+C para detener")
        
        try:
            while self.monitoring:
                data = self.collect_all_data()
                self.display_summary(data)
                self.save_to_log(data)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Monitor detenido por usuario")
            self.monitoring = False
    
    def monitor_once(self):
        """Monitoreo único"""
        data = self.collect_all_data()
        self.display_summary(data)
        return data

def main():
    import sys
    
    monitor = HardwareMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monitor.monitor_continuous(interval)
    else:
        print("🔍 MONITOR DE HARDWARE RAZONBILSTROS VM")
        print("=" * 50)
        data = monitor.monitor_once()
        
        print("\nPara monitoreo continuo:")
        print("  python3 hardware_monitor.py --continuous [intervalo_segundos]")

if __name__ == "__main__":
    main()
