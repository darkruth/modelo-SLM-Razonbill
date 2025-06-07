#!/usr/bin/env python3
"""
API Server RazonbilstroOS con autenticación por tokens
Sistema de acceso local y en nube
"""

from flask import Flask, request, jsonify, g
import jwt
import hashlib
import secrets
import sqlite3
import time
from datetime import datetime, timedelta
from functools import wraps
import os
import sys

# Agregar núcleo al path
sys.path.append('/workspace/razonbilstro_nucleus/core')
from tty_nucleus import TTYNucleus

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

class TokenManager:
    """Gestor de tokens de API"""
    
    def __init__(self, db_path="api_tokens.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inicializar base de datos de tokens"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT UNIQUE NOT NULL,
            key_hash TEXT NOT NULL,
            user_id TEXT NOT NULL,
            permissions TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0,
            rate_limit INTEGER DEFAULT 1000,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            request_data TEXT,
            response_data TEXT,
            processing_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_api_key(self, user_id: str, permissions: list, expires_days: int = 365) -> dict:
        """Generar nueva API key"""
        key_id = f"rzb_{secrets.token_hex(16)}"
        api_key = f"{key_id}_{secrets.token_hex(32)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        expires_at = datetime.now() + timedelta(days=expires_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO api_keys (key_id, key_hash, user_id, permissions, expires_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (key_id, key_hash, user_id, ','.join(permissions), expires_at))
        
        conn.commit()
        conn.close()
        
        return {
            "api_key": api_key,
            "key_id": key_id,
            "permissions": permissions,
            "expires_at": expires_at.isoformat()
        }
    
    def validate_api_key(self, api_key: str) -> dict:
        """Validar API key"""
        if not api_key:
            return {"valid": False, "error": "API key requerida"}
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT key_id, user_id, permissions, usage_count, rate_limit, expires_at, is_active
        FROM api_keys WHERE key_hash = ?
        ''', (key_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {"valid": False, "error": "API key inválida"}
        
        key_id, user_id, permissions, usage_count, rate_limit, expires_at, is_active = result
        
        if not is_active:
            return {"valid": False, "error": "API key desactivada"}
        
        if expires_at and datetime.fromisoformat(expires_at) < datetime.now():
            return {"valid": False, "error": "API key expirada"}
        
        if usage_count >= rate_limit:
            return {"valid": False, "error": "Límite de uso excedido"}
        
        return {
            "valid": True,
            "key_id": key_id,
            "user_id": user_id,
            "permissions": permissions.split(',') if permissions else []
        }
    
    def increment_usage(self, key_id: str, endpoint: str, processing_time: float):
        """Incrementar contador de uso"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE api_keys SET usage_count = usage_count + 1 WHERE key_id = ?
        ''', (key_id,))
        
        cursor.execute('''
        INSERT INTO api_usage (key_id, endpoint, processing_time)
        VALUES (?, ?, ?)
        ''', (key_id, endpoint, processing_time))
        
        conn.commit()
        conn.close()

# Instanciar gestor de tokens
token_manager = TokenManager()

def require_api_key(required_permission=None):
    """Decorador para requerir API key"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
            
            validation = token_manager.validate_api_key(api_key)
            if not validation["valid"]:
                return jsonify({"error": validation["error"]}), 401
            
            if required_permission and required_permission not in validation["permissions"]:
                return jsonify({"error": "Permisos insuficientes"}), 403
            
            g.api_key_info = validation
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Instanciar núcleo TTY
nucleus = None

def get_nucleus():
    """Obtener instancia del núcleo"""
    global nucleus
    if nucleus is None:
        nucleus = TTYNucleus()
        nucleus.start_privileged_shell()
    return nucleus

@app.route('/api/v1/generate_key', methods=['POST'])
def generate_key():
    """Generar nueva API key"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    permissions = data.get('permissions', ['chat', 'commands'])
    expires_days = data.get('expires_days', 365)
    
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400
    
    key_info = token_manager.generate_api_key(user_id, permissions, expires_days)
    return jsonify(key_info)

@app.route('/api/v1/chat', methods=['POST'])
@require_api_key('chat')
def chat():
    """Endpoint de chat conversacional"""
    start_time = time.time()
    
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "Mensaje requerido"}), 400
    
    try:
        nucleus_instance = get_nucleus()
        result = nucleus_instance.process_nucleus_command(message)
        
        response = {
            "response": result.get('response', 'Procesado'),
            "type": result.get('type', 'conversation'),
            "processing_time": time.time() - start_time,
            "timestamp": datetime.now().isoformat()
        }
        
        # Registrar uso
        token_manager.increment_usage(
            g.api_key_info['key_id'], 
            'chat', 
            response['processing_time']
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/execute', methods=['POST'])
@require_api_key('commands')
def execute_command():
    """Endpoint para ejecutar comandos del sistema"""
    start_time = time.time()
    
    data = request.get_json()
    command = data.get('command', '')
    
    if not command:
        return jsonify({"error": "Comando requerido"}), 400
    
    try:
        nucleus_instance = get_nucleus()
        result = nucleus_instance.execute_command(command)
        
        response = {
            "command": command,
            "output": result.get('output', ''),
            "success": result.get('success', False),
            "processing_time": time.time() - start_time,
            "timestamp": datetime.now().isoformat()
        }
        
        # Registrar uso
        token_manager.increment_usage(
            g.api_key_info['key_id'],
            'execute',
            response['processing_time']
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/process', methods=['POST'])
@require_api_key('process')
def process_input():
    """Endpoint para procesamiento completo con núcleo"""
    start_time = time.time()
    
    data = request.get_json()
    input_text = data.get('input', '')
    
    if not input_text:
        return jsonify({"error": "Input requerido"}), 400
    
    try:
        nucleus_instance = get_nucleus()
        result = nucleus_instance.process_nucleus_command(input_text)
        
        response = {
            "input": input_text,
            "result": result,
            "processing_time": time.time() - start_time,
            "timestamp": datetime.now().isoformat()
        }
        
        # Registrar uso
        token_manager.increment_usage(
            g.api_key_info['key_id'],
            'process',
            response['processing_time']
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/status', methods=['GET'])
@require_api_key()
def get_status():
    """Obtener estado del sistema"""
    try:
        nucleus_instance = get_nucleus()
        
        status = {
            "system": "RazonbilstroOS Nucleus API",
            "version": "4.1",
            "tty_active": nucleus_instance.is_active,
            "permissions": {
                "microphone": True,
                "camera": True,
                "display": True,
                "files": True,
                "network": True,
                "system": True
            },
            "api_info": {
                "user_id": g.api_key_info['user_id'],
                "permissions": g.api_key_info['permissions']
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/usage', methods=['GET'])
@require_api_key()
def get_usage():
    """Obtener estadísticas de uso"""
    try:
        conn = sqlite3.connect(token_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT endpoint, COUNT(*), AVG(processing_time)
        FROM api_usage WHERE key_id = ?
        GROUP BY endpoint
        ''', (g.api_key_info['key_id'],))
        
        usage_stats = []
        for endpoint, count, avg_time in cursor.fetchall():
            usage_stats.append({
                "endpoint": endpoint,
                "requests": count,
                "avg_processing_time": avg_time
            })
        
        conn.close()
        
        return jsonify({
            "key_id": g.api_key_info['key_id'],
            "usage_stats": usage_stats,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/reset', methods=['POST'])
@require_api_key('admin')
def reset_system():
    """Reset del sistema (requiere permisos admin)"""
    try:
        nucleus_instance = get_nucleus()
        nucleus_instance.stop_tty()
        nucleus_instance.start_privileged_shell()
        
        return jsonify({
            "message": "Sistema reiniciado",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Generar API key inicial para desarrollo
    initial_key = token_manager.generate_api_key(
        "admin", 
        ["chat", "commands", "process", "admin"],
        365
    )
    
    print("API Server RazonbilstroOS iniciado")
    print(f"API Key inicial: {initial_key['api_key']}")
    print("Endpoints disponibles:")
    print("  POST /api/v1/generate_key - Generar nueva API key")
    print("  POST /api/v1/chat - Chat conversacional")
    print("  POST /api/v1/execute - Ejecutar comandos")
    print("  POST /api/v1/process - Procesamiento completo")
    print("  GET  /api/v1/status - Estado del sistema")
    print("  GET  /api/v1/usage - Estadísticas de uso")
    print("  POST /api/v1/reset - Reset del sistema")
    
    app.run(host='0.0.0.0', port=8080, debug=True)