#!/usr/bin/env python3
"""
Binwalk Analyzer - Nivel Avanzado
Análisis de firmware y extracción de mapas ECU
"""

import subprocess
import logging
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class BinwalkAnalyzer:
    """Analizador de firmware ECU usando binwalk"""
    
    def __init__(self):
        self.analysis_dir = Path("gym_razonbilstro/analysis")
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Patrones específicos de ECU
        self.ecu_patterns = {
            "calibration_tables": [
                b"\x00\x01\x02\x03",  # Patrón típico de tabla
                b"\xFF\xFE\xFD\xFC",  # Patrón inverso
            ],
            "map_headers": [
                b"MAP_",
                b"CAL_",
                b"TBL_",
                b"AXIS_"
            ],
            "dtc_tables": [
                b"P0",
                b"B0", 
                b"C0",
                b"U0"
            ]
        }
    
    def analyze_firmware(self, firmware_file: str, extract: bool = False) -> Dict:
        """Análisis completo de firmware ECU"""
        if not os.path.exists(firmware_file):
            return {"error": f"Archivo {firmware_file} no existe"}
        
        # Análisis básico con binwalk
        basic_analysis = self._run_basic_binwalk(firmware_file)
        
        # Búsqueda de patrones ECU específicos
        ecu_patterns = self._find_ecu_patterns(firmware_file)
        
        # Análisis de entropía
        entropy_analysis = self._analyze_entropy(firmware_file)
        
        # Extracción opcional
        extracted_files = []
        if extract:
            extracted_files = self._extract_firmware(firmware_file)
        
        return {
            "status": "success",
            "firmware_file": firmware_file,
            "file_size": os.path.getsize(firmware_file),
            "basic_analysis": basic_analysis,
            "ecu_patterns": ecu_patterns,
            "entropy_analysis": entropy_analysis,
            "extracted_files": extracted_files if extract else [],
            "recommendations": self._generate_recommendations(basic_analysis, ecu_patterns)
        }
    
    def _run_basic_binwalk(self, firmware_file: str) -> Dict:
        """Ejecutar análisis básico con binwalk"""
        cmd = ["binwalk", "-B", firmware_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            signatures = self._parse_binwalk_output(result.stdout)
            
            return {
                "status": "success",
                "signatures_found": len(signatures),
                "signatures": signatures,
                "raw_output": result.stdout
            }
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Timeout analizando firmware"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _parse_binwalk_output(self, output: str) -> List[Dict]:
        """Parsear salida de binwalk"""
        signatures = []
        lines = output.split('\n')
        
        for line in lines:
            if line.strip() and not line.startswith('DECIMAL'):
                parts = line.split()
                if len(parts) >= 3 and parts[0].isdigit():
                    signature = {
                        "offset_decimal": int(parts[0]),
                        "offset_hex": parts[1],
                        "description": " ".join(parts[2:]),
                        "type": self._classify_signature(" ".join(parts[2:]))
                    }
                    signatures.append(signature)
        
        return signatures
    
    def _classify_signature(self, description: str) -> str:
        """Clasificar tipo de firma encontrada"""
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ["filesystem", "cramfs", "squashfs"]):
            return "filesystem"
        elif any(keyword in description_lower for keyword in ["compressed", "gzip", "lzma"]):
            return "compressed_data"
        elif any(keyword in description_lower for keyword in ["executable", "elf", "pe"]):
            return "executable"
        elif any(keyword in description_lower for keyword in ["certificate", "key", "crypto"]):
            return "cryptographic"
        else:
            return "unknown"
    
    def _find_ecu_patterns(self, firmware_file: str) -> Dict:
        """Buscar patrones específicos de ECU"""
        patterns_found = {}
        
        try:
            with open(firmware_file, 'rb') as f:
                content = f.read()
            
            for pattern_type, patterns in self.ecu_patterns.items():
                found_offsets = []
                
                for pattern in patterns:
                    offset = 0
                    while True:
                        pos = content.find(pattern, offset)
                        if pos == -1:
                            break
                        found_offsets.append({
                            "offset": pos,
                            "hex_offset": f"0x{pos:X}",
                            "pattern": pattern.hex(),
                            "context": content[max(0, pos-16):pos+16+len(pattern)].hex()
                        })
                        offset = pos + 1
                
                patterns_found[pattern_type] = found_offsets
            
            return {
                "status": "success",
                "patterns_found": patterns_found,
                "total_matches": sum(len(matches) for matches in patterns_found.values())
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _analyze_entropy(self, firmware_file: str) -> Dict:
        """Análisis de entropía para detectar datos comprimidos/cifrados"""
        cmd = ["binwalk", "-E", firmware_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                entropy_data = self._parse_entropy_output(result.stdout)
                return {
                    "status": "success",
                    "entropy_data": entropy_data,
                    "high_entropy_regions": [e for e in entropy_data if e.get("entropy", 0) > 0.8]
                }
            else:
                return {"status": "error", "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Timeout analizando entropía"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _parse_entropy_output(self, output: str) -> List[Dict]:
        """Parsear salida de análisis de entropía"""
        entropy_data = []
        lines = output.split('\n')
        
        for line in lines:
            if line.strip() and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        entropy_entry = {
                            "offset": int(parts[0]),
                            "entropy": float(parts[1]) if parts[1].replace('.', '').isdigit() else 0.0
                        }
                        entropy_data.append(entropy_entry)
                    except ValueError:
                        continue
        
        return entropy_data
    
    def _extract_firmware(self, firmware_file: str) -> List[Dict]:
        """Extraer archivos del firmware"""
        extract_dir = self.analysis_dir / f"extracted_{Path(firmware_file).stem}"
        extract_dir.mkdir(exist_ok=True)
        
        cmd = ["binwalk", "-e", "-C", str(extract_dir), firmware_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            extracted_files = []
            if extract_dir.exists():
                for root, dirs, files in os.walk(extract_dir):
                    for file in files:
                        file_path = Path(root) / file
                        file_info = {
                            "filename": file,
                            "path": str(file_path),
                            "size": file_path.stat().st_size,
                            "type": self._identify_file_type(file_path)
                        }
                        extracted_files.append(file_info)
            
            return extracted_files
            
        except subprocess.TimeoutExpired:
            return [{"error": "Timeout extrayendo firmware"}]
        except Exception as e:
            return [{"error": str(e)}]
    
    def _identify_file_type(self, file_path: Path) -> str:
        """Identificar tipo de archivo extraído"""
        try:
            cmd = ["file", str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                file_type = result.stdout.split(':')[1].strip() if ':' in result.stdout else "unknown"
                return file_type
            else:
                return "unknown"
                
        except Exception:
            return "unknown"
    
    def _generate_recommendations(self, basic_analysis: Dict, ecu_patterns: Dict) -> List[str]:
        """Generar recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Basado en firmas encontradas
        if basic_analysis.get("signatures_found", 0) > 0:
            filesystem_sigs = [s for s in basic_analysis.get("signatures", []) if s["type"] == "filesystem"]
            if filesystem_sigs:
                recommendations.append("Se encontraron sistemas de archivos - considerar extracción completa")
            
            crypto_sigs = [s for s in basic_analysis.get("signatures", []) if s["type"] == "cryptographic"]
            if crypto_sigs:
                recommendations.append("Se detectaron elementos criptográficos - firmware posiblemente cifrado")
        
        # Basado en patrones ECU
        if ecu_patterns.get("total_matches", 0) > 0:
            cal_matches = len(ecu_patterns.get("patterns_found", {}).get("calibration_tables", []))
            if cal_matches > 5:
                recommendations.append("Múltiples tablas de calibración detectadas - candidato para edición de mapas")
            
            dtc_matches = len(ecu_patterns.get("patterns_found", {}).get("dtc_tables", []))
            if dtc_matches > 0:
                recommendations.append("Códigos DTC encontrados - revisar tabla de diagnósticos")
        
        if not recommendations:
            recommendations.append("Análisis básico completado - considerar análisis manual adicional")
        
        return recommendations
    
    def extract_calibration_maps(self, firmware_file: str, output_dir: str = None) -> Dict:
        """Extraer mapas de calibración específicos"""
        if output_dir is None:
            output_dir = str(self.analysis_dir / "calibration_maps")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            with open(firmware_file, 'rb') as f:
                content = f.read()
            
            maps_extracted = []
            
            # Buscar patrones de mapas de calibración
            for pattern in self.ecu_patterns["calibration_tables"]:
                offset = 0
                map_count = 0
                
                while True:
                    pos = content.find(pattern, offset)
                    if pos == -1:
                        break
                    
                    # Extraer contexto alrededor del patrón (posible mapa)
                    map_start = max(0, pos - 1024)  # 1KB antes
                    map_end = min(len(content), pos + 4096)  # 4KB después
                    map_data = content[map_start:map_end]
                    
                    # Guardar mapa extraído
                    map_filename = f"cal_map_{pos:08X}_{map_count}.bin"
                    map_path = Path(output_dir) / map_filename
                    
                    with open(map_path, 'wb') as map_file:
                        map_file.write(map_data)
                    
                    maps_extracted.append({
                        "filename": map_filename,
                        "offset": pos,
                        "size": len(map_data),
                        "pattern": pattern.hex()
                    })
                    
                    map_count += 1
                    offset = pos + 1
                    
                    # Limitar extracción
                    if map_count >= 20:
                        break
            
            return {
                "status": "success",
                "maps_extracted": len(maps_extracted),
                "output_directory": output_dir,
                "extracted_maps": maps_extracted
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}


def main():
    """Función de prueba"""
    print("🔬 Binwalk Analyzer - Nivel Avanzado")
    print("=" * 50)
    
    analyzer = BinwalkAnalyzer()
    
    # Ejemplo de uso (requiere archivo de firmware real)
    firmware_file = "ejemplo_firmware.bin"
    
    print(f"Analizando firmware: {firmware_file}")
    print("(Requiere archivo de firmware real para funcionar)")
    
    # Mostrar patrones que busca
    print("\nPatrones ECU que busca:")
    for pattern_type, patterns in analyzer.ecu_patterns.items():
        print(f"  • {pattern_type}: {len(patterns)} patrones")


if __name__ == "__main__":
    main()