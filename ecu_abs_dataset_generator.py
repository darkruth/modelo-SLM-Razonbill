#!/usr/bin/env python3
"""
Generador de Dataset ECU ABS - EEPROM/EPROM Programming
100K parámetros: 50K entrada + 50K salida
Enfoque técnico en C/C++ para programación de ECU ABS
"""

import json
import random
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ECUABSDatasetGenerator:
    """
    Generador de dataset técnico para programación ECU ABS
    Enfoque en EEPROM/EPROM con código C/C++ real
    """
    
    def __init__(self):
        self.output_dir = Path("gym_razonbilstro/datasets/ecu_abs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Registros ABS reales
        self.abs_registers = {
            "WHEEL_SPEED_FL": {"address": "0x1000", "size": 16, "type": "uint16_t"},
            "WHEEL_SPEED_FR": {"address": "0x1002", "size": 16, "type": "uint16_t"},
            "WHEEL_SPEED_RL": {"address": "0x1004", "size": 16, "type": "uint16_t"},
            "WHEEL_SPEED_RR": {"address": "0x1006", "size": 16, "type": "uint16_t"},
            "BRAKE_PRESSURE": {"address": "0x1008", "size": 16, "type": "uint16_t"},
            "ABS_STATUS": {"address": "0x100A", "size": 8, "type": "uint8_t"},
            "SENSOR_CALIBRATION": {"address": "0x100C", "size": 32, "type": "uint32_t"},
            "THRESHOLD_TABLE": {"address": "0x1010", "size": 64, "type": "uint8_t[8]"},
            "ERROR_CODES": {"address": "0x1020", "size": 16, "type": "uint16_t"},
            "FIRMWARE_VERSION": {"address": "0x1030", "size": 32, "type": "char[4]"}
        }
        
        # Comandos EEPROM reales
        self.eeprom_commands = {
            "READ_BYTE": "0x03",
            "WRITE_BYTE": "0x02", 
            "READ_STATUS": "0x05",
            "WRITE_ENABLE": "0x06",
            "WRITE_DISABLE": "0x04",
            "CHIP_ERASE": "0xC7",
            "SECTOR_ERASE": "0x20",
            "PAGE_PROGRAM": "0x02"
        }
        
        # Códigos de error ABS reales
        self.abs_error_codes = {
            "0x01": "Sensor velocidad rueda delantera izquierda",
            "0x02": "Sensor velocidad rueda delantera derecha", 
            "0x03": "Sensor velocidad rueda trasera izquierda",
            "0x04": "Sensor velocidad rueda trasera derecha",
            "0x05": "Presión hidráulica insuficiente",
            "0x06": "Falla en modulador ABS",
            "0x07": "Error comunicación CAN",
            "0x08": "EEPROM corrupta"
        }
    
    def generate_complete_dataset(self) -> Dict:
        """Generar dataset completo de 100K parámetros"""
        
        print("🚗 Generando dataset ECU ABS - 100K parámetros")
        print("=" * 50)
        
        # Generar 50K entradas
        input_data = self._generate_input_dataset(50000)
        print(f"✓ Generadas {len(input_data)} entradas")
        
        # Generar 50K salidas correspondientes
        output_data = self._generate_output_dataset(input_data)
        print(f"✓ Generadas {len(output_data)} salidas")
        
        # Combinar en dataset híbrido
        combined_dataset = self._combine_input_output(input_data, output_data)
        
        # Guardar dataset
        dataset_file = self._save_dataset(combined_dataset)
        
        # Generar estadísticas
        stats = self._generate_dataset_statistics(combined_dataset)
        
        return {
            "status": "success",
            "dataset_file": str(dataset_file),
            "total_parameters": len(combined_dataset),
            "input_parameters": len(input_data),
            "output_parameters": len(output_data), 
            "statistics": stats
        }
    
    def _generate_input_dataset(self, count: int) -> List[Dict]:
        """Generar 50K parámetros de entrada técnicos"""
        input_data = []
        
        for i in range(count):
            # Tipos de entrada para ECU ABS
            input_type = random.choice([
                "sensor_reading",
                "eeprom_operation", 
                "calibration_request",
                "error_diagnosis",
                "firmware_update"
            ])
            
            if input_type == "sensor_reading":
                entry = self._generate_sensor_input()
            elif input_type == "eeprom_operation":
                entry = self._generate_eeprom_input()
            elif input_type == "calibration_request":
                entry = self._generate_calibration_input()
            elif input_type == "error_diagnosis":
                entry = self._generate_error_input()
            else:  # firmware_update
                entry = self._generate_firmware_input()
            
            entry["id"] = f"input_{i:05d}"
            entry["timestamp"] = 1609459200 + i  # Incrementar timestamp
            input_data.append(entry)
        
        return input_data
    
    def _generate_sensor_input(self) -> Dict:
        """Generar entrada de lectura de sensor"""
        wheel = random.choice(["FL", "FR", "RL", "RR"])
        speed = random.randint(0, 2500)  # RPM realista
        
        return {
            "type": "sensor_reading",
            "input": f"leer velocidad rueda {wheel} sensor {speed} rpm",
            "intent": "read_wheel_speed",
            "parameters": {
                "wheel_position": wheel,
                "speed_rpm": speed,
                "sensor_type": "hall_effect",
                "voltage_range": "5V"
            },
            "c_code_context": f"""uint16_t read_wheel_speed_{wheel.lower()}(void) {{
    uint16_t speed_raw = ADC_READ(WHEEL_SENSOR_{wheel});
    return (speed_raw * SPEED_SCALE_FACTOR);
}}""",
            "eeprom_address": self.abs_registers[f"WHEEL_SPEED_{wheel}"]["address"],
            "data_type": self.abs_registers[f"WHEEL_SPEED_{wheel}"]["type"]
        }
    
    def _generate_eeprom_input(self) -> Dict:
        """Generar entrada de operación EEPROM"""
        operation = random.choice(["read", "write", "erase", "verify"])
        register = random.choice(list(self.abs_registers.keys()))
        address = self.abs_registers[register]["address"]
        
        if operation == "read":
            cmd = self.eeprom_commands["READ_BYTE"]
            value = None
        elif operation == "write":
            cmd = self.eeprom_commands["WRITE_BYTE"]
            value = random.randint(0, 255)
        elif operation == "erase":
            cmd = self.eeprom_commands["SECTOR_ERASE"]
            value = None
        else:  # verify
            cmd = self.eeprom_commands["READ_STATUS"]
            value = None
        
        return {
            "type": "eeprom_operation",
            "input": f"{operation} EEPROM registro {register} dirección {address}",
            "intent": f"eeprom_{operation}",
            "parameters": {
                "operation": operation,
                "register": register,
                "address": address,
                "command": cmd,
                "value": value
            },
            "c_code_context": f"""uint8_t eeprom_{operation}(uint16_t addr{"" if value is None else ", uint8_t data"}) {{
    SPI_SELECT();
    SPI_TRANSMIT({cmd});
    SPI_TRANSMIT((addr >> 8) & 0xFF);
    SPI_TRANSMIT(addr & 0xFF);
    {"SPI_TRANSMIT(data);" if value is not None else ""}
    {"return SPI_RECEIVE();" if operation == "read" else "return 0;"}
    SPI_DESELECT();
}}""",
            "memory_type": "EEPROM_25LC256",
            "bus_interface": "SPI"
        }
    
    def _generate_calibration_input(self) -> Dict:
        """Generar entrada de calibración"""
        calibration_type = random.choice([
            "wheel_sensor", "pressure_sensor", "threshold_adjustment", "gain_compensation"
        ])
        
        cal_value = random.uniform(0.8, 1.2)  # Factor de calibración típico
        
        return {
            "type": "calibration_request",
            "input": f"calibrar {calibration_type} factor {cal_value:.3f}",
            "intent": "sensor_calibration",
            "parameters": {
                "calibration_type": calibration_type,
                "calibration_factor": cal_value,
                "target_accuracy": "±2%",
                "temperature_compensation": True
            },
            "c_code_context": f"""void calibrate_{calibration_type.replace('_', '')}(float factor) {{
    CAL_DATA cal = {{
        .type = CAL_{calibration_type.upper()},
        .factor = factor,
        .timestamp = get_system_time(),
        .checksum = calculate_checksum(&cal, sizeof(cal)-2)
    }};
    eeprom_write_block(CAL_BASE_ADDR, &cal, sizeof(cal));
}}""",
            "storage_location": "EEPROM_CAL_SECTOR",
            "backup_required": True
        }
    
    def _generate_error_input(self) -> Dict:
        """Generar entrada de diagnóstico de error"""
        error_code = random.choice(list(self.abs_error_codes.keys()))
        error_desc = self.abs_error_codes[error_code]
        
        return {
            "type": "error_diagnosis",
            "input": f"diagnosticar error código {error_code} {error_desc}",
            "intent": "error_diagnosis",
            "parameters": {
                "error_code": error_code,
                "error_description": error_desc,
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "persistent": random.choice([True, False])
            },
            "c_code_context": f"""ERROR_STATUS diagnose_error_{error_code.replace('0x', '')}(void) {{
    ERROR_DATA error = {{
        .code = {error_code},
        .description = "{error_desc}",
        .timestamp = get_system_time(),
        .counter = read_error_counter({error_code})
    }};
    log_error_to_eeprom(&error);
    return determine_error_action(error.code);
}}""",
            "dtc_standard": "ISO_14229",
            "logging_required": True
        }
    
    def _generate_firmware_input(self) -> Dict:
        """Generar entrada de actualización de firmware"""
        version = f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 99)}"
        
        return {
            "type": "firmware_update",
            "input": f"actualizar firmware versión {version} ECU ABS",
            "intent": "firmware_update",
            "parameters": {
                "new_version": version,
                "flash_size": "256KB",
                "bootloader_protected": True,
                "checksum_verify": True
            },
            "c_code_context": f"""FLASH_STATUS update_firmware(const FIRMWARE_IMAGE* image) {{
    if (verify_signature(image) != SIGNATURE_VALID) 
        return FLASH_ERROR_SIGNATURE;
    
    flash_unlock();
    for (uint32_t addr = APP_START_ADDR; addr < APP_END_ADDR; addr += FLASH_PAGE_SIZE) {{
        flash_erase_page(addr);
    }}
    
    return flash_write_image(APP_START_ADDR, image);
}}""",
            "flash_type": "NOR_FLASH",
            "update_method": "bootloader"
        }
    
    def _generate_output_dataset(self, input_data: List[Dict]) -> List[Dict]:
        """Generar 50K parámetros de salida correspondientes"""
        output_data = []
        
        for i, input_entry in enumerate(input_data):
            output_entry = self._generate_corresponding_output(input_entry, i)
            output_data.append(output_entry)
        
        return output_data
    
    def _generate_corresponding_output(self, input_entry: Dict, index: int) -> Dict:
        """Generar salida técnica correspondiente a la entrada"""
        input_type = input_entry["type"]
        
        base_output = {
            "id": f"output_{index:05d}",
            "input_ref": input_entry["id"],
            "timestamp": input_entry["timestamp"] + 1
        }
        
        if input_type == "sensor_reading":
            return self._generate_sensor_output(input_entry, base_output)
        elif input_type == "eeprom_operation":
            return self._generate_eeprom_output(input_entry, base_output)
        elif input_type == "calibration_request":
            return self._generate_calibration_output(input_entry, base_output)
        elif input_type == "error_diagnosis":
            return self._generate_error_output(input_entry, base_output)
        else:  # firmware_update
            return self._generate_firmware_output(input_entry, base_output)
    
    def _generate_sensor_output(self, input_entry: Dict, base: Dict) -> Dict:
        """Generar salida de lectura de sensor"""
        params = input_entry["parameters"]
        speed_rpm = params["speed_rpm"]
        
        # Simular respuesta técnica realista
        success = random.random() > 0.05  # 95% tasa de éxito
        
        if success:
            # Convertir RPM a voltaje del sensor
            voltage = (speed_rpm / 2500.0) * 5.0
            raw_adc = int((voltage / 5.0) * 4095)  # 12-bit ADC
            
            result = {
                **base,
                "type": "sensor_response",
                "status": "success",
                "response": f"Sensor {params['wheel_position']}: {speed_rpm} RPM, {voltage:.2f}V",
                "data": {
                    "wheel_speed_rpm": speed_rpm,
                    "sensor_voltage": round(voltage, 2),
                    "adc_raw_value": raw_adc,
                    "signal_quality": "good" if voltage > 0.5 else "weak"
                },
                "c_code_output": f"""// Resultado de lectura
WHEEL_DATA result = {{
    .wheel_id = WHEEL_{params['wheel_position']},
    .speed_rpm = {speed_rpm},
    .voltage = {voltage:.2f}f,
    .adc_raw = {raw_adc},
    .status = SENSOR_OK
}};
return result;""",
                "memory_written": {
                    "address": input_entry["eeprom_address"],
                    "value": f"0x{raw_adc:04X}",
                    "size": "2 bytes"
                }
            }
        else:
            result = {
                **base,
                "type": "sensor_response", 
                "status": "error",
                "response": f"Error lectura sensor {params['wheel_position']}",
                "error": {
                    "code": "0x01",
                    "description": "Sensor desconectado o dañado",
                    "recovery_action": "Verificar conexiones y reemplazar si necesario"
                },
                "c_code_output": f"""// Error en lectura
return (WHEEL_DATA){{
    .wheel_id = WHEEL_{params['wheel_position']},
    .status = SENSOR_ERROR,
    .error_code = 0x01
}};"""
            }
        
        return result
    
    def _generate_eeprom_output(self, input_entry: Dict, base: Dict) -> Dict:
        """Generar salida de operación EEPROM"""
        params = input_entry["parameters"]
        operation = params["operation"]
        
        success = random.random() > 0.02  # 98% tasa de éxito para EEPROM
        
        if success:
            if operation == "read":
                value = random.randint(0, 255)
                response_data = {
                    "operation": "read_complete",
                    "address": params["address"],
                    "value": f"0x{value:02X}",
                    "data_valid": True
                }
                c_output = f"return 0x{value:02X}; // Valor leído exitosamente"
            
            elif operation == "write":
                response_data = {
                    "operation": "write_complete", 
                    "address": params["address"],
                    "value": f"0x{params['value']:02X}",
                    "verification": "passed"
                }
                c_output = f"return EEPROM_WRITE_OK; // Escritura verificada"
            
            elif operation == "erase":
                response_data = {
                    "operation": "erase_complete",
                    "address": params["address"],
                    "sector_cleared": True,
                    "erase_time_ms": random.randint(5, 20)
                }
                c_output = f"return EEPROM_ERASE_OK; // Sector borrado"
            
            else:  # verify
                response_data = {
                    "operation": "verify_complete",
                    "checksum": f"0x{random.randint(0, 65535):04X}",
                    "integrity": "ok"
                }
                c_output = f"return EEPROM_VERIFY_OK; // Integridad verificada"
            
            result = {
                **base,
                "type": "eeprom_response",
                "status": "success", 
                "response": f"EEPROM {operation} exitoso en {params['address']}",
                "data": response_data,
                "c_code_output": c_output,
                "timing": {
                    "operation_time_us": random.randint(50, 500),
                    "bus_speed_khz": 400
                }
            }
        else:
            result = {
                **base,
                "type": "eeprom_response",
                "status": "error",
                "response": f"Error EEPROM {operation} en {params['address']}",
                "error": {
                    "code": "0x08",
                    "description": "EEPROM no responde o corrupta",
                    "recovery_action": "Reiniciar comunicación SPI"
                },
                "c_code_output": "return EEPROM_ERROR; // Falla de comunicación"
            }
        
        return result
    
    def _generate_calibration_output(self, input_entry: Dict, base: Dict) -> Dict:
        """Generar salida de calibración"""
        params = input_entry["parameters"]
        
        return {
            **base,
            "type": "calibration_response",
            "status": "success",
            "response": f"Calibración {params['calibration_type']} completada",
            "data": {
                "calibration_applied": params["calibration_factor"],
                "accuracy_achieved": "±1.8%",
                "verification_passed": True
            },
            "c_code_output": "return CAL_SUCCESS; // Calibración guardada"
        }
    
    def _generate_error_output(self, input_entry: Dict, base: Dict) -> Dict:
        """Generar salida de diagnóstico de error"""
        params = input_entry["parameters"]
        
        return {
            **base,
            "type": "error_response",
            "status": "diagnosed",
            "response": f"Error {params['error_code']} diagnosticado",
            "data": {
                "diagnosis": "Sensor desconectado",
                "recommended_action": "Verificar conexiones",
                "severity": params["severity"]
            },
            "c_code_output": "return ERROR_DIAGNOSED; // Error identificado"
        }
    
    def _generate_firmware_output(self, input_entry: Dict, base: Dict) -> Dict:
        """Generar salida de actualización de firmware"""
        params = input_entry["parameters"]
        
        return {
            **base,
            "type": "firmware_response",
            "status": "updated",
            "response": f"Firmware actualizado a {params['new_version']}",
            "data": {
                "version_installed": params["new_version"],
                "checksum_verified": True,
                "update_time_seconds": random.randint(30, 120)
            },
            "c_code_output": "return FIRMWARE_UPDATE_OK; // Actualización exitosa"
        }
    
    def _combine_input_output(self, inputs: List[Dict], outputs: List[Dict]) -> List[Dict]:
        """Combinar entradas y salidas en dataset híbrido"""
        combined = []
        
        for inp, out in zip(inputs, outputs):
            # Formato híbrido semántico-binarizado
            hybrid_entry = {
                "id": f"hybrid_{inp['id'].split('_')[1]}",
                "input_data": inp,
                "output_data": out,
                "relationship": {
                    "input_id": inp["id"],
                    "output_id": out["id"],
                    "processing_time_us": random.randint(10, 1000),
                    "success": out["status"] in ["success", "diagnosed", "updated"]
                },
                "technical_metadata": {
                    "ecu_type": "ABS_Controller",
                    "protocol": "SPI/CAN",
                    "memory_type": "EEPROM_25LC256",
                    "mcu_family": "ARM_Cortex_M4",
                    "compiler": "GCC_ARM",
                    "optimization": "-O2"
                },
                "binary_representation": {
                    "input_hash": hashlib.md5(json.dumps(inp, sort_keys=True).encode()).hexdigest()[:8],
                    "output_hash": hashlib.md5(json.dumps(out, sort_keys=True).encode()).hexdigest()[:8],
                    "size_bytes": len(json.dumps(inp)) + len(json.dumps(out))
                }
            }
            combined.append(hybrid_entry)
        
        return combined
    
    def _save_dataset(self, dataset: List[Dict]) -> Path:
        """Guardar dataset en formato JSONL"""
        timestamp = int(time.time())
        filename = f"ecu_abs_dataset_100k_{timestamp}.jsonl"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in dataset:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"✓ Dataset guardado: {filepath}")
        return filepath
    
    def _generate_dataset_statistics(self, dataset: List[Dict]) -> Dict:
        """Generar estadísticas del dataset"""
        total_entries = len(dataset)
        
        # Contar tipos de entrada
        input_types = {}
        success_count = 0
        
        for entry in dataset:
            inp_type = entry["input_data"]["type"]
            input_types[inp_type] = input_types.get(inp_type, 0) + 1
            
            if entry["relationship"]["success"]:
                success_count += 1
        
        return {
            "total_entries": total_entries,
            "input_types_distribution": input_types,
            "success_rate": round(success_count / total_entries, 3),
            "file_size_mb": round(sum(len(json.dumps(entry)) for entry in dataset) / (1024*1024), 2),
            "technical_coverage": {
                "eeprom_operations": input_types.get("eeprom_operation", 0),
                "sensor_readings": input_types.get("sensor_reading", 0),
                "calibrations": input_types.get("calibration_request", 0),
                "error_diagnosis": input_types.get("error_diagnosis", 0),
                "firmware_updates": input_types.get("firmware_update", 0)
            }
        }


def main():
    """Función principal"""
    generator = ECUABSDatasetGenerator()
    
    print("🚗 Generador Dataset ECU ABS")
    print("Programación EEPROM/EPROM en C/C++")
    print("100K parámetros técnicos especializados")
    print("=" * 50)
    
    start_time = time.time()
    
    # Generar dataset completo
    result = generator.generate_complete_dataset()
    
    end_time = time.time()
    generation_time = end_time - start_time
    
    print(f"\n✅ Dataset generado exitosamente!")
    print(f"📊 Parámetros totales: {result['total_parameters']:,}")
    print(f"📥 Entradas: {result['input_parameters']:,}")
    print(f"📤 Salidas: {result['output_parameters']:,}")
    print(f"⏱️ Tiempo de generación: {generation_time:.2f} segundos")
    print(f"📁 Archivo: {result['dataset_file']}")
    print(f"📈 Tasa de éxito: {result['statistics']['success_rate']*100:.1f}%")
    print(f"💾 Tamaño: {result['statistics']['file_size_mb']} MB")


if __name__ == "__main__":
    main()