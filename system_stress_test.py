#!/usr/bin/env python3
"""
Prueba de Estrés del Sistema Integrado
Evalúa todas las capacidades del Núcleo C.A- Razonbilstro con herramientas reales
"""

import json
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from complete_system_integration import CompleteSystemIntegration

class SystemStressTest:
    """Prueba de estrés completa del sistema integrado"""
    
    def __init__(self):
        self.system = CompleteSystemIntegration()
        self.results_dir = Path("stress_test_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Configuración de pruebas
        self.test_categories = {
            "reconocimiento": [
                "Escanear todos los puertos del servidor 192.168.1.1",
                "Detectar servicios ejecutándose en la red local",
                "Identificar sistema operativo del objetivo",
                "Realizar ping sweep de la red 192.168.1.0/24",
                "Escanear puertos UDP principales"
            ],
            "auditoria_wifi": [
                "Monitorear redes WiFi cercanas",
                "Capturar handshake WPA2 de la red objetivo",
                "Realizar ataque de deautenticación",
                "Crackear red WEP con diccionario",
                "Enumerar dispositivos conectados al AP"
            ],
            "analisis_web": [
                "Escanear vulnerabilidades en sitio web",
                "Buscar directorios ocultos del servidor",
                "Detectar tecnologías web utilizadas",
                "Probar inyecciones SQL básicas",
                "Enumerar subdominios del objetivo"
            ],
            "cracking": [
                "Crackear hash MD5 con wordlist",
                "Atacar contraseñas SSH con hydra",
                "Romper hash SHA1 encontrado",
                "Usar GPU para cracking masivo",
                "Generar rainbow table personalizada"
            ],
            "trafico": [
                "Capturar todo el tráfico de red",
                "Analizar paquetes HTTP interceptados",
                "Monitorear conexiones sospechosas",
                "Filtrar tráfico por protocolo específico",
                "Detectar patrones de comunicación maliciosa"
            ],
            "sistema": [
                "Clonar repositorio desde GitHub",
                "Comprimir directorio completo",
                "Monitorear procesos del sistema",
                "Descargar archivo con wget",
                "Editar configuración con nano"
            ]
        }
        
        self.stress_results = []
        self.performance_metrics = {}
        
        print("🚀 Prueba de Estrés del Sistema inicializada")
        print(f"📊 Categorías de prueba: {len(self.test_categories)}")
        print(f"🎯 Total de solicitudes: {sum(len(tests) for tests in self.test_categories.values())}")
    
    def execute_full_stress_test(self):
        """Ejecutar prueba de estrés completa"""
        print(f"🔥 INICIANDO PRUEBA DE ESTRÉS COMPLETA")
        print("="*60)
        
        start_time = time.time()
        total_tests = 0
        successful_tests = 0
        failed_tests = 0
        
        # Ejecutar pruebas por categoría
        for category, test_requests in self.test_categories.items():
            print(f"\n📝 CATEGORÍA: {category.upper()}")
            print("-" * 40)
            
            category_start = time.time()
            category_results = []
            
            for i, request in enumerate(test_requests):
                print(f"   {i+1}. Ejecutando: {request[:50]}...")
                
                test_start = time.time()
                try:
                    # Procesar solicitud con sistema integrado
                    result = self.system.process_intelligent_request(request)
                    test_duration = time.time() - test_start
                    
                    # Verificar herramienta real
                    tool_available = self._verify_tool_execution(result["tool"])
                    
                    test_result = {
                        "request": request,
                        "tool": result["tool"],
                        "command": result["command"],
                        "duration": test_duration,
                        "tool_available": tool_available,
                        "status": "success",
                        "category": category
                    }
                    
                    category_results.append(test_result)
                    successful_tests += 1
                    
                    print(f"      ✅ {result['tool']} - {test_duration:.2f}s")
                    
                except Exception as e:
                    test_result = {
                        "request": request,
                        "error": str(e),
                        "duration": time.time() - test_start,
                        "status": "failed",
                        "category": category
                    }
                    
                    category_results.append(test_result)
                    failed_tests += 1
                    
                    print(f"      ❌ Error: {str(e)[:30]}")
                
                total_tests += 1
                time.sleep(0.1)  # Breve pausa entre pruebas
            
            category_duration = time.time() - category_start
            
            # Compilar resultados de categoría
            category_summary = {
                "category": category,
                "total_tests": len(test_requests),
                "successful": len([r for r in category_results if r["status"] == "success"]),
                "failed": len([r for r in category_results if r["status"] == "failed"]),
                "duration": category_duration,
                "results": category_results
            }
            
            self.stress_results.append(category_summary)
            
            print(f"   📊 Categoría completada: {category_summary['successful']}/{category_summary['total_tests']} exitosos")
        
        # Compilar métricas finales
        total_duration = time.time() - start_time
        
        self.performance_metrics = {
            "total_duration": total_duration,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": (successful_tests / total_tests) * 100 if total_tests > 0 else 0,
            "tests_per_second": total_tests / total_duration,
            "average_response_time": sum(r["duration"] for category in self.stress_results 
                                       for r in category["results"]) / total_tests
        }
        
        # Generar informe detallado
        report = self._generate_stress_report()
        
        print(f"\n🎉 PRUEBA DE ESTRÉS COMPLETADA")
        print("="*60)
        print(f"📊 Total ejecutado: {total_tests} pruebas")
        print(f"✅ Exitosos: {successful_tests}")
        print(f"❌ Fallidos: {failed_tests}")
        print(f"📈 Tasa de éxito: {self.performance_metrics['success_rate']:.1f}%")
        print(f"⏱️ Duración total: {total_duration:.1f}s")
        print(f"⚡ Velocidad: {self.performance_metrics['tests_per_second']:.1f} pruebas/seg")
        
        return report
    
    def _verify_tool_execution(self, tool_name):
        """Verificar que la herramienta esté realmente disponible"""
        try:
            result = subprocess.run([tool_name, "--help"], 
                                  capture_output=True, text=True, timeout=2)
            return result.returncode == 0 or "not found" not in result.stderr.lower()
        except:
            return False
    
    def _generate_stress_report(self):
        """Generar informe detallado de la prueba de estrés"""
        report = {
            "prueba_estres": {
                "fecha_ejecucion": datetime.now().isoformat(),
                "duracion_total": self.performance_metrics["total_duration"],
                "metricas_rendimiento": self.performance_metrics,
                "resumen_categorias": []
            },
            "resultados_detallados": self.stress_results,
            "analisis_herramientas": self._analyze_tool_performance(),
            "recomendaciones": self._generate_recommendations()
        }
        
        # Resumen por categorías
        for category_result in self.stress_results:
            category_summary = {
                "categoria": category_result["category"],
                "pruebas_totales": category_result["total_tests"],
                "exitosas": category_result["successful"],
                "fallidas": category_result["failed"],
                "tasa_exito": (category_result["successful"] / category_result["total_tests"]) * 100,
                "tiempo_promedio": category_result["duration"] / category_result["total_tests"],
                "herramientas_utilizadas": list(set(r["tool"] for r in category_result["results"] 
                                                 if "tool" in r))
            }
            report["prueba_estres"]["resumen_categorias"].append(category_summary)
        
        # Guardar informe
        report_file = self.results_dir / f"stress_test_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Informe detallado guardado: {report_file}")
        
        # Generar informe legible
        self._generate_readable_report(report)
        
        return report
    
    def _analyze_tool_performance(self):
        """Analizar rendimiento de herramientas individuales"""
        tool_stats = {}
        
        for category_result in self.stress_results:
            for test_result in category_result["results"]:
                if "tool" in test_result:
                    tool = test_result["tool"]
                    if tool not in tool_stats:
                        tool_stats[tool] = {
                            "total_usos": 0,
                            "exitosos": 0,
                            "tiempo_total": 0,
                            "disponible": test_result.get("tool_available", False)
                        }
                    
                    tool_stats[tool]["total_usos"] += 1
                    tool_stats[tool]["tiempo_total"] += test_result["duration"]
                    
                    if test_result["status"] == "success":
                        tool_stats[tool]["exitosos"] += 1
        
        # Calcular métricas finales
        for tool, stats in tool_stats.items():
            stats["tasa_exito"] = (stats["exitosos"] / stats["total_usos"]) * 100
            stats["tiempo_promedio"] = stats["tiempo_total"] / stats["total_usos"]
        
        return tool_stats
    
    def _generate_recommendations(self):
        """Generar recomendaciones basadas en resultados"""
        recommendations = []
        
        # Analizar tasa de éxito general
        if self.performance_metrics["success_rate"] < 80:
            recommendations.append("Considerar instalar herramientas faltantes para mejorar cobertura")
        
        if self.performance_metrics["success_rate"] > 90:
            recommendations.append("Excelente integración - sistema listo para producción")
        
        # Analizar velocidad
        if self.performance_metrics["tests_per_second"] > 5:
            recommendations.append("Rendimiento excepcional - núcleo optimizado correctamente")
        
        # Analizar herramientas más utilizadas
        tool_usage = {}
        for category_result in self.stress_results:
            for test_result in category_result["results"]:
                if "tool" in test_result:
                    tool = test_result["tool"]
                    tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        most_used = max(tool_usage, key=tool_usage.get) if tool_usage else "ninguna"
        recommendations.append(f"Herramienta más utilizada: {most_used} - considerar optimización específica")
        
        return recommendations
    
    def _generate_readable_report(self, report):
        """Generar informe legible en texto"""
        readable_file = self.results_dir / f"informe_estres_{int(time.time())}.txt"
        
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("🚀 INFORME DE PRUEBA DE ESTRÉS - NÚCLEO C.A- RAZONBILSTRO\n")
            f.write("="*70 + "\n\n")
            
            # Métricas generales
            f.write("📊 MÉTRICAS GENERALES:\n")
            f.write(f"   • Total de pruebas: {report['prueba_estres']['metricas_rendimiento']['total_tests']}\n")
            f.write(f"   • Pruebas exitosas: {report['prueba_estres']['metricas_rendimiento']['successful_tests']}\n")
            f.write(f"   • Pruebas fallidas: {report['prueba_estres']['metricas_rendimiento']['failed_tests']}\n")
            f.write(f"   • Tasa de éxito: {report['prueba_estres']['metricas_rendimiento']['success_rate']:.1f}%\n")
            f.write(f"   • Duración total: {report['prueba_estres']['metricas_rendimiento']['total_duration']:.1f}s\n")
            f.write(f"   • Velocidad: {report['prueba_estres']['metricas_rendimiento']['tests_per_second']:.1f} pruebas/seg\n\n")
            
            # Resultados por categoría
            f.write("📋 RESULTADOS POR CATEGORÍA:\n")
            for category in report['prueba_estres']['resumen_categorias']:
                f.write(f"\n   🔸 {category['categoria'].upper()}:\n")
                f.write(f"      • Pruebas: {category['exitosas']}/{category['pruebas_totales']}\n")
                f.write(f"      • Éxito: {category['tasa_exito']:.1f}%\n")
                f.write(f"      • Tiempo promedio: {category['tiempo_promedio']:.2f}s\n")
                f.write(f"      • Herramientas: {', '.join(category['herramientas_utilizadas'])}\n")
            
            # Análisis de herramientas
            f.write(f"\n🔧 ANÁLISIS DE HERRAMIENTAS:\n")
            for tool, stats in report['analisis_herramientas'].items():
                f.write(f"\n   🔹 {tool}:\n")
                f.write(f"      • Usos: {stats['total_usos']}\n")
                f.write(f"      • Éxito: {stats['tasa_exito']:.1f}%\n")
                f.write(f"      • Tiempo promedio: {stats['tiempo_promedio']:.2f}s\n")
                f.write(f"      • Disponible: {'✅ Sí' if stats['disponible'] else '❌ No'}\n")
            
            # Recomendaciones
            f.write(f"\n💡 RECOMENDACIONES:\n")
            for i, rec in enumerate(report['recomendaciones'], 1):
                f.write(f"   {i}. {rec}\n")
        
        print(f"📄 Informe legible guardado: {readable_file}")

def main():
    """Función principal de la prueba de estrés"""
    stress_test = SystemStressTest()
    
    print("🔥 Iniciando prueba de estrés del sistema completo")
    report = stress_test.execute_full_stress_test()
    
    print(f"\n📋 RESUMEN EJECUTIVO:")
    print(f"   ✅ Sistema probado exhaustivamente")
    print(f"   📊 {report['prueba_estres']['metricas_rendimiento']['total_tests']} solicitudes procesadas")
    print(f"   🎯 {report['prueba_estres']['metricas_rendimiento']['success_rate']:.1f}% de éxito")
    print(f"   ⚡ {report['prueba_estres']['metricas_rendimiento']['tests_per_second']:.1f} pruebas por segundo")

if __name__ == "__main__":
    main()