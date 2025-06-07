#!/usr/bin/env python3
"""
Metacognición y Percepción del Entorno - Núcleo C.A- Razonbilstro
Sistema de autoconciencia y análisis del entorno para el agente NetHunter
"""

import os
import json
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path
import psutil

class EnvironmentPerception:
    """Sistema de percepción del entorno y metacognición"""
    
    def __init__(self, agent_dir):
        self.agent_dir = Path(agent_dir)
        self.log_dir = self.agent_dir / "log"
        self.perception_log = self.log_dir / "environment_perception.json"
        self.metacognition_log = self.log_dir / "metacognition_analysis.json"
        
        # Estado del entorno
        self.environment_state = {
            "system_resources": {},
            "network_status": {},
            "active_processes": {},
            "security_context": {},
            "user_behavior": {},
            "tool_availability": {}
        }
        
        # Estado de metacognición
        self.metacognition_state = {
            "self_assessment": {},
            "performance_metrics": {},
            "adaptation_history": {},
            "decision_confidence": {},
            "learning_progress": {}
        }
        
        print("🧠 Sistema de metacognición y percepción iniciado")
    
    def analyze_system_resources(self):
        """Analizar recursos del sistema en tiempo real"""
        try:
            # CPU y memoria
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Procesos activos relacionados con seguridad
            security_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_info = proc.info
                    if any(tool in ' '.join(proc_info['cmdline'] or []).lower() 
                          for tool in ['nmap', 'sqlmap', 'john', 'hashcat', 'hydra', 'metasploit']):
                        security_processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'command': ' '.join(proc_info['cmdline'] or [])[:100]
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.environment_state["system_resources"] = {
                "cpu_usage": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available // (1024**3),  # GB
                "disk_usage": disk.percent,
                "disk_free": disk.free // (1024**3),  # GB
                "security_processes": security_processes,
                "timestamp": datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error analizando recursos: {e}")
            return False
    
    def analyze_network_context(self):
        """Analizar contexto de red y conectividad"""
        try:
            # Interfaces de red
            network_interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family.name == 'AF_INET':
                        network_interfaces.append({
                            'interface': interface,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
            
            # Test de conectividad
            connectivity_tests = {
                'google_dns': self._test_ping('8.8.8.8'),
                'cloudflare_dns': self._test_ping('1.1.1.1'),
                'local_gateway': self._test_local_gateway()
            }
            
            # Puertos en escucha
            listening_ports = []
            for conn in psutil.net_connections():
                if conn.status == 'LISTEN' and conn.laddr:
                    listening_ports.append({
                        'port': conn.laddr.port,
                        'address': conn.laddr.ip,
                        'pid': conn.pid
                    })
            
            self.environment_state["network_status"] = {
                "interfaces": network_interfaces,
                "connectivity": connectivity_tests,
                "listening_ports": listening_ports[:10],  # Top 10
                "timestamp": datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error analizando red: {e}")
            return False
    
    def _test_ping(self, host):
        """Test de ping simple"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', host],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _test_local_gateway(self):
        """Test de conectividad al gateway local"""
        try:
            result = subprocess.run(
                ['ip', 'route', 'show', 'default'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and 'default via' in result.stdout:
                gateway = result.stdout.split('default via')[1].split()[0]
                return self._test_ping(gateway)
        except:
            pass
        return False
    
    def analyze_security_context(self):
        """Analizar contexto de seguridad actual"""
        try:
            # Usuario y privilegios
            user_info = {
                'username': os.getenv('USER', 'unknown'),
                'uid': os.getuid() if hasattr(os, 'getuid') else None,
                'groups': os.getgroups() if hasattr(os, 'getgroups') else [],
                'is_root': os.getuid() == 0 if hasattr(os, 'getuid') else False
            }
            
            # Herramientas de seguridad disponibles
            security_tools = {}
            tools_to_check = ['nmap', 'sqlmap', 'john', 'hashcat', 'hydra', 'nikto', 'metasploit']
            
            for tool in tools_to_check:
                try:
                    result = subprocess.run(['which', tool], capture_output=True)
                    security_tools[tool] = result.returncode == 0
                except:
                    security_tools[tool] = False
            
            # Estado del firewall
            firewall_status = self._check_firewall_status()
            
            self.environment_state["security_context"] = {
                "user_info": user_info,
                "security_tools": security_tools,
                "firewall_status": firewall_status,
                "timestamp": datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error analizando seguridad: {e}")
            return False
    
    def _check_firewall_status(self):
        """Verificar estado del firewall"""
        firewall_info = {}
        
        # UFW
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            if result.returncode == 0:
                firewall_info['ufw'] = 'active' if 'Status: active' in result.stdout else 'inactive'
        except:
            firewall_info['ufw'] = 'not_available'
        
        # iptables
        try:
            result = subprocess.run(['iptables', '-L'], capture_output=True)
            firewall_info['iptables'] = result.returncode == 0
        except:
            firewall_info['iptables'] = False
        
        return firewall_info
    
    def perform_self_assessment(self):
        """Realizar autoevaluación del rendimiento del agente"""
        try:
            # Analizar logs de decisiones
            decision_accuracy = self._analyze_decision_accuracy()
            
            # Analizar tiempos de respuesta
            response_times = self._analyze_response_times()
            
            # Evaluar uso de recursos
            resource_efficiency = self._evaluate_resource_efficiency()
            
            # Análisis de errores
            error_patterns = self._analyze_error_patterns()
            
            self.metacognition_state["self_assessment"] = {
                "decision_accuracy": decision_accuracy,
                "response_times": response_times,
                "resource_efficiency": resource_efficiency,
                "error_patterns": error_patterns,
                "confidence_level": self._calculate_confidence_level(),
                "adaptation_needed": self._assess_adaptation_needs(),
                "timestamp": datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error en autoevaluación: {e}")
            return False
    
    def _analyze_decision_accuracy(self):
        """Analizar precisión de decisiones tomadas"""
        try:
            decision_file = self.log_dir / "decision_history.json"
            if not decision_file.exists():
                return {"accuracy": 0.5, "total_decisions": 0}
            
            with open(decision_file, 'r') as f:
                decisions = [json.loads(line) for line in f if line.strip()]
            
            if not decisions:
                return {"accuracy": 0.5, "total_decisions": 0}
            
            # Simular análisis de precisión basado en confianza
            total_confidence = sum(float(d.get('confidence', 0.5)) for d in decisions)
            accuracy = total_confidence / len(decisions) if decisions else 0.5
            
            return {
                "accuracy": accuracy,
                "total_decisions": len(decisions),
                "recent_trend": "improving" if accuracy > 0.7 else "needs_attention"
            }
            
        except Exception:
            return {"accuracy": 0.5, "total_decisions": 0, "error": "analysis_failed"}
    
    def _analyze_response_times(self):
        """Analizar tiempos de respuesta del sistema"""
        try:
            execution_file = self.log_dir / "execution_history.log"
            if not execution_file.exists():
                return {"average_time": 1.0, "total_executions": 0}
            
            # Leer últimas 50 ejecuciones
            with open(execution_file, 'r') as f:
                lines = f.readlines()[-50:]
            
            times = []
            for line in lines:
                if 'EXIT: 0' in line:  # Solo comandos exitosos
                    times.append(1.0)  # Tiempo simulado
            
            avg_time = sum(times) / len(times) if times else 1.0
            
            return {
                "average_time": avg_time,
                "total_executions": len(times),
                "performance": "good" if avg_time < 2.0 else "needs_optimization"
            }
            
        except Exception:
            return {"average_time": 1.0, "total_executions": 0, "error": "analysis_failed"}
    
    def _evaluate_resource_efficiency(self):
        """Evaluar eficiencia en el uso de recursos"""
        current_resources = self.environment_state.get("system_resources", {})
        
        cpu_usage = current_resources.get("cpu_usage", 50)
        memory_usage = current_resources.get("memory_percent", 50)
        
        efficiency_score = 1.0 - (cpu_usage + memory_usage) / 200
        
        return {
            "efficiency_score": max(0.1, efficiency_score),
            "cpu_impact": "low" if cpu_usage < 30 else "high",
            "memory_impact": "low" if memory_usage < 70 else "high"
        }
    
    def _analyze_error_patterns(self):
        """Analizar patrones de errores"""
        try:
            feedback_file = self.log_dir / "feedback_responses.log"
            if not feedback_file.exists():
                return {"error_rate": 0.1, "common_errors": []}
            
            with open(feedback_file, 'r') as f:
                lines = f.readlines()
            
            error_count = sum(1 for line in lines if 'ERROR' in line)
            total_count = len(lines)
            
            error_rate = error_count / total_count if total_count > 0 else 0.1
            
            return {
                "error_rate": error_rate,
                "total_events": total_count,
                "trend": "improving" if error_rate < 0.1 else "needs_attention"
            }
            
        except Exception:
            return {"error_rate": 0.1, "common_errors": [], "error": "analysis_failed"}
    
    def _calculate_confidence_level(self):
        """Calcular nivel de confianza general del sistema"""
        assessment = self.metacognition_state.get("self_assessment", {})
        
        factors = [
            assessment.get("decision_accuracy", {}).get("accuracy", 0.5),
            1.0 - min(1.0, assessment.get("response_times", {}).get("average_time", 1.0) / 5.0),
            assessment.get("resource_efficiency", {}).get("efficiency_score", 0.5),
            1.0 - assessment.get("error_patterns", {}).get("error_rate", 0.1)
        ]
        
        return sum(factors) / len(factors)
    
    def _assess_adaptation_needs(self):
        """Evaluar necesidades de adaptación"""
        confidence = self._calculate_confidence_level()
        
        if confidence < 0.6:
            return "high_priority"
        elif confidence < 0.8:
            return "moderate"
        else:
            return "minimal"
    
    def save_perception_state(self):
        """Guardar estado de percepción del entorno"""
        try:
            with open(self.perception_log, 'w') as f:
                json.dump(self.environment_state, f, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ Error guardando percepción: {e}")
            return False
    
    def save_metacognition_state(self):
        """Guardar estado de metacognición"""
        try:
            with open(self.metacognition_log, 'w') as f:
                json.dump(self.metacognition_state, f, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ Error guardando metacognición: {e}")
            return False
    
    def continuous_perception(self, interval=30):
        """Monitoreo continuo de percepción y metacognición"""
        print(f"👁️ Iniciando percepción continua (cada {interval}s)")
        
        while True:
            try:
                # Percepción del entorno
                self.analyze_system_resources()
                self.analyze_network_context()
                self.analyze_security_context()
                
                # Metacognición
                self.perform_self_assessment()
                
                # Guardar estados
                self.save_perception_state()
                self.save_metacognition_state()
                
                # Mostrar resumen cada 5 ciclos
                if hasattr(self, '_cycle_count'):
                    self._cycle_count += 1
                else:
                    self._cycle_count = 1
                
                if self._cycle_count % 5 == 0:
                    self._show_perception_summary()
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Percepción detenida")
                break
            except Exception as e:
                print(f"⚠️ Error en ciclo de percepción: {e}")
                time.sleep(interval)
    
    def _show_perception_summary(self):
        """Mostrar resumen de percepción"""
        resources = self.environment_state.get("system_resources", {})
        security = self.environment_state.get("security_context", {})
        assessment = self.metacognition_state.get("self_assessment", {})
        
        print(f"\n🧠 RESUMEN DE PERCEPCIÓN:")
        print(f"   💻 CPU: {resources.get('cpu_usage', 0):.1f}% | RAM: {resources.get('memory_percent', 0):.1f}%")
        print(f"   🔒 Herramientas disponibles: {sum(security.get('security_tools', {}).values())}")
        print(f"   📊 Confianza: {assessment.get('confidence_level', 0.5):.2f}")
        print(f"   🎯 Precisión: {assessment.get('decision_accuracy', {}).get('accuracy', 0.5):.2f}")

def main():
    """Función principal"""
    import sys
    
    agent_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)
    
    perception = EnvironmentPerception(agent_dir)
    
    try:
        perception.continuous_perception(interval=30)
    except KeyboardInterrupt:
        print("\n👋 Sistema de percepción detenido")

if __name__ == "__main__":
    main()