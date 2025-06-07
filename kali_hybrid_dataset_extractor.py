#!/usr/bin/env python3
"""
Extractor de Dataset Híbrido Kali Linux - StationX
Extrae contenido auténtico completo con comandos reales, imágenes y ejemplos ejecutables
"""

import json
import time
import requests
import hashlib
from pathlib import Path
from datetime import datetime
import trafilatura
from urllib.parse import urljoin, urlparse
import re

class KaliHybridDatasetExtractor:
    """Extractor de dataset híbrido auténtico de Kali Linux desde StationX"""
    
    def __init__(self, base_url="https://www.stationx.net/kali-linux-tutorial/"):
        self.base_url = base_url
        self.output_dir = Path("datasets/kali_hybrid_authentic")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Directorio para imágenes extraídas
        self.images_dir = self.output_dir / "tool_images" 
        self.images_dir.mkdir(exist_ok=True)
        
        # Configuración de extracción
        self.extracted_pages = set()
        self.tool_links = []
        self.authentic_pairs = []
        
        print("🚀 Extractor de Dataset Híbrido Kali Linux inicializado")
        print(f"🎯 URL base: {self.base_url}")
        print("📊 Extrayendo contenido auténtico con imágenes y comandos reales")
    
    def extract_complete_kali_dataset(self):
        """Extraer dataset completo de Kali Linux desde StationX"""
        print(f"🔍 INICIANDO EXTRACCIÓN COMPLETA DE KALI LINUX")
        print("="*70)
        
        start_time = time.time()
        
        # 1. Extraer página principal
        print("📄 Extrayendo página principal...")
        main_content = self._extract_page_content(self.base_url)
        
        if not main_content:
            print("❌ No se pudo extraer la página principal")
            return None
        
        # 2. Encontrar enlaces a herramientas específicas
        print("🔗 Buscando enlaces a herramientas de Kali...")
        tool_links = self._find_tool_links(main_content, self.base_url)
        
        print(f"✅ Encontrados {len(tool_links)} enlaces a herramientas")
        
        # 3. Extraer contenido de cada herramienta
        total_pairs = 0
        
        for i, tool_link in enumerate(tool_links):
            print(f"\n📝 Extrayendo herramienta {i+1}/{len(tool_links)}: {tool_link}")
            
            tool_pairs = self._extract_tool_content(tool_link)
            total_pairs += len(tool_pairs)
            
            print(f"   ✅ {len(tool_pairs)} pares extraídos")
            
            # Pausa cortés entre requests
            time.sleep(1)
        
        # 4. Agregar contenido de la página principal
        main_pairs = self._process_main_content(main_content)
        total_pairs += len(main_pairs)
        
        # 5. Generar dataset final
        dataset_file = self._generate_final_dataset()
        
        elapsed = time.time() - start_time
        
        print(f"\n🎉 EXTRACCIÓN COMPLETA FINALIZADA")
        print(f"📊 Total pares extraídos: {total_pairs:,}")
        print(f"⏱️ Tiempo: {elapsed:.1f}s")
        print(f"💾 Dataset: {dataset_file}")
        
        return dataset_file, total_pairs
    
    def _extract_page_content(self, url):
        """Extraer contenido auténtico de una página"""
        try:
            print(f"   🔍 Descargando: {url}")
            
            # Headers para simular navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Extraer contenido limpio con trafilatura
            content = trafilatura.extract(response.text, include_images=True, include_links=True)
            
            if content:
                print(f"   ✅ Contenido extraído: {len(content)} caracteres")
                return {
                    'url': url,
                    'content': content,
                    'html': response.text,
                    'extracted_at': datetime.now().isoformat()
                }
            else:
                print(f"   ⚠️ No se pudo extraer contenido de {url}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error extrayendo {url}: {e}")
            return None
    
    def _find_tool_links(self, content_data, base_url):
        """Encontrar enlaces a herramientas específicas de Kali"""
        tool_links = []
        
        if not content_data or 'html' not in content_data:
            return tool_links
        
        html = content_data['html']
        
        # Patrones para encontrar enlaces a herramientas
        tool_patterns = [
            r'href="([^"]*kali[^"]*)"',
            r'href="([^"]*tool[^"]*)"', 
            r'href="([^"]*nmap[^"]*)"',
            r'href="([^"]*metasploit[^"]*)"',
            r'href="([^"]*burp[^"]*)"',
            r'href="([^"]*wireshark[^"]*)"',
            r'href="([^"]*aircrack[^"]*)"',
            r'href="([^"]*john[^"]*)"',
            r'href="([^"]*hydra[^"]*)"',
            r'href="([^"]*sqlmap[^"]*)"'
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                full_url = urljoin(base_url, match)
                if self._is_valid_tool_url(full_url):
                    tool_links.append(full_url)
        
        # Eliminar duplicados y ordenar
        tool_links = list(set(tool_links))
        
        return tool_links[:20]  # Limitar para demo
    
    def _is_valid_tool_url(self, url):
        """Verificar si URL es válida para herramienta"""
        # Filtrar URLs no deseadas
        excluded = ['javascript:', 'mailto:', '#', 'facebook.com', 'twitter.com']
        
        for exclude in excluded:
            if exclude in url.lower():
                return False
        
        # Debe ser del mismo dominio o subdirectorio
        parsed = urlparse(url)
        return 'stationx.net' in parsed.netloc or url.startswith('/')
    
    def _extract_tool_content(self, tool_url):
        """Extraer contenido específico de una herramienta"""
        tool_pairs = []
        
        # Extraer contenido de la página
        content_data = self._extract_page_content(tool_url)
        
        if not content_data:
            return tool_pairs
        
        content = content_data['content']
        
        # Extraer comandos y ejemplos
        commands = self._extract_commands(content)
        examples = self._extract_code_examples(content)
        images = self._extract_images(content_data['html'], tool_url)
        
        # Determinar nombre de la herramienta
        tool_name = self._extract_tool_name(content, tool_url)
        
        # Crear pares semántica-binarizados
        for i, command in enumerate(commands):
            pair = self._create_kali_pair(
                tool_name=tool_name,
                command=command,
                content=content,
                images=images,
                index=i,
                url=tool_url
            )
            tool_pairs.append(pair)
        
        # Agregar ejemplos adicionales
        for i, example in enumerate(examples):
            pair = self._create_example_pair(
                tool_name=tool_name,
                example=example,
                content=content,
                index=len(commands) + i,
                url=tool_url
            )
            tool_pairs.append(pair)
        
        return tool_pairs
    
    def _extract_commands(self, content):
        """Extraer comandos auténticos del contenido"""
        commands = []
        
        # Patrones para comandos de Kali Linux
        command_patterns = [
            r'`([^`]+)`',  # Comandos en backticks
            r'```\s*bash\s*\n(.*?)```',  # Bloques de código bash
            r'```\s*shell\s*\n(.*?)```',  # Bloques shell
            r'\$\s*([^\n]+)',  # Comandos con $
            r'#\s*([^\n]+)',  # Comandos con #
            r'sudo\s+([^\n]+)',  # Comandos sudo
            r'(nmap[^\n]+)',  # Comandos nmap específicos
            r'(metasploit[^\n]+)',  # Comandos metasploit
            r'(aircrack-ng[^\n]+)',  # Comandos aircrack
        ]
        
        for pattern in command_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                
                # Limpiar y validar comando
                clean_command = self._clean_command(match)
                if self._is_valid_command(clean_command):
                    commands.append(clean_command)
        
        return list(set(commands))  # Eliminar duplicados
    
    def _extract_code_examples(self, content):
        """Extraer ejemplos de código del contenido"""
        examples = []
        
        # Buscar bloques de código
        code_patterns = [
            r'```(.*?)```',
            r'<code>(.*?)</code>',
            r'<pre>(.*?)</pre>'
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                if len(match.strip()) > 10:  # Solo ejemplos sustanciales
                    examples.append(match.strip())
        
        return examples
    
    def _extract_images(self, html, base_url):
        """Extraer información de imágenes relevantes"""
        images = []
        
        # Encontrar imágenes en el HTML
        img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
        matches = re.findall(img_pattern, html)
        
        for img_src in matches:
            full_img_url = urljoin(base_url, img_src)
            
            # Metadata de la imagen
            img_info = {
                'url': full_img_url,
                'alt': self._extract_img_alt(html, img_src),
                'context': 'kali_tool_screenshot',
                'extracted_at': datetime.now().isoformat()
            }
            
            images.append(img_info)
        
        return images[:5]  # Limitar imágenes por herramienta
    
    def _extract_img_alt(self, html, img_src):
        """Extraer texto alt de imagen"""
        pattern = rf'<img[^>]+src="{re.escape(img_src)}"[^>]+alt="([^"]*)"'
        match = re.search(pattern, html)
        return match.group(1) if match else "Kali Linux tool screenshot"
    
    def _extract_tool_name(self, content, url):
        """Extraer nombre de la herramienta"""
        # Buscar en el contenido
        tool_names = ['nmap', 'metasploit', 'burp', 'wireshark', 'aircrack', 
                     'john', 'hydra', 'sqlmap', 'nikto', 'dirb', 'gobuster']
        
        content_lower = content.lower()
        for tool in tool_names:
            if tool in content_lower:
                return tool
        
        # Extraer del URL
        url_parts = url.split('/')
        for part in url_parts:
            if any(tool in part.lower() for tool in tool_names):
                return part.replace('-', '_')
        
        return "kali_tool"
    
    def _clean_command(self, command):
        """Limpiar comando extraído"""
        # Remover caracteres no deseados
        command = re.sub(r'[^\w\s\-\.\:/=\$]+', '', command)
        return command.strip()
    
    def _is_valid_command(self, command):
        """Validar si es un comando útil"""
        if len(command) < 3:
            return False
        
        # Palabras clave que indican comandos válidos
        valid_keywords = ['sudo', 'apt', 'nmap', 'metasploit', 'aircrack', 
                         'john', 'hydra', 'sqlmap', 'cd', 'ls', 'cat', 'grep']
        
        return any(keyword in command.lower() for keyword in valid_keywords)
    
    def _create_kali_pair(self, tool_name, command, content, images, index, url):
        """Crear par híbrido semántica-binarizado para Kali"""
        
        # Descripción semántica del comando
        semantic_input = f"Usar {tool_name} para ejecutar: {command}"
        
        # Tokenización semántica y binarización
        semantic_tokens = self._tokenize_semantic(semantic_input)
        command_tokens = self._tokenize_command(command)
        
        semantic_binary = self._binarize_int8(semantic_tokens)
        command_binary = self._binarize_int8(command_tokens)
        
        # Hash único
        pair_hash = hashlib.md5(f"{tool_name}{command}".encode()).hexdigest()[:16]
        
        return {
            "id": f"kali_{tool_name}_{index:04d}",
            "hash": pair_hash,
            "tool_name": tool_name,
            "category": "kali_security_tool",
            "semantic_input": {
                "raw": semantic_input,
                "tokens": semantic_tokens,
                "binary_int8": semantic_binary,
                "token_count": len(semantic_tokens)
            },
            "command_output": {
                "raw": command,
                "tokens": command_tokens,
                "binary_int8": command_binary,
                "token_count": len(command_tokens),
                "executable": True,
                "platform": "kali_linux"
            },
            "visual_context": {
                "images": images,
                "image_count": len(images),
                "ocr_training_data": True
            },
            "metadata": {
                "source_url": url,
                "extracted_at": datetime.now().isoformat(),
                "authentic": True,
                "complexity_score": self._calculate_command_complexity(command),
                "security_category": self._categorize_security_tool(tool_name)
            }
        }
    
    def _create_example_pair(self, tool_name, example, content, index, url):
        """Crear par para ejemplo de código"""
        semantic_input = f"Ejemplo de uso de {tool_name}: {example[:100]}..."
        
        semantic_tokens = self._tokenize_semantic(semantic_input)
        example_tokens = self._tokenize_command(example)
        
        semantic_binary = self._binarize_int8(semantic_tokens)
        example_binary = self._binarize_int8(example_tokens)
        
        pair_hash = hashlib.md5(f"{tool_name}_example_{example}".encode()).hexdigest()[:16]
        
        return {
            "id": f"kali_example_{tool_name}_{index:04d}",
            "hash": pair_hash,
            "tool_name": tool_name,
            "category": "kali_example",
            "semantic_input": {
                "raw": semantic_input,
                "tokens": semantic_tokens,
                "binary_int8": semantic_binary,
                "token_count": len(semantic_tokens)
            },
            "code_output": {
                "raw": example,
                "tokens": example_tokens,
                "binary_int8": example_binary,
                "token_count": len(example_tokens),
                "executable": True,
                "type": "code_example"
            },
            "metadata": {
                "source_url": url,
                "extracted_at": datetime.now().isoformat(),
                "authentic": True,
                "example_type": "tutorial_code"
            }
        }
    
    def _tokenize_semantic(self, text):
        """Tokenizar texto semántico"""
        import re
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())
        return tokens
    
    def _tokenize_command(self, command):
        """Tokenizar comando de shell"""
        # Separar por espacios y caracteres especiales
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
    
    def _calculate_command_complexity(self, command):
        """Calcular complejidad del comando"""
        complexity = 0
        complexity += len(command.split()) * 2
        complexity += command.count('|') * 5
        complexity += command.count('&&') * 3
        complexity += command.count(';') * 2
        
        # Comandos complejos
        complex_tools = ['nmap', 'metasploit', 'sqlmap']
        for tool in complex_tools:
            if tool in command.lower():
                complexity += 10
        
        return min(complexity, 100)
    
    def _categorize_security_tool(self, tool_name):
        """Categorizar herramienta de seguridad"""
        categories = {
            'nmap': 'network_scanner',
            'metasploit': 'exploitation_framework',
            'burp': 'web_application_security',
            'wireshark': 'network_analysis',
            'aircrack': 'wireless_security',
            'john': 'password_cracking',
            'hydra': 'brute_force',
            'sqlmap': 'sql_injection'
        }
        
        return categories.get(tool_name, 'general_security')
    
    def _process_main_content(self, content_data):
        """Procesar contenido de la página principal"""
        pairs = []
        
        if not content_data:
            return pairs
        
        content = content_data['content']
        
        # Extraer comandos generales
        commands = self._extract_commands(content)
        
        for i, command in enumerate(commands):
            pair = self._create_kali_pair(
                tool_name="kali_general",
                command=command,
                content=content,
                images=[],
                index=i,
                url=content_data['url']
            )
            pairs.append(pair)
        
        return pairs
    
    def _generate_final_dataset(self):
        """Generar dataset final en formato JSONL"""
        dataset_file = self.output_dir / "kali_hybrid_authentic.jsonl"
        
        print(f"💾 Generando dataset final: {dataset_file}")
        
        with open(dataset_file, 'w', encoding='utf-8') as f:
            for pair in self.authentic_pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + '\n')
        
        # Generar metadatos
        metadata = {
            "dataset_info": {
                "name": "Kali Linux Hybrid Authentic Dataset",
                "source": "StationX.net Kali Tutorial",
                "extracted_at": datetime.now().isoformat(),
                "total_pairs": len(self.authentic_pairs),
                "authentic_content": True,
                "images_included": True,
                "ocr_training_ready": True
            },
            "extraction_summary": {
                "pages_processed": len(self.extracted_pages),
                "tools_covered": len(set(p.get('tool_name', '') for p in self.authentic_pairs)),
                "commands_extracted": sum(1 for p in self.authentic_pairs if 'command_output' in p),
                "examples_extracted": sum(1 for p in self.authentic_pairs if 'code_output' in p)
            }
        }
        
        metadata_file = self.output_dir / "extraction_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return dataset_file

def main():
    """Función principal de extracción"""
    extractor = KaliHybridDatasetExtractor()
    
    print("🚀 Iniciando extracción de dataset híbrido Kali Linux auténtico")
    dataset_file, total_pairs = extractor.extract_complete_kali_dataset()
    
    if dataset_file:
        print(f"\n✅ Dataset híbrido generado exitosamente")
        print(f"📁 Archivo: {dataset_file}")
        print(f"📊 Pares extraídos: {total_pairs:,}")

if __name__ == "__main__":
    main()