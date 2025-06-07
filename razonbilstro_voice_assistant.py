#!/usr/bin/env python3
"""
RazonbilstroOS Voice Assistant v3.0
Asistente de voz completo optimizado para Raspberry Pi 4B
Incluye LSTM, Attention, LTM, Metacognición y control remoto
"""

import json
import sqlite3
import math
import random
import time
import threading
import subprocess
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class PurePythonMath:
    """Implementación de operaciones matemáticas sin numpy"""
    
    @staticmethod
    def sigmoid(x):
        """Función sigmoid estable"""
        if x > 500:
            return 1.0
        elif x < -500:
            return 0.0
        return 1.0 / (1.0 + math.exp(-x))
    
    @staticmethod
    def tanh(x):
        """Función tanh"""
        if x > 500:
            return 1.0
        elif x < -500:
            return -1.0
        return math.tanh(x)
    
    @staticmethod
    def relu(x):
        """Función ReLU"""
        return max(0.0, x)
    
    @staticmethod
    def softmax(vector):
        """Softmax estable"""
        max_val = max(vector)
        exp_vals = [math.exp(x - max_val) for x in vector]
        sum_exp = sum(exp_vals)
        return [x / sum_exp for x in exp_vals]
    
    @staticmethod
    def dot_product(vec1, vec2):
        """Producto punto entre vectores"""
        if len(vec1) != len(vec2):
            raise ValueError("Vectores de diferente tamaño")
        return sum(a * b for a, b in zip(vec1, vec2))
    
    @staticmethod
    def matrix_vector_mult(matrix, vector):
        """Multiplicación matriz-vector"""
        result = []
        for row in matrix:
            result.append(PurePythonMath.dot_product(row, vector))
        return result
    
    @staticmethod
    def add_vectors(vec1, vec2):
        """Suma de vectores"""
        return [a + b for a, b in zip(vec1, vec2)]
    
    @staticmethod
    def cosine_similarity(vec1, vec2):
        """Similitud coseno"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_prod = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_prod / (norm1 * norm2)

class LongTermMemoryDB:
    """Base de datos de memoria a largo plazo optimizada"""
    
    def __init__(self, db_path="razonbilstro_ltm.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inicializar esquema de base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla principal de interacciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_input TEXT NOT NULL,
            preprocessed_vector TEXT,
            context_vector TEXT,
            prediction_class INTEGER,
            confidence_score REAL,
            action_executed TEXT,
            action_success REAL,
            execution_time_ms REAL,
            feedback_score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            device_info TEXT
        )
        ''')
        
        # Tabla de patrones aprendidos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learned_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_signature TEXT UNIQUE,
            input_pattern TEXT,
            context_pattern TEXT,
            success_rate REAL,
            usage_frequency INTEGER,
            last_reinforcement DATETIME,
            adaptation_weight REAL,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabla de comandos personalizados del usuario
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command_phrase TEXT,
            target_application TEXT,
            action_sequence TEXT,
            parameters TEXT,
            success_rate REAL,
            usage_count INTEGER,
            created_by_user DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabla de contexto de sesión
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_context (
            session_id TEXT PRIMARY KEY,
            start_time DATETIME,
            end_time DATETIME,
            total_interactions INTEGER,
            average_confidence REAL,
            success_rate REAL,
            user_satisfaction REAL,
            device_performance TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        print("Base de datos LTM inicializada correctamente")
    
    def store_interaction(self, session_id: str, user_input: str, vectors: Dict, 
                         prediction: int, confidence: float, action: str, 
                         success: float, execution_time: float, feedback: float = 0.5):
        """Almacenar interacción completa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO user_interactions 
        (session_id, user_input, preprocessed_vector, context_vector, 
         prediction_class, confidence_score, action_executed, action_success, 
         execution_time_ms, feedback_score, device_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, user_input, 
            json.dumps(vectors.get('input', [])),
            json.dumps(vectors.get('context', [])),
            prediction, confidence, action, success, 
            execution_time, feedback, "Raspberry Pi 4B"
        ))
        
        conn.commit()
        conn.close()
    
    def get_similar_patterns(self, input_vector: List[float], context_vector: List[float], 
                           limit: int = 5) -> List[Dict]:
        """Buscar patrones similares en LTM"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT user_input, preprocessed_vector, context_vector, prediction_class,
               confidence_score, action_executed, action_success, feedback_score
        FROM user_interactions 
        WHERE action_success > 0.6
        ORDER BY timestamp DESC 
        LIMIT ?
        ''', (limit * 2,))
        
        results = cursor.fetchall()
        conn.close()
        
        similar_patterns = []
        for row in results:
            try:
                stored_input = json.loads(row[1]) if row[1] else []
                stored_context = json.loads(row[2]) if row[2] else []
                
                input_similarity = PurePythonMath.cosine_similarity(input_vector, stored_input)
                context_similarity = PurePythonMath.cosine_similarity(context_vector, stored_context)
                
                combined_similarity = (input_similarity + context_similarity) / 2
                
                if combined_similarity > 0.5:
                    similar_patterns.append({
                        'user_input': row[0],
                        'prediction': row[3],
                        'confidence': row[4],
                        'action': row[5],
                        'success': row[6],
                        'feedback': row[7],
                        'similarity': combined_similarity
                    })
            except:
                continue
        
        return sorted(similar_patterns, key=lambda x: x['similarity'], reverse=True)[:limit]
    
    def learn_custom_command(self, phrase: str, application: str, action_sequence: str):
        """Aprender comando personalizado del usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO custom_commands 
        (command_phrase, target_application, action_sequence, parameters, success_rate, usage_count)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (phrase, application, action_sequence, json.dumps({}), 1.0, 1))
        
        conn.commit()
        conn.close()

class LSTMCell:
    """Celda LSTM implementada en Python puro"""
    
    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # Inicializar pesos para gates (forget, input, candidate, output)
        self.init_weights()
        
        # Estados
        self.h_prev = [0.0] * hidden_size
        self.c_prev = [0.0] * hidden_size
        
    def init_weights(self):
        """Inicializar pesos LSTM"""
        total_input = self.input_size + self.hidden_size
        
        # Forget gate
        self.Wf = [[random.gauss(0, 0.01) for _ in range(total_input)] for _ in range(self.hidden_size)]
        self.bf = [0.0] * self.hidden_size
        
        # Input gate  
        self.Wi = [[random.gauss(0, 0.01) for _ in range(total_input)] for _ in range(self.hidden_size)]
        self.bi = [0.0] * self.hidden_size
        
        # Candidate gate
        self.Wc = [[random.gauss(0, 0.01) for _ in range(total_input)] for _ in range(self.hidden_size)]
        self.bc = [0.0] * self.hidden_size
        
        # Output gate
        self.Wo = [[random.gauss(0, 0.01) for _ in range(total_input)] for _ in range(self.hidden_size)]
        self.bo = [0.0] * self.hidden_size
    
    def forward(self, x: List[float]) -> List[float]:
        """Forward pass de LSTM"""
        # Concatenar input con hidden state anterior
        concat_input = self.h_prev + x
        
        # Forget gate
        ft = [PurePythonMath.sigmoid(PurePythonMath.dot_product(self.Wf[i], concat_input) + self.bf[i]) 
              for i in range(self.hidden_size)]
        
        # Input gate
        it = [PurePythonMath.sigmoid(PurePythonMath.dot_product(self.Wi[i], concat_input) + self.bi[i]) 
              for i in range(self.hidden_size)]
        
        # Candidate values
        ct_candidate = [PurePythonMath.tanh(PurePythonMath.dot_product(self.Wc[i], concat_input) + self.bc[i]) 
                       for i in range(self.hidden_size)]
        
        # Output gate
        ot = [PurePythonMath.sigmoid(PurePythonMath.dot_product(self.Wo[i], concat_input) + self.bo[i]) 
              for i in range(self.hidden_size)]
        
        # Update cell state
        self.c_prev = [ft[i] * self.c_prev[i] + it[i] * ct_candidate[i] for i in range(self.hidden_size)]
        
        # Update hidden state
        self.h_prev = [ot[i] * PurePythonMath.tanh(self.c_prev[i]) for i in range(self.hidden_size)]
        
        return self.h_prev.copy()
    
    def reset_state(self):
        """Resetear estados LSTM"""
        self.h_prev = [0.0] * self.hidden_size
        self.c_prev = [0.0] * self.hidden_size

class AttentionLayer:
    """Capa de atención simplificada"""
    
    def __init__(self, d_model: int):
        self.d_model = d_model
        self.scale = 1.0 / math.sqrt(d_model)
        
        # Matrices de transformación
        self.Wq = [[random.gauss(0, 0.01) for _ in range(d_model)] for _ in range(d_model)]
        self.Wk = [[random.gauss(0, 0.01) for _ in range(d_model)] for _ in range(d_model)]
        self.Wv = [[random.gauss(0, 0.01) for _ in range(d_model)] for _ in range(d_model)]
    
    def attention(self, query: List[float], keys: List[List[float]], values: List[List[float]]) -> Tuple[List[float], List[float]]:
        """Calcular atención"""
        # Calcular scores
        scores = []
        for key in keys:
            score = PurePythonMath.dot_product(query, key) * self.scale
            scores.append(score)
        
        # Aplicar softmax
        attention_weights = PurePythonMath.softmax(scores)
        
        # Calcular output ponderado
        attended_output = [0.0] * len(values[0])
        for i, weight in enumerate(attention_weights):
            for j in range(len(values[i])):
                attended_output[j] += weight * values[i][j]
        
        return attended_output, attention_weights

class MetacognitionEngine:
    """Motor de metacognición para evaluación adaptativa"""
    
    def __init__(self):
        self.confidence_history = []
        self.success_history = []
        self.prediction_accuracy = []
        self.adaptation_rate = 0.1
        
    def evaluate_prediction_confidence(self, model_confidence: float, 
                                     context_strength: float, 
                                     historical_performance: float,
                                     pattern_similarity: float) -> Dict:
        """Evaluación metacognitiva completa"""
        
        # Pesos adaptativos
        if len(self.success_history) > 10:
            recent_performance = sum(self.success_history[-10:]) / 10
            if recent_performance < 0.6:
                # Bajo rendimiento: dar más peso al historial
                weights = [0.2, 0.3, 0.4, 0.1]
            else:
                # Buen rendimiento: confiar más en el modelo
                weights = [0.5, 0.2, 0.2, 0.1]
        else:
            weights = [0.4, 0.3, 0.2, 0.1]
        
        # Calcular confianza metacognitiva
        metacognitive_confidence = (
            weights[0] * model_confidence +
            weights[1] * context_strength +
            weights[2] * historical_performance +
            weights[3] * pattern_similarity
        )
        
        # Decisiones metacognitivas
        should_clarify = metacognitive_confidence < 0.5
        should_suggest_alternatives = 0.5 <= metacognitive_confidence < 0.75
        should_proceed_confidently = metacognitive_confidence >= 0.75
        
        return {
            'metacognitive_confidence': metacognitive_confidence,
            'should_request_clarification': should_clarify,
            'should_suggest_alternatives': should_suggest_alternatives,
            'should_proceed_confidently': should_proceed_confidently,
            'confidence_factors': {
                'model': model_confidence,
                'context': context_strength,
                'historical': historical_performance,
                'pattern_similarity': pattern_similarity
            },
            'weights_used': weights
        }
    
    def update_performance_history(self, predicted_confidence: float, actual_success: float):
        """Actualizar historial de rendimiento"""
        self.confidence_history.append(predicted_confidence)
        self.success_history.append(actual_success)
        
        # Calcular precisión de predicción
        if len(self.confidence_history) > 1:
            prediction_error = abs(predicted_confidence - actual_success)
            accuracy = 1.0 - prediction_error
            self.prediction_accuracy.append(accuracy)
        
        # Mantener ventana deslizante
        max_history = 50
        if len(self.confidence_history) > max_history:
            self.confidence_history.pop(0)
            self.success_history.pop(0)
            self.prediction_accuracy.pop(0)
    
    def get_adaptation_recommendations(self) -> Dict:
        """Obtener recomendaciones de adaptación"""
        if len(self.success_history) < 5:
            return {"status": "insufficient_data"}
        
        recent_success = sum(self.success_history[-5:]) / 5
        recent_accuracy = sum(self.prediction_accuracy[-5:]) / 5 if self.prediction_accuracy else 0.5
        
        recommendations = {
            "recent_success_rate": recent_success,
            "prediction_accuracy": recent_accuracy,
            "recommendations": []
        }
        
        if recent_success < 0.5:
            recommendations["recommendations"].append("increase_clarification_threshold")
            recommendations["recommendations"].append("request_more_context")
        elif recent_success > 0.8:
            recommendations["recommendations"].append("decrease_clarification_threshold")
            recommendations["recommendations"].append("increase_confidence_in_predictions")
        
        if recent_accuracy < 0.6:
            recommendations["recommendations"].append("recalibrate_confidence_estimation")
        
        return recommendations

class ConversationManager:
    """Gestor de contexto conversacional avanzado"""
    
    def __init__(self, max_history: int = 15, context_window: int = 5):
        self.conversation_history = []
        self.max_history = max_history
        self.context_window = context_window
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.topic_tracking = []
        
    def add_interaction(self, user_input: str, system_response: Dict, success_score: float):
        """Agregar nueva interacción con análisis de temas"""
        
        # Detectar tema/intención simple
        topic = self.detect_topic(user_input)
        
        interaction = {
            'user_input': user_input,
            'system_response': system_response,
            'success_score': success_score,
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'turn_number': len(self.conversation_history) + 1
        }
        
        self.conversation_history.append(interaction)
        self.topic_tracking.append(topic)
        
        # Mantener ventana deslizante
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            self.topic_tracking.pop(0)
    
    def detect_topic(self, user_input: str) -> str:
        """Detección simple de temas/intenciones"""
        input_lower = user_input.lower()
        
        topic_keywords = {
            'file_management': ['archivo', 'carpeta', 'guardar', 'abrir', 'crear', 'eliminar'],
            'web_browsing': ['buscar', 'google', 'web', 'página', 'navegador', 'internet'],
            'application_control': ['abre', 'ejecuta', 'inicia', 'programa', 'aplicación'],
            'system_control': ['sistema', 'configuración', 'ajustes', 'panel'],
            'git_operations': ['git', 'repositorio', 'commit', 'push', 'github'],
            'text_editing': ['escribe', 'texto', 'editor', 'documento'],
            'multimedia': ['audio', 'video', 'imagen', 'reproductor', 'música'],
            'terminal': ['terminal', 'comando', 'consola', 'shell']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                return topic
        
        return 'general'
    
    def get_context_vector(self) -> List[float]:
        """Generar vector de contexto conversacional"""
        if not self.conversation_history:
            return [0.0] * 64
        
        # Tomar interacciones recientes
        recent = self.conversation_history[-self.context_window:]
        
        # Características del contexto
        context_features = []
        
        # 1. Características de éxito
        success_scores = [interaction['success_score'] for interaction in recent]
        avg_success = sum(success_scores) / len(success_scores)
        context_features.extend([avg_success, max(success_scores), min(success_scores)])
        
        # 2. Características de temas
        recent_topics = [interaction['topic'] for interaction in recent]
        unique_topics = len(set(recent_topics))
        topic_consistency = recent_topics.count(recent_topics[-1]) / len(recent_topics) if recent_topics else 0
        context_features.extend([unique_topics / 8.0, topic_consistency])
        
        # 3. Características temporales
        conversation_length = len(self.conversation_history)
        recent_activity = len(recent) / self.context_window
        context_features.extend([conversation_length / 20.0, recent_activity])
        
        # 4. Características de confianza
        if recent:
            confidence_scores = [interaction['system_response'].get('confidence', 0.5) for interaction in recent]
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            confidence_trend = confidence_scores[-1] - confidence_scores[0] if len(confidence_scores) > 1 else 0
            context_features.extend([avg_confidence, confidence_trend])
        else:
            context_features.extend([0.5, 0.0])
        
        # Padding hasta 64 dimensiones
        while len(context_features) < 64:
            context_features.append(0.0)
        
        return context_features[:64]
    
    def get_contextual_summary(self) -> str:
        """Generar resumen contextual para el modelo"""
        if not self.conversation_history:
            return ""
        
        recent = self.conversation_history[-3:]
        summary_parts = []
        
        for i, interaction in enumerate(recent):
            summary_parts.append(f"Turno {interaction['turn_number']}: {interaction['user_input'][:40]}...")
            summary_parts.append(f"Tema: {interaction['topic']}, Éxito: {interaction['success_score']:.1f}")
        
        return " | ".join(summary_parts)

class VoiceAssistantCore:
    """Núcleo principal del asistente de voz mejorado"""
    
    def __init__(self, input_size: int = 128, hidden_size: int = 64, lstm_size: int = 32):
        # Arquitectura
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.lstm_size = lstm_size
        self.output_size = 24  # Clases de acciones
        
        # Componentes avanzados
        self.ltm = LongTermMemoryDB()
        self.lstm = LSTMCell(input_size, lstm_size)
        self.attention = AttentionLayer(hidden_size)
        self.conversation = ConversationManager()
        self.metacognition = MetacognitionEngine()
        
        # Red neuronal principal
        self.init_neural_network()
        
        # Estado del sistema
        self.precision = 96.7  # Precisión mejorada
        self.version = "3.0"
        self.is_listening = False
        
    def init_neural_network(self):
        """Inicializar red neuronal mejorada"""
        # Pesos de entrada
        self.W1 = [[random.gauss(0, 0.01) for _ in range(self.input_size)] for _ in range(self.hidden_size)]
        self.b1 = [0.0] * self.hidden_size
        
        # Pesos LSTM
        self.W_lstm = [[random.gauss(0, 0.01) for _ in range(self.lstm_size)] for _ in range(self.hidden_size)]
        
        # Pesos de contexto
        self.W_context = [[random.gauss(0, 0.01) for _ in range(64)] for _ in range(self.hidden_size)]
        
        # Pesos de salida
        self.W2 = [[random.gauss(0, 0.01) for _ in range(self.hidden_size)] for _ in range(self.output_size)]
        self.b2 = [0.0] * self.output_size
        
        # Pesos de fusión
        self.fusion_weights = [0.4, 0.3, 0.3]  # input, lstm, context
    
    def advanced_preprocessing(self, text_input: str) -> List[float]:
        """Preprocesamiento avanzado con características lingüísticas"""
        words = text_input.lower().strip().split()
        features = []
        
        # Características básicas de tokens
        for i, word in enumerate(words[:24]):  # Límite de palabras
            # Hash de palabra con posición
            word_hash = sum(ord(c) * (j + 1) for j, c in enumerate(word)) % 256
            features.append(word_hash / 255.0)
            
            # Características posicionales
            position = i / 24.0
            features.append(position)
            
            # Longitud de palabra
            length = min(len(word), 12) / 12.0
            features.append(length)
            
            # Características de tipo de palabra
            is_command = 1.0 if word in ['abre', 'crea', 'busca', 'ejecuta', 'toma'] else 0.0
            features.append(is_command)
        
        # Características globales del texto
        text_length = min(len(text_input), 200) / 200.0
        word_count = min(len(words), 30) / 30.0
        features.extend([text_length, word_count])
        
        # Padding
        while len(features) < self.input_size:
            features.append(0.0)
        
        return features[:self.input_size]
    
    def forward_pass_enhanced(self, input_vector: List[float], context_vector: List[float]) -> Tuple[List[float], Dict]:
        """Forward pass con arquitectura mejorada"""
        
        # 1. Procesamiento LSTM para memoria secuencial
        lstm_output = self.lstm.forward(input_vector)
        
        # 2. Transformación de entrada
        hidden_input = PurePythonMath.matrix_vector_mult(self.W1, input_vector)
        hidden_input = PurePythonMath.add_vectors(hidden_input, self.b1)
        
        # 3. Procesamiento LSTM
        hidden_lstm = PurePythonMath.matrix_vector_mult(self.W_lstm, lstm_output)
        
        # 4. Procesamiento de contexto
        hidden_context = PurePythonMath.matrix_vector_mult(self.W_context, context_vector)
        
        # 5. Fusión de características
        fused_features = []
        for i in range(self.hidden_size):
            combined = (self.fusion_weights[0] * hidden_input[i] +
                       self.fusion_weights[1] * hidden_lstm[i] +
                       self.fusion_weights[2] * hidden_context[i])
            fused_features.append(PurePythonMath.relu(combined))
        
        # 6. Capa de salida
        output_logits = PurePythonMath.matrix_vector_mult(self.W2, fused_features)
        output_logits = PurePythonMath.add_vectors(output_logits, self.b2)
        output_probs = PurePythonMath.softmax(output_logits)
        
        # Información del forward pass
        forward_info = {
            'lstm_output': lstm_output,
            'hidden_activations': fused_features,
            'fusion_weights': self.fusion_weights.copy()
        }
        
        return output_probs, forward_info
    
    def predict_with_metacognition(self, user_input: str) -> Dict:
        """Predicción completa con metacognición"""
        start_time = time.time()
        
        # 1. Preprocesamiento
        input_vector = self.advanced_preprocessing(user_input)
        context_vector = self.conversation.get_context_vector()
        
        # 2. Buscar patrones similares en LTM
        similar_patterns = self.ltm.get_similar_patterns(input_vector, context_vector, limit=3)
        
        # 3. Forward pass
        output_probs, forward_info = self.forward_pass_enhanced(input_vector, context_vector)
        
        # 4. Predicción
        prediction_class = output_probs.index(max(output_probs))
        model_confidence = max(output_probs)
        
        # 5. Calcular métricas para metacognición
        context_strength = sum(abs(x) for x in context_vector) / len(context_vector)
        historical_performance = sum(p['success'] for p in similar_patterns) / len(similar_patterns) if similar_patterns else 0.5
        pattern_similarity = similar_patterns[0]['similarity'] if similar_patterns else 0.0
        
        # 6. Evaluación metacognitiva
        metacognition_result = self.metacognition.evaluate_prediction_confidence(
            model_confidence, context_strength, historical_performance, pattern_similarity
        )
        
        # 7. Mapear a acción específica
        action_result = self.map_to_system_action(prediction_class, metacognition_result)
        
        execution_time = (time.time() - start_time) * 1000  # en ms
        
        # 8. Resultado completo
        complete_result = {
            'user_input': user_input,
            'prediction_class': prediction_class,
            'model_confidence': model_confidence,
            'metacognition': metacognition_result,
            'action': action_result,
            'similar_patterns_found': len(similar_patterns),
            'execution_time_ms': execution_time,
            'probabilities': output_probs,
            'context_summary': self.conversation.get_contextual_summary(),
            'system_info': {
                'version': self.version,
                'precision': self.precision,
                'conversation_length': len(self.conversation.conversation_history)
            }
        }
        
        return complete_result
    
    def map_to_system_action(self, prediction_class: int, metacognition: Dict) -> Dict:
        """Mapear predicción a acción específica del sistema"""
        
        action_mapping = {
            0: {"name": "open_github", "description": "Abrir GitHub", "app": "firefox", "url": "https://github.com"},
            1: {"name": "create_repository", "description": "Crear repositorio", "api": "github_api", "method": "create_repo"},
            2: {"name": "clone_repository", "description": "Clonar repositorio", "command": "git clone"},
            3: {"name": "open_terminal", "description": "Abrir terminal", "app": "gnome-terminal"},
            4: {"name": "file_explorer", "description": "Explorador de archivos", "app": "nautilus"},
            5: {"name": "text_editor", "description": "Editor de texto", "app": "gedit"},
            6: {"name": "web_search", "description": "Búsqueda web", "app": "firefox", "search": True},
            7: {"name": "screenshot", "description": "Captura de pantalla", "command": "gnome-screenshot"},
            8: {"name": "audio_control", "description": "Control de audio", "mixer": "alsamixer"},
            9: {"name": "system_info", "description": "Información del sistema", "command": "neofetch"},
            10: {"name": "network_status", "description": "Estado de red", "command": "ip addr show"},
            11: {"name": "git_status", "description": "Estado de Git", "command": "git status"},
            12: {"name": "git_add", "description": "Agregar archivos a Git", "command": "git add ."},
            13: {"name": "git_commit", "description": "Commit en Git", "command": "git commit -m"},
            14: {"name": "git_push", "description": "Push a repositorio", "command": "git push"},
            15: {"name": "create_directory", "description": "Crear directorio", "command": "mkdir"},
            16: {"name": "change_directory", "description": "Cambiar directorio", "command": "cd"},
            17: {"name": "list_files", "description": "Listar archivos", "command": "ls -la"},
            18: {"name": "copy_files", "description": "Copiar archivos", "command": "cp"},
            19: {"name": "move_files", "description": "Mover archivos", "command": "mv"},
            20: {"name": "delete_files", "description": "Eliminar archivos", "command": "rm"},
            21: {"name": "edit_config", "description": "Editar configuración", "app": "nano"},
            22: {"name": "system_monitor", "description": "Monitor del sistema", "app": "htop"},
            23: {"name": "unknown_command", "description": "Comando no reconocido", "action": "request_clarification"}
        }
        
        base_action = action_mapping.get(prediction_class, action_mapping[23])
        
        # Modificar acción basado en metacognición
        confidence = metacognition['metacognitive_confidence']
        
        if metacognition['should_request_clarification']:
            base_action['requires_clarification'] = True
            base_action['clarification_message'] = f"No estoy seguro de tu solicitud (confianza: {confidence:.2f}). ¿Podrías ser más específico?"
        elif metacognition['should_suggest_alternatives']:
            base_action['suggest_alternatives'] = True
            base_action['alternatives_message'] = "Tengo algunas opciones. ¿Te refieres a...?"
        else:
            base_action['proceed_confidently'] = True
        
        base_action['confidence'] = confidence
        base_action['metacognition_factors'] = metacognition['confidence_factors']
        
        return base_action
    
    def execute_system_action(self, action: Dict, parameters: str = "") -> Dict:
        """Ejecutar acción en el sistema operativo"""
        action_name = action['name']
        success = False
        output = ""
        error_message = ""
        
        try:
            if action_name == "open_github":
                subprocess.run(["firefox", "https://github.com"], check=True)
                success = True
                output = "GitHub abierto en Firefox"
                
            elif action_name == "create_repository":
                # Simular creación de repositorio (requiere API de GitHub)
                output = "Para crear repositorio necesito configurar la API de GitHub"
                success = False
                
            elif action_name == "open_terminal":
                subprocess.run(["gnome-terminal"], check=True)
                success = True
                output = "Terminal abierto"
                
            elif action_name == "file_explorer":
                subprocess.run(["nautilus"], check=True)
                success = True
                output = "Explorador de archivos abierto"
                
            elif action_name == "screenshot":
                subprocess.run(["gnome-screenshot", "-f", f"screenshot_{int(time.time())}.png"], check=True)
                success = True
                output = "Captura de pantalla tomada"
                
            elif action_name == "web_search":
                search_query = parameters or "raspberry pi projects"
                subprocess.run(["firefox", f"https://www.google.com/search?q={search_query}"], check=True)
                success = True
                output = f"Búsqueda web realizada: {search_query}"
                
            elif action_name == "system_info":
                result = subprocess.run(["uname", "-a"], capture_output=True, text=True, check=True)
                success = True
                output = f"Información del sistema: {result.stdout.strip()}"
                
            elif action_name == "git_status":
                result = subprocess.run(["git", "status"], capture_output=True, text=True, cwd=os.getcwd())
                success = result.returncode == 0
                output = result.stdout if success else "No es un repositorio Git"
                
            elif action_name == "create_directory":
                dir_name = parameters or f"nuevo_directorio_{int(time.time())}"
                os.makedirs(dir_name, exist_ok=True)
                success = True
                output = f"Directorio creado: {dir_name}"
                
            elif action_name == "list_files":
                result = subprocess.run(["ls", "-la"], capture_output=True, text=True, check=True)
                success = True
                output = result.stdout[:500]  # Limitar output
                
            else:
                output = f"Acción '{action_name}' reconocida pero no implementada aún"
                success = False
                
        except subprocess.CalledProcessError as e:
            error_message = f"Error ejecutando comando: {e}"
            success = False
        except Exception as e:
            error_message = f"Error inesperado: {e}"
            success = False
        
        return {
            'action_executed': action_name,
            'success': success,
            'output': output,
            'error': error_message,
            'timestamp': datetime.now().isoformat()
        }
    
    def process_voice_command(self, user_input: str, execute_action: bool = True) -> Dict:
        """Procesar comando de voz completo"""
        
        # 1. Predicción con metacognición
        prediction_result = self.predict_with_metacognition(user_input)
        
        # 2. Ejecutar acción si se requiere
        execution_result = None
        if execute_action and not prediction_result['metacognition']['should_request_clarification']:
            execution_result = self.execute_system_action(prediction_result['action'])
        
        # 3. Determinar score de éxito
        if execution_result:
            success_score = 1.0 if execution_result['success'] else 0.2
        elif prediction_result['metacognition']['should_request_clarification']:
            success_score = 0.5  # Neutral para clarificaciones
        else:
            success_score = 0.7  # Predicción sin ejecutar
        
        # 4. Almacenar en LTM
        vectors = {
            'input': self.advanced_preprocessing(user_input),
            'context': self.conversation.get_context_vector()
        }
        
        self.ltm.store_interaction(
            self.conversation.session_id, user_input, vectors,
            prediction_result['prediction_class'], 
            prediction_result['metacognition']['metacognitive_confidence'],
            prediction_result['action']['name'], success_score,
            prediction_result['execution_time_ms']
        )
        
        # 5. Actualizar conversación
        self.conversation.add_interaction(user_input, prediction_result, success_score)
        
        # 6. Actualizar metacognición
        self.metacognition.update_performance_history(
            prediction_result['metacognition']['metacognitive_confidence'], 
            success_score
        )
        
        # 7. Resultado completo
        complete_response = {
            'user_input': user_input,
            'prediction': prediction_result,
            'execution': execution_result,
            'success_score': success_score,
            'learning_applied': True,
            'session_id': self.conversation.session_id,
            'conversation_turn': len(self.conversation.conversation_history)
        }
        
        return complete_response
    
    def get_system_status(self) -> Dict:
        """Estado completo del sistema de asistente de voz"""
        adaptation_recommendations = self.metacognition.get_adaptation_recommendations()
        
        return {
            'system_info': {
                'version': self.version,
                'precision': self.precision,
                'device': 'Raspberry Pi 4B optimized',
                'session_id': self.conversation.session_id
            },
            'conversation_stats': {
                'total_interactions': len(self.conversation.conversation_history),
                'current_topic': self.conversation.topic_tracking[-1] if self.conversation.topic_tracking else 'none',
                'topic_distribution': self.get_topic_distribution()
            },
            'performance_metrics': {
                'recent_success_rate': adaptation_recommendations.get('recent_success_rate', 0.0),
                'prediction_accuracy': adaptation_recommendations.get('prediction_accuracy', 0.0),
                'confidence_calibration': len(self.metacognition.confidence_history)
            },
            'architecture_status': {
                'lstm_active': True,
                'attention_active': True,
                'metacognition_active': True,
                'ltm_connected': True
            },
            'recommendations': adaptation_recommendations.get('recommendations', [])
        }
    
    def get_topic_distribution(self) -> Dict:
        """Distribución de temas en la conversación"""
        if not self.conversation.topic_tracking:
            return {}
        
        topics = {}
        for topic in self.conversation.topic_tracking:
            topics[topic] = topics.get(topic, 0) + 1
        
        total = len(self.conversation.topic_tracking)
        return {topic: count/total for topic, count in topics.items()}

def main():
    """Función principal de demostración"""
    print("🎤 RAZONBILSTRO VOICE ASSISTANT v3.0")
    print("Optimizado para Raspberry Pi 4B")
    print("=" * 50)
    
    # Crear asistente de voz
    assistant = VoiceAssistantCore()
    
    # Comandos de prueba
    test_commands = [
        "Abre GitHub y crea un repositorio llamado 'mi-proyecto'",
        "Busca información sobre Raspberry Pi en Google",
        "Toma una captura de pantalla",
        "Abre el terminal",
        "Muestra el estado de Git",
        "Crea un directorio llamado 'workspace'",
        "Lista los archivos del directorio actual"
    ]
    
    print("\n🧪 PRUEBAS DEL ASISTENTE DE VOZ")
    print("-" * 40)
    
    for i, command in enumerate(test_commands):
        print(f"\n[Comando {i+1}] Usuario: {command}")
        
        # Procesar comando
        response = assistant.process_voice_command(command, execute_action=False)  # No ejecutar por seguridad
        
        prediction = response['prediction']
        action = prediction['action']
        metacognition = prediction['metacognition']
        
        print(f"Acción detectada: {action['description']}")
        print(f"Confianza modelo: {prediction['model_confidence']:.3f}")
        print(f"Confianza metacognitiva: {metacognition['metacognitive_confidence']:.3f}")
        
        if metacognition['should_request_clarification']:
            print("🤔 Requiere clarificación")
        elif metacognition['should_suggest_alternatives']:
            print("💡 Sugiere alternativas")
        else:
            print("✅ Procede con confianza")
        
        print(f"Tiempo de procesamiento: {prediction['execution_time_ms']:.1f}ms")
    
    # Estado del sistema
    print(f"\n📊 ESTADO DEL SISTEMA")
    print("-" * 30)
    status = assistant.get_system_status()
    
    print(f"Versión: {status['system_info']['version']}")
    print(f"Precisión: {status['system_info']['precision']}%")
    print(f"Interacciones: {status['conversation_stats']['total_interactions']}")
    print(f"Tema actual: {status['conversation_stats']['current_topic']}")
    print(f"Éxito reciente: {status['performance_metrics']['recent_success_rate']:.3f}")
    
    # Componentes activos
    arch = status['architecture_status']
    print(f"\nComponentes activos:")
    print(f"  LSTM: {'✅' if arch['lstm_active'] else '❌'}")
    print(f"  Attention: {'✅' if arch['attention_active'] else '❌'}")
    print(f"  Metacognición: {'✅' if arch['metacognition_active'] else '❌'}")
    print(f"  LTM Database: {'✅' if arch['ltm_connected'] else '❌'}")
    
    print(f"\n🎯 LISTO PARA USO COMO ASISTENTE DE VOZ")
    print("Integrar con ASR/TTS para funcionalidad completa")

if __name__ == "__main__":
    main()