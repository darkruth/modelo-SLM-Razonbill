#!/usr/bin/env python3
"""
Escritorio Blue Theme RazonbilstroOS
Diseño inspirado en LinuxPorn con temática azul
Integración completa con núcleo C.A- Razonbilstro
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class BlueDesktopRazonbilstro:
    """Escritorio con temática azul estilo LinuxPorn"""
    
    def __init__(self):
        self.width = 1600
        self.height = 1000
        
        # Esquema de colores azul inspirado en LinuxPorn
        self.colors = {
            'bg': (13, 17, 23),           # Azul muy oscuro de fondo
            'bg_secondary': (21, 32, 43), # Azul oscuro secundario
            'panel': (30, 41, 59),        # Azul medio para paneles
            'panel_light': (48, 71, 94),  # Azul más claro para destacar
            'accent': (58, 150, 221),     # Azul brillante principal
            'accent_light': (100, 181, 246), # Azul claro para highlights
            'text': (229, 233, 240),      # Texto principal
            'text_secondary': (139, 148, 158), # Texto secundario
            'success': (67, 160, 71),     # Verde para éxito
            'warning': (255, 193, 7),     # Amarillo para advertencias
            'danger': (244, 67, 54),      # Rojo para errores
            'border': (79, 91, 102)       # Bordes sutiles
        }
        
        # Crear imagen base
        self.image = Image.new('RGB', (self.width, self.height), self.colors['bg'])
        self.draw = ImageDraw.Draw(self.image)
        
        # Configurar fuentes
        try:
            self.font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
            self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
        except:
            self.font_title = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
    
    def draw_gradient_background(self):
        """Crear fondo con gradiente azul"""
        # Gradiente vertical suave
        for y in range(self.height):
            # Interpolación de color del gradiente
            ratio = y / self.height
            r = int(self.colors['bg'][0] + (self.colors['bg_secondary'][0] - self.colors['bg'][0]) * ratio)
            g = int(self.colors['bg'][1] + (self.colors['bg_secondary'][1] - self.colors['bg'][1]) * ratio)
            b = int(self.colors['bg'][2] + (self.colors['bg_secondary'][2] - self.colors['bg'][2]) * ratio)
            
            self.draw.line([(0, y), (self.width, y)], fill=(r, g, b))
    
    def draw_modern_top_bar(self):
        """Barra superior moderna estilo tiling WM"""
        # Barra principal
        bar_height = 35
        self.draw.rectangle([0, 0, self.width, bar_height], 
                          fill=self.colors['panel'], outline=self.colors['border'])
        
        # Logo/Icono del sistema (izquierda)
        logo_rect = [10, 5, 40, 30]
        self.draw.rectangle(logo_rect, fill=self.colors['accent'], outline=self.colors['accent_light'])
        self.draw.text((16, 10), "R", fill=self.colors['text'], font=self.font_title)
        
        # Workspaces estilo i3/sway
        workspaces = [
            ("1:term", True), ("2:web", False), ("3:code", False), 
            ("4:files", True), ("5:chat", True), ("6:media", False)
        ]
        
        x_pos = 60
        for workspace, active in workspaces:
            ws_width = 80
            ws_rect = [x_pos, 5, x_pos + ws_width, 30]
            
            if active:
                self.draw.rectangle(ws_rect, fill=self.colors['accent'], outline=self.colors['accent_light'])
                text_color = self.colors['text']
            else:
                self.draw.rectangle(ws_rect, fill=self.colors['bg_secondary'], outline=self.colors['border'])
                text_color = self.colors['text_secondary']
            
            # Centrar texto
            bbox = self.draw.textbbox((0, 0), workspace, font=self.font_small)
            text_width = bbox[2] - bbox[0]
            text_x = x_pos + (ws_width - text_width) // 2
            self.draw.text((text_x, 12), workspace, fill=text_color, font=self.font_small)
            
            x_pos += ws_width + 3
        
        # Información del sistema (centro-derecha)
        current_time = datetime.now().strftime('%H:%M:%S')
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Sistema stats
        system_info = [
            f"🔋 85%", f"🔊 Vol:70%", f"📡 WiFi", f"💻 CPU:15%", 
            f"🧠 RAM:45%", f"📶 eth0", f"🕒 {current_time}"
        ]
        
        x_pos = self.width - 20
        for info in reversed(system_info):
            bbox = self.draw.textbbox((0, 0), info, font=self.font_small)
            text_width = bbox[2] - bbox[0]
            x_pos -= text_width + 15
            self.draw.text((x_pos, 12), info, fill=self.colors['accent_light'], font=self.font_small)
    
    def draw_left_sidebar(self):
        """Sidebar izquierdo con información del sistema"""
        sidebar_width = 320
        sidebar_rect = [10, 45, sidebar_width, self.height - 10]
        
        # Fondo del sidebar con transparencia
        self.draw.rectangle(sidebar_rect, fill=self.colors['panel'], outline=self.colors['border'])
        
        y_pos = 60
        
        # Título del sidebar
        self.draw.text((20, y_pos), "🔹 RazonbilstroOS Control Panel", 
                      fill=self.colors['accent'], font=self.font_title)
        y_pos += 40
        
        # Información del núcleo
        nucleus_info = [
            "🧠 NÚCLEO C.A- RAZONBILSTRO",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "Estado: ✅ Activo y Operativo",
            "Versión: v2.1.0 Enhanced",
            "Precisión: 94.18%",
            "Pares entrenados: 15,000",
            "Neuronas temporales: 2 activas",
            "",
            "🤖 PWNAGOTCHI AI MODULE",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "Nivel: 4 (Experto)",
            "Redes capturadas: 3",
            "Handshakes: 1",
            "Estado: 📡 Escaneando...",
            "",
            "🔧 HERRAMIENTAS INTEGRADAS",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "Total: 27 herramientas",
            "Disponibles: 22/27 (81.5%)",
            "Categorías:",
            "  • Seguridad: 9/11",
            "  • Sistema: 9/12", 
            "  • Desarrollo: 4/4",
            "",
            "📊 SISTEMA OPERATIVO",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "OS: RazonbilstroOS Blue v1.0.0",
            "Kernel: 6.2.16",
            "DE: Blue Theme Desktop",
            "WM: i3-gaps with blue theme",
            "Shell: bash 5.2.37",
            "Terminal: kitty (blue config)"
        ]
        
        for line in nucleus_info:
            if y_pos < self.height - 30:
                if line.startswith("🧠") or line.startswith("🤖") or line.startswith("🔧") or line.startswith("📊"):
                    color = self.colors['accent']
                    font = self.font_medium
                elif line.startswith("━"):
                    color = self.colors['accent_light']
                    font = self.font_small
                elif "✅" in line or "📡" in line:
                    color = self.colors['success']
                    font = self.font_small
                elif line.startswith("  •"):
                    color = self.colors['text_secondary']
                    font = self.font_small
                else:
                    color = self.colors['text']
                    font = self.font_small
                
                self.draw.text((25, y_pos), line, fill=color, font=font)
                y_pos += 18
        
        # Panel de control rápido
        control_y = self.height - 200
        self.draw.rectangle([20, control_y, sidebar_width - 20, self.height - 20], 
                          fill=self.colors['bg_secondary'], outline=self.colors['border'])
        
        self.draw.text((30, control_y + 10), "⚡ Control Rápido", 
                      fill=self.colors['accent'], font=self.font_medium)
        
        # Botones de control
        buttons = [
            ("🔄 Restart Nucleus", self.colors['warning']),
            ("📡 Launch Pwnagotchi", self.colors['accent']),
            ("🔧 System Tools", self.colors['success']),
            ("📊 Performance Monitor", self.colors['accent_light'])
        ]
        
        btn_y = control_y + 35
        for btn_text, btn_color in buttons:
            btn_rect = [30, btn_y, sidebar_width - 30, btn_y + 25]
            self.draw.rectangle(btn_rect, fill=btn_color, outline=self.colors['border'])
            
            bbox = self.draw.textbbox((0, 0), btn_text, font=self.font_small)
            text_width = bbox[2] - bbox[0]
            text_x = 30 + ((sidebar_width - 60 - text_width) // 2)
            self.draw.text((text_x, btn_y + 6), btn_text, fill=self.colors['text'], font=self.font_small)
            
            btn_y += 30
    
    def draw_main_terminal(self):
        """Terminal principal con tema azul"""
        terminal_x = 340
        terminal_width = self.width - terminal_x - 20
        terminal_rect = [terminal_x, 45, self.width - 10, 650]
        
        # Fondo del terminal
        self.draw.rectangle(terminal_rect, fill=self.colors['bg'], outline=self.colors['accent'])
        
        # Barra de título del terminal
        title_rect = [terminal_x, 45, self.width - 10, 75]
        self.draw.rectangle(title_rect, fill=self.colors['panel'], outline=self.colors['border'])
        
        # Título y botones
        self.draw.text((terminal_x + 10, 55), "💻 user@razonbilstro-blue:~$", 
                      fill=self.colors['accent'], font=self.font_medium)
        
        # Botones de ventana (derecha)
        btn_size = 20
        btn_y = 50
        
        # Minimizar
        min_rect = [self.width - 80, btn_y, self.width - 60, btn_y + btn_size]
        self.draw.rectangle(min_rect, fill=self.colors['warning'], outline=self.colors['border'])
        self.draw.text((self.width - 75, btn_y + 5), "−", fill=self.colors['text'], font=self.font_small)
        
        # Maximizar
        max_rect = [self.width - 55, btn_y, self.width - 35, btn_y + btn_size]
        self.draw.rectangle(max_rect, fill=self.colors['success'], outline=self.colors['border'])
        self.draw.text((self.width - 49, btn_y + 5), "□", fill=self.colors['text'], font=self.font_small)
        
        # Cerrar
        close_rect = [self.width - 30, btn_y, self.width - 10, btn_y + btn_size]
        self.draw.rectangle(close_rect, fill=self.colors['danger'], outline=self.colors['border'])
        self.draw.text((self.width - 25, btn_y + 5), "×", fill=self.colors['text'], font=self.font_small)
        
        # Contenido del terminal
        terminal_content = [
            "user@razonbilstro-blue:~$ neofetch",
            "",
            "                    ##        OS: RazonbilstroOS Blue v1.0.0",
            "               ############   Kernel: 6.2.16",
            "            ###############   Uptime: 2 hours, 14 mins",
            "         ##################   Packages: 1847 (apt)",
            "       ####################   Shell: bash 5.2.37",
            "     ######################   Resolution: 1920x1080",
            "   ########################   DE: Blue Theme Desktop",
            " ##########################   WM: i3-gaps",
            "############################   Theme: RazonbilstroBlue",
            " ##########################   Icons: Papirus-Blue",
            "   ########################   Terminal: kitty",
            "     ######################   CPU: AMD EPYC 7B13 (8) @ 3.049GHz",
            "       ####################   GPU: Built-in",
            "         ##################   Memory: 28356MiB / 63391MiB",
            "            ###############",
            "               ############",
            "                    ##",
            "",
            "user@razonbilstro-blue:~$ nucleus --status --verbose",
            "🔵 Initializing RazonbilstroOS Blue Nucleus...",
            "🧠 Neural Core Status: ACTIVE ✅",
            "    ├─ Training Data: 15,000 processed pairs",
            "    ├─ Precision Rate: 94.18%",
            "    ├─ Loss Function: 0.058 (excellent)",
            "    └─ Temporal Neurons: 2/2 active",
            "",
            "🤖 Pwnagotchi AI Module: ONLINE ✅",
            "    ├─ Experience Level: 4 (Expert)",
            "    ├─ Networks Captured: 3",
            "    ├─ Handshakes Collected: 1",
            "    └─ AI State: hunting_mode_active",
            "",
            "🔧 Tool Integration Status:",
            "    ├─ Security Tools: 9/11 (81.8%)",
            "    ├─ System Tools: 9/12 (75.0%)",
            "    ├─ Development Tools: 4/4 (100%)",
            "    └─ Overall Integration: 22/27 (81.5%)",
            "",
            "🎨 Blue Theme Status: ACTIVE ✅",
            "    ├─ Color Scheme: Deep Blue + Accent Blue",
            "    ├─ Window Manager: i3-gaps configured",
            "    ├─ Terminal Theme: Blue variant",
            "    └─ System Icons: Papirus-Blue",
            "",
            "user@razonbilstro-blue:~$ pwn --scan --aggressive",
            "🤖 Pwnagotchi AI: Iniciating aggressive WiFi scan...",
            "📡 Interface: wlan0 (monitor mode enabled)",
            "🔍 Scanning for wireless networks...",
            "",
            "    BSSID              PWR  Beacons  #Data  CH  Encryption  ESSID",
            "    ──────────────────────────────────────────────────────────────",
            "    AA:BB:CC:DD:EE:FF  -42      127      0   6  WPA2        HomeNetwork",
            "    11:22:33:44:55:66  -58       89      0  11  WPA3        Office_WiFi",
            "    99:88:77:66:55:44  -71       45      0   1  WEP         OldRouter",
            "",
            "🎯 3 networks detected, 1 vulnerable (WEP)",
            "🤖 AI Decision: Targeting WEP network for analysis...",
            "",
            "user@razonbilstro-blue:~$ ▌"
        ]
        
        y_pos = 85
        for line in terminal_content:
            if y_pos < 630:
                # Colorear según el contenido
                if line.startswith("user@razonbilstro-blue"):
                    color = self.colors['accent']
                elif line.startswith("🔵") or line.startswith("🧠") or line.startswith("🤖"):
                    color = self.colors['accent_light']
                elif "✅" in line:
                    color = self.colors['success']
                elif line.startswith("    ├─") or line.startswith("    └─"):
                    color = self.colors['text_secondary']
                elif "##" in line:
                    color = self.colors['accent']
                elif line.startswith("    AA:BB") or line.startswith("    11:22") or line.startswith("    99:88"):
                    color = self.colors['warning']
                elif line.startswith("    ──"):
                    color = self.colors['border']
                else:
                    color = self.colors['text']
                
                self.draw.text((terminal_x + 15, y_pos), line, fill=color, font=self.font_small)
                y_pos += 15
    
    def draw_bottom_status_bar(self):
        """Barra de estado inferior con información detallada"""
        status_height = 120
        status_rect = [10, self.height - status_height, self.width - 10, self.height - 10]
        
        # Fondo de la barra
        self.draw.rectangle(status_rect, fill=self.colors['panel'], outline=self.colors['accent'])
        
        # Dividir en secciones
        section_width = (self.width - 40) // 4
        
        # Sección 1: Network Status
        net_x = 20
        self.draw.text((net_x, self.height - 110), "🌐 Network Status", 
                      fill=self.colors['accent'], font=self.font_medium)
        
        net_info = [
            "eth0: 192.168.1.100/24 ✅",
            "wlan0: monitor mode ✅", 
            "DNS: 1.1.1.1, 8.8.8.8",
            "Firewall: active (ufw)"
        ]
        
        net_y = self.height - 90
        for info in net_info:
            self.draw.text((net_x, net_y), info, fill=self.colors['text'], font=self.font_small)
            net_y += 15
        
        # Sección 2: System Resources
        sys_x = 20 + section_width
        self.draw.text((sys_x, self.height - 110), "💻 System Resources", 
                      fill=self.colors['accent'], font=self.font_medium)
        
        sys_info = [
            "CPU: 15% (8 cores)",
            "RAM: 28.3GB / 63.4GB",
            "Disk: 23GB / 50GB used",
            "Temp: 45°C (normal)"
        ]
        
        sys_y = self.height - 90
        for info in sys_info:
            self.draw.text((sys_x, sys_y), info, fill=self.colors['text'], font=self.font_small)
            sys_y += 15
        
        # Sección 3: Security Status
        sec_x = 20 + section_width * 2
        self.draw.text((sec_x, self.height - 110), "🔒 Security Status", 
                      fill=self.colors['accent'], font=self.font_medium)
        
        sec_info = [
            "Firewall: active ✅",
            "AV: real-time scan ✅",
            "VPN: disconnected ⚠️",
            "Last scan: 2h ago"
        ]
        
        sec_y = self.height - 90
        for info in sec_info:
            if "✅" in info:
                color = self.colors['success']
            elif "⚠️" in info:
                color = self.colors['warning']
            else:
                color = self.colors['text']
            
            self.draw.text((sec_x, sec_y), info, fill=color, font=self.font_small)
            sec_y += 15
        
        # Sección 4: Quick Actions
        act_x = 20 + section_width * 3
        self.draw.text((act_x, self.height - 110), "⚡ Quick Actions", 
                      fill=self.colors['accent'], font=self.font_medium)
        
        # Botones de acción rápida
        actions = ["🔄 Restart", "📊 Monitor", "🔧 Tools", "⚙️ Settings"]
        
        act_y = self.height - 90
        for action in actions:
            btn_rect = [act_x, act_y, act_x + 120, act_y + 12]
            self.draw.rectangle(btn_rect, fill=self.colors['accent'], outline=self.colors['accent_light'])
            self.draw.text((act_x + 5, act_y), action, fill=self.colors['text'], font=self.font_small)
            act_y += 15
    
    def generate_blue_desktop(self):
        """Generar escritorio completo con tema azul"""
        print("Generando escritorio RazonbilstroOS Blue Theme...")
        
        # Dibujar todos los componentes
        self.draw_gradient_background()
        self.draw_modern_top_bar()
        self.draw_left_sidebar()
        self.draw_main_terminal()
        self.draw_bottom_status_bar()
        
        # Guardar imagen
        screenshot_path = "blue_desktop_razonbilstro.png"
        self.image.save(screenshot_path, "PNG", quality=95)
        
        print(f"Escritorio Blue Theme guardado: {screenshot_path}")
        print(f"Dimensiones: {self.width}x{self.height}")
        print("Tema: Deep Blue con acentos modernos")
        
        return screenshot_path

def main():
    """Generar escritorio Blue Theme"""
    desktop = BlueDesktopRazonbilstro()
    screenshot_path = desktop.generate_blue_desktop()
    
    print("\n✅ Escritorio Blue Theme RazonbilstroOS completado")
    print(f"📁 Archivo: {screenshot_path}")
    print("🎨 Tema azul moderno con integración completa del núcleo")

if __name__ == "__main__":
    main()