#!/usr/bin/env python3
"""
OBD-II Interface - Nivel Básico
Herramientas para comunicación OBD-II estándar
"""

import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class OBDInterface:
    """Interfaz OBD-II para diagnóstico básico"""
    
    def __init__(self):
        self.connection = None
        self.supported_pids = []
        
    def connect(self, port: str = None) -> Dict:
        """Conectar al puerto OBD-II"""
        try:
            import obd
            
            if port:
                self.connection = obd.OBD(port)
            else:
                self.connection = obd.OBD()  # Autodetectar
            
            if self.connection.is_connected():
                # Obtener PIDs soportados
                self._discover_supported_pids()
                
                return {
                    "status": "connected",
                    "port": self.connection.port_name(),
                    "protocol": str(self.connection.protocol_name()),
                    "supported_pids": len(self.supported_pids)
                }
            else:
                return {"status": "failed", "error": "No se pudo conectar"}
                
        except ImportError:
            return {"status": "error", "error": "python-obd no instalado"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def read_diagnostic_codes(self) -> Dict:
        """Leer códigos de diagnóstico (DTCs)"""
        if not self.connection or not self.connection.is_connected():
            return {"error": "No hay conexión OBD"}
        
        try:
            import obd
            
            cmd = obd.commands.GET_DTC
            response = self.connection.query(cmd)
            
            if response.is_null():
                return {"dtc_count": 0, "codes": []}
            
            dtc_list = []
            for dtc in response.value:
                dtc_info = {
                    "code": dtc[0],
                    "description": dtc[1] if len(dtc) > 1 else "Sin descripción",
                    "severity": self._classify_dtc_severity(dtc[0])
                }
                dtc_list.append(dtc_info)
            
            return {
                "dtc_count": len(dtc_list),
                "codes": dtc_list,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"error": f"Error leyendo DTCs: {str(e)}"}
    
    def _discover_supported_pids(self):
        """Descubrir PIDs soportados por el vehículo"""
        try:
            import obd
            
            # PIDs básicos comunes
            basic_pids = [
                obd.commands.GET_DTC,
                obd.commands.ENGINE_LOAD,
                obd.commands.COOLANT_TEMP,
                obd.commands.RPM,
                obd.commands.SPEED,
                obd.commands.MAF,
                obd.commands.THROTTLE_POS
            ]
            
            for pid in basic_pids:
                response = self.connection.query(pid)
                if not response.is_null():
                    self.supported_pids.append(pid.name)
                    
        except Exception as e:
            logger.warning(f"Error descubriendo PIDs: {e}")
    
    def _classify_dtc_severity(self, code: str) -> str:
        """Clasificar severidad del código DTC"""
        if code.startswith('P0'):
            return "high"  # Códigos de powertrain críticos
        elif code.startswith('P1'):
            return "medium"  # Códigos específicos del fabricante
        elif code.startswith('B'):
            return "medium"  # Códigos de carrocería
        elif code.startswith('C'):
            return "medium"  # Códigos de chasis
        elif code.startswith('U'):
            return "low"  # Códigos de red/comunicación
        else:
            return "unknown"


def main():
    """Función de prueba"""
    print("🚗 OBD-II Interface - Nivel Básico")
    print("=" * 40)


if __name__ == "__main__":
    main()