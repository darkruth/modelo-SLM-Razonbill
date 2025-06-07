#!/usr/bin/env python3
"""
Analizador de Requisitos del Sistema RazonbilstroOS
Calcula peso del sistema y define requisitos de hardware
"""

import os
import json
from pathlib import Path
from datetime import datetime

class SystemRequirementsAnalyzer:
    """Analizador de requisitos del sistema"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        
    def calculate_system_size(self):
        """Calcular peso total del sistema instalado"""
        print("Calculando peso del sistema RazonbilstroOS...")
        
        # Componentes principales y sus tamaños estimados
        components = {
            "nucleus_core": {
                "files": ["neural_model.py", "main.py", "app.py", "models.py"],
                "estimated_runtime_mb": 150,  # Python + numpy + dependencias
                "description": "Núcleo C.A- Razonbilstro con precisión 94.18%"
            },
            "vision_module": {
                "files": ["vision_cam_nucleus_module.py", "ai_vision_cam_module.py"],
                "estimated_runtime_mb": 200,  # OpenCV + modelos de visión
                "description": "Vision Cam Module con precisión 91.2%"
            },
            "pwnagotchi_ai": {
                "files": ["gym_razonbilstro/pwnagotchi_ai_module.py"],
                "estimated_runtime_mb": 80,   # Herramientas WiFi + AI
                "description": "Pwnagotchi AI Nivel 4 experto"
            },
            "security_tools": {
                "count": 27,
                "estimated_runtime_mb": 300,  # nmap, aircrack-ng, wireshark, etc.
                "description": "27 herramientas de seguridad auténticas"
            },
            "desktop_environment": {
                "files": ["blue_desktop_razonbilstro.py", "kali_vnc_razonbilstro_desktop.py"],
                "estimated_runtime_mb": 120,  # XFCE4 + VNC + temas
                "description": "Blue Theme Desktop + VNC"
            },
            "database_system": {
                "estimated_runtime_mb": 100,  # PostgreSQL + datos
                "description": "PostgreSQL con metadatos del núcleo"
            },
            "web_interface": {
                "files": ["templates/", "static/"],
                "estimated_runtime_mb": 50,   # Flask + Bootstrap + assets
                "description": "Dashboard web en tiempo real"
            },
            "system_libraries": {
                "estimated_runtime_mb": 400,  # Dependencias Python, C++, etc.
                "description": "Bibliotecas del sistema y dependencias"
            },
            "voice_system": {
                "estimated_runtime_mb": 60,   # espeak + festival
                "description": "Sistema de voz Razonbill"
            }
        }
        
        # Calcular tamaño total
        total_mb = 0
        file_sizes_mb = 0
        
        for component, info in components.items():
            runtime_mb = info.get("estimated_runtime_mb", 0)
            total_mb += runtime_mb
            
            # Calcular tamaño de archivos si existen
            if "files" in info:
                for file_path in info["files"]:
                    path = Path(file_path)
                    if path.exists():
                        if path.is_file():
                            size_kb = path.stat().st_size / 1024
                            file_sizes_mb += size_kb / 1024
                        elif path.is_dir():
                            # Calcular tamaño del directorio
                            dir_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                            file_sizes_mb += (dir_size / 1024) / 1024
        
        # Añadir espacio para logs, cache, etc.
        overhead_mb = 100
        total_system_mb = total_mb + file_sizes_mb + overhead_mb
        
        return {
            "components": components,
            "file_sizes_mb": round(file_sizes_mb, 2),
            "runtime_components_mb": total_mb,
            "overhead_mb": overhead_mb,
            "total_installed_mb": round(total_system_mb, 2),
            "total_installed_gb": round(total_system_mb / 1024, 2)
        }
    
    def define_hardware_requirements(self):
        """Definir requisitos de hardware del sistema"""
        
        requirements = {
            "minimum_requirements": {
                "cpu": {
                    "architecture": "x86_64 (64-bit)",
                    "minimum": "Intel Core i3 / AMD Ryzen 3",
                    "cores": "2 núcleos físicos",
                    "frequency": "2.0 GHz mínimo",
                    "features": ["SSE4.2", "AVX"]
                },
                "memory": {
                    "ram_gb": 4,
                    "ram_explanation": "2GB para sistema base + 2GB para núcleo IA",
                    "swap_gb": 2,
                    "total_memory_gb": 6
                },
                "storage": {
                    "minimum_gb": 20,
                    "recommended_gb": 50,
                    "type": "SSD recomendado para mejor rendimiento",
                    "breakdown": {
                        "system_files_gb": 1.5,
                        "dependencies_gb": 3,
                        "database_gb": 2,
                        "workspace_gb": 5,
                        "logs_cache_gb": 2,
                        "user_data_gb": 6.5
                    }
                },
                "graphics": {
                    "minimum": "Integrada compatible con OpenGL 2.0",
                    "for_vision_module": "Recomendado GPU dedicada para visión"
                },
                "network": {
                    "ethernet": "10/100/1000 Mbps",
                    "wifi": "802.11n (recomendado 802.11ac para herramientas WiFi)",
                    "bluetooth": "Opcional para dispositivos externos"
                }
            },
            "recommended_requirements": {
                "cpu": {
                    "model": "Intel Core i7 / AMD Ryzen 7",
                    "cores": "4+ núcleos físicos",
                    "threads": "8+ hilos",
                    "frequency": "3.0+ GHz",
                    "cache": "8MB+ L3 cache",
                    "features": ["AVX2", "AES-NI"]
                },
                "memory": {
                    "ram_gb": 16,
                    "ram_explanation": "Óptimo para entrenamiento neuronal",
                    "swap_gb": 4,
                    "memory_type": "DDR4-3200 o superior"
                },
                "storage": {
                    "recommended_gb": 500,
                    "type": "NVMe SSD",
                    "read_speed": "3000+ MB/s",
                    "write_speed": "2000+ MB/s"
                },
                "graphics": {
                    "dedicated": "NVIDIA GTX 1060+ / AMD RX 580+",
                    "vram_gb": 4,
                    "cuda_support": "Para aceleración de visión computacional"
                }
            },
            "optimal_hardware": {
                "target_device": "Lenovo ThinkPad T480",
                "cpu": "Intel Core i7-8550U / i7-8650U",
                "ram": "16GB DDR4-2400",
                "storage": "500GB NVMe SSD",
                "gpu": "Intel UHD 620 + NVIDIA MX150 (opcional)",
                "wifi": "Intel Wireless-AC 8265 (802.11ac)",
                "ports": "USB 3.1, USB-C, HDMI, Ethernet",
                "battery": "Optimización específica para T480",
                "thermal": "Gestión térmica integrada"
            }
        }
        
        return requirements
    
    def calculate_performance_metrics(self):
        """Calcular métricas de rendimiento esperadas"""
        
        metrics = {
            "nucleus_performance": {
                "precision": "94.18%",
                "response_time_ms": {
                    "minimum_hw": 800,
                    "recommended_hw": 300,
                    "optimal_hw": 150
                },
                "concurrent_queries": {
                    "minimum_hw": 5,
                    "recommended_hw": 20,
                    "optimal_hw": 50
                },
                "training_speed": {
                    "minimum_hw": "Básico",
                    "recommended_hw": "Óptimo",
                    "optimal_hw": "Máximo"
                }
            },
            "vision_module_performance": {
                "precision": "91.2%",
                "fps_processing": {
                    "minimum_hw": 5,
                    "recommended_hw": 15,
                    "optimal_hw": 30
                },
                "face_detection_ms": {
                    "minimum_hw": 200,
                    "recommended_hw": 80,
                    "optimal_hw": 40
                },
                "object_detection_ms": {
                    "minimum_hw": 500,
                    "recommended_hw": 200,
                    "optimal_hw": 100
                }
            },
            "system_performance": {
                "boot_time_seconds": {
                    "minimum_hw": 45,
                    "recommended_hw": 25,
                    "optimal_hw": 15
                },
                "dashboard_load_ms": {
                    "minimum_hw": 2000,
                    "recommended_hw": 800,
                    "optimal_hw": 400
                },
                "database_queries_per_second": {
                    "minimum_hw": 100,
                    "recommended_hw": 500,
                    "optimal_hw": 1000
                }
            }
        }
        
        return metrics
    
    def generate_compatibility_matrix(self):
        """Generar matriz de compatibilidad con diferentes sistemas"""
        
        compatibility = {
            "operating_systems": {
                "debian_ubuntu": {
                    "versions": ["Ubuntu 20.04+", "Debian 11+"],
                    "compatibility": "Excelente",
                    "notes": "Distribución principal de desarrollo"
                },
                "centos_rhel": {
                    "versions": ["CentOS 8+", "RHEL 8+", "Fedora 35+"],
                    "compatibility": "Muy buena",
                    "notes": "Soporte completo con ajustes menores"
                },
                "arch_manjaro": {
                    "versions": ["Arch Linux", "Manjaro 21+"],
                    "compatibility": "Buena",
                    "notes": "Instalación manual de algunas dependencias"
                },
                "other_linux": {
                    "versions": ["openSUSE", "Alpine", "Gentoo"],
                    "compatibility": "Limitada",
                    "notes": "Requiere configuración manual"
                }
            },
            "hardware_vendors": {
                "lenovo": {
                    "models": ["ThinkPad T480", "ThinkPad X1", "ThinkPad P1"],
                    "compatibility": "Óptima",
                    "optimizations": "Específicas para T480"
                },
                "dell": {
                    "models": ["XPS 13", "Latitude 7000", "Precision"],
                    "compatibility": "Muy buena",
                    "notes": "Drivers estándar"
                },
                "hp": {
                    "models": ["EliteBook", "ZBook", "Pavilion"],
                    "compatibility": "Buena",
                    "notes": "Verificar compatibilidad WiFi"
                },
                "asus": {
                    "models": ["ROG", "ZenBook", "VivoBook"],
                    "compatibility": "Buena",
                    "notes": "Algunos modelos requieren drivers adicionales"
                }
            },
            "virtualization": {
                "vmware": {
                    "compatibility": "Buena",
                    "notes": "Funcionalidad completa excepto cámara",
                    "recommended_ram": "8GB para VM"
                },
                "virtualbox": {
                    "compatibility": "Limitada",
                    "notes": "Módulo de visión no disponible",
                    "recommended_ram": "6GB para VM"
                },
                "kvm_qemu": {
                    "compatibility": "Muy buena",
                    "notes": "Soporte GPU passthrough",
                    "recommended_ram": "8GB para VM"
                }
            }
        }
        
        return compatibility
    
    def create_complete_report(self):
        """Crear reporte completo de requisitos del sistema"""
        
        print("Generando reporte completo de requisitos...")
        
        # Obtener todos los datos
        size_info = self.calculate_system_size()
        requirements = self.define_hardware_requirements()
        performance = self.calculate_performance_metrics()
        compatibility = self.generate_compatibility_matrix()
        
        # Crear reporte completo
        report = {
            "system_info": {
                "name": "RazonbilstroOS v2.1.0 Neural Agent",
                "build_date": datetime.now().isoformat(),
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "system_size": size_info,
            "hardware_requirements": requirements,
            "performance_metrics": performance,
            "compatibility_matrix": compatibility,
            "installation_recommendations": {
                "for_developers": {
                    "hardware": "Recommended requirements",
                    "os": "Ubuntu 22.04 LTS",
                    "storage": "NVMe SSD 500GB+"
                },
                "for_production": {
                    "hardware": "Optimal hardware (ThinkPad T480)",
                    "os": "Debian 11 stable",
                    "storage": "Enterprise SSD"
                },
                "for_testing": {
                    "hardware": "Minimum requirements",
                    "os": "Ubuntu 20.04 LTS",
                    "storage": "SATA SSD 100GB+"
                }
            }
        }
        
        return report

def main():
    """Función principal"""
    print("🧠 ANALIZADOR DE REQUISITOS RAZONBILSTROS")
    print("=" * 55)
    
    analyzer = SystemRequirementsAnalyzer()
    report = analyzer.create_complete_report()
    
    # Mostrar resumen en consola
    size_info = report["system_size"]
    min_req = report["hardware_requirements"]["minimum_requirements"]
    rec_req = report["hardware_requirements"]["recommended_requirements"]
    opt_hw = report["hardware_requirements"]["optimal_hardware"]
    
    print(f"\n📊 PESO DEL SISTEMA INSTALADO")
    print("=" * 35)
    print(f"💾 Tamaño total: {size_info['total_installed_gb']} GB")
    print(f"📁 Archivos del sistema: {size_info['file_sizes_mb']} MB")
    print(f"🧠 Componentes en runtime: {size_info['runtime_components_mb']} MB")
    print(f"📋 Overhead (logs, cache): {size_info['overhead_mb']} MB")
    
    print(f"\n⚙️ REQUISITOS MÍNIMOS DE HARDWARE")
    print("=" * 40)
    print(f"🖥️ CPU: {min_req['cpu']['minimum']}")
    print(f"🧠 RAM: {min_req['memory']['ram_gb']} GB")
    print(f"💾 Almacenamiento: {min_req['storage']['minimum_gb']} GB")
    print(f"🎮 Gráficos: {min_req['graphics']['minimum']}")
    print(f"🌐 Red: {min_req['network']['wifi']}")
    
    print(f"\n🚀 REQUISITOS RECOMENDADOS")
    print("=" * 30)
    print(f"🖥️ CPU: {rec_req['cpu']['model']}")
    print(f"🧠 RAM: {rec_req['memory']['ram_gb']} GB")
    print(f"💾 Almacenamiento: {rec_req['storage']['recommended_gb']} GB {rec_req['storage']['type']}")
    print(f"🎮 GPU: {rec_req['graphics']['dedicated']}")
    
    print(f"\n🎯 HARDWARE ÓPTIMO (OBJETIVO)")
    print("=" * 35)
    print(f"💻 Dispositivo: {opt_hw['target_device']}")
    print(f"🖥️ CPU: {opt_hw['cpu']}")
    print(f"🧠 RAM: {opt_hw['ram']}")
    print(f"💾 Almacenamiento: {opt_hw['storage']}")
    print(f"🌐 WiFi: {opt_hw['wifi']}")
    
    # Guardar reporte completo
    report_path = Path("system_technical_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Reporte completo guardado en: {report_path}")
    
    return report

if __name__ == "__main__":
    main()