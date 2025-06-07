#!/usr/bin/env python3
"""
Procesador de URLs Simplificado para Núcleo C.A- Razonbilstro
Extracción de contenido web con análisis básico
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import uuid

class SimpleURLProcessor:
    """Procesador simplificado de URLs para extracción de contenido web"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def process_url(self, url):
        """Procesar URL y extraer contenido disponible"""
        try:
            # Validar URL
            if not self.is_valid_url(url):
                return {
                    'error': 'URL no válida',
                    'url': url,
                    'success': False
                }
            
            result = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'html_content': None,
                'images_found': [],
                'links_found': [],
                'metadata': {}
            }
            
            # Extraer contenido HTML
            html_result = self.extract_html_content(url)
            if html_result['success']:
                result['html_content'] = html_result
                
                # Extraer imágenes y enlaces
                images_result = self.extract_images_and_links(html_result.get('soup'))
                result['images_found'] = images_result.get('images', [])
                result['links_found'] = images_result.get('links', [])
            
            # Generar resumen del contenido
            result['content_summary'] = self.generate_content_summary(result)
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'url': url,
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def is_valid_url(self, url):
        """Validar si la URL es válida"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def extract_html_content(self, url):
        """Extraer contenido HTML de la página"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer metadatos
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'Sin título'
            
            # Extraer descripción
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag.get('content', '') if description_tag else ''
            
            # Extraer keywords
            keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            keywords = keywords_tag.get('content', '') if keywords_tag else ''
            
            # Extraer texto principal
            # Remover scripts y estilos
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Buscar contenido principal
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))
            
            if main_content:
                text_content = main_content.get_text()
            else:
                text_content = soup.get_text()
            
            # Limpiar texto
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk and len(chunk) > 10)
            
            # Limitar el texto para evitar respuestas muy largas
            if len(text_content) > 3000:
                text_content = text_content[:3000] + "... [contenido truncado]"
            
            # Extraer headings
            headings = []
            for i in range(1, 7):
                for heading in soup.find_all(f'h{i}'):
                    heading_text = heading.get_text().strip()
                    if heading_text:
                        headings.append({
                            'level': i,
                            'text': heading_text
                        })
            
            return {
                'success': True,
                'title': title_text,
                'description': description,
                'keywords': keywords,
                'text_content': text_content,
                'headings': headings[:10],  # Limitar a 10 headings
                'status_code': response.status_code,
                'content_length': len(response.text),
                'soup': soup  # Para uso interno
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_images_and_links(self, soup):
        """Extraer imágenes y enlaces de la página"""
        if not soup:
            return {'images': [], 'links': []}
        
        try:
            # Extraer imágenes
            images = []
            for img in soup.find_all('img', limit=20):  # Limitar a 20 imágenes
                img_src = img.get('src', '')
                img_alt = img.get('alt', '')
                img_title = img.get('title', '')
                
                if img_src:
                    # Convertir URLs relativas a absolutas si es necesario
                    if img_src.startswith('//'):
                        img_src = 'https:' + img_src
                    elif img_src.startswith('/'):
                        # Necesitaríamos la URL base para esto, simplificamos
                        pass
                    
                    images.append({
                        'src': img_src,
                        'alt': img_alt,
                        'title': img_title,
                        'has_text_description': bool(img_alt or img_title)
                    })
            
            # Extraer enlaces importantes
            links = []
            for link in soup.find_all('a', href=True, limit=30):  # Limitar a 30 enlaces
                href = link.get('href', '')
                link_text = link.get_text().strip()
                
                if href and link_text and len(link_text) > 3:
                    # Filtrar enlaces de navegación comunes
                    if not any(skip in href.lower() for skip in ['#', 'javascript:', 'mailto:']):
                        links.append({
                            'href': href,
                            'text': link_text[:100],  # Limitar texto del enlace
                            'is_external': href.startswith('http')
                        })
            
            return {
                'images': images,
                'links': links
            }
            
        except Exception as e:
            return {
                'images': [],
                'links': [],
                'error': str(e)
            }
    
    def generate_content_summary(self, result):
        """Generar resumen del contenido extraído"""
        summary = {
            'url_accessible': result.get('html_content', {}).get('success', False),
            'has_title': bool(result.get('html_content', {}).get('title')),
            'has_description': bool(result.get('html_content', {}).get('description')),
            'content_length': len(result.get('html_content', {}).get('text_content', '')),
            'images_count': len(result.get('images_found', [])),
            'links_count': len(result.get('links_found', [])),
            'headings_count': len(result.get('html_content', {}).get('headings', [])),
            'content_types': []
        }
        
        if summary['url_accessible']:
            summary['content_types'].append('HTML')
        if summary['images_count'] > 0:
            summary['content_types'].append('Images')
        if summary['links_count'] > 0:
            summary['content_types'].append('Links')
        if summary['headings_count'] > 0:
            summary['content_types'].append('Structured_Content')
        
        return summary

def test_simple_url_processor():
    """Función de prueba del procesador simplificado"""
    processor = SimpleURLProcessor()
    
    # URL de prueba
    test_url = "https://example.com"
    
    print("Probando procesador simplificado de URLs...")
    result = processor.process_url(test_url)
    
    if result['success']:
        print("✓ Procesamiento exitoso")
        print(f"✓ Título: {result.get('html_content', {}).get('title', 'N/A')}")
        print(f"✓ Contenido extraído: {len(result.get('html_content', {}).get('text_content', ''))} caracteres")
        print(f"✓ Imágenes encontradas: {len(result.get('images_found', []))}")
        print(f"✓ Enlaces encontrados: {len(result.get('links_found', []))}")
    else:
        print(f"✗ Error: {result.get('error', 'Error desconocido')}")
    
    return result

if __name__ == '__main__':
    test_simple_url_processor()