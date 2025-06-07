#!/usr/bin/env python3
"""
Ejecutor de Entrenamiento - Núcleo C.A- Razonbilstro
Integra dataset ECU ABS y monitorea comportamiento completo
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import numpy as np

# Importar componentes del sistema
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_model import NeuralModel
from core.meta_learning_system import MetaLearningSystem

logger = logging.getLogger(__name__)

class TrainingExecutor:
    """
    Ejecutor principal de entrenamiento con monitoreo completo
    """
    
    def __init__(self):
        # Componentes principales
        self.neural_model = NeuralModel()
        self.meta_learning = MetaLearningSystem()
        self.hybrid_training = HybridTrainingSystem()
        
        # Configuración de monitoreo
        self.monitoring_data = {
            "initial_state": {},
            "training_progression": [],
            "behavior_changes": [],
            "final_state": {},
            "performance_metrics": []
        }
        
        # Directorios
        self.reports_dir = Path("gym_razonbilstro/training_reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Estado inicial del núcleo
        self.initial_weights = None
        self.initial_performance = None
        
    def execute_full_training_cycle(self) -> Dict:
        """
        Ejecutar ciclo completo de entrenamiento con monitoreo
        """
        print("🧠 Iniciando Entrenamiento Núcleo C.A- Razonbilstro")
        print("=" * 60)
        
        # 1. Capturar estado inicial
        self._capture_initial_state()
        
        # 2. Cargar dataset ECU ABS
        dataset = self._load_ecu_abs_dataset()
        
        # 3. Configurar sesión de entrenamiento
        session_config = self._setup_training_session(dataset)
        
        # 4. Ejecutar entrenamiento con monitoreo
        training_results = self._execute_monitored_training(dataset, session_config)
        
        # 5. Capturar estado final
        self._capture_final_state()
        
        # 6. Generar informe detallado
        report_file = self._generate_detailed_report(training_results)
        
        return {
            "status": "completed",
            "training_results": training_results,
            "report_file": str(report_file),
            "total_examples": len(dataset),
            "performance_improvement": self._calculate_improvement(),
            "behavioral_changes": len(self.monitoring_data["behavior_changes"])
        }
    
    def _capture_initial_state(self):
        """Capturar estado inicial del núcleo"""
        print("📸 Capturando estado inicial del núcleo...")
        
        # Estado de pesos
        self.initial_weights = {
            "input_weights": self.neural_model.weights.copy(),
            "output_weights": self.neural_model.weights.copy(),
            "weights_sum": float(np.sum(self.neural_model.weights)),
            "weights_mean": float(np.mean(self.neural_model.weights))
        }
        
        # Estado de configuración
        initial_config = {
            "input_size": self.neural_model.input_size,
            "output_size": self.neural_model.output_size,
            "learning_rate": self.neural_model.learning_rate,
            "activation_function": self.neural_model.activation_name,
            "bias_input": float(self.neural_model.bias_input),
            "bias_output": float(self.neural_model.bias_output)
        }
        
        # Rendimiento inicial
        test_inputs = np.random.rand(10, self.neural_model.input_size)
        initial_outputs = []
        for inp in test_inputs:
            output = self.neural_model.forward(inp)
            initial_outputs.append(output.tolist())
        
        self.monitoring_data["initial_state"] = {
            "timestamp": time.time(),
            "weights": self.initial_weights,
            "configuration": initial_config,
            "test_outputs": initial_outputs,
            "response_variance": float(np.var(initial_outputs)),
            "meta_learning_status": self.meta_learning.get_system_status()
        }
        
        print(f"✓ Estado inicial capturado:")
        print(f"  • Suma de pesos: {self.initial_weights['weights_sum']:.4f}")
        print(f"  • Media de pesos: {self.initial_weights['weights_mean']:.4f}")
        print(f"  • Tasa de aprendizaje: {initial_config['learning_rate']}")
        print(f"  • Función activación: {initial_config['activation_function']}")
    
    def _load_ecu_abs_dataset(self) -> List[Dict]:
        """Cargar dataset ECU ABS generado"""
        print("📁 Cargando dataset ECU ABS...")
        
        # Buscar archivo más reciente
        dataset_dir = Path("gym_razonbilstro/datasets/ecu_abs")
        dataset_files = list(dataset_dir.glob("ecu_abs_dataset_100k_*.jsonl"))
        
        if not dataset_files:
            raise FileNotFoundError("No se encontró dataset ECU ABS")
        
        latest_file = max(dataset_files, key=lambda f: f.stat().st_mtime)
        
        # Cargar datos
        dataset = []
        with open(latest_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    dataset.append(entry)
        
        print(f"✓ Dataset cargado: {len(dataset)} ejemplos")
        print(f"  • Archivo: {latest_file.name}")
        print(f"  • Tamaño: {latest_file.stat().st_size / (1024*1024):.1f} MB")
        
        return dataset
    
    def _setup_training_session(self, dataset: List[Dict]) -> Dict:
        """Configurar sesión de entrenamiento"""
        print("⚙️ Configurando sesión de entrenamiento...")
        
        # Crear sesión de metaaprendizaje
        session_id = f"ecu_abs_training_{int(time.time())}"
        temporal_node = self.meta_learning.create_temporal_node(session_id)
        
        # Configuración de entrenamiento
        config = {
            "session_id": session_id,
            "dataset_size": len(dataset),
            "temporal_node": temporal_node,
            "epochs": 100,  # Reducido para monitoreo detallado
            "batch_size": 50,
            "monitoring_interval": 10,  # Cada 10 epochs
            "technical_focus": True,
            "emotion_filtering": True
        }
        
        print(f"✓ Sesión configurada: {session_id}")
        print(f"  • Épocas: {config['epochs']}")
        print(f"  • Tamaño de lote: {config['batch_size']}")
        print(f"  • Nodo temporal activo: {temporal_node.is_active}")
        
        return config
    
    def _execute_monitored_training(self, dataset: List[Dict], config: Dict) -> Dict:
        """Ejecutar entrenamiento con monitoreo completo"""
        print("🚀 Iniciando entrenamiento monitoreado...")
        
        # Preparar datos de entrenamiento
        training_data = self._prepare_training_data(dataset[:1000])  # Primeros 1000 para demo
        
        start_time = time.time()
        epoch_data = []
        
        # Entrenamiento por épocas con monitoreo
        for epoch in range(config["epochs"]):
            epoch_start = time.time()
            
            # Entrenar época
            epoch_results = self._train_epoch(training_data, epoch)
            
            # Monitorear comportamiento
            if epoch % config["monitoring_interval"] == 0:
                behavior = self._monitor_behavior(epoch, epoch_results)
                self.monitoring_data["behavior_changes"].append(behavior)
                
                print(f"Época {epoch:3d}: Loss={epoch_results['loss']:.6f}, "
                      f"Cambio pesos={behavior['weight_change']:.6f}")
            
            # Registrar progresión
            epoch_data.append({
                "epoch": epoch,
                "loss": epoch_results["loss"],
                "accuracy": epoch_results["accuracy"],
                "time_seconds": time.time() - epoch_start,
                "weight_variance": float(np.var(self.neural_model.weights_input))
            })
            
            # Compilar experiencia en nodo temporal
            config["temporal_node"].compile_experience(
                "ecu_training_epoch",
                {
                    "epoch": epoch,
                    "loss": epoch_results["loss"],
                    "dataset_type": "ecu_abs",
                    "success": epoch_results["loss"] < 1.0
                },
                epoch_results["loss"] < 1.0
            )
        
        total_time = time.time() - start_time
        
        # Registrar progresión completa
        self.monitoring_data["training_progression"] = epoch_data
        
        print(f"✓ Entrenamiento completado en {total_time:.2f} segundos")
        print(f"  • Loss final: {epoch_data[-1]['loss']:.6f}")
        print(f"  • Precisión final: {epoch_data[-1]['accuracy']:.3f}")
        
        return {
            "total_epochs": config["epochs"],
            "total_time_seconds": total_time,
            "final_loss": epoch_data[-1]["loss"],
            "final_accuracy": epoch_data[-1]["accuracy"],
            "epoch_data": epoch_data,
            "examples_processed": len(training_data) * config["epochs"]
        }
    
    def _prepare_training_data(self, dataset: List[Dict]) -> List[Dict]:
        """Preparar datos para entrenamiento del modelo neural"""
        training_data = []
        
        for entry in dataset:
            # Extraer entrada técnica
            input_data = entry["input_data"]
            output_data = entry["output_data"]
            
            # Codificar entrada técnica
            if input_data["type"] == "sensor_reading":
                # Codificar lectura de sensor
                encoded_input = [
                    input_data["parameters"]["speed_rpm"] / 2500.0,  # Normalizar RPM
                    1.0 if input_data["parameters"]["wheel_position"] == "FL" else 0.0,
                    1.0 if input_data["parameters"]["sensor_type"] == "hall_effect" else 0.0,
                    float(input_data["timestamp"] % 1000) / 1000.0  # Timestamp normalizado
                ]
                
            elif input_data["type"] == "eeprom_operation":
                # Codificar operación EEPROM
                encoded_input = [
                    1.0 if input_data["parameters"]["operation"] == "read" else 0.5,
                    int(input_data["parameters"]["address"], 16) / 65535.0,  # Normalizar dirección
                    input_data["parameters"]["value"] / 255.0 if input_data["parameters"]["value"] else 0.0,
                    1.0 if input_data["parameters"]["register"] == "WHEEL_SPEED_FL" else 0.0
                ]
            
            else:
                # Codificación genérica
                encoded_input = [0.5, 0.5, 0.5, 0.5]
            
            # Asegurar tamaño correcto
            while len(encoded_input) < self.neural_model.input_size:
                encoded_input.append(0.0)
            encoded_input = encoded_input[:self.neural_model.input_size]
            
            # Codificar salida esperada
            success_value = 1.0 if output_data["status"] in ["success", "diagnosed", "updated"] else 0.0
            encoded_output = [success_value, 0.5, 0.3, 0.7, 0.9][:self.neural_model.output_size]
            
            training_data.append({
                "input": np.array(encoded_input),
                "output": np.array(encoded_output),
                "metadata": {
                    "original_type": input_data["type"],
                    "ecu_component": input_data.get("intent", "unknown")
                }
            })
        
        return training_data
    
    def _train_epoch(self, training_data: List[Dict], epoch: int) -> Dict:
        """Entrenar una época"""
        total_loss = 0.0
        correct_predictions = 0
        
        for data in training_data:
            # Forward pass
            output = self.neural_model.forward(data["input"])
            
            # Calcular error
            error = self.neural_model.backward(data["output"], output)
            total_loss += abs(error)
            
            # Verificar precisión (simplificado)
            predicted = 1 if output[0] > 0.5 else 0
            expected = 1 if data["output"][0] > 0.5 else 0
            if predicted == expected:
                correct_predictions += 1
        
        avg_loss = total_loss / len(training_data)
        accuracy = correct_predictions / len(training_data)
        
        return {
            "loss": avg_loss,
            "accuracy": accuracy,
            "epoch": epoch
        }
    
    def _monitor_behavior(self, epoch: int, epoch_results: Dict) -> Dict:
        """Monitorear comportamiento del núcleo"""
        current_weights = {
            "input_sum": float(np.sum(self.neural_model.weights_input)),
            "output_sum": float(np.sum(self.neural_model.weights_output)),
            "input_mean": float(np.mean(self.neural_model.weights_input)),
            "output_mean": float(np.mean(self.neural_model.weights_output))
        }
        
        # Calcular cambios
        weight_change = abs(current_weights["input_sum"] - self.initial_weights["weights_sum"])
        
        behavior = {
            "epoch": epoch,
            "timestamp": time.time(),
            "loss": epoch_results["loss"],
            "accuracy": epoch_results["accuracy"],
            "weights": current_weights,
            "weight_change": weight_change,
            "learning_stability": "stable" if weight_change < 10.0 else "adapting",
            "bias_drift": {
                "input": float(self.neural_model.bias_input),
                "output": float(self.neural_model.bias_output)
            }
        }
        
        return behavior
    
    def _capture_final_state(self):
        """Capturar estado final del núcleo"""
        print("📸 Capturando estado final del núcleo...")
        
        # Estado final de pesos
        final_weights = {
            "input_weights": self.neural_model.weights_input.copy(),
            "output_weights": self.neural_model.weights_output.copy(),
            "weights_sum": float(np.sum(self.neural_model.weights_input) + np.sum(self.neural_model.weights_output)),
            "weights_mean": float(np.mean(self.neural_model.weights_input))
        }
        
        # Configuración final
        final_config = {
            "input_size": self.neural_model.input_size,
            "output_size": self.neural_model.output_size,
            "learning_rate": self.neural_model.learning_rate,
            "activation_function": self.neural_model.activation_name,
            "bias_input": float(self.neural_model.bias_input),
            "bias_output": float(self.neural_model.bias_output)
        }
        
        # Rendimiento final
        test_inputs = np.random.rand(10, self.neural_model.input_size)
        final_outputs = []
        for inp in test_inputs:
            output = self.neural_model.forward(inp)
            final_outputs.append(output.tolist())
        
        self.monitoring_data["final_state"] = {
            "timestamp": time.time(),
            "weights": final_weights,
            "configuration": final_config,
            "test_outputs": final_outputs,
            "response_variance": float(np.var(final_outputs)),
            "meta_learning_status": self.meta_learning.get_system_status()
        }
        
        print(f"✓ Estado final capturado:")
        print(f"  • Suma de pesos: {final_weights['weights_sum']:.4f}")
        print(f"  • Media de pesos: {final_weights['weights_mean']:.4f}")
        print(f"  • Varianza respuesta: {self.monitoring_data['final_state']['response_variance']:.6f}")
    
    def _calculate_improvement(self) -> Dict:
        """Calcular mejora general"""
        initial = self.monitoring_data["initial_state"]
        final = self.monitoring_data["final_state"]
        
        weight_change = abs(final["weights"]["weights_sum"] - initial["weights"]["weights_sum"])
        variance_change = final["response_variance"] - initial["response_variance"]
        
        return {
            "weight_change_magnitude": weight_change,
            "response_variance_change": variance_change,
            "learning_occurred": weight_change > 0.1,
            "stability_improved": abs(variance_change) < 0.1
        }
    
    def _generate_detailed_report(self, training_results: Dict) -> Path:
        """Generar informe detallado en TXT"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"nucleo_ca_training_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("INFORME DETALLADO - ENTRENAMIENTO NÚCLEO C.A- RAZONBILSTRO\n")
            f.write("=" * 80 + "\n\n")
            
            # Información general
            f.write("1. INFORMACIÓN GENERAL\n")
            f.write("-" * 40 + "\n")
            f.write(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Dataset: ECU ABS (EEPROM/EPROM Programming)\n")
            f.write(f"Ejemplos procesados: {training_results['examples_processed']:,}\n")
            f.write(f"Épocas completadas: {training_results['total_epochs']}\n")
            f.write(f"Tiempo total: {training_results['total_time_seconds']:.2f} segundos\n\n")
            
            # Estado inicial
            f.write("2. ESTADO INICIAL DEL NÚCLEO\n")
            f.write("-" * 40 + "\n")
            initial = self.monitoring_data["initial_state"]
            f.write(f"Configuración:\n")
            f.write(f"  • Tamaño entrada: {initial['configuration']['input_size']}\n")
            f.write(f"  • Tamaño salida: {initial['configuration']['output_size']}\n")
            f.write(f"  • Tasa aprendizaje: {initial['configuration']['learning_rate']}\n")
            f.write(f"  • Función activación: {initial['configuration']['activation_function']}\n\n")
            f.write(f"Pesos iniciales:\n")
            f.write(f"  • Suma total: {initial['weights']['weights_sum']:.6f}\n")
            f.write(f"  • Media: {initial['weights']['weights_mean']:.6f}\n")
            f.write(f"  • Bias entrada: {initial['configuration']['bias_input']:.6f}\n")
            f.write(f"  • Bias salida: {initial['configuration']['bias_output']:.6f}\n\n")
            f.write(f"Rendimiento inicial:\n")
            f.write(f"  • Varianza respuesta: {initial['response_variance']:.6f}\n\n")
            
            # Comportamiento durante entrenamiento
            f.write("3. COMPORTAMIENTO DURANTE ENTRENAMIENTO\n")
            f.write("-" * 40 + "\n")
            f.write(f"Loss inicial: {training_results['epoch_data'][0]['loss']:.6f}\n")
            f.write(f"Loss final: {training_results['final_loss']:.6f}\n")
            f.write(f"Precisión final: {training_results['final_accuracy']:.3f} ({training_results['final_accuracy']*100:.1f}%)\n\n")
            
            f.write("Progresión por épocas (cada 10):\n")
            for i in range(0, len(training_results['epoch_data']), 10):
                epoch_data = training_results['epoch_data'][i]
                f.write(f"  Época {epoch_data['epoch']:3d}: "
                       f"Loss={epoch_data['loss']:.6f}, "
                       f"Precisión={epoch_data['accuracy']:.3f}, "
                       f"Varianza pesos={epoch_data['weight_variance']:.6f}\n")
            f.write("\n")
            
            # Cambios comportamentales detectados
            f.write("Cambios comportamentales detectados:\n")
            for change in self.monitoring_data["behavior_changes"]:
                f.write(f"  Época {change['epoch']:3d}: "
                       f"Estabilidad={change['learning_stability']}, "
                       f"Cambio pesos={change['weight_change']:.6f}\n")
            f.write("\n")
            
            # Estado final
            f.write("4. ESTADO FINAL DEL NÚCLEO\n")
            f.write("-" * 40 + "\n")
            final = self.monitoring_data["final_state"]
            f.write(f"Pesos finales:\n")
            f.write(f"  • Suma total: {final['weights']['weights_sum']:.6f}\n")
            f.write(f"  • Media: {final['weights']['weights_mean']:.6f}\n")
            f.write(f"  • Bias entrada: {final['configuration']['bias_input']:.6f}\n")
            f.write(f"  • Bias salida: {final['configuration']['bias_output']:.6f}\n\n")
            f.write(f"Rendimiento final:\n")
            f.write(f"  • Varianza respuesta: {final['response_variance']:.6f}\n\n")
            
            # Análisis de mejora
            f.write("5. ANÁLISIS DE MEJORA\n")
            f.write("-" * 40 + "\n")
            improvement = self._calculate_improvement()
            f.write(f"Cambio magnitud pesos: {improvement['weight_change_magnitude']:.6f}\n")
            f.write(f"Cambio varianza respuesta: {improvement['response_variance_change']:.6f}\n")
            f.write(f"Aprendizaje detectado: {'SÍ' if improvement['learning_occurred'] else 'NO'}\n")
            f.write(f"Estabilidad mejorada: {'SÍ' if improvement['stability_improved'] else 'NO'}\n\n")
            
            # Metaaprendizaje
            f.write("6. ESTADO DEL METAAPRENDIZAJE\n")
            f.write("-" * 40 + "\n")
            meta_status = final["meta_learning_status"]
            f.write(f"Entradas memoria corta: {meta_status['short_memory_entries']}\n")
            f.write(f"Nodo temporal activo: {'SÍ' if meta_status['temporal_node_active'] else 'NO'}\n")
            f.write(f"Sesiones experiencia: {meta_status['experience_sessions']}\n")
            f.write(f"Patrones aprendidos: {meta_status['total_learned_patterns']}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("FIN DEL INFORME\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ Informe detallado generado: {report_file}")
        return report_file


def main():
    """Función principal"""
    executor = TrainingExecutor()
    
    # Ejecutar entrenamiento completo
    results = executor.execute_full_training_cycle()
    
    print(f"\n🎉 ¡Entrenamiento completado exitosamente!")
    print(f"📊 Ejemplos procesados: {results['total_examples']:,}")
    print(f"📈 Mejora rendimiento: {results['performance_improvement']['learning_occurred']}")
    print(f"📝 Informe: {results['report_file']}")
    print(f"🔄 Cambios comportamentales: {results['behavioral_changes']}")


if __name__ == "__main__":
    main()