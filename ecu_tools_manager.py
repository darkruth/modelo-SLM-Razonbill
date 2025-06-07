#!/usr/bin/env python3
"""
ECU Tools Manager para Gym-Razonbilstro-µCore v1.0
Gestiona herramientas de diagnóstico y programación de ECU por niveles
"""

import os
import json
import subprocess
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ToolLevel(Enum):
    """Niveles de herramientas según complejidad y acceso"""
    BASIC = "basic"          # OBD-II, lectura básica
    INTERMEDIATE = "intermediate"  # EEPROM, FLASH básico
    ADVANCED = "advanced"    # MCU, programación directa
    PROFESSIONAL = "professional"  # Herramientas comerciales

class ECUComponent(Enum):
    """Componentes de ECU soportados"""
    EEPROM = "eeprom"       # Datos de calibración, kilometraje
    FLASH = "flash"         # Firmware, mapas del motor
    MCU = "mcu"            # Microcontrolador principal

class ECUToolsManager:
    """
    Gestor principal de herramientas ECU
    Organiza herramientas por nivel y función específica
    """
    
    def __init__(self):
        self.tools_base_dir = Path("gym_razonbilstro/tools")
        self.metadata_dir = Path("gym_razonbilstro/metadata")
        
        # Crear estructura de directorios
        self._create_directory_structure()
        
        # Configuración de herramientas por nivel
        self.tools_config = {
            ToolLevel.BASIC: {
                "python-obd": {
                    "component": ECUComponent.EEPROM,
                    "description": "Lectura OBD-II estándar",
                    "install_cmd": ["pip", "install", "obd"],
                    "test_cmd": ["python", "-c", "import obd; print('OBD OK')"],
                    "functions": ["read_dtc", "read_sensors", "clear_codes"]
                },
                "can-utils": {
                    "component": ECUComponent.MCU,
                    "description": "Utilidades CAN bus",
                    "install_cmd": ["apt", "install", "-y", "can-utils"],
                    "test_cmd": ["which", "cansend"],
                    "functions": ["can_send", "can_dump", "can_monitor"]
                }
            },
            ToolLevel.INTERMEDIATE: {
                "flashrom": {
                    "component": ECUComponent.FLASH,
                    "description": "Lectura/escritura EEPROM y Flash",
                    "install_cmd": ["apt", "install", "-y", "flashrom"],
                    "test_cmd": ["flashrom", "--version"],
                    "functions": ["read_flash", "write_flash", "verify_flash"]
                },
                "minipro": {
                    "component": ECUComponent.EEPROM,
                    "description": "Programador TL866",
                    "install_cmd": ["git", "clone", "https://gitlab.com/DavidGriffith/minipro.git"],
                    "build_cmd": ["make", "-C", "minipro", "&&", "make", "-C", "minipro", "install"],
                    "test_cmd": ["minipro", "--version"],
                    "functions": ["read_eeprom", "write_eeprom", "verify_eeprom"]
                },
                "pyserial": {
                    "component": ECUComponent.MCU,
                    "description": "Comunicación serial",
                    "install_cmd": ["pip", "install", "pyserial"],
                    "test_cmd": ["python", "-c", "import serial; print('Serial OK')"],
                    "functions": ["serial_communication", "uart_access"]
                }
            },
            ToolLevel.ADVANCED: {
                "openocd": {
                    "component": ECUComponent.MCU,
                    "description": "JTAG/SWD debugger",
                    "install_cmd": ["apt", "install", "-y", "openocd"],
                    "test_cmd": ["openocd", "--version"],
                    "functions": ["jtag_debug", "mcu_programming", "memory_dump"]
                },
                "avrdude": {
                    "component": ECUComponent.MCU,
                    "description": "Programador AVR/ARM",
                    "install_cmd": ["apt", "install", "-y", "avrdude"],
                    "test_cmd": ["avrdude", "-?"],
                    "functions": ["avr_programming", "fuse_bits", "memory_read"]
                },
                "binwalk": {
                    "component": ECUComponent.FLASH,
                    "description": "Análisis de firmware binario",
                    "install_cmd": ["apt", "install", "-y", "binwalk"],
                    "test_cmd": ["binwalk", "--help"],
                    "functions": ["firmware_analysis", "extract_maps", "find_tables"]
                }
            },
            ToolLevel.PROFESSIONAL: {
                "wine": {
                    "component": ECUComponent.FLASH,
                    "description": "Ejecutar herramientas Windows",
                    "install_cmd": ["apt", "install", "-y", "wine64"],
                    "test_cmd": ["wine", "--version"],
                    "functions": ["run_winols", "run_ecuflash", "run_ecm_titanium"]
                }
            }
        }
        
        # Estado de instalación
        self.installed_tools = {}
        self.tool_metadata = {}
        
    def _create_directory_structure(self):
        """Crear estructura de directorios para herramientas"""
        directories = [
            self.tools_base_dir / "basic",
            self.tools_base_dir / "intermediate", 
            self.tools_base_dir / "advanced",
            self.tools_base_dir / "professional",
            self.metadata_dir / "training_metadata",
            self.metadata_dir / "tool_configs",
            self.metadata_dir / "datasets"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        logger.info("Estructura de directorios ECU creada")
    
    def install_tools_by_level(self, level: ToolLevel) -> Dict[str, bool]:
        """
        Instalar herramientas de un nivel específico
        
        Args:
            level: Nivel de herramientas a instalar
            
        Returns:
            Estado de instalación por herramienta
        """
        if level not in self.tools_config:
            return {"error": f"Nivel {level} no configurado"}
        
        installation_results = {}
        tools = self.tools_config[level]
        
        logger.info(f"Instalando herramientas nivel {level.value}")
        
        for tool_name, tool_config in tools.items():
            try:
                success = self._install_single_tool(tool_name, tool_config, level)
                installation_results[tool_name] = success
                
                if success:
                    self.installed_tools[tool_name] = {
                        "level": level,
                        "component": tool_config["component"],
                        "status": "installed"
                    }
                    logger.info(f"✓ {tool_name} instalado exitosamente")
                else:
                    logger.warning(f"⚠ {tool_name} falló en instalación")
                    
            except Exception as e:
                logger.error(f"❌ Error instalando {tool_name}: {e}")
                installation_results[tool_name] = False
        
        return installation_results
    
    def _install_single_tool(self, tool_name: str, config: Dict, level: ToolLevel) -> bool:
        """Instalar una herramienta específica"""
        try:
            # Verificar si ya está instalado
            if self._test_tool_installation(tool_name, config):
                logger.info(f"{tool_name} ya está instalado")
                return True
            
            # Ejecutar comando de instalación
            install_cmd = config.get("install_cmd", [])
            if install_cmd:
                if install_cmd[0] == "apt":
                    # Comando con sudo para apt
                    cmd = ["sudo"] + install_cmd
                else:
                    cmd = install_cmd
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    logger.error(f"Error en instalación de {tool_name}: {result.stderr}")
                    return False
            
            # Ejecutar comando de build si existe
            build_cmd = config.get("build_cmd")
            if build_cmd:
                build_result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True, timeout=600)
                if build_result.returncode != 0:
                    logger.error(f"Error en build de {tool_name}: {build_result.stderr}")
                    return False
            
            # Verificar instalación
            return self._test_tool_installation(tool_name, config)
            
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout instalando {tool_name}")
            return False
        except Exception as e:
            logger.error(f"Excepción instalando {tool_name}: {e}")
            return False
    
    def _test_tool_installation(self, tool_name: str, config: Dict) -> bool:
        """Probar si una herramienta está instalada correctamente"""
        test_cmd = config.get("test_cmd")
        if not test_cmd:
            return True  # Asumir éxito si no hay test
        
        try:
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def create_tool_metadata(self, tool_name: str, dataset_level: str, training_data: Dict) -> str:
        """
        Crear archivo de metadatos para herramienta durante entrenamiento
        
        Args:
            tool_name: Nombre de la herramienta
            dataset_level: Nivel del dataset (basic, intermediate, etc.)
            training_data: Datos del entrenamiento
            
        Returns:
            Ruta del archivo de metadatos creado
        """
        metadata = {
            "tool_name": tool_name,
            "dataset_level": dataset_level,
            "timestamp": time.time(),
            "training_session": training_data.get("session_id"),
            "tool_config": self.tools_config.get(ToolLevel(dataset_level), {}).get(tool_name, {}),
            "training_metrics": {
                "examples_processed": training_data.get("examples_count", 0),
                "success_rate": training_data.get("success_rate", 0.0),
                "tool_usage_patterns": training_data.get("usage_patterns", [])
            },
            "generated_mappings": training_data.get("component_mappings", {}),
            "learned_commands": training_data.get("learned_commands", [])
        }
        
        # Generar nombre de archivo único
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tool_name}_{dataset_level}_{timestamp_str}.json"
        
        # Determinar directorio según nivel
        metadata_dir = self.metadata_dir / "training_metadata" / dataset_level
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        metadata_file = metadata_dir / filename
        
        # Guardar metadatos
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Metadatos de entrenamiento guardados: {metadata_file}")
        return str(metadata_file)
    
    def get_tools_by_component(self, component: ECUComponent) -> List[Dict]:
        """Obtener herramientas disponibles para un componente específico"""
        matching_tools = []
        
        for level, tools in self.tools_config.items():
            for tool_name, config in tools.items():
                if config["component"] == component:
                    tool_info = {
                        "name": tool_name,
                        "level": level.value,
                        "component": component.value,
                        "description": config["description"],
                        "functions": config["functions"],
                        "installed": tool_name in self.installed_tools
                    }
                    matching_tools.append(tool_info)
        
        return matching_tools
    
    def get_installation_status(self) -> Dict:
        """Obtener estado de instalación de todas las herramientas"""
        status = {
            "installed_tools": len(self.installed_tools),
            "tools_by_level": {},
            "tools_by_component": {},
            "installation_details": {}
        }
        
        # Agrupar por nivel
        for level in ToolLevel:
            level_tools = [name for name, info in self.installed_tools.items() 
                          if info["level"] == level]
            status["tools_by_level"][level.value] = len(level_tools)
        
        # Agrupar por componente
        for component in ECUComponent:
            comp_tools = [name for name, info in self.installed_tools.items() 
                         if info["component"] == component]
            status["tools_by_component"][component.value] = len(comp_tools)
        
        # Detalles de instalación
        for tool_name, info in self.installed_tools.items():
            status["installation_details"][tool_name] = {
                "level": info["level"].value,
                "component": info["component"].value,
                "status": info["status"]
            }
        
        return status


def main():
    """Función principal para probar el gestor de herramientas"""
    print("🔧 ECU Tools Manager - Gym-Razonbilstro-µCore v1.0")
    print("=" * 60)
    
    manager = ECUToolsManager()
    
    # Mostrar herramientas por componente
    print("\n🔍 Herramientas para EEPROM:")
    eeprom_tools = manager.get_tools_by_component(ECUComponent.EEPROM)
    for tool in eeprom_tools:
        print(f"  • {tool['name']} ({tool['level']}) - {tool['description']}")
    
    # Estado de instalación
    status = manager.get_installation_status()
    print(f"\n📊 Estado: {status['installed_tools']} herramientas instaladas")


if __name__ == "__main__":
    main()