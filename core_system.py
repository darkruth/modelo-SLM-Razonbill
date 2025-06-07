#!/usr/bin/env python3
"""
Gym-Razonbilstro-µCore v1.0
Sistema de diagnóstico automotriz con metaaprendizaje integrado
Optimizado para ARM/RISC-V con baja RAM
"""

import json
import time
import hashlib
from typing import Dict, List, Optional, Set
from pathlib import Path
import logging

# Importar sistema de metaaprendizaje
from core.meta_learning_system import MetaLearningSystem, TemporalNode

logger = logging.getLogger(__name__)

class FuzzyMatcher:
    """Sistema de coincidencias difusas para alias técnicos"""
    
    def __init__(self):
        # Diccionario técnico con alias y errores ortográficos
        self.technical_dictionary = {
            "hasguar": {
                "canonical": "hardware", 
                "alias": ["hardware", "hazguar", "hasuar", "hasgwar", "hardwar"],
                "acciones": ["leer_estado", "verificar_conexion", "diagnosticar_fallo"]
            },
            "sensor": {
                "canonical": "sensor",
                "alias": ["senser", "censor", "sensore", "senso"],
                "acciones": ["leer_datos", "verificar_voltaje", "calibrar"]
            },
            "valvula": {
                "canonical": "valvula",
                "alias": ["valvla", "valbula", "balvula", "valve"],
                "acciones": ["probar_funcionamiento", "verificar_apertura", "limpiar"]
            },
            "filtro": {
                "canonical": "filtro",
                "alias": ["filtero", "filtr", "filter"],
                "acciones": ["verificar_estado", "reemplazar", "limpiar"]
            }
        }
        
        # Cache de coincidencias para optimización
        self._match_cache = {}
    
    def fuzzy_match(self, input_word: str, threshold: float = 0.7) -> Optional[Dict]:
        """
        Coincidencia difusa para palabras técnicas
        
        Args:
            input_word: Palabra de entrada (con posibles errores)
            threshold: Umbral de similitud mínima
            
        Returns:
            Diccionario con información técnica o None
        """
        input_clean = input_word.lower().strip()
        
        # Verificar cache
        if input_clean in self._match_cache:
            return self._match_cache[input_clean]
        
        best_match = None
        best_score = 0.0
        
        for canonical, data in self.technical_dictionary.items():
            # Verificar coincidencia exacta
            if input_clean == canonical or input_clean in data["alias"]:
                best_match = {
                    "canonical": data["canonical"],
                    "matched_alias": input_clean,
                    "confidence": 1.0,
                    "acciones": data["acciones"]
                }
                break
            
            # Calcular similitud con Levenshtein simplificado
            for alias in [canonical] + data["alias"]:
                similarity = self._calculate_similarity(input_clean, alias)
                if similarity > best_score and similarity >= threshold:
                    best_score = similarity
                    best_match = {
                        "canonical": data["canonical"],
                        "matched_alias": alias,
                        "confidence": similarity,
                        "acciones": data["acciones"]
                    }
        
        # Cachear resultado
        self._match_cache[input_clean] = best_match
        return best_match
    
    def _calculate_similarity(self, word1: str, word2: str) -> float:
        """Calcular similitud simple entre dos palabras"""
        if not word1 or not word2:
            return 0.0
        
        # Distancia de Levenshtein simplificada
        len1, len2 = len(word1), len(word2)
        if len1 > len2:
            word1, word2 = word2, word1
            len1, len2 = len2, len1
        
        # Matriz de distancias
        current = list(range(len1 + 1))
        for i in range(1, len2 + 1):
            previous, current = current, [i] + [0] * len1
            for j in range(1, len1 + 1):
                add, delete, change = previous[j] + 1, current[j - 1] + 1, previous[j - 1]
                if word1[j - 1] != word2[i - 1]:
                    change += 1
                current[j] = min(add, delete, change)
        
        # Convertir distancia a similitud
        max_len = max(len1, len2)
        if max_len == 0:
            return 1.0
        
        return 1.0 - (current[len1] / max_len)


class AutomotiveDiagnosticCore:
    """
    Núcleo de diagnóstico automotriz sin contexto emocional
    Enfocado en respuestas técnicas directas y precisas
    """
    
    def __init__(self):
        self.fuzzy_matcher = FuzzyMatcher()
        self.component_map = self._load_component_map()
        self.obd_commands = self._load_obd_commands()
        
        # Estado del diagnóstico
        self.current_mode = "diagnostico"  # diagnostico | edicion_firmware
        self.sandbox_locked = False
        self.session_id = None
        
        # Logs de acciones
        self.action_log = []
        
    def _load_component_map(self) -> Dict:
        """Cargar mapa de componentes automotrices"""
        return {
            "switch_ventana_elevador": {
                "hex_address": "0x12FA",
                "voltage_range": "5V",
                "common_failures": ["desconexion", "linea_cortada", "switch_defectuoso"],
                "diagnostic_steps": ["verificar_voltaje", "probar_continuidad", "verificar_switch"]
            },
            "valvula_iac": {
                "hex_address": "0x015",
                "type": "actuador",
                "common_failures": ["suciedad", "carbon_acumulado", "bobina_quemada"],
                "symptoms": ["ralenti_inestable", "apagado_en_neutro", "rpm_fluctuante"]
            },
            "sensor_maf": {
                "hex_address": "0x21A1", 
                "voltage_range": "0-5V",
                "common_failures": ["suciedad", "filamento_roto", "cortocircuito"],
                "normal_values": "1.5-4.5V en funcionamiento"
            }
        }
    
    def _load_obd_commands(self) -> Dict:
        """Cargar comandos OBD-II estándar"""
        return {
            "0x015": "Lectura estado válvula IAC",
            "0x21A1": "Datos sensor MAF",
            "0x12FA": "Estado switch elevadores",
            "0x0105": "Temperatura refrigerante",
            "0x010C": "RPM motor",
            "0x010D": "Velocidad vehículo"
        }
    
    def process_diagnostic_input(self, user_input: str) -> Dict:
        """
        Procesar entrada de diagnóstico sin contexto emocional
        
        Args:
            user_input: Entrada del usuario con descripción del problema
            
        Returns:
            Respuesta técnica estructurada
        """
        # Log de la acción
        self._log_action("diagnostic_input", {"input": user_input})
        
        # Analizar entrada con fuzzy matching
        analysis = self._analyze_diagnostic_input(user_input)
        
        if not analysis["components_detected"]:
            return {
                "status": "E-404",
                "mensaje": "No se encontró ese componente en el mapa actual.",
                "sugerencias": ["verificar ortografía", "usar términos técnicos específicos"]
            }
        
        # Generar diagnóstico
        diagnostic = self._generate_diagnostic(analysis)
        
        return {
            "status": "OK",
            "analisis": analysis,
            "diagnostico": diagnostic,
            "timestamp": time.time()
        }
    
    def _analyze_diagnostic_input(self, user_input: str) -> Dict:
        """Analizar entrada para detectar componentes y síntomas"""
        words = user_input.lower().split()
        detected_components = []
        detected_symptoms = []
        
        # Detectar componentes con fuzzy matching
        for word in words:
            match = self.fuzzy_matcher.fuzzy_match(word)
            if match:
                detected_components.append(match)
        
        # Detectar síntomas conocidos
        symptom_patterns = {
            "se apaga": "motor_apagado",
            "ralenti": "ralenti_problema", 
            "vibra": "vibracion_motor",
            "no arranca": "fallo_arranque",
            "humo": "combustion_defectuosa"
        }
        
        for pattern, symptom in symptom_patterns.items():
            if pattern in user_input.lower():
                detected_symptoms.append(symptom)
        
        return {
            "components_detected": detected_components,
            "symptoms_detected": detected_symptoms,
            "input_words": words,
            "confidence": sum(c["confidence"] for c in detected_components) / max(len(detected_components), 1)
        }
    
    def _generate_diagnostic(self, analysis: Dict) -> Dict:
        """Generar diagnóstico técnico basado en análisis"""
        diagnostics = []
        
        for component in analysis["components_detected"]:
            canonical = component["canonical"]
            
            # Buscar en mapa de componentes
            for comp_id, comp_data in self.component_map.items():
                if canonical.lower() in comp_id.lower() or any(canonical in str(v).lower() for v in comp_data.values()):
                    diagnostic = {
                        "componente": comp_id,
                        "accion_recomendada": component["acciones"][0] if component["acciones"] else "verificar_estado",
                        "comando_obd": comp_data.get("hex_address", "N/A"),
                        "fallas_comunes": comp_data.get("common_failures", []),
                        "pasos_diagnostico": comp_data.get("diagnostic_steps", [])
                    }
                    diagnostics.append(diagnostic)
        
        # Correlacionar con síntomas
        for symptom in analysis["symptoms_detected"]:
            if symptom == "ralenti_problema":
                diagnostics.append({
                    "componente": "valvula_iac",
                    "accion_recomendada": "verificar_funcionamiento",
                    "comando_obd": "0x015",
                    "explicacion": "Ralentí inestable sugiere problema en control de aire de ralentí"
                })
        
        return {
            "diagnosticos_encontrados": len(diagnostics),
            "resultados": diagnostics,
            "prioridad": "alta" if analysis["confidence"] > 0.8 else "media"
        }
    
    def execute_obd_command(self, command: str) -> Dict:
        """
        Ejecutar comando OBD-II (simulado para desarrollo)
        
        Args:
            command: Comando hexadecimal OBD
            
        Returns:
            Resultado del comando
        """
        self._log_action("obd_command", {"command": command})
        
        if command not in self.obd_commands:
            return {
                "status": "E-CMD",
                "mensaje": f"Comando {command} no reconocido",
                "comandos_disponibles": list(self.obd_commands.keys())
            }
        
        # Simular respuesta OBD (en implementación real, usar biblioteca OBD)
        simulated_responses = {
            "0x015": {"value": "45%", "status": "normal", "description": "Posición válvula IAC"},
            "0x21A1": {"value": "3.2V", "status": "normal", "description": "Voltaje sensor MAF"},
            "0x12FA": {"value": "0V", "status": "fallo", "description": "Switch elevador sin voltaje"}
        }
        
        return {
            "status": "OK",
            "comando": command,
            "descripcion": self.obd_commands[command],
            "respuesta": simulated_responses.get(command, {"value": "N/A", "status": "unknown"})
        }
    
    def _log_action(self, action_type: str, data: Dict):
        """Registrar acción en logs"""
        log_entry = {
            "timestamp": time.time(),
            "action": action_type,
            "data": data,
            "session_id": self.session_id,
            "mode": self.current_mode
        }
        
        self.action_log.append(log_entry)
        
        # Mantener solo últimas 1000 entradas
        if len(self.action_log) > 1000:
            self.action_log = self.action_log[-1000:]


class GymRazonbilstroSystem:
    """
    Sistema principal Gym-Razonbilstro-µCore v1.0
    Integra diagnóstico automotriz con metaaprendizaje
    """
    
    def __init__(self):
        # Componentes principales
        self.diagnostic_core = AutomotiveDiagnosticCore()
        self.meta_learning = MetaLearningSystem(max_filesystem_memory=5000)
        
        # Configuración del sistema
        self.config = {
            "version": "1.0",
            "name": "Gym-Razonbilstro-µCore",
            "optimization": {
                "int8_quantization": True,
                "model_distillation": True,
                "arm_optimized": True,
                "low_ram_mode": True
            },
            "training": {
                "no_emotions": True,
                "no_user_context": True,
                "technical_only": True,
                "binary_semantic_hybrid": True
            }
        }
        
        # Estado del sistema
        self.system_active = True
        self.training_session = None
        self.temporal_node = None
        
        logger.info("Gym-Razonbilstro-µCore v1.0 inicializado")
    
    def diagnose(self, problem_description: str) -> Dict:
        """
        Realizar diagnóstico automotriz
        
        Args:
            problem_description: Descripción del problema
            
        Returns:
            Diagnóstico técnico
        """
        # Agregar a memoria corta solo si no es entrenamiento
        if not self.training_session:
            self.meta_learning.add_short_memory(problem_description, "diagnostic_request")
        
        # Procesar diagnóstico
        result = self.diagnostic_core.process_diagnostic_input(problem_description)
        
        return result


def main():
    """Función principal para probar Gym-Razonbilstro-µCore"""
    print("🔧 Gym-Razonbilstro-µCore v1.0")
    print("Sistema de Diagnóstico Automotriz con Metaaprendizaje")
    print("=" * 60)
    
    # Inicializar sistema
    gym_system = GymRazonbilstroSystem()
    
    # Ejemplo de uso en modo diagnóstico
    print("\n🚗 Modo Diagnóstico:")
    diagnosis = gym_system.diagnose("checa el hasguar y busca el dese d la esa que sube los vidrios")
    print(f"Resultado: {diagnosis}")


if __name__ == "__main__":
    main()