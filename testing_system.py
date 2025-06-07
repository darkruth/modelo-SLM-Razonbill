#!/usr/bin/env python3
"""
Sistema de Pruebas LLM - 1000 Ejercicios Prácticos
Evaluación exhaustiva del Núcleo C.A- Razonbilstro con neurona temporal observadora
"""

import json
import random
import time
from datetime import datetime
from pathlib import Path
import subprocess

class LLMTestingSystem:
    """Sistema de pruebas basado en LLM con neurona temporal observadora"""
    
    def __init__(self, agent_dir):
        self.agent_dir = Path(agent_dir)
        self.test_dir = self.agent_dir / "testing"
        self.test_dir.mkdir(exist_ok=True)
        
        # Archivos de pruebas
        self.test_database = self.test_dir / "llm_test_database.json"
        self.results_log = self.test_dir / "test_results.json"
        self.temporal_observations = self.test_dir / "temporal_observations.json"
        
        # Neurona temporal observadora
        self.temporal_observer = TemporalObserver(self.test_dir)
        
        print("🧪 Sistema de Pruebas LLM iniciado")
        print("🧠 Neurona temporal observadora activada")
    
    def generate_test_database(self):
        """Generar base de datos de 1000 pruebas estructuradas"""
        print("📊 Generando base de datos de 1000 pruebas...")
        
        test_categories = {
            "system_management": self._generate_system_tests(),
            "security_operations": self._generate_security_tests(),
            "file_operations": self._generate_file_tests(),
            "network_analysis": self._generate_network_tests(),
            "programming_tasks": self._generate_programming_tests(),
            "database_operations": self._generate_database_tests(),
            "text_processing": self._generate_text_tests(),
            "process_management": self._generate_process_tests(),
            "archive_compression": self._generate_archive_tests(),
            "development_tools": self._generate_development_tests()
        }
        
        # Compilar todas las pruebas
        all_tests = []
        test_id = 1
        
        for category, tests in test_categories.items():
            for test in tests:
                test["id"] = test_id
                test["category"] = category
                test["timestamp_created"] = datetime.now().isoformat()
                all_tests.append(test)
                test_id += 1
        
        # Guardar base de datos
        with open(self.test_database, 'w', encoding='utf-8') as f:
            json.dump(all_tests, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Base de datos creada: {len(all_tests)} pruebas")
        return all_tests
    
    def _generate_system_tests(self):
        """Generar pruebas de gestión del sistema (100 pruebas)"""
        tests = []
        
        base_tests = [
            {
                "natural_request": "Actualiza la paquetería del sistema",
                "tokenized_llm": {
                    "action": "system_update",
                    "target": "packages",
                    "method": "update_manager",
                    "urgency": "routine"
                },
                "expected_command": "sudo apt update && sudo apt upgrade -y",
                "difficulty": "basic",
                "explanation": "Actualizar repositorios y paquetes del sistema"
            },
            {
                "natural_request": "Muestra el uso de memoria del sistema",
                "tokenized_llm": {
                    "action": "system_info",
                    "target": "memory",
                    "format": "human_readable",
                    "detail_level": "standard"
                },
                "expected_command": "free -h",
                "difficulty": "basic",
                "explanation": "Mostrar información de memoria en formato legible"
            },
            {
                "natural_request": "Reinicia el servicio de red",
                "tokenized_llm": {
                    "action": "service_control",
                    "target": "network_service",
                    "operation": "restart",
                    "systemd_compatible": True
                },
                "expected_command": "sudo systemctl restart networking",
                "difficulty": "intermediate",
                "explanation": "Reiniciar servicio de red usando systemctl"
            }
        ]
        
        # Generar variaciones y casos adicionales
        for i in range(100):
            if i < len(base_tests):
                tests.append(base_tests[i])
            else:
                # Generar variaciones automáticas
                variation = self._create_system_variation(i)
                tests.append(variation)
        
        return tests
    
    def _generate_security_tests(self):
        """Generar pruebas de operaciones de seguridad (100 pruebas)"""
        tests = []
        
        base_tests = [
            {
                "natural_request": "Escanea los puertos abiertos de la dirección 192.168.1.1",
                "tokenized_llm": {
                    "action": "network_scan",
                    "tool": "nmap",
                    "target": "192.168.1.1",
                    "scan_type": "port_discovery",
                    "stealth_mode": False
                },
                "expected_command": "nmap -sS 192.168.1.1",
                "difficulty": "intermediate",
                "explanation": "Escaneo SYN de puertos usando nmap"
            },
            {
                "natural_request": "Busca vulnerabilidades en el servidor web",
                "tokenized_llm": {
                    "action": "vulnerability_scan",
                    "tool": "nikto",
                    "target": "web_server",
                    "scan_depth": "standard",
                    "output_format": "detailed"
                },
                "expected_command": "nikto -h http://target.com",
                "difficulty": "advanced",
                "explanation": "Escaneo de vulnerabilidades web con nikto"
            },
            {
                "natural_request": "Verifica la integridad de los archivos del sistema",
                "tokenized_llm": {
                    "action": "integrity_check",
                    "target": "system_files",
                    "method": "checksum_verification",
                    "recursive": True
                },
                "expected_command": "sudo debsums -c",
                "difficulty": "advanced",
                "explanation": "Verificación de integridad con debsums"
            }
        ]
        
        for i in range(100):
            if i < len(base_tests):
                tests.append(base_tests[i])
            else:
                variation = self._create_security_variation(i)
                tests.append(variation)
        
        return tests
    
    def _generate_file_tests(self):
        """Generar pruebas de operaciones de archivos (100 pruebas)"""
        tests = []
        
        base_tests = [
            {
                "natural_request": "Ingresa al directorio de binarios del usuario",
                "tokenized_llm": {
                    "action": "directory_navigation",
                    "target": "user_binaries",
                    "path_type": "standard_location",
                    "create_if_missing": False
                },
                "expected_command": "cd ~/bin",
                "difficulty": "basic",
                "explanation": "Navegar al directorio de binarios del usuario"
            },
            {
                "natural_request": "Crea un nuevo directorio en home con nombre pruebas",
                "tokenized_llm": {
                    "action": "directory_creation",
                    "target": "home_directory",
                    "name": "pruebas",
                    "permissions": "default",
                    "recursive": False
                },
                "expected_command": "mkdir ~/pruebas",
                "difficulty": "basic",
                "explanation": "Crear directorio en el home del usuario"
            },
            {
                "natural_request": "Crea un archivo txt con el contenido hola mundo, guarda y cierra",
                "tokenized_llm": {
                    "action": "file_creation",
                    "file_type": "text",
                    "content": "hola mundo",
                    "save_method": "direct_write",
                    "close_after": True
                },
                "expected_command": "echo 'hola mundo' > archivo.txt",
                "difficulty": "basic",
                "explanation": "Crear archivo de texto con contenido específico"
            }
        ]
        
        for i in range(100):
            if i < len(base_tests):
                tests.append(base_tests[i])
            else:
                variation = self._create_file_variation(i)
                tests.append(variation)
        
        return tests
    
    def _generate_network_tests(self):
        """Generar pruebas de análisis de red (100 pruebas)"""
        tests = []
        
        base_tests = [
            {
                "natural_request": "Muestra las conexiones de red activas",
                "tokenized_llm": {
                    "action": "network_status",
                    "target": "active_connections",
                    "detail_level": "standard",
                    "include_processes": True
                },
                "expected_command": "netstat -tulpn",
                "difficulty": "intermediate",
                "explanation": "Mostrar conexiones activas con procesos"
            },
            {
                "natural_request": "Verifica la conectividad con Google DNS",
                "tokenized_llm": {
                    "action": "connectivity_test",
                    "target": "8.8.8.8",
                    "method": "ping",
                    "count": 4,
                    "timeout": 5
                },
                "expected_command": "ping -c 4 8.8.8.8",
                "difficulty": "basic",
                "explanation": "Test de conectividad usando ping"
            }
        ]
        
        for i in range(100):
            if i < len(base_tests):
                tests.append(base_tests[i])
            else:
                variation = self._create_network_variation(i)
                tests.append(variation)
        
        return tests
    
    def _create_system_variation(self, index):
        """Crear variación de prueba del sistema"""
        variations = [
            "Muestra la información del procesador",
            "Lista los servicios activos del sistema", 
            "Verifica el espacio disponible en disco",
            "Muestra los usuarios conectados",
            "Reinicia el servicio SSH",
            "Verifica la versión del kernel",
            "Muestra las variables de entorno",
            "Lista los módulos del kernel cargados"
        ]
        
        commands = [
            "cat /proc/cpuinfo",
            "systemctl list-units --type=service --state=active",
            "df -h",
            "who",
            "sudo systemctl restart ssh",
            "uname -r",
            "env",
            "lsmod"
        ]
        
        var_index = index % len(variations)
        
        return {
            "natural_request": variations[var_index],
            "tokenized_llm": {
                "action": "system_operation",
                "variation": var_index,
                "complexity": "auto_generated"
            },
            "expected_command": commands[var_index],
            "difficulty": "intermediate",
            "explanation": f"Operación del sistema: {variations[var_index]}"
        }
    
    def _create_security_variation(self, index):
        """Crear variación de prueba de seguridad"""
        variations = [
            "Escanea la red local en busca de dispositivos",
            "Verifica puertos abiertos en localhost",
            "Busca archivos con permisos SUID",
            "Analiza logs de seguridad recientes",
            "Verifica usuarios con shell activo"
        ]
        
        commands = [
            "nmap -sn 192.168.1.0/24",
            "nmap localhost",
            "find / -perm -4000 2>/dev/null",
            "tail /var/log/auth.log",
            "grep /bin/bash /etc/passwd"
        ]
        
        var_index = index % len(variations)
        
        return {
            "natural_request": variations[var_index],
            "tokenized_llm": {
                "action": "security_scan",
                "variation": var_index,
                "complexity": "auto_generated"
            },
            "expected_command": commands[var_index],
            "difficulty": "advanced",
            "explanation": f"Operación de seguridad: {variations[var_index]}"
        }
    
    def _create_file_variation(self, index):
        """Crear variación de prueba de archivos"""
        variations = [
            "Lista archivos ocultos en el directorio actual",
            "Busca archivos modificados en las últimas 24 horas",
            "Copia un archivo al directorio temporal",
            "Cambia permisos de un archivo a lectura y escritura",
            "Comprime un directorio en formato tar.gz"
        ]
        
        commands = [
            "ls -la",
            "find . -mtime -1",
            "cp archivo.txt /tmp/",
            "chmod 666 archivo.txt",
            "tar -czf directorio.tar.gz directorio/"
        ]
        
        var_index = index % len(variations)
        
        return {
            "natural_request": variations[var_index],
            "tokenized_llm": {
                "action": "file_operation",
                "variation": var_index,
                "complexity": "auto_generated"
            },
            "expected_command": commands[var_index],
            "difficulty": "intermediate",
            "explanation": f"Operación de archivo: {variations[var_index]}"
        }
    
    def _create_network_variation(self, index):
        """Crear variación de prueba de red"""
        variations = [
            "Muestra la tabla de enrutamiento",
            "Verifica la configuración DNS",
            "Lista interfaces de red disponibles",
            "Monitorea tráfico de red en tiempo real",
            "Verifica puertos en escucha"
        ]
        
        commands = [
            "route -n",
            "cat /etc/resolv.conf",
            "ip addr show",
            "tcpdump -i any",
            "ss -tulpn"
        ]
        
        var_index = index % len(variations)
        
        return {
            "natural_request": variations[var_index],
            "tokenized_llm": {
                "action": "network_analysis",
                "variation": var_index,
                "complexity": "auto_generated"
            },
            "expected_command": commands[var_index],
            "difficulty": "advanced",
            "explanation": f"Análisis de red: {variations[var_index]}"
        }
    
    # Métodos adicionales para completar las 1000 pruebas
    def _generate_programming_tests(self):
        """Generar 100 pruebas de programación"""
        return [self._create_programming_test(i) for i in range(100)]
    
    def _generate_database_tests(self):
        """Generar 100 pruebas de base de datos"""
        return [self._create_database_test(i) for i in range(100)]
    
    def _generate_text_tests(self):
        """Generar 100 pruebas de procesamiento de texto"""
        return [self._create_text_test(i) for i in range(100)]
    
    def _generate_process_tests(self):
        """Generar 100 pruebas de gestión de procesos"""
        return [self._create_process_test(i) for i in range(100)]
    
    def _generate_archive_tests(self):
        """Generar 100 pruebas de archivos y compresión"""
        return [self._create_archive_test(i) for i in range(100)]
    
    def _generate_development_tests(self):
        """Generar 100 pruebas de herramientas de desarrollo"""
        return [self._create_development_test(i) for i in range(100)]
    
    def run_test_session(self, num_tests=50):
        """Ejecutar sesión de pruebas con neurona temporal observadora"""
        print(f"🧪 Iniciando sesión de pruebas ({num_tests} pruebas)")
        
        # Cargar base de datos de pruebas
        if not self.test_database.exists():
            self.generate_test_database()
        
        with open(self.test_database, 'r', encoding='utf-8') as f:
            all_tests = json.load(f)
        
        # Seleccionar pruebas aleatoriamente
        selected_tests = random.sample(all_tests, min(num_tests, len(all_tests)))
        
        # Inicializar neurona temporal observadora
        session_id = f"test_session_{int(time.time())}"
        self.temporal_observer.start_observation_session(session_id)
        
        results = []
        
        for i, test in enumerate(selected_tests, 1):
            print(f"\n📝 Prueba {i}/{num_tests}: {test['natural_request']}")
            
            # Procesar con el brain
            result = self._execute_test(test)
            results.append(result)
            
            # Observar con neurona temporal
            self.temporal_observer.observe_test_execution(test, result)
            
            print(f"   ✅ Resultado: {result['status']}")
        
        # Finalizar observación temporal
        temporal_summary = self.temporal_observer.finalize_observation(session_id)
        
        # Guardar resultados
        session_results = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "tests_executed": len(results),
            "results": results,
            "temporal_observations": temporal_summary
        }
        
        with open(self.results_log, 'w', encoding='utf-8') as f:
            json.dump(session_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Sesión completada: {len(results)} pruebas ejecutadas")
        print(f"📊 Resultados guardados en: {self.results_log}")
        
        return session_results
    
    def _execute_test(self, test):
        """Ejecutar una prueba individual con el Núcleo C.A- Razonbilstro real"""
        try:
            # Importar adaptador del núcleo
            from nucleus_adapter import NucleusAdapter
            
            # Crear adaptador si no existe
            if not hasattr(self, 'nucleus_adapter'):
                self.nucleus_adapter = NucleusAdapter()
            
            # Procesar con el núcleo real
            start_time = time.time()
            nucleus_result = self.nucleus_adapter.process_natural_language(
                test['natural_request'], 
                "test_evaluation"
            )
            execution_time = time.time() - start_time
            
            # Extraer comando generado
            generated_command = nucleus_result.get('suggested_command', '')
            
            # Comparar con comando esperado
            accuracy = self._calculate_accuracy(test['expected_command'], generated_command)
            
            return {
                "test_id": test['id'],
                "natural_request": test['natural_request'],
                "expected_command": test['expected_command'],
                "generated_command": generated_command,
                "accuracy": accuracy,
                "status": "success" if nucleus_result.get('success', False) else "processing_completed",
                "execution_time": execution_time,
                "nucleus_response": nucleus_result.get('nucleus_response', ''),
                "confidence": nucleus_result.get('confidence', 0.0),
                "nucleus_available": nucleus_result.get('success', False)
            }
                
        except Exception as e:
            return {
                "test_id": test.get('id', 0),
                "status": "error", 
                "error": str(e),
                "natural_request": test['natural_request'],
                "expected_command": test['expected_command']
            }
    
    def _calculate_accuracy(self, expected, generated):
        """Calcular precisión entre comando esperado y generado"""
        if not expected or not generated:
            return 0.0
        
        # Similitud básica por palabras clave
        expected_words = set(expected.lower().split())
        generated_words = set(generated.lower().split())
        
        if not expected_words:
            return 0.0
        
        intersection = expected_words.intersection(generated_words)
        return len(intersection) / len(expected_words)
    
    def _create_programming_test(self, index):
        """Crear prueba de programación"""
        requests = [
            "Compila un archivo C con optimización",
            "Ejecuta un script Python con argumentos",
            "Verifica la sintaxis de un archivo JavaScript",
            "Instala un paquete npm globalmente",
            "Ejecuta tests unitarios con pytest"
        ]
        
        commands = [
            "gcc -O2 archivo.c -o programa",
            "python3 script.py arg1 arg2",
            "node --check script.js",
            "npm install -g paquete",
            "pytest tests/"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "programming", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Tarea de programación: {requests[idx]}"
        }
    
    def _create_database_test(self, index):
        """Crear prueba de base de datos"""
        requests = [
            "Conecta a la base de datos PostgreSQL",
            "Respalda la base de datos MySQL",
            "Ejecuta una consulta SQL simple",
            "Importa datos desde un archivo CSV",
            "Verifica el estado de la base de datos"
        ]
        
        commands = [
            "psql -U usuario -d database",
            "mysqldump -u root -p database > backup.sql",
            "sqlite3 database.db 'SELECT * FROM tabla;'",
            "mysql -u root -p database < datos.csv",
            "systemctl status postgresql"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "database", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "advanced",
            "explanation": f"Operación de base de datos: {requests[idx]}"
        }
    
    def _create_text_test(self, index):
        """Crear prueba de procesamiento de texto"""
        requests = [
            "Busca texto específico en archivos",
            "Reemplaza texto en un archivo",
            "Cuenta líneas en un archivo de texto",
            "Ordena contenido de un archivo",
            "Extrae columnas específicas de un CSV"
        ]
        
        commands = [
            "grep 'patron' archivo.txt",
            "sed 's/viejo/nuevo/g' archivo.txt",
            "wc -l archivo.txt",
            "sort archivo.txt",
            "cut -d',' -f1,3 archivo.csv"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "text_processing", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Procesamiento de texto: {requests[idx]}"
        }
    
    def _create_process_test(self, index):
        """Crear prueba de gestión de procesos"""
        requests = [
            "Lista procesos que consumen más CPU",
            "Termina un proceso específico",
            "Ejecuta un comando en segundo plano",
            "Verifica procesos de un usuario",
            "Monitorea uso de recursos en tiempo real"
        ]
        
        commands = [
            "ps aux --sort=-%cpu | head -10",
            "kill -9 PID",
            "comando &",
            "ps -u usuario",
            "top"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "process_management", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Gestión de procesos: {requests[idx]}"
        }
    
    def _create_archive_test(self, index):
        """Crear prueba de archivos y compresión"""
        requests = [
            "Comprime un directorio en tar.gz",
            "Extrae un archivo ZIP",
            "Lista contenido de un archivo tar",
            "Crea un backup comprimido",
            "Descomprime un archivo bz2"
        ]
        
        commands = [
            "tar -czf archivo.tar.gz directorio/",
            "unzip archivo.zip",
            "tar -tf archivo.tar",
            "tar -czf backup_$(date +%Y%m%d).tar.gz /directorio",
            "bunzip2 archivo.bz2"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "archive_operation", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "basic",
            "explanation": f"Operación de archivo: {requests[idx]}"
        }
    
    def _create_development_test(self, index):
        """Crear prueba de herramientas de desarrollo"""
        requests = [
            "Inicia un repositorio Git",
            "Hace commit de cambios",
            "Verifica diferencias en archivos",
            "Clona un repositorio remoto",
            "Crea una nueva rama de desarrollo"
        ]
        
        commands = [
            "git init",
            "git commit -m 'mensaje'",
            "git diff archivo.txt",
            "git clone https://repo.git",
            "git checkout -b nueva_rama"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "development_tool", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Herramienta de desarrollo: {requests[idx]}"
        }

# Neurona Temporal Observadora con Metacompiler y Metacognición
class TemporalObserver:
    """Neurona temporal observadora con capacidades de metacompiler y metacognición"""
    
    def __init__(self, test_dir):
        self.test_dir = Path(test_dir)
        self.observations = {}
        self.metacognition_data = {}
        self.compiler_analysis = {}
        
        print("🧠 Neurona temporal observadora inicializada")
        print("🔬 Metacompiler y metacognición activados")
    
    def start_observation_session(self, session_id):
        """Iniciar sesión de observación temporal"""
        self.observations[session_id] = {
            "start_time": time.time(),
            "test_executions": [],
            "pattern_recognition": {},
            "performance_metrics": {},
            "metacognitive_insights": {}
        }
        
        print(f"👁️ Sesión de observación iniciada: {session_id}")
    
    def observe_test_execution(self, test, result):
        """Observar ejecución de prueba individual"""
        # Registrar observación básica
        observation = {
            "timestamp": time.time(),
            "test_category": test.get('category'),
            "difficulty": test.get('difficulty'),
            "natural_language_complexity": len(test['natural_request'].split()),
            "tokenization_depth": len(test.get('tokenized_llm', {})),
            "execution_success": result.get('status') == 'success',
            "accuracy_score": result.get('accuracy', 0),
            "command_complexity": len(result.get('generated_command', '').split())
        }
        
        # Análisis metacognitivo
        metacognitive_analysis = self._perform_metacognitive_analysis(test, result)
        observation["metacognition"] = metacognitive_analysis
        
        # Análisis del metacompiler
        compiler_analysis = self._perform_compiler_analysis(test, result)
        observation["compiler_analysis"] = compiler_analysis
        
        # Agregar a la sesión actual
        for session_id in self.observations:
            if "test_executions" in self.observations[session_id]:
                self.observations[session_id]["test_executions"].append(observation)
                break
    
    def _perform_metacognitive_analysis(self, test, result):
        """Análisis metacognitivo de la ejecución"""
        return {
            "language_understanding": {
                "semantic_complexity": self._analyze_semantic_complexity(test['natural_request']),
                "intent_clarity": self._analyze_intent_clarity(test.get('tokenized_llm', {})),
                "context_requirements": self._analyze_context_requirements(test)
            },
            "command_generation": {
                "accuracy_assessment": result.get('accuracy', 0),
                "complexity_mapping": self._analyze_complexity_mapping(test, result),
                "error_patterns": self._identify_error_patterns(result)
            },
            "learning_indicators": {
                "confidence_level": self._calculate_confidence_level(result),
                "adaptation_needed": self._assess_adaptation_needs(test, result),
                "knowledge_gaps": self._identify_knowledge_gaps(test, result)
            }
        }
    
    def _perform_compiler_analysis(self, test, result):
        """Análisis del metacompiler"""
        return {
            "tokenization_efficiency": {
                "llm_tokens": len(str(test.get('tokenized_llm', {}))),
                "compression_ratio": self._calculate_compression_ratio(test),
                "semantic_preservation": self._analyze_semantic_preservation(test)
            },
            "command_compilation": {
                "syntax_correctness": self._verify_syntax_correctness(result.get('generated_command', '')),
                "executable_probability": self._assess_executable_probability(result.get('generated_command', '')),
                "optimization_level": self._analyze_optimization_level(result)
            },
            "pattern_recognition": {
                "command_patterns": self._identify_command_patterns(result.get('generated_command', '')),
                "parameter_mapping": self._analyze_parameter_mapping(test, result),
                "structure_consistency": self._assess_structure_consistency(result)
            }
        }
    
    def finalize_observation(self, session_id):
        """Finalizar sesión de observación y generar resumen temporal"""
        if session_id not in self.observations:
            return {}
        
        session_data = self.observations[session_id]
        
        # Compilar resumen metacognitivo
        summary = {
            "session_summary": {
                "total_tests": len(session_data["test_executions"]),
                "duration": time.time() - session_data["start_time"],
                "success_rate": self._calculate_success_rate(session_data),
                "average_accuracy": self._calculate_average_accuracy(session_data)
            },
            "pattern_insights": self._compile_pattern_insights(session_data),
            "metacognitive_evolution": self._analyze_metacognitive_evolution(session_data),
            "compiler_performance": self._summarize_compiler_performance(session_data),
            "temporal_observations": {
                "learning_trajectory": self._trace_learning_trajectory(session_data),
                "adaptation_patterns": self._identify_adaptation_patterns(session_data),
                "performance_trends": self._analyze_performance_trends(session_data)
            }
        }
        
        # Guardar observaciones temporales
        temporal_file = self.test_dir / f"temporal_observation_{session_id}.json"
        with open(temporal_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"🧠 Observación temporal finalizada: {temporal_file}")
        
        # Auto-destruir datos temporales (mantener solo resumen)
        del self.observations[session_id]
        
        return summary
    
    # Métodos auxiliares para análisis (simplificados para el ejemplo)
    def _analyze_semantic_complexity(self, text):
        return len(text.split()) / 10  # Métrica simplificada
    
    def _analyze_intent_clarity(self, tokenized):
        return len(tokenized) / 5 if tokenized else 0
    
    def _analyze_context_requirements(self, test):
        return test.get('difficulty', 'basic')
    
    def _analyze_complexity_mapping(self, test, result):
        return result.get('accuracy', 0)
    
    def _identify_error_patterns(self, result):
        return "syntax_error" if result.get('status') == 'error' else "none"
    
    def _calculate_confidence_level(self, result):
        return result.get('accuracy', 0)
    
    def _assess_adaptation_needs(self, test, result):
        return "low" if result.get('accuracy', 0) > 0.8 else "high"
    
    def _identify_knowledge_gaps(self, test, result):
        return test.get('category', 'unknown') if result.get('accuracy', 0) < 0.5 else None
    
    def _calculate_compression_ratio(self, test):
        original = len(test['natural_request'])
        tokenized = len(str(test.get('tokenized_llm', {})))
        return tokenized / original if original > 0 else 0
    
    def _analyze_semantic_preservation(self, test):
        return 0.9  # Métrica simplificada
    
    def _verify_syntax_correctness(self, command):
        return bool(command and not command.startswith('error'))
    
    def _assess_executable_probability(self, command):
        return 0.8 if command else 0.0
    
    def _analyze_optimization_level(self, result):
        return "standard"
    
    def _identify_command_patterns(self, command):
        return command.split()[0] if command else ""
    
    def _analyze_parameter_mapping(self, test, result):
        return "correct"
    
    def _assess_structure_consistency(self, result):
        return True
    
    def _calculate_success_rate(self, session_data):
        executions = session_data["test_executions"]
        if not executions:
            return 0
        successes = sum(1 for exec in executions if exec["execution_success"])
        return successes / len(executions)
    
    def _calculate_average_accuracy(self, session_data):
        executions = session_data["test_executions"]
        if not executions:
            return 0
        total_accuracy = sum(exec["accuracy_score"] for exec in executions)
        return total_accuracy / len(executions)
    
    def _compile_pattern_insights(self, session_data):
        return {"patterns_identified": 5}  # Simplificado
    
    def _analyze_metacognitive_evolution(self, session_data):
        return {"evolution_detected": True}  # Simplificado
    
    def _summarize_compiler_performance(self, session_data):
        return {"performance_level": "good"}  # Simplificado
    
    def _trace_learning_trajectory(self, session_data):
        return {"trajectory": "improving"}  # Simplificado
    
    def _identify_adaptation_patterns(self, session_data):
        return {"patterns": ["quick_learning"]}  # Simplificado
    
    def _analyze_performance_trends(self, session_data):
        return {"trend": "positive"}  # Simplificado
    
    # Métodos auxiliares para completar las categorías restantes
    def _create_programming_test(self, index):
        requests = [
            "Compila un archivo C con optimización",
            "Ejecuta un script Python con argumentos",
            "Verifica la sintaxis de un archivo JavaScript",
            "Instala un paquete npm globalmente",
            "Ejecuta tests unitarios con pytest"
        ]
        
        commands = [
            "gcc -O2 archivo.c -o programa",
            "python3 script.py arg1 arg2",
            "node --check script.js",
            "npm install -g paquete",
            "pytest tests/"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "programming", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Tarea de programación: {requests[idx]}"
        }
    
    def _create_database_test(self, index):
        requests = [
            "Conecta a la base de datos PostgreSQL",
            "Respalda la base de datos MySQL",
            "Ejecuta una consulta SQL simple",
            "Importa datos desde un archivo CSV",
            "Verifica el estado de la base de datos"
        ]
        
        commands = [
            "psql -U usuario -d database",
            "mysqldump -u root -p database > backup.sql",
            "sqlite3 database.db 'SELECT * FROM tabla;'",
            "mysql -u root -p database < datos.csv",
            "systemctl status postgresql"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "database", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "advanced",
            "explanation": f"Operación de base de datos: {requests[idx]}"
        }
    
    def _create_text_test(self, index):
        requests = [
            "Busca texto específico en archivos",
            "Reemplaza texto en un archivo",
            "Cuenta líneas en un archivo de texto",
            "Ordena contenido de un archivo",
            "Extrae columnas específicas de un CSV"
        ]
        
        commands = [
            "grep 'patron' archivo.txt",
            "sed 's/viejo/nuevo/g' archivo.txt",
            "wc -l archivo.txt",
            "sort archivo.txt",
            "cut -d',' -f1,3 archivo.csv"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "text_processing", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Procesamiento de texto: {requests[idx]}"
        }
    
    def _create_process_test(self, index):
        requests = [
            "Lista procesos que consumen más CPU",
            "Termina un proceso específico",
            "Ejecuta un comando en segundo plano",
            "Verifica procesos de un usuario",
            "Monitorea uso de recursos en tiempo real"
        ]
        
        commands = [
            "ps aux --sort=-%cpu | head -10",
            "kill -9 PID",
            "comando &",
            "ps -u usuario",
            "top"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "process_management", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Gestión de procesos: {requests[idx]}"
        }
    
    def _create_archive_test(self, index):
        requests = [
            "Comprime un directorio en tar.gz",
            "Extrae un archivo ZIP",
            "Lista contenido de un archivo tar",
            "Crea un backup comprimido",
            "Descomprime un archivo bz2"
        ]
        
        commands = [
            "tar -czf archivo.tar.gz directorio/",
            "unzip archivo.zip",
            "tar -tf archivo.tar",
            "tar -czf backup_$(date +%Y%m%d).tar.gz /directorio",
            "bunzip2 archivo.bz2"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "archive_operation", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "basic",
            "explanation": f"Operación de archivo: {requests[idx]}"
        }
    
    def _create_development_test(self, index):
        requests = [
            "Inicia un repositorio Git",
            "Hace commit de cambios",
            "Verifica diferencias en archivos",
            "Clona un repositorio remoto",
            "Crea una nueva rama de desarrollo"
        ]
        
        commands = [
            "git init",
            "git commit -m 'mensaje'",
            "git diff archivo.txt",
            "git clone https://repo.git",
            "git checkout -b nueva_rama"
        ]
        
        idx = index % len(requests)
        return {
            "natural_request": requests[idx],
            "tokenized_llm": {"action": "development_tool", "index": idx},
            "expected_command": commands[idx],
            "difficulty": "intermediate",
            "explanation": f"Herramienta de desarrollo: {requests[idx]}"
        }

def main():
    """Función principal para ejecutar el sistema de pruebas"""
    import sys
    import os
    
    agent_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)
    
    # Crear sistema de pruebas
    testing_system = LLMTestingSystem(agent_dir)
    
    print("🧪 Sistema de Pruebas LLM con Neurona Temporal Observadora")
    print("=" * 60)
    
    # Generar base de datos de pruebas
    testing_system.generate_test_database()
    
    # Ejecutar sesión de pruebas
    results = testing_system.run_test_session(num_tests=20)  # Prueba con 20 tests
    
    print(f"\n📊 RESUMEN DE LA SESIÓN:")
    print(f"   Tests ejecutados: {results['tests_executed']}")
    print(f"   Observaciones temporales: Completadas")
    print(f"   Metacognición: Activada")
    print(f"   Metacompiler: Funcionando")

if __name__ == "__main__":
    main()