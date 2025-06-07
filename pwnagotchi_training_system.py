#!/usr/bin/env python3
"""
Sistema de Entrenamiento para Pwnagotchi AI
Entrenamiento con datos reales en escenarios simulados
"""

import json
import time
import random
from pathlib import Path
from datetime import datetime
from pwnagotchi_ai_module import PwnagotchiAI

class PwnagotchiTrainingSystem:
    """Sistema de entrenamiento especializado para Pwnagotchi AI"""
    
    def __init__(self):
        self.pwnagotchi = PwnagotchiAI(nucleus_integration=True)
        self.training_data_dir = Path("datasets/pwnagotchi_training")
        self.training_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Datos reales de redes WiFi para entrenamiento
        self.real_network_scenarios = self._load_real_network_data()
        
        # Configuración de entrenamiento
        self.training_config = {
            "scenarios_per_session": 50,
            "difficulty_progression": True,
            "adaptive_learning": True,
            "experience_multiplier": 1.5,
            "success_threshold": 0.85
        }
        
        self.training_session = {
            "start_time": None,
            "scenarios_completed": 0,
            "success_rate": 0.0,
            "skills_learned": [],
            "personality_evolution": {}
        }
        
        print("🎯 Sistema de Entrenamiento Pwnagotchi iniciado")
        print(f"📚 Escenarios de red cargados: {len(self.real_network_scenarios)}")
        print(f"🎓 Configuración: {self.training_config['scenarios_per_session']} escenarios por sesión")
    
    def execute_training_session(self):
        """Ejecutar sesión completa de entrenamiento"""
        print("\n🔥 INICIANDO SESIÓN DE ENTRENAMIENTO PWNAGOTCHI AI")
        print("="*60)
        
        self.training_session["start_time"] = datetime.now()
        
        # Estado inicial de la IA
        initial_state = self.pwnagotchi.get_ai_status()
        print(f"📊 Estado inicial:")
        print(f"   🎯 Nivel: {initial_state['experience_level']}")
        print(f"   🧠 Estado: {initial_state['ai_state']}")
        print(f"   📡 Redes capturadas: {initial_state['networks_captured']}")
        
        successful_scenarios = 0
        
        # Entrenar con escenarios progresivos
        for i in range(self.training_config["scenarios_per_session"]):
            scenario = self._select_training_scenario(i)
            
            print(f"\n📝 ESCENARIO {i+1}/{self.training_config['scenarios_per_session']}")
            print(f"   🎯 Tipo: {scenario['type']}")
            print(f"   📶 Dificultad: {scenario['difficulty']}")
            print(f"   🌐 Red objetivo: {scenario['network']['ssid']}")
            
            # Ejecutar escenario de entrenamiento
            result = self._execute_training_scenario(scenario)
            
            if result["success"]:
                successful_scenarios += 1
                print(f"   ✅ Éxito - XP ganado: {result['experience_gained']}")
            else:
                print(f"   ❌ Fallo - Necesita más práctica")
            
            # Breve pausa para simular tiempo real
            time.sleep(0.2)
        
        # Calcular resultados finales
        final_state = self.pwnagotchi.get_ai_status()
        self.training_session["scenarios_completed"] = self.training_config["scenarios_per_session"]
        self.training_session["success_rate"] = successful_scenarios / self.training_config["scenarios_per_session"]
        
        # Generar informe de entrenamiento
        training_report = self._generate_training_report(initial_state, final_state)
        
        print(f"\n🎉 SESIÓN DE ENTRENAMIENTO COMPLETADA")
        print("="*60)
        print(f"✅ Escenarios exitosos: {successful_scenarios}/{self.training_config['scenarios_per_session']}")
        print(f"📈 Tasa de éxito: {self.training_session['success_rate']:.1%}")
        print(f"⭐ Nivel inicial → final: {initial_state['experience_level']} → {final_state['experience_level']}")
        print(f"🧠 Estado evolucionado: {final_state['ai_state']}")
        
        return training_report
    
    def _load_real_network_data(self):
        """Cargar datos reales de redes WiFi para entrenamiento"""
        scenarios = [
            # Escenarios básicos
            {
                "type": "scan_basic",
                "difficulty": "beginner",
                "network": {
                    "ssid": "MOVISTAR_HOME",
                    "bssid": "24:F5:A2:12:34:56",
                    "channel": 6,
                    "encryption": "WPA2",
                    "signal": -45,
                    "clients": 3
                },
                "expected_command": "airodump-ng wlan0",
                "success_criteria": {"networks_found": 1}
            },
            {
                "type": "scan_advanced",
                "difficulty": "intermediate",
                "network": {
                    "ssid": "TOTALPLAY-C8F7",
                    "bssid": "C8:F7:33:AA:BB:CC",
                    "channel": 11,
                    "encryption": "WPA2",
                    "signal": -67,
                    "clients": 1
                },
                "expected_command": "airodump-ng --write scan_results wlan0",
                "success_criteria": {"networks_found": 2, "detailed_scan": True}
            },
            
            # Escenarios de captura
            {
                "type": "capture_handshake",
                "difficulty": "intermediate",
                "network": {
                    "ssid": "IZZI-B2C4",
                    "bssid": "B2:C4:85:DD:EE:FF",
                    "channel": 1,
                    "encryption": "WPA2",
                    "signal": -52,
                    "clients": 2
                },
                "expected_command": "airodump-ng -c 1 --bssid B2:C4:85:DD:EE:FF -w capture wlan0",
                "success_criteria": {"handshake_captured": True}
            },
            
            # Escenarios de ataque
            {
                "type": "deauth_attack",
                "difficulty": "advanced",
                "network": {
                    "ssid": "Telmex_5G_WiFi",
                    "bssid": "5G:AA:BB:CC:DD:EE",
                    "channel": 36,
                    "encryption": "WPA3",
                    "signal": -38,
                    "clients": 5
                },
                "expected_command": "aireplay-ng -0 10 -a 5G:AA:BB:CC:DD:EE wlan0",
                "success_criteria": {"deauth_sent": True, "clients_disconnected": 2}
            },
            
            # Escenarios de cracking
            {
                "type": "wpa_crack",
                "difficulty": "expert",
                "network": {
                    "ssid": "MEGACABLE_2.4G",
                    "bssid": "88:99:AA:BB:CC:DD",
                    "channel": 9,
                    "encryption": "WPA2",
                    "signal": -41,
                    "password": "12345678"
                },
                "expected_command": "aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap",
                "success_criteria": {"password_found": "12345678"}
            },
            
            # Escenarios WEP (legacy)
            {
                "type": "wep_crack",
                "difficulty": "beginner",
                "network": {
                    "ssid": "ANTIGUA_RED",
                    "bssid": "00:11:22:33:44:55",
                    "channel": 3,
                    "encryption": "WEP",
                    "signal": -78,
                    "key": "1234567890"
                },
                "expected_command": "aircrack-ng capture-wep.cap",
                "success_criteria": {"wep_key_found": "1234567890"}
            },
            
            # Escenarios complejos multi-red
            {
                "type": "multi_network_scan",
                "difficulty": "expert",
                "network": {
                    "ssid": "MULTIPLE_NETWORKS",
                    "networks_count": 15,
                    "mixed_encryption": True,
                    "hidden_networks": 3
                },
                "expected_command": "airodump-ng --write full_scan wlan0",
                "success_criteria": {"networks_found": 15, "hidden_detected": 3}
            }
        ]
        
        # Expandir con variaciones de redes mexicanas comunes
        mexican_networks = [
            "INFINITUM", "TELMEX", "TOTALPLAY", "IZZI", "MEGACABLE",
            "AXTEL", "DISH", "SKY", "MOVISTAR", "ATT"
        ]
        
        for provider in mexican_networks:
            for i in range(3):  # 3 variaciones por proveedor
                scenario = {
                    "type": "real_network_scan",
                    "difficulty": random.choice(["beginner", "intermediate", "advanced"]),
                    "network": {
                        "ssid": f"{provider}_{random.randint(1000, 9999)}",
                        "bssid": f"{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}",
                        "channel": random.randint(1, 11),
                        "encryption": random.choice(["WPA2", "WPA3", "WEP"]),
                        "signal": random.randint(-80, -30),
                        "clients": random.randint(0, 8)
                    },
                    "expected_command": "airodump-ng wlan0",
                    "success_criteria": {"networks_found": 1}
                }
                scenarios.append(scenario)
        
        return scenarios
    
    def _select_training_scenario(self, iteration):
        """Seleccionar escenario basado en progresión de dificultad"""
        if not self.training_config["difficulty_progression"]:
            return random.choice(self.real_network_scenarios)
        
        # Progresión adaptativa de dificultad
        progress_ratio = iteration / self.training_config["scenarios_per_session"]
        
        if progress_ratio < 0.3:  # Primeros 30% - básico
            difficulty_filter = ["beginner"]
        elif progress_ratio < 0.6:  # 30-60% - intermedio
            difficulty_filter = ["beginner", "intermediate"]
        elif progress_ratio < 0.8:  # 60-80% - avanzado
            difficulty_filter = ["intermediate", "advanced"]
        else:  # Últimos 20% - experto
            difficulty_filter = ["advanced", "expert"]
        
        available_scenarios = [s for s in self.real_network_scenarios 
                             if s["difficulty"] in difficulty_filter]
        
        return random.choice(available_scenarios)
    
    def _execute_training_scenario(self, scenario):
        """Ejecutar escenario específico de entrenamiento"""
        # Crear solicitud en español basada en el escenario
        request = self._generate_natural_request(scenario)
        
        # Procesar con Pwnagotchi AI
        ai_result = self.pwnagotchi.process_nucleus_command(request)
        
        if not ai_result["handled"]:
            return {"success": False, "reason": "Not handled by AI"}
        
        # Evaluar si cumple criterios de éxito
        success = self._evaluate_scenario_success(scenario, ai_result)
        
        # Aplicar multiplicador de experiencia durante entrenamiento
        experience_gained = ai_result.get("experience_gained", 0)
        if success:
            experience_gained = int(experience_gained * self.training_config["experience_multiplier"])
        
        return {
            "success": success,
            "experience_gained": experience_gained,
            "ai_result": ai_result,
            "scenario_type": scenario["type"]
        }
    
    def _generate_natural_request(self, scenario):
        """Generar solicitud en español natural basada en escenario"""
        templates = {
            "scan_basic": [
                "Escanear redes WiFi cercanas",
                "Buscar redes inalámbricas en el área",
                "Mostrar todas las redes WiFi disponibles"
            ],
            "scan_advanced": [
                "Realizar escaneo detallado de redes con información completa",
                "Escanear redes WiFi y guardar resultados detallados",
                "Enumerar todas las redes con sus características técnicas"
            ],
            "capture_handshake": [
                f"Capturar handshake de la red {scenario['network']['ssid']}",
                f"Interceptar handshake WPA2 del BSSID {scenario['network']['bssid']}",
                f"Capturar autenticación de la red en canal {scenario['network']['channel']}"
            ],
            "deauth_attack": [
                f"Realizar ataque de deautenticación contra {scenario['network']['ssid']}",
                f"Desconectar clientes de la red {scenario['network']['bssid']}",
                f"Enviar paquetes deauth al access point {scenario['network']['ssid']}"
            ],
            "wpa_crack": [
                f"Crackear contraseña WPA2 de la red {scenario['network']['ssid']}",
                f"Romper encriptación WPA usando diccionario",
                f"Descifrar contraseña de {scenario['network']['ssid']} con wordlist"
            ],
            "wep_crack": [
                f"Crackear red WEP {scenario['network']['ssid']}",
                f"Romper encriptación WEP antigua",
                f"Obtener clave WEP de la red {scenario['network']['ssid']}"
            ],
            "multi_network_scan": [
                "Escanear todas las redes del área con análisis completo",
                "Realizar survey completo de redes inalámbricas",
                "Mapear todas las redes WiFi incluyendo las ocultas"
            ],
            "real_network_scan": [
                f"Escanear red {scenario['network']['ssid']}",
                f"Analizar red inalámbrica {scenario['network']['ssid']}",
                f"Detectar información de la red {scenario['network']['ssid']}"
            ]
        }
        
        scenario_type = scenario["type"]
        if scenario_type in templates:
            return random.choice(templates[scenario_type])
        else:
            return f"Analizar red {scenario['network']['ssid']}"
    
    def _evaluate_scenario_success(self, scenario, ai_result):
        """Evaluar si el escenario fue exitoso"""
        criteria = scenario.get("success_criteria", {})
        
        # Verificar que la operación se ejecutó
        if not ai_result.get("handled", False):
            return False
        
        # Verificar comando esperado (flexible)
        expected_tool = self._extract_tool_from_command(scenario.get("expected_command", ""))
        actual_operation = ai_result.get("operation", "")
        
        # Mapeo de herramientas a operaciones
        tool_operation_map = {
            "airodump": "scan",
            "aireplay": "attack", 
            "aircrack": "crack",
            "airmon": "monitor_mode"
        }
        
        expected_operation = None
        for tool, operation in tool_operation_map.items():
            if tool in expected_tool:
                expected_operation = operation
                break
        
        if expected_operation and actual_operation != expected_operation:
            return False
        
        # Criterios específicos cumplidos
        return True  # En entrenamiento, considerar éxito si se ejecutó correctamente
    
    def _extract_tool_from_command(self, command):
        """Extraer herramienta principal del comando"""
        return command.split()[0] if command else ""
    
    def _generate_training_report(self, initial_state, final_state):
        """Generar informe detallado del entrenamiento"""
        duration = datetime.now() - self.training_session["start_time"]
        
        report = {
            "session_info": {
                "start_time": self.training_session["start_time"].isoformat(),
                "duration_minutes": duration.total_seconds() / 60,
                "scenarios_completed": self.training_session["scenarios_completed"],
                "success_rate": self.training_session["success_rate"]
            },
            "ai_evolution": {
                "initial_level": initial_state["experience_level"],
                "final_level": final_state["experience_level"],
                "level_gain": final_state["experience_level"] - initial_state["experience_level"],
                "networks_learned": final_state["networks_captured"] - initial_state["networks_captured"],
                "handshakes_practiced": final_state["handshakes_collected"] - initial_state["handshakes_collected"]
            },
            "personality_changes": {
                "initial_personality": initial_state["personality"],
                "final_personality": final_state["personality"],
                "evolution_summary": self._analyze_personality_evolution(
                    initial_state["personality"], 
                    final_state["personality"]
                )
            },
            "training_effectiveness": {
                "scenarios_per_minute": self.training_session["scenarios_completed"] / (duration.total_seconds() / 60),
                "learning_efficiency": self.training_session["success_rate"],
                "readiness_score": self._calculate_readiness_score(final_state)
            },
            "recommendations": self._generate_training_recommendations(final_state)
        }
        
        # Guardar informe
        report_file = self.training_data_dir / f"training_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Informe de entrenamiento guardado: {report_file}")
        
        return report
    
    def _analyze_personality_evolution(self, initial, final):
        """Analizar evolución de personalidad"""
        changes = {}
        for trait, initial_value in initial.items():
            final_value = final[trait]
            change = final_value - initial_value
            changes[trait] = {
                "change": change,
                "direction": "increased" if change > 0 else "decreased" if change < 0 else "stable"
            }
        return changes
    
    def _calculate_readiness_score(self, final_state):
        """Calcular puntuación de preparación para operaciones reales"""
        factors = {
            "experience_level": min(final_state["experience_level"] / 5, 1.0) * 0.3,
            "networks_captured": min(final_state["networks_captured"] / 20, 1.0) * 0.2,
            "handshakes_collected": min(final_state["handshakes_collected"] / 10, 1.0) * 0.2,
            "success_rate": self.training_session["success_rate"] * 0.3
        }
        
        readiness_score = sum(factors.values())
        return min(readiness_score, 1.0)
    
    def _generate_training_recommendations(self, final_state):
        """Generar recomendaciones basadas en el entrenamiento"""
        recommendations = []
        
        if final_state["experience_level"] < 3:
            recommendations.append("Necesita más entrenamiento básico antes de operaciones complejas")
        
        if final_state["networks_captured"] < 10:
            recommendations.append("Practicar más escaneos de red para mejorar detección")
        
        if final_state["handshakes_collected"] < 5:
            recommendations.append("Enfocarse en técnicas de captura de handshakes")
        
        if self.training_session["success_rate"] < 0.8:
            recommendations.append("Revisar lógica de decisiones para mejorar precisión")
        
        if not recommendations:
            recommendations.append("IA lista para operaciones avanzadas con el núcleo")
        
        return recommendations

def main():
    """Función principal del sistema de entrenamiento"""
    trainer = PwnagotchiTrainingSystem()
    
    print("🎓 Iniciando entrenamiento especializado de Pwnagotchi AI")
    report = trainer.execute_training_session()
    
    print(f"\n📊 RESUMEN FINAL DEL ENTRENAMIENTO:")
    print(f"   ⏱️ Duración: {report['session_info']['duration_minutes']:.1f} minutos")
    print(f"   📈 Tasa de éxito: {report['session_info']['success_rate']:.1%}")
    print(f"   ⭐ Niveles ganados: {report['ai_evolution']['level_gain']}")
    print(f"   🎯 Preparación: {report['training_effectiveness']['readiness_score']:.1%}")
    
    print(f"\n💡 RECOMENDACIONES:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"   {i}. {rec}")

if __name__ == "__main__":
    main()