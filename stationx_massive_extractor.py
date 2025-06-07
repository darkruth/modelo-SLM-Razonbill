#!/usr/bin/env python3
"""
Extractor Masivo StationX - Datasets Auténticos Individuales
Extrae contenido auténtico de múltiples URLs y entrena con dos neuronas temporales
"""

import json
import time
import requests
import hashlib
from pathlib import Path
from datetime import datetime
import trafilatura
import re
from dual_temporal_training_system import DualTemporalTrainingSystem

class StationXMassiveExtractor:
    """Extractor masivo para múltiples herramientas de StationX"""
    
    def __init__(self):
        self.output_dir = Path("datasets/stationx_massive")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # URLs objetivo para extracción
        self.target_urls = [
            "https://www.stationx.net/linux-command-line-cheat-sheet/",
            "https://www.stationx.net/beef-hacking-tool/",
            "https://www.stationx.net/bash-cheat-sheet/",
            "https://www.stationx.net/tmux-cheat-sheet/",
            "https://www.stationx.net/metasploit-cheat-sheet/",
            "https://www.stationx.net/how-to-use-metasploit-in-kali-linux/",
            "https://www.stationx.net/meterpreter-commands/",
            "https://www.stationx.net/nmap-cheat-sheet/",
            "https://www.stationx.net/nmap-udp-scan/",
            "https://www.stationx.net/nmap-vulnerability-scan/",
            "https://www.stationx.net/nmap-ping-sweep/",
            "https://www.stationx.net/nmap-os-detection/",
            "https://www.stationx.net/how-to-use-nmap-to-scan-a-network/",
            "https://www.stationx.net/how-to-use-aircrack-ng-tutorial/",
            "https://www.stationx.net/bettercap-tutorial/",
            "https://www.stationx.net/wireshark-cheat-sheet/",
            "https://www.stationx.net/how-to-use-wifite/",
            "https://www.stationx.net/how-to-use-powershell-empire/",
            "https://www.stationx.net/what-is-a-c2-framework/"
        ]
        
        # Contador de datasets procesados
        self.processed_datasets = 0
        self.total_pairs_extracted = 0
        
        print("🚀 Extractor Masivo StationX inicializado")
        print(f"🎯 URLs objetivo: {len(self.target_urls)}")
        print("📊 Extracción auténtica + entrenamiento dual por URL")
    
    def extract_and_train_all_urls(self):
        """Extraer contenido de todas las URLs y entrenar individualmente"""
        print(f"🔥 INICIANDO EXTRACCIÓN MASIVA Y ENTRENAMIENTO DUAL")
        print("="*80)
        
        training_results = []
        
        for i, url in enumerate(self.target_urls):
            print(f"\n📝 PROCESANDO URL {i+1}/{len(self.target_urls)}")
            print(f"🔗 {url}")
            print("-" * 60)
            
            # 1. Extraer contenido auténtico
            tool_data = self._extract_tool_data(url)
            
            if not tool_data:
                print(f"⚠️ No se pudo extraer contenido de {url}")
                continue
            
            # 2. Crear dataset individual
            dataset_file = self._create_individual_dataset(tool_data, i)
            
            if not dataset_file:
                print(f"⚠️ No se pudo crear dataset para {url}")
                continue
            
            # 3. Entrenar con doble neurona temporal
            training_result = self._train_with_dual_neurons(dataset_file, tool_data["tool_name"])
            
            if training_result:
                training_results.append(training_result)
                self.processed_datasets += 1
            
            print(f"✅ Herramienta {tool_data['tool_name']} completada")
            
            # Pausa cortés entre extracciones
            time.sleep(2)
        
        # Compilar resultados finales
        final_summary = self._compile_final_summary(training_results)
        
        print(f"\n🎉 EXTRACCIÓN MASIVA Y ENTRENAMIENTO COMPLETADOS")
        print("="*80)
        print(f"📊 Datasets procesados: {self.processed_datasets}")
        print(f"🎯 Total pares extraídos: {self.total_pairs_extracted:,}")
        print(f"🧠 Entrenamientos duales completados: {len(training_results)}")
        
        return final_summary
    
    def _extract_tool_data(self, url):
        """Extraer datos auténticos de una herramienta específica"""
        try:
            print(f"   🔍 Extrayendo contenido auténtico...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Extraer contenido limpio
            content = trafilatura.extract(response.text, include_links=True)
            
            if not content:
                return None
            
            print(f"   ✅ Contenido extraído: {len(content)} caracteres")
            
            # Determinar herramienta y categoría
            tool_name = self._extract_tool_name_from_url(url)
            category = self._categorize_tool(tool_name)
            
            # Extraer comandos y ejemplos
            commands = self._extract_commands_with_translation(content)
            examples = self._extract_code_examples_with_translation(content)
            
            print(f"   📋 Comandos extraídos: {len(commands)}")
            print(f"   💻 Ejemplos extraídos: {len(examples)}")
            
            return {
                "url": url,
                "tool_name": tool_name,
                "category": category,
                "content": content,
                "commands": commands,
                "examples": examples,
                "extracted_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"   ❌ Error extrayendo {url}: {e}")
            return None
    
    def _extract_tool_name_from_url(self, url):
        """Extraer nombre de herramienta desde URL"""
        url_parts = url.split('/')
        
        # Mapeo de URLs a nombres de herramientas
        tool_mapping = {
            'linux-command-line': 'linux',
            'beef-hacking-tool': 'beef',
            'bash-cheat-sheet': 'bash',
            'tmux-cheat-sheet': 'tmux',
            'metasploit': 'metasploit',
            'meterpreter': 'meterpreter',
            'nmap': 'nmap',
            'aircrack-ng': 'aircrack',
            'bettercap': 'bettercap',
            'wireshark': 'wireshark',
            'wifite': 'wifite',
            'powershell-empire': 'empire',
            'c2-framework': 'c2'
        }
        
        for key, tool in tool_mapping.items():
            if key in url:
                return tool
        
        return "herramienta_general"
    
    def _categorize_tool(self, tool_name):
        """Categorizar herramienta de seguridad"""
        categories = {
            'linux': 'sistema_operativo',
            'bash': 'shell_scripting',
            'tmux': 'terminal_multiplexer',
            'beef': 'explotacion_web',
            'metasploit': 'framework_explotacion',
            'meterpreter': 'shell_avanzado',
            'nmap': 'escaneo_red',
            'aircrack': 'seguridad_wifi',
            'bettercap': 'ataques_red',
            'wireshark': 'analisis_trafico',
            'wifite': 'auditoria_wifi',
            'empire': 'post_explotacion',
            'c2': 'comando_control'
        }
        
        return categories.get(tool_name, 'herramienta_seguridad')
    
    def _extract_commands_with_translation(self, content):
        """Extraer comandos traduciendo comentarios al español"""
        commands = []
        
        # Patrones para comandos
        command_patterns = [
            r'`([^`]+)`',
            r'```\s*bash\s*\n(.*?)```',
            r'```\s*shell\s*\n(.*?)```',
            r'\$\s*([^\n]+)',
            r'sudo\s+([^\n]+)',
            r'(nmap[^\n]+)',
            r'(metasploit[^\n]+)',
            r'(msfvenom[^\n]+)',
            r'(aircrack-ng[^\n]+)',
            r'(wireshark[^\n]+)'
        ]
        
        for pattern in command_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                
                clean_command = self._clean_and_validate_command(match)
                if clean_command:
                    # Traducir descripción si existe
                    translated_description = self._translate_description(clean_command)
                    commands.append({
                        "comando": clean_command,
                        "descripcion": translated_description
                    })
        
        return commands
    
    def _extract_code_examples_with_translation(self, content):
        """Extraer ejemplos de código traduciendo explicaciones"""
        examples = []
        
        # Buscar bloques de código con contexto
        code_patterns = [
            r'```(.*?)```',
            r'<pre>(.*?)</pre>',
            r'<code>(.*?)</code>'
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                if len(match.strip()) > 10:
                    translated_explanation = self._generate_spanish_explanation(match)
                    examples.append({
                        "codigo": match.strip(),
                        "explicacion": translated_explanation
                    })
        
        return examples
    
    def _translate_description(self, command):
        """Traducir descripción del comando al español"""
        # Diccionario de traducciones comunes
        translations = {
            "scan": "escanear",
            "network": "red",
            "port": "puerto",
            "vulnerability": "vulnerabilidad",
            "exploit": "explotar",
            "payload": "carga útil",
            "target": "objetivo",
            "host": "host",
            "service": "servicio",
            "attack": "ataque",
            "password": "contraseña",
            "crack": "crackear",
            "capture": "capturar",
            "analyze": "analizar",
            "monitor": "monitorear"
        }
        
        # Generar descripción en español basada en el comando
        if "nmap" in command.lower():
            return "Comando de escaneo de red con nmap"
        elif "metasploit" in command.lower():
            return "Comando del framework Metasploit"
        elif "aircrack" in command.lower():
            return "Comando para auditoría de redes WiFi"
        elif "wireshark" in command.lower():
            return "Comando para análisis de tráfico de red"
        else:
            return "Comando de herramienta de seguridad"
    
    def _generate_spanish_explanation(self, code):
        """Generar explicación en español para código"""
        if "#!/bin/bash" in code:
            return "Script de shell bash para automatización"
        elif "import" in code:
            return "Script de Python con importación de módulos"
        elif "function" in code or "def " in code:
            return "Definición de función para procesamiento"
        else:
            return "Ejemplo de código ejecutable con parámetros específicos"
    
    def _clean_and_validate_command(self, command):
        """Limpiar y validar comando"""
        # Remover caracteres problemáticos pero mantener funcionalidad
        command = command.strip()
        
        # Validar que sea un comando útil
        if len(command) < 3:
            return None
        
        # Palabras clave que indican comandos válidos
        valid_keywords = [
            'nmap', 'metasploit', 'msfvenom', 'aircrack-ng', 'wireshark',
            'bash', 'tmux', 'sudo', 'ls', 'cd', 'grep', 'cat', 'ps'
        ]
        
        if any(keyword in command.lower() for keyword in valid_keywords):
            return command
        
        return None
    
    def _create_individual_dataset(self, tool_data, index):
        """Crear dataset individual para una herramienta"""
        tool_name = tool_data["tool_name"]
        dataset_file = self.output_dir / f"{tool_name}_dataset.jsonl"
        
        print(f"   💾 Creando dataset: {dataset_file}")
        
        pairs = []
        pair_count = 0
        
        # Crear pares desde comandos
        for cmd_data in tool_data["commands"]:
            pair = self._create_spanish_pair(
                tool_name=tool_name,
                command=cmd_data["comando"],
                description=cmd_data["descripcion"],
                category=tool_data["category"],
                index=pair_count,
                url=tool_data["url"]
            )
            pairs.append(pair)
            pair_count += 1
        
        # Crear pares desde ejemplos
        for example_data in tool_data["examples"]:
            pair = self._create_example_spanish_pair(
                tool_name=tool_name,
                code=example_data["codigo"],
                explanation=example_data["explicacion"],
                category=tool_data["category"],
                index=pair_count,
                url=tool_data["url"]
            )
            pairs.append(pair)
            pair_count += 1
        
        # Guardar dataset
        with open(dataset_file, 'w', encoding='utf-8') as f:
            for pair in pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + '\n')
        
        self.total_pairs_extracted += len(pairs)
        
        print(f"   ✅ Dataset creado: {len(pairs)} pares")
        
        return dataset_file
    
    def _create_spanish_pair(self, tool_name, command, description, category, index, url):
        """Crear par semántica-binarizado en español"""
        # Entrada semántica en español
        semantic_input = f"Usar {tool_name} para {description}"
        
        # Tokenización
        semantic_tokens = self._tokenize_spanish(semantic_input)
        command_tokens = self._tokenize_command(command)
        
        # Binarización int8
        semantic_binary = self._binarize_int8(semantic_tokens)
        command_binary = self._binarize_int8(command_tokens)
        
        # Hash único
        pair_hash = hashlib.md5(f"{tool_name}{command}".encode()).hexdigest()[:16]
        
        return {
            "id": f"{tool_name}_{index:04d}",
            "hash": pair_hash,
            "herramienta": tool_name,
            "categoria": category,
            "entrada_semantica": {
                "texto": semantic_input,
                "tokens": semantic_tokens,
                "binario_int8": semantic_binary,
                "cantidad_tokens": len(semantic_tokens)
            },
            "salida_comando": {
                "texto": command,
                "tokens": command_tokens,
                "binario_int8": command_binary,
                "cantidad_tokens": len(command_tokens),
                "ejecutable": True,
                "plataforma": "linux"
            },
            "descripcion": description,
            "metadatos": {
                "url_fuente": url,
                "extraido_en": datetime.now().isoformat(),
                "autentico": True,
                "puntuacion_complejidad": self._calculate_complexity(command),
                "idioma": "español_comandos_ingles"
            }
        }
    
    def _create_example_spanish_pair(self, tool_name, code, explanation, category, index, url):
        """Crear par de ejemplo en español"""
        semantic_input = f"Ejemplo de {tool_name}: {explanation}"
        
        semantic_tokens = self._tokenize_spanish(semantic_input)
        code_tokens = self._tokenize_command(code)
        
        semantic_binary = self._binarize_int8(semantic_tokens)
        code_binary = self._binarize_int8(code_tokens)
        
        pair_hash = hashlib.md5(f"{tool_name}_ejemplo_{code}".encode()).hexdigest()[:16]
        
        return {
            "id": f"{tool_name}_ejemplo_{index:04d}",
            "hash": pair_hash,
            "herramienta": tool_name,
            "categoria": f"{category}_ejemplo",
            "entrada_semantica": {
                "texto": semantic_input,
                "tokens": semantic_tokens,
                "binario_int8": semantic_binary,
                "cantidad_tokens": len(semantic_tokens)
            },
            "salida_codigo": {
                "texto": code,
                "tokens": code_tokens,
                "binario_int8": code_binary,
                "cantidad_tokens": len(code_tokens),
                "ejecutable": True,
                "tipo": "ejemplo_codigo"
            },
            "explicacion": explanation,
            "metadatos": {
                "url_fuente": url,
                "extraido_en": datetime.now().isoformat(),
                "autentico": True,
                "tipo_ejemplo": "tutorial_codigo"
            }
        }
    
    def _tokenize_spanish(self, text):
        """Tokenizar texto en español"""
        import re
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())
        return tokens
    
    def _tokenize_command(self, command):
        """Tokenizar comando preservando estructura"""
        import re
        tokens = re.findall(r'\w+|[^\w\s]', command)
        return tokens
    
    def _binarize_int8(self, tokens):
        """Convertir tokens a representación binaria int8"""
        binary_repr = []
        for token in tokens:
            token_hash = hash(token) % 256
            if token_hash > 127:
                token_hash = token_hash - 256
            binary_repr.append(token_hash)
        return binary_repr
    
    def _calculate_complexity(self, command):
        """Calcular complejidad del comando"""
        complexity = len(command.split()) * 3
        complexity += command.count('|') * 5
        complexity += command.count('&&') * 4
        complexity += command.count(';') * 3
        
        # Herramientas complejas
        complex_tools = ['nmap', 'metasploit', 'msfvenom', 'aircrack-ng']
        for tool in complex_tools:
            if tool in command.lower():
                complexity += 15
        
        return min(complexity, 100)
    
    def _train_with_dual_neurons(self, dataset_file, tool_name):
        """Entrenar con sistema de doble neurona temporal"""
        try:
            print(f"   🧠 Iniciando entrenamiento dual para {tool_name}...")
            
            # Crear instancia del sistema de entrenamiento dual
            trainer = DualTemporalTrainingSystem(str(dataset_file))
            
            # Ejecutar entrenamiento
            results, insights = trainer.execute_dual_temporal_training()
            
            print(f"   ✅ Entrenamiento dual completado")
            print(f"      🧠 Metacognición: {insights['metacognitive_efficiency']:.3f}")
            print(f"      👁️ Visión/Patrones: {insights['vision_efficiency']:.3f}")
            print(f"      🔗 Sinergia: {insights['dual_synergy']:.3f}")
            
            return {
                "tool_name": tool_name,
                "dataset_file": str(dataset_file),
                "training_results": results,
                "dual_insights": insights
            }
            
        except Exception as e:
            print(f"   ❌ Error en entrenamiento dual: {e}")
            return None
    
    def _compile_final_summary(self, training_results):
        """Compilar resumen final de todos los entrenamientos"""
        summary = {
            "procesamiento_masivo": {
                "urls_procesadas": len(self.target_urls),
                "datasets_creados": self.processed_datasets,
                "total_pares_extraidos": self.total_pairs_extracted,
                "entrenamientos_duales": len(training_results)
            },
            "resultados_entrenamiento": training_results,
            "metricas_promedio": self._calculate_average_metrics(training_results),
            "completado_en": datetime.now().isoformat()
        }
        
        # Guardar resumen
        summary_file = self.output_dir / "resumen_masivo_stationx.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return summary
    
    def _calculate_average_metrics(self, training_results):
        """Calcular métricas promedio"""
        if not training_results:
            return {}
        
        avg_metacognitive = sum(r["dual_insights"]["metacognitive_efficiency"] 
                               for r in training_results) / len(training_results)
        avg_vision = sum(r["dual_insights"]["vision_efficiency"] 
                        for r in training_results) / len(training_results)
        avg_synergy = sum(r["dual_insights"]["dual_synergy"] 
                         for r in training_results) / len(training_results)
        
        return {
            "eficiencia_metacognitiva_promedio": avg_metacognitive,
            "eficiencia_vision_promedio": avg_vision,
            "sinergia_dual_promedio": avg_synergy
        }

def main():
    """Función principal de extracción masiva"""
    extractor = StationXMassiveExtractor()
    
    print("🚀 Iniciando extracción masiva y entrenamiento dual StationX")
    summary = extractor.extract_and_train_all_urls()
    
    print(f"\n🎉 Procesamiento masivo completado")
    print(f"📊 Datasets: {summary['procesamiento_masivo']['datasets_creados']}")
    print(f"🧠 Entrenamientos duales: {summary['procesamiento_masivo']['entrenamientos_duales']}")

if __name__ == "__main__":
    main()