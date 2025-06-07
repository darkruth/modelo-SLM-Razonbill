#!/usr/bin/env python3
"""
Dataset Híbrido Int8 Semántico-Binarizado para Pwnagotchi AI
Especializado en vulnerabilidades WiFi y captura de paquetes
"""

import json
import random
from pathlib import Path
from datetime import datetime

class PwnagotchiHybridDataset:
    """Generador de dataset híbrido int8 para entrenamiento de Pwnagotchi AI"""
    
    def __init__(self):
        self.output_dir = Path("datasets/pwnagotchi_hybrid")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Vocabulario especializado WiFi
        self.wifi_vocabulary = {
            # Comandos principales
            "airodump": 1, "aircrack": 2, "aireplay": 3, "airmon": 4,
            "wireshark": 5, "tcpdump": 6, "iwconfig": 7, "iwlist": 8,
            
            # Términos técnicos WiFi
            "handshake": 10, "wpa": 11, "wep": 12, "wps": 13, "ssid": 14,
            "bssid": 15, "channel": 16, "beacon": 17, "deauth": 18,
            "monitor": 19, "injection": 20, "capture": 21, "crack": 22,
            
            # Vulnerabilidades
            "bruteforce": 30, "dictionary": 31, "wordlist": 32, "rainbow": 33,
            "vulnerability": 34, "exploit": 35, "attack": 36, "penetration": 37,
            
            # Protocolos y encriptación
            "802.11": 40, "wpa2": 41, "wpa3": 42, "tkip": 43, "aes": 44,
            "ccmp": 45, "eapol": 46, "pmkid": 47, "psk": 48,
            
            # Hardware y interfaces
            "wlan": 50, "interface": 51, "adapter": 52, "antenna": 53,
            "frequency": 54, "power": 55, "signal": 56, "noise": 57,
            
            # Acciones específicas
            "scan": 60, "monitor": 61, "inject": 62, "decrypt": 63,
            "analyze": 64, "filter": 65, "export": 66, "import": 67
        }
        
        # Comandos auténticos extraídos de documentación aircrack-ng
        self.authentic_commands = self._load_authentic_commands()
        
        print("🔧 Dataset Híbrido Pwnagotchi inicializado")
        print(f"📚 Vocabulario WiFi: {len(self.wifi_vocabulary)} términos")
        print(f"⚡ Comandos auténticos: {len(self.authentic_commands)}")
    
    def _load_authentic_commands(self):
        """Cargar comandos auténticos de herramientas WiFi"""
        return {
            "scan_basic": {
                "command": "airodump-ng wlan0",
                "description": "Escaneo básico de redes inalámbricas",
                "output_pattern": "BSSID.*ESSID.*Encryption",
                "vulnerabilities": ["open_networks", "weak_encryption"]
            },
            "scan_targeted": {
                "command": "airodump-ng -c {channel} --bssid {bssid} -w {output} wlan0",
                "description": "Escaneo dirigido para captura de handshake",
                "output_pattern": "WPA handshake.*captured",
                "vulnerabilities": ["wpa_handshake_capture"]
            },
            "monitor_mode": {
                "command": "airmon-ng start wlan0",
                "description": "Activar modo monitor en interfaz inalámbrica",
                "output_pattern": "monitor mode.*enabled",
                "vulnerabilities": ["interface_monitoring"]
            },
            "deauth_attack": {
                "command": "aireplay-ng -0 {count} -a {bssid} -c {client} wlan0",
                "description": "Ataque de deautenticación para forzar reconexión",
                "output_pattern": "Sending.*DeAuth.*ACKs",
                "vulnerabilities": ["forced_disconnection", "handshake_capture"]
            },
            "wpa_crack": {
                "command": "aircrack-ng -w {wordlist} {capture_file}",
                "description": "Cracking de contraseña WPA usando diccionario",
                "output_pattern": "KEY FOUND.*password",
                "vulnerabilities": ["weak_passwords", "dictionary_attack"]
            },
            "wep_crack": {
                "command": "aircrack-ng {capture_file}",
                "description": "Cracking de red WEP mediante análisis estadístico",
                "output_pattern": "KEY FOUND.*WEP",
                "vulnerabilities": ["wep_weakness", "statistical_attack"]
            },
            "packet_capture": {
                "command": "tcpdump -i wlan0 -w {output_file} -s 0",
                "description": "Captura completa de paquetes de red",
                "output_pattern": "packets captured.*packets received",
                "vulnerabilities": ["traffic_analysis", "data_leakage"]
            },
            "injection_test": {
                "command": "aireplay-ng -9 -e {ssid} -a {bssid} wlan0",
                "description": "Prueba de inyección de paquetes",
                "output_pattern": "Injection is working",
                "vulnerabilities": ["packet_injection"]
            },
            "pmkid_attack": {
                "command": "hcxdumptool -i wlan0 -o {output} --enable_status=1",
                "description": "Captura de PMKID para ataque sin handshake",
                "output_pattern": "PMKID.*found",
                "vulnerabilities": ["pmkid_attack", "wpa3_downgrade"]
            },
            "wireless_survey": {
                "command": "iwlist wlan0 scan | grep -E '(ESSID|Encryption|Signal)'",
                "description": "Survey completo de redes inalámbricas del área",
                "output_pattern": "ESSID.*Encryption key.*Signal level",
                "vulnerabilities": ["network_enumeration", "signal_analysis"]
            }
        }
    
    def generate_hybrid_dataset(self, pairs_count=5000):
        """Generar dataset híbrido int8 con pares semántico-binarizados"""
        print(f"\n🔥 GENERANDO DATASET HÍBRIDO PWNAGOTCHI")
        print("="*50)
        
        dataset_pairs = []
        
        for i in range(pairs_count):
            # Seleccionar comando base
            command_key = random.choice(list(self.authentic_commands.keys()))
            command_data = self.authentic_commands[command_key]
            
            # Generar solicitud en español natural
            natural_request = self._generate_natural_request(command_key, command_data)
            
            # Tokenizar entrada
            input_tokens = self._tokenize_input(natural_request)
            input_semantic = self._semantic_encoding(natural_request)
            input_binary_int8 = self._binary_int8_encoding(input_tokens)
            
            # Generar salida estructurada
            output_command = self._generate_parameterized_command(command_data)
            output_explanation = self._generate_technical_explanation(command_data)
            output_tokens = self._tokenize_output(output_command)
            output_binary_int8 = self._binary_int8_encoding(output_tokens)
            
            # Análisis de vulnerabilidades
            vulnerability_analysis = self._analyze_vulnerabilities(command_data)
            
            # Crear par híbrido
            pair = {
                # Entrada híbrida
                "input_raw": natural_request,
                "input_tokens": input_tokens,
                "input_semantic_type": self._classify_request_type(natural_request),
                "input_intent": self._extract_intent(natural_request),
                "input_binary_int8": input_binary_int8,
                
                # Salida híbrida
                "output_command": output_command,
                "output_explanation": output_explanation,
                "output_tokens": output_tokens,
                "output_binary_int8": output_binary_int8,
                
                # Metadatos especializados
                "wifi_category": command_key,
                "vulnerability_class": vulnerability_analysis["class"],
                "security_level": vulnerability_analysis["level"],
                "tool_complexity": self._calculate_complexity(command_data),
                "expected_success_rate": vulnerability_analysis["success_rate"],
                
                # Fuzzy matching para núcleo
                "fuzzy_mapping": {
                    "semantic_similarity": self._calculate_semantic_similarity(natural_request, output_command),
                    "command_confidence": self._calculate_command_confidence(command_data),
                    "context_relevance": self._calculate_context_relevance(natural_request)
                },
                
                # Timestamp
                "created_at": datetime.now().isoformat()
            }
            
            dataset_pairs.append(pair)
            
            if (i + 1) % 500 == 0:
                print(f"   ✅ Generados {i + 1}/{pairs_count} pares híbridos")
        
        # Guardar dataset
        dataset_file = self.output_dir / f"pwnagotchi_hybrid_dataset_{int(datetime.now().timestamp())}.jsonl"
        
        with open(dataset_file, 'w', encoding='utf-8') as f:
            for pair in dataset_pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + '\n')
        
        # Generar estadísticas
        stats = self._generate_dataset_statistics(dataset_pairs)
        
        print(f"\n🎉 DATASET HÍBRIDO COMPLETADO")
        print(f"   📁 Archivo: {dataset_file}")
        print(f"   📊 Pares generados: {len(dataset_pairs)}")
        print(f"   🔧 Comandos únicos: {stats['unique_commands']}")
        print(f"   🎯 Tipos de vulnerabilidades: {stats['vulnerability_types']}")
        
        return dataset_file, stats
    
    def _generate_natural_request(self, command_key, command_data):
        """Generar solicitud natural en español"""
        templates = {
            "scan_basic": [
                "Escanear todas las redes WiFi del área",
                "Buscar redes inalámbricas cercanas",
                "Mostrar todas las redes WiFi disponibles",
                "Detectar access points en la zona"
            ],
            "scan_targeted": [
                "Capturar handshake de la red objetivo",
                "Monitorear red específica para obtener autenticación",
                "Interceptar handshake WPA de {ssid}",
                "Enfocar captura en BSSID {bssid}"
            ],
            "monitor_mode": [
                "Activar modo monitor en la interfaz inalámbrica",
                "Configurar interfaz para monitoreo de paquetes",
                "Habilitar modo promiscuo en wlan0",
                "Preparar interfaz para captura"
            ],
            "deauth_attack": [
                "Desconectar cliente del access point",
                "Realizar ataque de deautenticación",
                "Forzar reconexión del dispositivo {client}",
                "Enviar paquetes deauth a {bssid}"
            ],
            "wpa_crack": [
                "Crackear contraseña WPA de la red capturada",
                "Romper encriptación WPA usando diccionario",
                "Descifrar contraseña de handshake capturado",
                "Ejecutar ataque de diccionario contra WPA"
            ],
            "wep_crack": [
                "Crackear red WEP antigua",
                "Romper encriptación WEP débil",
                "Obtener clave WEP mediante análisis",
                "Explotar vulnerabilidad WEP"
            ],
            "packet_capture": [
                "Capturar todo el tráfico de la red",
                "Monitorear paquetes en tiempo real",
                "Interceptar comunicaciones de red",
                "Analizar tráfico inalámbrico"
            ],
            "injection_test": [
                "Probar inyección de paquetes en la red",
                "Verificar capacidad de inyección",
                "Testear envío de paquetes personalizados",
                "Comprobar vulnerabilidad de inyección"
            ],
            "pmkid_attack": [
                "Capturar PMKID de la red objetivo",
                "Realizar ataque sin handshake",
                "Obtener hash PMKID para cracking",
                "Explotar vulnerabilidad PMKID"
            ],
            "wireless_survey": [
                "Realizar survey completo de redes",
                "Analizar todas las señales inalámbricas",
                "Mapear redes WiFi del entorno",
                "Enumerar access points detectables"
            ]
        }
        
        if command_key in templates:
            template = random.choice(templates[command_key])
            # Reemplazar variables si es necesario
            template = template.replace("{ssid}", "RedWiFi_Casa")
            template = template.replace("{bssid}", "AA:BB:CC:DD:EE:FF")
            template = template.replace("{client}", "FF:EE:DD:CC:BB:AA")
            return template
        else:
            return f"Ejecutar operación {command_key} en red inalámbrica"
    
    def _tokenize_input(self, text):
        """Tokenizar entrada usando vocabulario WiFi"""
        tokens = []
        words = text.lower().split()
        
        for word in words:
            # Buscar en vocabulario especializado
            token = self.wifi_vocabulary.get(word, len(self.wifi_vocabulary) + 1)
            tokens.append(token)
        
        # Padding a longitud fija
        max_length = 20
        if len(tokens) < max_length:
            tokens.extend([0] * (max_length - len(tokens)))
        else:
            tokens = tokens[:max_length]
        
        return tokens
    
    def _semantic_encoding(self, text):
        """Codificación semántica de la entrada"""
        semantic_features = {
            "scan": 1, "attack": 2, "crack": 3, "monitor": 4, "capture": 5
        }
        
        text_lower = text.lower()
        for semantic, value in semantic_features.items():
            if semantic in text_lower:
                return value
        
        return 0  # Desconocido
    
    def _binary_int8_encoding(self, tokens):
        """Codificación binaria int8 de tokens"""
        binary_int8 = []
        
        for token in tokens:
            # Convertir a binario de 8 bits
            binary = format(min(token, 255), '08b')
            # Convertir cada bit a int8
            bits = [int(bit) for bit in binary]
            binary_int8.extend(bits)
        
        return binary_int8
    
    def _generate_parameterized_command(self, command_data):
        """Generar comando parametrizado"""
        command = command_data["command"]
        
        # Reemplazar parámetros con valores realistas
        replacements = {
            "{channel}": str(random.randint(1, 12)),
            "{bssid}": "AA:BB:CC:DD:EE:FF",
            "{output}": "capture",
            "{count}": str(random.randint(5, 20)),
            "{client}": "FF:EE:DD:CC:BB:AA",
            "{wordlist}": "/usr/share/wordlists/rockyou.txt",
            "{capture_file}": "handshake.cap",
            "{output_file}": "packets.pcap",
            "{ssid}": "RedWiFi_Casa"
        }
        
        for param, value in replacements.items():
            command = command.replace(param, value)
        
        return command
    
    def _generate_technical_explanation(self, command_data):
        """Generar explicación técnica del comando"""
        base_description = command_data["description"]
        vulnerabilities = command_data["vulnerabilities"]
        
        explanation = f"{base_description}. "
        explanation += f"Explota vulnerabilidades: {', '.join(vulnerabilities)}. "
        explanation += f"Patrón de salida esperado: {command_data['output_pattern']}"
        
        return explanation
    
    def _tokenize_output(self, command):
        """Tokenizar comando de salida"""
        tokens = []
        words = command.split()
        
        for word in words:
            # Limpiar parámetros
            clean_word = word.strip('"-()[]{}')
            token = self.wifi_vocabulary.get(clean_word, len(self.wifi_vocabulary) + 1)
            tokens.append(token)
        
        return tokens
    
    def _classify_request_type(self, text):
        """Clasificar tipo de solicitud"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["escanear", "buscar", "detectar"]):
            return "reconnaissance"
        elif any(word in text_lower for word in ["atacar", "desconectar", "forzar"]):
            return "attack"
        elif any(word in text_lower for word in ["crackear", "romper", "descifrar"]):
            return "exploitation"
        elif any(word in text_lower for word in ["capturar", "monitorear", "interceptar"]):
            return "monitoring"
        else:
            return "general"
    
    def _extract_intent(self, text):
        """Extraer intención específica"""
        text_lower = text.lower()
        
        if "handshake" in text_lower:
            return "handshake_capture"
        elif "contraseña" in text_lower or "password" in text_lower:
            return "password_crack"
        elif "deauth" in text_lower:
            return "deauth_attack"
        elif "monitor" in text_lower:
            return "monitor_mode"
        else:
            return "network_scan"
    
    def _analyze_vulnerabilities(self, command_data):
        """Analizar vulnerabilidades del comando"""
        vulnerabilities = command_data["vulnerabilities"]
        
        # Clasificar severidad
        high_severity = ["wep_weakness", "pmkid_attack", "weak_passwords"]
        medium_severity = ["handshake_capture", "packet_injection"]
        low_severity = ["network_enumeration", "interface_monitoring"]
        
        severity_level = "low"
        for vuln in vulnerabilities:
            if vuln in high_severity:
                severity_level = "high"
                break
            elif vuln in medium_severity:
                severity_level = "medium"
        
        # Calcular tasa de éxito esperada
        success_rates = {
            "high": 0.9,
            "medium": 0.7,
            "low": 0.5
        }
        
        return {
            "class": vulnerabilities[0] if vulnerabilities else "unknown",
            "level": severity_level,
            "success_rate": success_rates[severity_level]
        }
    
    def _calculate_complexity(self, command_data):
        """Calcular complejidad del comando"""
        command = command_data["command"]
        param_count = command.count("{")
        option_count = command.count("-")
        
        complexity = param_count + option_count
        
        if complexity <= 2:
            return "simple"
        elif complexity <= 5:
            return "moderate"
        else:
            return "complex"
    
    def _calculate_semantic_similarity(self, input_text, output_command):
        """Calcular similitud semántica"""
        input_words = set(input_text.lower().split())
        output_words = set(output_command.lower().split())
        
        intersection = len(input_words.intersection(output_words))
        union = len(input_words.union(output_words))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_command_confidence(self, command_data):
        """Calcular confianza del comando"""
        # Basado en la especificidad del comando
        command = command_data["command"]
        
        if "{" in command:  # Comando parametrizado
            return 0.8
        elif len(command.split()) > 3:  # Comando complejo
            return 0.9
        else:  # Comando simple
            return 0.7
    
    def _calculate_context_relevance(self, text):
        """Calcular relevancia contextual"""
        wifi_terms = ["wifi", "wireless", "red", "network", "wpa", "wep"]
        text_lower = text.lower()
        
        relevance = sum(1 for term in wifi_terms if term in text_lower)
        return min(relevance / len(wifi_terms), 1.0)
    
    def _generate_dataset_statistics(self, dataset_pairs):
        """Generar estadísticas del dataset"""
        unique_commands = len(set(pair["wifi_category"] for pair in dataset_pairs))
        vulnerability_types = len(set(pair["vulnerability_class"] for pair in dataset_pairs))
        
        semantic_types = {}
        for pair in dataset_pairs:
            semantic_type = pair["input_semantic_type"]
            semantic_types[semantic_type] = semantic_types.get(semantic_type, 0) + 1
        
        return {
            "unique_commands": unique_commands,
            "vulnerability_types": vulnerability_types,
            "semantic_distribution": semantic_types,
            "total_pairs": len(dataset_pairs)
        }

def main():
    """Función principal para generar dataset"""
    generator = PwnagotchiHybridDataset()
    
    print("🔧 Generando dataset híbrido especializado para Pwnagotchi AI")
    dataset_file, stats = generator.generate_hybrid_dataset(pairs_count=3000)
    
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   📁 Dataset guardado: {dataset_file}")
    print(f"   🎯 Pares totales: {stats['total_pairs']}")
    print(f"   🔧 Comandos únicos: {stats['unique_commands']}")
    print(f"   🛡️ Tipos de vulnerabilidades: {stats['vulnerability_types']}")
    print(f"   📈 Distribución semántica: {stats['semantic_distribution']}")

if __name__ == "__main__":
    main()