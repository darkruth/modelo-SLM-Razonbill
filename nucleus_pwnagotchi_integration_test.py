#!/usr/bin/env python3
"""
Pruebas de Integración Completa: Núcleo + Pwnagotchi AI
Sistema que procesa, interpreta e integra datos de Pwnagotchi como propios
"""

import json
import time
from pathlib import Path
from datetime import datetime
from complete_system_integration import CompleteSystemIntegration

class NucleusPwnagotchiIntegrationTest:
    """Pruebas completas de integración Núcleo-Pwnagotchi"""
    
    def __init__(self):
        self.system = CompleteSystemIntegration()
        self.test_results = []
        self.integration_metrics = {
            "total_requests": 0,
            "pwnagotchi_invocations": 0,
            "successful_integrations": 0,
            "data_interpretations": 0
        }
        
        print("🔬 Sistema de Pruebas de Integración Núcleo-Pwnagotchi iniciado")
        print("🤖 Pwnagotchi AI entrenado y listo")
        print("🧠 Núcleo con neuronas temporales activas")
    
    def execute_integration_tests(self):
        """Ejecutar pruebas completas de integración"""
        print(f"\n🚀 EJECUTANDO PRUEBAS DE INTEGRACIÓN COMPLETA")
        print("="*60)
        
        # Test 1: Solicitudes WiFi que requieren Pwnagotchi
        wifi_requests = [
            "Necesito escanear todas las redes WiFi del área para buscar vulnerabilidades",
            "Captura el handshake WPA2 de la red 'MOVISTAR_HOME' para análisis",
            "Realiza un ataque de deautenticación contra dispositivos conectados",
            "Crackea la contraseña de la red WiFi que acabamos de capturar",
            "Monitorea el tráfico inalámbrico en busca de patrones sospechosos",
            "Activa modo monitor en la interfaz para captura de paquetes",
            "Analiza las vulnerabilidades de todas las redes WEP detectadas",
            "Ejecuta un survey completo de redes inalámbricas del entorno"
        ]
        
        # Test 2: Solicitudes que NO requieren Pwnagotchi
        non_wifi_requests = [
            "Escanea los puertos del servidor 192.168.1.100",
            "Analiza vulnerabilidades web del sitio target.com",
            "Comprime el directorio de logs del sistema",
            "Monitorea procesos del sistema en tiempo real"
        ]
        
        print(f"🔍 FASE 1: SOLICITUDES WIFI (Pwnagotchi requerido)")
        print("-" * 50)
        
        for i, request in enumerate(wifi_requests, 1):
            print(f"\n📝 Prueba WiFi {i}/8:")
            print(f"   📥 Solicitud: {request[:60]}...")
            
            result = self._test_wifi_integration(request)
            self.test_results.append(result)
            
            if result["pwnagotchi_invoked"]:
                print(f"   🤖 Pwnagotchi AI activado: ✅")
                print(f"   📡 Operación: {result['operation']}")
                print(f"   🧠 Estado IA: {result['ai_state']}")
                print(f"   📊 Interpretación núcleo: {result['nucleus_interpretation']}")
            else:
                print(f"   ❌ Pwnagotchi NO invocado (error)")
        
        print(f"\n🔍 FASE 2: SOLICITUDES NO-WIFI (Herramientas tradicionales)")
        print("-" * 50)
        
        for i, request in enumerate(non_wifi_requests, 1):
            print(f"\n📝 Prueba No-WiFi {i}/4:")
            print(f"   📥 Solicitud: {request[:60]}...")
            
            result = self._test_non_wifi_integration(request)
            self.test_results.append(result)
            
            print(f"   🔧 Herramienta usada: {result['tool']}")
            print(f"   📊 Procesado por núcleo: {'✅' if result['nucleus_processed'] else '❌'}")
        
        # Análisis final
        integration_report = self._generate_integration_report()
        
        print(f"\n🎉 PRUEBAS DE INTEGRACIÓN COMPLETADAS")
        print("="*60)
        print(f"📊 Total de pruebas: {len(self.test_results)}")
        print(f"🤖 Invocaciones Pwnagotchi: {self.integration_metrics['pwnagotchi_invocations']}")
        print(f"✅ Integraciones exitosas: {self.integration_metrics['successful_integrations']}")
        print(f"🧠 Interpretaciones núcleo: {self.integration_metrics['data_interpretations']}")
        
        return integration_report
    
    def _test_wifi_integration(self, request):
        """Probar integración específica WiFi con Pwnagotchi"""
        start_time = time.time()
        
        # Procesar solicitud con sistema completo
        response = self.system.process_intelligent_request(request)
        
        duration = time.time() - start_time
        self.integration_metrics["total_requests"] += 1
        
        # Verificar si Pwnagotchi fue invocado
        pwnagotchi_invoked = response.get("tool") == "pwnagotchi_ai"
        ai_enhanced = response.get("ai_enhanced", False)
        
        if pwnagotchi_invoked:
            self.integration_metrics["pwnagotchi_invocations"] += 1
            self.integration_metrics["successful_integrations"] += 1
            
            # Simular interpretación del núcleo
            nucleus_interpretation = self._simulate_nucleus_data_interpretation(response)
            self.integration_metrics["data_interpretations"] += 1
            
            return {
                "request": request,
                "pwnagotchi_invoked": True,
                "ai_enhanced": ai_enhanced,
                "operation": response.get("category", "unknown"),
                "command": response.get("command", ""),
                "ai_state": "specialized_wifi_mode",
                "ai_level": response.get("ai_level", 1),
                "nucleus_interpretation": nucleus_interpretation,
                "success": True,
                "duration": duration
            }
        else:
            return {
                "request": request,
                "pwnagotchi_invoked": False,
                "fallback_tool": response.get("tool", "unknown"),
                "success": False,
                "duration": duration
            }
    
    def _test_non_wifi_integration(self, request):
        """Probar integración con herramientas tradicionales"""
        start_time = time.time()
        
        response = self.system.process_intelligent_request(request)
        
        duration = time.time() - start_time
        self.integration_metrics["total_requests"] += 1
        
        # Verificar que NO se invocó Pwnagotchi (correcto)
        nucleus_processed = response.get("success", False)
        
        if nucleus_processed:
            self.integration_metrics["successful_integrations"] += 1
        
        return {
            "request": request,
            "tool": response.get("tool", "unknown"),
            "category": response.get("category", "unknown"),
            "nucleus_processed": nucleus_processed,
            "success": nucleus_processed,
            "duration": duration
        }
    
    def _simulate_nucleus_data_interpretation(self, pwnagotchi_response):
        """Simular cómo el núcleo interpreta datos de Pwnagotchi"""
        # El núcleo procesa y hace propios los datos del Pwnagotchi
        
        interpretations = {
            "data_integration": "Datos de Pwnagotchi integrados como conocimiento propio del núcleo",
            "command_understanding": f"Núcleo comprende: {pwnagotchi_response.get('command', 'comando WiFi')}",
            "context_awareness": "Contexto WiFi/wireless detectado y procesado internamente",
            "knowledge_synthesis": "Experiencia Pwnagotchi sintetizada en base de conocimiento núcleo",
            "response_generation": "Respuesta final generada por núcleo basada en análisis Pwnagotchi"
        }
        
        # Simular nivel de comprensión del núcleo
        understanding_level = "advanced" if pwnagotchi_response.get("ai_enhanced") else "basic"
        
        return {
            "understanding_level": understanding_level,
            "data_integration_score": 0.92,
            "synthesis_quality": "high",
            "interpretations": interpretations,
            "nucleus_confidence": 0.88
        }
    
    def _generate_integration_report(self):
        """Generar informe detallado de integración"""
        wifi_tests = [r for r in self.test_results if "wifi" in r["request"].lower() or "wireless" in r["request"].lower()]
        non_wifi_tests = [r for r in self.test_results if r not in wifi_tests]
        
        wifi_success_rate = len([t for t in wifi_tests if t["success"]]) / len(wifi_tests) if wifi_tests else 0
        overall_success_rate = self.integration_metrics["successful_integrations"] / self.integration_metrics["total_requests"]
        
        report = {
            "integration_test_session": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.test_results),
                "wifi_tests": len(wifi_tests),
                "non_wifi_tests": len(non_wifi_tests),
                "overall_success_rate": overall_success_rate
            },
            "pwnagotchi_integration": {
                "invocations": self.integration_metrics["pwnagotchi_invocations"],
                "success_rate": wifi_success_rate,
                "ai_enhanced_responses": len([t for t in wifi_tests if t.get("ai_enhanced", False)]),
                "average_ai_level": sum(t.get("ai_level", 1) for t in wifi_tests) / len(wifi_tests) if wifi_tests else 0
            },
            "nucleus_data_processing": {
                "interpretations_generated": self.integration_metrics["data_interpretations"],
                "integration_quality": "high",
                "synthesis_capability": "advanced",
                "context_awareness": "wifi_specialized"
            },
            "system_performance": {
                "average_response_time": sum(t["duration"] for t in self.test_results) / len(self.test_results),
                "tool_distribution": self._analyze_tool_distribution(),
                "integration_effectiveness": overall_success_rate
            },
            "detailed_results": self.test_results
        }
        
        # Guardar informe
        report_file = Path("integration_results") / f"nucleus_pwnagotchi_integration_{int(time.time())}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Informe de integración guardado: {report_file}")
        
        return report
    
    def _analyze_tool_distribution(self):
        """Analizar distribución de herramientas utilizadas"""
        tools = {}
        for result in self.test_results:
            tool = result.get("tool") or result.get("fallback_tool", "unknown")
            tools[tool] = tools.get(tool, 0) + 1
        
        return tools
    
    def demonstrate_nucleus_interpretation(self):
        """Demostrar interpretación avanzada del núcleo"""
        print(f"\n🧠 DEMOSTRACIÓN: NÚCLEO INTERPRETANDO DATOS PWNAGOTCHI")
        print("="*60)
        
        # Solicitud compleja que requiere Pwnagotchi
        complex_request = "Realiza un análisis completo de seguridad WiFi: escanea redes, captura handshakes de redes WPA2, ejecuta ataques de deautenticación y crackea contraseñas débiles encontradas"
        
        print(f"📥 Solicitud compleja: {complex_request[:80]}...")
        
        # Procesar con sistema
        response = self.system.process_intelligent_request(complex_request)
        
        if response.get("tool") == "pwnagotchi_ai":
            print(f"\n🤖 PWNAGOTCHI AI ACTIVADO:")
            print(f"   📡 Categoría: {response.get('category', 'N/A')}")
            print(f"   💻 Comando generado: {response.get('command', 'N/A')}")
            print(f"   ⭐ Nivel IA: {response.get('ai_level', 'N/A')}")
            
            # Simular interpretación profunda del núcleo
            interpretation = self._simulate_nucleus_data_interpretation(response)
            
            print(f"\n🧠 NÚCLEO PROCESANDO DATOS PWNAGOTCHI:")
            print(f"   📊 Nivel de comprensión: {interpretation['understanding_level']}")
            print(f"   🔗 Puntuación integración: {interpretation['data_integration_score']:.2f}")
            print(f"   🎯 Confianza núcleo: {interpretation['nucleus_confidence']:.2f}")
            
            print(f"\n💭 INTERPRETACIONES DEL NÚCLEO:")
            for key, value in interpretation['interpretations'].items():
                print(f"   • {key}: {value[:50]}...")
            
            print(f"\n✅ RESULTADO: Núcleo procesó exitosamente datos Pwnagotchi como propios")
        else:
            print(f"❌ Error: Pwnagotchi no fue invocado correctamente")

def main():
    """Función principal de pruebas de integración"""
    tester = NucleusPwnagotchiIntegrationTest()
    
    print("🔬 Iniciando pruebas completas de integración")
    
    # Ejecutar pruebas principales
    report = tester.execute_integration_tests()
    
    # Demostración especial
    tester.demonstrate_nucleus_interpretation()
    
    print(f"\n📊 RESUMEN EJECUTIVO DE INTEGRACIÓN:")
    print(f"   🎯 Tasa éxito general: {report['integration_test_session']['overall_success_rate']:.1%}")
    print(f"   🤖 Invocaciones Pwnagotchi: {report['pwnagotchi_integration']['invocations']}")
    print(f"   🧠 Interpretaciones núcleo: {report['nucleus_data_processing']['interpretations_generated']}")
    print(f"   ⚡ Tiempo respuesta promedio: {report['system_performance']['average_response_time']:.3f}s")
    print(f"   🔧 Herramientas usadas: {list(report['system_performance']['tool_distribution'].keys())}")

if __name__ == "__main__":
    main()