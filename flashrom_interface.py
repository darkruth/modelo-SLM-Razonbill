#!/usr/bin/env python3
"""
Flashrom Interface - Nivel Intermedio
Herramientas para lectura/escritura de EEPROM y FLASH
"""

import subprocess
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class FlashromInterface:
    """Interfaz para flashrom - lectura/escritura de chips FLASH/EEPROM"""
    
    def __init__(self):
        self.supported_programmers = [
            "ch341a_spi",  # Programador CH341A USB
            "buspirate_spi",  # Bus Pirate
            "ft2232_spi",  # FTDI FT2232
            "serprog",  # Protocolo serprog
            "internal"  # Programador interno
        ]
        
        self.backup_dir = Path("gym_razonbilstro/backups/flash")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def detect_chip(self, programmer: str = "ch341a_spi") -> Dict:
        """Detectar chip FLASH/EEPROM conectado"""
        cmd = ["sudo", "flashrom", "-p", programmer]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parsear salida para detectar chip
            chip_info = self._parse_chip_detection(result.stdout)
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "programmer": programmer,
                "detected_chips": chip_info,
                "raw_output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Timeout detectando chip"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _parse_chip_detection(self, output: str) -> List[Dict]:
        """Parsear salida de detección de chip"""
        chips = []
        lines = output.split('\n')
        
        for line in lines:
            if "Found" in line and "flash chip" in line:
                # Extraer información del chip
                parts = line.split()
                if len(parts) >= 4:
                    chip_info = {
                        "manufacturer": parts[1] if len(parts) > 1 else "Unknown",
                        "model": parts[2] if len(parts) > 2 else "Unknown", 
                        "size": self._extract_size(line),
                        "supported": "supported" in line.lower()
                    }
                    chips.append(chip_info)
        
        return chips
    
    def _extract_size(self, line: str) -> str:
        """Extraer tamaño del chip de la línea de salida"""
        size_indicators = ["KB", "MB", "kB", "mB"]
        for indicator in size_indicators:
            if indicator in line:
                words = line.split()
                for i, word in enumerate(words):
                    if indicator in word and i > 0:
                        return words[i-1] + " " + indicator
        return "Unknown"
    
    def read_flash(self, programmer: str, output_file: str, chip_type: str = None) -> Dict:
        """Leer contenido del chip FLASH"""
        # Crear backup con timestamp
        timestamp = int(time.time())
        backup_file = self.backup_dir / f"flash_backup_{timestamp}.bin"
        
        cmd = ["sudo", "flashrom", "-p", programmer, "-r", str(backup_file)]
        
        if chip_type:
            cmd.extend(["-c", chip_type])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0 and backup_file.exists():
                # Copiar a archivo solicitado si es diferente
                if output_file != str(backup_file):
                    import shutil
                    shutil.copy2(backup_file, output_file)
                
                # Generar checksum
                checksum = self._calculate_checksum(backup_file)
                
                return {
                    "status": "success",
                    "file_created": output_file,
                    "backup_file": str(backup_file),
                    "file_size": backup_file.stat().st_size,
                    "checksum_md5": checksum,
                    "programmer": programmer,
                    "chip_type": chip_type,
                    "read_time": self._extract_read_time(result.stdout)
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "output": result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Timeout leyendo flash"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def write_flash(self, programmer: str, input_file: str, chip_type: str = None, verify: bool = True) -> Dict:
        """Escribir archivo al chip FLASH"""
        if not os.path.exists(input_file):
            return {"status": "error", "error": f"Archivo {input_file} no existe"}
        
        # Verificar checksum antes de escribir
        pre_checksum = self._calculate_checksum(input_file)
        
        cmd = ["sudo", "flashrom", "-p", programmer, "-w", input_file]
        
        if chip_type:
            cmd.extend(["-c", chip_type])
        
        if verify:
            cmd.append("-v")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            success = result.returncode == 0
            
            response = {
                "status": "success" if success else "error",
                "programmer": programmer,
                "input_file": input_file,
                "pre_write_checksum": pre_checksum,
                "chip_type": chip_type,
                "verification": verify and success,
                "write_time": self._extract_write_time(result.stdout),
                "output": result.stdout
            }
            
            if not success:
                response["error"] = result.stderr
            
            return response
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Timeout escribiendo flash"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def verify_flash(self, programmer: str, reference_file: str, chip_type: str = None) -> Dict:
        """Verificar contenido del chip contra archivo de referencia"""
        if not os.path.exists(reference_file):
            return {"status": "error", "error": f"Archivo de referencia {reference_file} no existe"}
        
        cmd = ["sudo", "flashrom", "-p", programmer, "-v", reference_file]
        
        if chip_type:
            cmd.extend(["-c", chip_type])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            verification_passed = result.returncode == 0 and "VERIFIED" in result.stdout
            
            return {
                "status": "success",
                "verification_passed": verification_passed,
                "programmer": programmer,
                "reference_file": reference_file,
                "chip_type": chip_type,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Timeout verificando flash"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calcular checksum MD5 de un archivo"""
        import hashlib
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception:
            return "unknown"
    
    def _extract_read_time(self, output: str) -> str:
        """Extraer tiempo de lectura de la salida"""
        for line in output.split('\n'):
            if "Reading flash" in line or "took" in line:
                if "s" in line:
                    words = line.split()
                    for i, word in enumerate(words):
                        if word.endswith('s') and word[:-1].replace('.', '').isdigit():
                            return word
        return "unknown"
    
    def _extract_write_time(self, output: str) -> str:
        """Extraer tiempo de escritura de la salida"""
        for line in output.split('\n'):
            if "Writing flash" in line or "took" in line:
                if "s" in line:
                    words = line.split()
                    for i, word in enumerate(words):
                        if word.endswith('s') and word[:-1].replace('.', '').isdigit():
                            return word
        return "unknown"
    
    def get_supported_chips(self) -> Dict:
        """Obtener lista de chips soportados"""
        cmd = ["flashrom", "--list-supported"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parsear lista de chips soportados
                chips = self._parse_supported_chips(result.stdout)
                
                return {
                    "status": "success",
                    "total_chips": len(chips),
                    "chips": chips[:50],  # Limitar a primeros 50
                    "programmers": self.supported_programmers
                }
            else:
                return {"status": "error", "error": result.stderr}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _parse_supported_chips(self, output: str) -> List[Dict]:
        """Parsear lista de chips soportados"""
        chips = []
        lines = output.split('\n')
        
        for line in lines:
            if line.strip() and not line.startswith('#') and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    chip = {
                        "manufacturer": parts[0].strip(),
                        "model": parts[1].strip(),
                        "size": parts[2].strip() if len(parts) > 2 else "Unknown"
                    }
                    chips.append(chip)
        
        return chips


def main():
    """Función de prueba"""
    import time
    
    print("⚡ Flashrom Interface - Nivel Intermedio")
    print("=" * 50)
    
    flashrom = FlashromInterface()
    
    # Detectar chip
    print("Detectando chips...")
    detection = flashrom.detect_chip()
    print(f"Detección: {detection['status']}")
    if detection.get('detected_chips'):
        for chip in detection['detected_chips']:
            print(f"  • {chip['manufacturer']} {chip['model']} ({chip['size']})")
    
    # Mostrar chips soportados
    print("\nObteniendo lista de chips soportados...")
    supported = flashrom.get_supported_chips()
    print(f"Chips soportados: {supported.get('total_chips', 0)}")


if __name__ == "__main__":
    main()