#!/usr/bin/env python3
"""
Generador de 1 Millón de Pruebas - Núcleo C.A- Razonbilstro
Sistema exhaustivo de evaluación con bloques de conocimiento especializados
"""

import json
import random
import time
from datetime import datetime
from pathlib import Path

class MillionTestGenerator:
    """Generador de 1 millón de pruebas estructuradas por bloques de conocimiento"""
    
    def __init__(self, agent_dir):
        self.agent_dir = Path(agent_dir)
        self.test_dir = self.agent_dir / "million_tests"
        self.test_dir.mkdir(exist_ok=True)
        
        # Archivos de salida
        self.million_db = self.test_dir / "million_test_database.json"
        self.blocks_summary = self.test_dir / "knowledge_blocks_summary.json"
        
        print("🎯 Generador de 1 Millón de Pruebas iniciado")
        print("📊 Bloques de conocimiento especializados activados")
    
    def generate_million_tests(self):
        """Generar 1 millón de pruebas organizadas en bloques de conocimiento"""
        print("🚀 Iniciando generación de 1,000,000 pruebas...")
        
        # Definir bloques de conocimiento especializados
        knowledge_blocks = {
            "security_mastery": 150000,      # 150k pruebas de seguridad
            "system_administration": 120000, # 120k administración de sistemas
            "network_analysis": 100000,      # 100k análisis de red
            "programming_expertise": 100000, # 100k programación
            "database_operations": 80000,    # 80k bases de datos
            "file_management": 80000,        # 80k gestión de archivos
            "process_control": 70000,        # 70k control de procesos
            "development_tools": 70000,      # 70k herramientas de desarrollo
            "text_processing": 60000,        # 60k procesamiento de texto
            "backup_recovery": 50000,        # 50k respaldo y recuperación
            "monitoring_diagnostics": 50000, # 50k monitoreo y diagnósticos
            "automation_scripting": 40000,   # 40k automatización
            "performance_tuning": 30000,     # 30k optimización
            "troubleshooting": 20000         # 20k resolución de problemas
        }
        
        # Verificar que suma 1 millón
        total_tests = sum(knowledge_blocks.values())
        if total_tests != 1000000:
            print(f"⚠️ Ajustando total: {total_tests} -> 1,000,000")
            # Ajustar el último bloque
            last_block = list(knowledge_blocks.keys())[-1]
            knowledge_blocks[last_block] += (1000000 - total_tests)
        
        print(f"✅ Configuración validada: {sum(knowledge_blocks.values()):,} pruebas")
        
        # Generar pruebas por bloques
        all_tests = []
        test_id = 1
        
        for block_name, count in knowledge_blocks.items():
            print(f"📝 Generando bloque: {block_name} ({count:,} pruebas)")
            
            block_tests = self._generate_knowledge_block(block_name, count, test_id)
            all_tests.extend(block_tests)
            test_id += len(block_tests)
            
            print(f"   ✅ Completado: {len(block_tests):,} pruebas generadas")
        
        # Guardar base de datos completa
        print("💾 Guardando base de datos de 1 millón de pruebas...")
        with open(self.million_db, 'w', encoding='utf-8') as f:
            json.dump(all_tests, f, indent=None, ensure_ascii=False)
        
        # Crear resumen de bloques
        summary = {
            "total_tests": len(all_tests),
            "generation_date": datetime.now().isoformat(),
            "knowledge_blocks": knowledge_blocks,
            "file_size_mb": self.million_db.stat().st_size / (1024 * 1024)
        }
        
        with open(self.blocks_summary, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"🎉 ¡1,000,000 pruebas generadas exitosamente!")
        print(f"📁 Archivo: {self.million_db}")
        print(f"📊 Tamaño: {summary['file_size_mb']:.1f} MB")
        
        return all_tests
    
    def _generate_knowledge_block(self, block_name, count, start_id):
        """Generar pruebas para un bloque de conocimiento específico"""
        tests = []
        
        # Templates por bloque de conocimiento
        block_templates = {
            "security_mastery": self._get_security_templates(),
            "system_administration": self._get_sysadmin_templates(),
            "network_analysis": self._get_network_templates(),
            "programming_expertise": self._get_programming_templates(),
            "database_operations": self._get_database_templates(),
            "file_management": self._get_file_templates(),
            "process_control": self._get_process_templates(),
            "development_tools": self._get_devtools_templates(),
            "text_processing": self._get_text_templates(),
            "backup_recovery": self._get_backup_templates(),
            "monitoring_diagnostics": self._get_monitoring_templates(),
            "automation_scripting": self._get_automation_templates(),
            "performance_tuning": self._get_performance_templates(),
            "troubleshooting": self._get_troubleshooting_templates()
        }
        
        templates = block_templates.get(block_name, [])
        
        for i in range(count):
            # Seleccionar template aleatorio
            template = random.choice(templates)
            
            # Generar variación del template
            test = self._generate_test_variation(template, start_id + i, block_name)
            tests.append(test)
        
        return tests
    
    def _generate_test_variation(self, template, test_id, block_name):
        """Generar variación de un template de prueba"""
        # Variables aleatorias para generar variaciones
        variables = {
            "file": random.choice(["archivo.txt", "documento.pdf", "script.sh", "config.conf"]),
            "directory": random.choice(["~/pruebas", "/tmp/test", "/var/data", "~/projects"]),
            "ip": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
            "port": random.choice([22, 80, 443, 3306, 5432, 8080]),
            "process": random.choice(["apache2", "nginx", "mysql", "postgresql", "ssh"]),
            "user": random.choice(["admin", "user", "guest", "operator"]),
            "number": random.randint(1, 100)
        }
        
        # Reemplazar variables en el template
        natural_request = template["natural_request"]
        expected_command = template["expected_command"]
        
        for var, value in variables.items():
            natural_request = natural_request.replace(f"${var}", str(value))
            expected_command = expected_command.replace(f"${var}", str(value))
        
        return {
            "id": test_id,
            "knowledge_block": block_name,
            "natural_request": natural_request,
            "tokenized_llm": {
                "action": template["action"],
                "target": template.get("target", "system"),
                "complexity": template.get("complexity", "intermediate"),
                "block_specific": True
            },
            "expected_command": expected_command,
            "difficulty": template["difficulty"],
            "explanation": template["explanation"],
            "timestamp_created": datetime.now().isoformat()
        }
    
    def _get_security_templates(self):
        """Templates para seguridad (150k pruebas)"""
        return [
            {
                "natural_request": "Escanea puertos abiertos en la IP $ip",
                "expected_command": "nmap -sS $ip",
                "action": "port_scan",
                "difficulty": "intermediate",
                "explanation": "Escaneo de puertos con nmap"
            },
            {
                "natural_request": "Busca vulnerabilidades web en puerto $port",
                "expected_command": "nikto -h http://$ip:$port",
                "action": "vulnerability_scan",
                "difficulty": "advanced",
                "explanation": "Análisis de vulnerabilidades web"
            },
            {
                "natural_request": "Verifica integridad de archivos del sistema",
                "expected_command": "sudo debsums -c",
                "action": "integrity_check",
                "difficulty": "advanced",
                "explanation": "Verificación de integridad"
            },
            {
                "natural_request": "Analiza logs de autenticación de las últimas $number horas",
                "expected_command": "sudo tail -n $number /var/log/auth.log",
                "action": "log_analysis",
                "difficulty": "intermediate",
                "explanation": "Análisis de logs de seguridad"
            },
            {
                "natural_request": "Encuentra archivos con permisos SUID peligrosos",
                "expected_command": "find / -perm -4000 -type f 2>/dev/null",
                "action": "permission_audit",
                "difficulty": "advanced",
                "explanation": "Auditoría de permisos SUID"
            }
        ]
    
    def _get_sysadmin_templates(self):
        """Templates para administración de sistemas (120k pruebas)"""
        return [
            {
                "natural_request": "Actualiza todos los paquetes del sistema",
                "expected_command": "sudo apt update && sudo apt upgrade -y",
                "action": "system_update",
                "difficulty": "basic",
                "explanation": "Actualización completa del sistema"
            },
            {
                "natural_request": "Reinicia el servicio $process",
                "expected_command": "sudo systemctl restart $process",
                "action": "service_management",
                "difficulty": "intermediate",
                "explanation": "Gestión de servicios systemd"
            },
            {
                "natural_request": "Verifica el uso de disco en formato legible",
                "expected_command": "df -h",
                "action": "disk_monitoring",
                "difficulty": "basic",
                "explanation": "Monitoreo de espacio en disco"
            },
            {
                "natural_request": "Lista servicios que fallan en el arranque",
                "expected_command": "systemctl --failed",
                "action": "service_diagnostics",
                "difficulty": "intermediate",
                "explanation": "Diagnóstico de servicios fallidos"
            },
            {
                "natural_request": "Agrega usuario $user al grupo sudo",
                "expected_command": "sudo usermod -aG sudo $user",
                "action": "user_management",
                "difficulty": "intermediate",
                "explanation": "Gestión de usuarios y grupos"
            }
        ]
    
    def _get_network_templates(self):
        """Templates para análisis de red (100k pruebas)"""
        return [
            {
                "natural_request": "Muestra conexiones de red activas con procesos",
                "expected_command": "netstat -tulpn",
                "action": "network_monitoring",
                "difficulty": "intermediate",
                "explanation": "Monitoreo de conexiones de red"
            },
            {
                "natural_request": "Prueba conectividad con $ip usando $number paquetes",
                "expected_command": "ping -c $number $ip",
                "action": "connectivity_test",
                "difficulty": "basic",
                "explanation": "Test de conectividad con ping"
            },
            {
                "natural_request": "Traza la ruta hacia $ip",
                "expected_command": "traceroute $ip",
                "action": "route_tracing",
                "difficulty": "intermediate",
                "explanation": "Trazado de ruta de red"
            },
            {
                "natural_request": "Captura tráfico en la interfaz eth0 por $number segundos",
                "expected_command": "sudo tcpdump -i eth0 -c $number",
                "action": "packet_capture",
                "difficulty": "advanced",
                "explanation": "Captura de paquetes de red"
            },
            {
                "natural_request": "Muestra tabla de enrutamiento del sistema",
                "expected_command": "route -n",
                "action": "routing_info",
                "difficulty": "intermediate",
                "explanation": "Información de enrutamiento"
            }
        ]
    
    def _get_programming_templates(self):
        """Templates para programación (100k pruebas)"""
        return [
            {
                "natural_request": "Compila $file con optimización nivel 2",
                "expected_command": "gcc -O2 $file -o programa",
                "action": "code_compilation",
                "difficulty": "intermediate",
                "explanation": "Compilación optimizada con GCC"
            },
            {
                "natural_request": "Ejecuta script Python $file con argumentos de prueba",
                "expected_command": "python3 $file --test",
                "action": "script_execution",
                "difficulty": "basic",
                "explanation": "Ejecución de script Python"
            },
            {
                "natural_request": "Verifica sintaxis de archivo JavaScript $file",
                "expected_command": "node --check $file",
                "action": "syntax_check",
                "difficulty": "basic",
                "explanation": "Verificación de sintaxis JS"
            },
            {
                "natural_request": "Instala dependencias de proyecto Node.js",
                "expected_command": "npm install",
                "action": "dependency_install",
                "difficulty": "basic",
                "explanation": "Instalación de dependencias npm"
            },
            {
                "natural_request": "Ejecuta tests unitarios con pytest en $directory",
                "expected_command": "pytest $directory",
                "action": "testing",
                "difficulty": "intermediate",
                "explanation": "Ejecución de tests unitarios"
            }
        ]
    
    def _get_database_templates(self):
        """Templates para bases de datos (80k pruebas)"""
        return [
            {
                "natural_request": "Conecta a base de datos PostgreSQL como usuario $user",
                "expected_command": "psql -U $user -h localhost",
                "action": "db_connection",
                "difficulty": "intermediate",
                "explanation": "Conexión a PostgreSQL"
            },
            {
                "natural_request": "Respalda base de datos MySQL en $file",
                "expected_command": "mysqldump -u root -p database > $file",
                "action": "db_backup",
                "difficulty": "intermediate",
                "explanation": "Respaldo de base de datos MySQL"
            },
            {
                "natural_request": "Ejecuta consulta SQL desde $file",
                "expected_command": "mysql -u root -p < $file",
                "action": "sql_execution",
                "difficulty": "intermediate",
                "explanation": "Ejecución de archivo SQL"
            },
            {
                "natural_request": "Verifica estado del servicio PostgreSQL",
                "expected_command": "systemctl status postgresql",
                "action": "db_status",
                "difficulty": "basic",
                "explanation": "Verificación de estado de BD"
            },
            {
                "natural_request": "Optimiza tablas de base de datos MySQL",
                "expected_command": "mysqlcheck -o --all-databases -u root -p",
                "action": "db_optimization",
                "difficulty": "advanced",
                "explanation": "Optimización de base de datos"
            }
        ]
    
    def _get_file_templates(self):
        """Templates para gestión de archivos (80k pruebas)"""
        return [
            {
                "natural_request": "Crea directorio $directory con permisos 755",
                "expected_command": "mkdir -p $directory && chmod 755 $directory",
                "action": "directory_creation",
                "difficulty": "basic",
                "explanation": "Creación de directorio con permisos"
            },
            {
                "natural_request": "Busca archivos modificados en últimas $number horas",
                "expected_command": "find . -mtime -$number",
                "action": "file_search",
                "difficulty": "intermediate",
                "explanation": "Búsqueda por fecha de modificación"
            },
            {
                "natural_request": "Copia $file a $directory preservando permisos",
                "expected_command": "cp -p $file $directory/",
                "action": "file_copy",
                "difficulty": "basic",
                "explanation": "Copia preservando atributos"
            },
            {
                "natural_request": "Cambia propietario de $file a usuario $user",
                "expected_command": "sudo chown $user $file",
                "action": "ownership_change",
                "difficulty": "intermediate",
                "explanation": "Cambio de propietario"
            },
            {
                "natural_request": "Muestra tamaño de $directory en formato legible",
                "expected_command": "du -sh $directory",
                "action": "size_calculation",
                "difficulty": "basic",
                "explanation": "Cálculo de tamaño de directorio"
            }
        ]
    
    # Métodos para los demás templates (simplificados por espacio)
    def _get_process_templates(self):
        return [
            {"natural_request": "Termina proceso $process con PID $number", "expected_command": "kill $number", "action": "process_kill", "difficulty": "intermediate", "explanation": "Terminación de proceso"},
            {"natural_request": "Lista procesos del usuario $user", "expected_command": "ps -u $user", "action": "user_processes", "difficulty": "basic", "explanation": "Procesos por usuario"},
            {"natural_request": "Monitorea procesos en tiempo real", "expected_command": "top", "action": "process_monitoring", "difficulty": "basic", "explanation": "Monitor de procesos"},
            {"natural_request": "Ejecuta $process en segundo plano", "expected_command": "$process &", "action": "background_execution", "difficulty": "intermediate", "explanation": "Ejecución en background"},
            {"natural_request": "Muestra procesos ordenados por CPU", "expected_command": "ps aux --sort=-%cpu", "action": "process_sorting", "difficulty": "intermediate", "explanation": "Ordenamiento por uso de CPU"}
        ]
    
    def _get_devtools_templates(self):
        return [
            {"natural_request": "Inicia repositorio Git en $directory", "expected_command": "git init $directory", "action": "git_init", "difficulty": "basic", "explanation": "Inicialización de repositorio Git"},
            {"natural_request": "Hace commit con mensaje '$file modificado'", "expected_command": "git commit -m '$file modificado'", "action": "git_commit", "difficulty": "basic", "explanation": "Commit en Git"},
            {"natural_request": "Clona repositorio desde URL remota", "expected_command": "git clone URL", "action": "git_clone", "difficulty": "basic", "explanation": "Clonación de repositorio"},
            {"natural_request": "Crea rama nueva llamada feature-$number", "expected_command": "git checkout -b feature-$number", "action": "git_branch", "difficulty": "intermediate", "explanation": "Creación de rama Git"},
            {"natural_request": "Muestra diferencias en $file", "expected_command": "git diff $file", "action": "git_diff", "difficulty": "basic", "explanation": "Visualización de diferencias"}
        ]
    
    def _get_text_templates(self):
        return [
            {"natural_request": "Busca patrón '$user' en $file", "expected_command": "grep '$user' $file", "action": "text_search", "difficulty": "basic", "explanation": "Búsqueda de texto con grep"},
            {"natural_request": "Cuenta líneas en $file", "expected_command": "wc -l $file", "action": "line_count", "difficulty": "basic", "explanation": "Conteo de líneas"},
            {"natural_request": "Ordena contenido de $file", "expected_command": "sort $file", "action": "text_sort", "difficulty": "basic", "explanation": "Ordenamiento de texto"},
            {"natural_request": "Reemplaza '$user' por '$process' en $file", "expected_command": "sed 's/$user/$process/g' $file", "action": "text_replace", "difficulty": "intermediate", "explanation": "Reemplazo de texto con sed"},
            {"natural_request": "Muestra primeras $number líneas de $file", "expected_command": "head -n $number $file", "action": "text_head", "difficulty": "basic", "explanation": "Visualización de primeras líneas"}
        ]
    
    def _get_backup_templates(self):
        return [
            {"natural_request": "Comprime $directory en archivo tar.gz", "expected_command": "tar -czf backup.tar.gz $directory", "action": "archive_create", "difficulty": "basic", "explanation": "Creación de archivo comprimido"},
            {"natural_request": "Extrae contenido de $file", "expected_command": "tar -xzf $file", "action": "archive_extract", "difficulty": "basic", "explanation": "Extracción de archivo"},
            {"natural_request": "Sincroniza $directory con respaldo remoto", "expected_command": "rsync -av $directory/ backup/", "action": "sync_backup", "difficulty": "intermediate", "explanation": "Sincronización con rsync"},
            {"natural_request": "Lista contenido de archivo $file sin extraer", "expected_command": "tar -tzf $file", "action": "archive_list", "difficulty": "basic", "explanation": "Listado de contenido de archivo"},
            {"natural_request": "Crea respaldo incremental de $directory", "expected_command": "rsync -av --link-dest=backup.old $directory backup.new", "action": "incremental_backup", "difficulty": "advanced", "explanation": "Respaldo incremental"}
        ]
    
    def _get_monitoring_templates(self):
        return [
            {"natural_request": "Muestra uso de memoria del sistema", "expected_command": "free -h", "action": "memory_check", "difficulty": "basic", "explanation": "Verificación de memoria"},
            {"natural_request": "Monitorea CPU por $number segundos", "expected_command": "sar -u $number 1", "action": "cpu_monitoring", "difficulty": "intermediate", "explanation": "Monitoreo de CPU"},
            {"natural_request": "Verifica temperatura del sistema", "expected_command": "sensors", "action": "temperature_check", "difficulty": "basic", "explanation": "Verificación de temperatura"},
            {"natural_request": "Muestra información detallada de hardware", "expected_command": "lshw", "action": "hardware_info", "difficulty": "basic", "explanation": "Información de hardware"},
            {"natural_request": "Analiza rendimiento de disco $file", "expected_command": "iostat -x 1 $number", "action": "disk_performance", "difficulty": "intermediate", "explanation": "Análisis de rendimiento de disco"}
        ]
    
    def _get_automation_templates(self):
        return [
            {"natural_request": "Programa tarea para ejecutar $file cada $number minutos", "expected_command": "echo '*/$number * * * * $file' | crontab -", "action": "cron_schedule", "difficulty": "intermediate", "explanation": "Programación con cron"},
            {"natural_request": "Ejecuta comando $process cada vez que se modifique $file", "expected_command": "inotifywait -m $file -e modify --format '%f' | while read file; do $process; done", "action": "file_watch", "difficulty": "advanced", "explanation": "Monitoreo de archivos"},
            {"natural_request": "Crea script que procese archivos en $directory", "expected_command": "for file in $directory/*; do echo 'Procesando $file'; done", "action": "batch_processing", "difficulty": "intermediate", "explanation": "Procesamiento en lote"},
            {"natural_request": "Automatiza respaldo diario de $directory", "expected_command": "echo '0 2 * * * tar -czf backup-$(date +%Y%m%d).tar.gz $directory' | crontab -", "action": "automated_backup", "difficulty": "advanced", "explanation": "Respaldo automatizado"},
            {"natural_request": "Configura alerta cuando uso de disco supere $number%", "expected_command": "df | awk '{print $5}' | grep -o '[0-9]*' | awk '{if($1>$number) print \"Alerta: Disco lleno\"}'", "action": "disk_alert", "difficulty": "advanced", "explanation": "Alerta de espacio en disco"}
        ]
    
    def _get_performance_templates(self):
        return [
            {"natural_request": "Optimiza parámetros del kernel para rendimiento", "expected_command": "echo 'vm.swappiness=10' >> /etc/sysctl.conf", "action": "kernel_tuning", "difficulty": "advanced", "explanation": "Optimización del kernel"},
            {"natural_request": "Analiza cuellos de botella en el sistema", "expected_command": "vmstat 1 $number", "action": "bottleneck_analysis", "difficulty": "intermediate", "explanation": "Análisis de rendimiento"},
            {"natural_request": "Optimiza base de datos MySQL", "expected_command": "mysql_tune", "action": "db_tuning", "difficulty": "advanced", "explanation": "Optimización de base de datos"},
            {"natural_request": "Limpia cache del sistema", "expected_command": "sync && echo 3 > /proc/sys/vm/drop_caches", "action": "cache_cleanup", "difficulty": "intermediate", "explanation": "Limpieza de cache"},
            {"natural_request": "Ajusta prioridad del proceso $process", "expected_command": "renice -10 $(pgrep $process)", "action": "priority_adjust", "difficulty": "intermediate", "explanation": "Ajuste de prioridad"}
        ]
    
    def _get_troubleshooting_templates(self):
        return [
            {"natural_request": "Diagnostica problemas de red en $ip", "expected_command": "ping $ip && traceroute $ip && nslookup $ip", "action": "network_troubleshoot", "difficulty": "intermediate", "explanation": "Diagnóstico de red"},
            {"natural_request": "Verifica integridad del sistema de archivos", "expected_command": "fsck -f /dev/sda1", "action": "filesystem_check", "difficulty": "advanced", "explanation": "Verificación de sistema de archivos"},
            {"natural_request": "Analiza logs del sistema para errores", "expected_command": "journalctl -p err", "action": "error_analysis", "difficulty": "intermediate", "explanation": "Análisis de errores en logs"},
            {"natural_request": "Diagnostica problemas de memoria", "expected_command": "memtest86", "action": "memory_test", "difficulty": "advanced", "explanation": "Test de memoria"},
            {"natural_request": "Verifica estado de hardware", "expected_command": "dmesg | grep -i error", "action": "hardware_diagnostics", "difficulty": "intermediate", "explanation": "Diagnóstico de hardware"}
        ]

def main():
    """Función principal para generar 1 millón de pruebas"""
    import sys
    
    agent_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Crear generador
    generator = MillionTestGenerator(agent_dir)
    
    # Generar 1 millón de pruebas
    tests = generator.generate_million_tests()
    
    print(f"\n🎉 ¡GENERACIÓN COMPLETADA!")
    print(f"📊 Total: {len(tests):,} pruebas")
    print(f"💾 Archivo: {generator.million_db}")

if __name__ == "__main__":
    main()