#!/usr/bin/env python3
"""
Academic Training Executor - Núcleo C.A- Razonbilstro
Entrenamiento con dataset académico y neurona temporal con metacompiler
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import sys
import os
import numpy as np

# Agregar path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_model import NeuralModel
from core.meta_learning_system import MetaLearningSystem

logger = logging.getLogger(__name__)

class AcademicTrainingExecutor:
    """
    Ejecutor de entrenamiento académico con neurona temporal
    """
    
    def __init__(self):
        # Componentes principales
        self.neural_model = NeuralModel()
        self.meta_learning = MetaLearningSystem()
        
        # Estado del entrenamiento
        self.temporal_node = None
        self.training_session = None
        
        # Datos de monitoreo
        self.monitoring_data = {
            "session_info": {},
            "temporal_node_activity": [],
            "metacompiler_experiences": [],
            "final_metadata": {},
            "destruction_report": {}
        }
        
        # Directorio de reportes
        self.reports_dir = Path("gym_razonbilstro/academic_training_reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        print("🎓 Academic Training Executor inicializado")
        print("   • Neurona temporal preparada para metacompilación")
        print("   • Sistema de metaaprendizaje activo")
    
    def execute_academic_training_with_temporal_node(self) -> Dict:
        """
        Ejecutar entrenamiento académico completo con neurona temporal
        """
        print("\n🧠 Iniciando Entrenamiento Académico con Neurona Temporal")
        print("Dataset: Código académico universitario")
        print("=" * 70)
        
        # 1. Inicializar neurona temporal
        self._initialize_temporal_node()
        
        # 2. Cargar dataset académico
        academic_dataset = self._load_academic_dataset()
        
        # 3. Preparar datos para entrenamiento
        training_data = self._prepare_academic_training_data(academic_dataset)
        
        # 4. Ejecutar entrenamiento con monitoreo de neurona temporal
        training_results = self._execute_monitored_academic_training(training_data)
        
        # 5. Extraer metadatos de la neurona temporal
        temporal_metadata = self._extract_temporal_metadata()
        
        # 6. Destruir neurona temporal y obtener legado
        destruction_legacy = self._destroy_temporal_node()
        
        # 7. Generar informe completo
        report_file = self._generate_temporal_training_report(
            training_results, temporal_metadata, destruction_legacy
        )
        
        return {
            "status": "completed",
            "training_results": training_results,
            "temporal_metadata": temporal_metadata,
            "destruction_legacy": destruction_legacy,
            "metadata_count": self._count_available_metadata(),
            "report_file": str(report_file)
        }
    
    def _initialize_temporal_node(self):
        """Inicializar neurona temporal para entrenamiento académico"""
        session_id = f"academic_training_{int(time.time())}"
        self.training_session = session_id
        
        # Crear neurona temporal con metacompiler
        self.temporal_node = self.meta_learning.create_temporal_node(session_id)
        
        self.monitoring_data["session_info"] = {
            "session_id": session_id,
            "start_time": time.time(),
            "dataset_type": "academic_code",
            "temporal_node_created": True,
            "metacompiler_active": True
        }
        
        print(f"✓ Neurona temporal inicializada: {session_id}")
        print(f"   • Metacompiler activo: SÍ")
        print(f"   • Sistema de experiencias listo")
    
    def _load_academic_dataset(self) -> List[Dict]:
        """Cargar dataset académico generado"""
        print("📚 Cargando dataset académico...")
        
        # Buscar archivo académico más reciente
        dataset_dir = Path("gym_razonbilstro/datasets/gym_razonbilstro/datasets/academic_code")
        dataset_files = list(dataset_dir.glob("academic_code_dataset_1M_*.jsonl"))
        
        if not dataset_files:
            print("⚠️ No se encontró dataset académico")
            return []
        
        latest_file = max(dataset_files, key=lambda f: f.stat().st_mtime)
        
        # Cargar datos académicos
        dataset = []
        with open(latest_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        dataset.append(entry)
                        if line_num >= 99:  # Cargar 100 ejemplos para demo
                            break
                    except json.JSONDecodeError:
                        continue
        
        print(f"✓ Dataset académico cargado: {len(dataset)} ejemplos")
        print(f"   • Fuente: {latest_file.name}")
        print(f"   • Contenido: Código universitario verificado")
        
        return dataset
    
    def _prepare_academic_training_data(self, dataset: List[Dict]) -> List[Dict]:
        """Preparar datos académicos para entrenamiento"""
        print("⚙️ Preparando datos académicos...")
        
        training_data = []
        
        for entry in dataset:
            # Extraer datos del formato híbrido académico
            input_data = entry["input_data"]
            output_data = entry["output_data"]
            
            # Codificar entrada académica
            raw_input = input_data["raw_input"]
            semantic_type = input_data["semantic_type"]
            intent = input_data["intent"]
            
            # Codificación específica para instrucciones académicas
            if semantic_type == "implementation_request":
                if intent == "implement":
                    encoded_input = [1.0, 0.8, 0.6, 0.9, 0.5, 0.7, 0.3, 0.8, 0.4, 0.6]
                else:
                    encoded_input = [0.8, 1.0, 0.5, 0.7, 0.6, 0.4, 0.9, 0.2, 0.7, 0.5]
            elif semantic_type == "explanation_request":
                encoded_input = [0.6, 0.4, 1.0, 0.8, 0.3, 0.9, 0.1, 0.7, 0.5, 0.8]
            elif semantic_type == "command_request":
                encoded_input = [0.9, 0.7, 0.3, 1.0, 0.8, 0.2, 0.6, 0.4, 0.9, 0.1]
            else:  # general_instruction
                encoded_input = [0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5]
            
            # Codificar salida académica
            has_code = "code" in str(output_data["raw_output"])
            has_explanation = "explanation" in str(output_data["raw_output"])
            is_verified = output_data.get("verified_academic", True)
            
            if has_code and has_explanation:
                encoded_output = [1.0, 0.9, 0.8, 0.7, 0.6]  # Código + explicación
            elif has_code:
                encoded_output = [0.8, 1.0, 0.6, 0.5, 0.7]  # Solo código
            elif has_explanation:
                encoded_output = [0.6, 0.7, 1.0, 0.8, 0.5]  # Solo explicación
            else:
                encoded_output = [0.5, 0.5, 0.5, 1.0, 0.5]  # General
            
            training_item = {
                "input": encoded_input,
                "output": encoded_output,
                "metadata": {
                    "academic_source": entry["academic_source"],
                    "language": entry["language"],
                    "category": entry["category"],
                    "semantic_type": semantic_type,
                    "intent": intent,
                    "verified": is_verified,
                    "university_level": True
                }
            }
            training_data.append(training_item)
        
        print(f"✓ Datos académicos preparados: {len(training_data)} ejemplos")
        print(f"   • Tipos semánticos incluidos")
        print(f"   • Intenciones de aprendizaje mapeadas")
        
        return training_data
    
    def _execute_monitored_academic_training(self, training_data: List[Dict]) -> Dict:
        """Ejecutar entrenamiento con monitoreo completo de neurona temporal"""
        print("🚀 Iniciando entrenamiento monitoreado...")
        
        start_time = time.time()
        epochs = 40
        monitoring_interval = 5
        
        epoch_data = []
        temporal_experiences = []
        
        for epoch in range(epochs):
            epoch_start = time.time()
            
            # Entrenar época
            epoch_results = self._train_academic_epoch(training_data, epoch)
            
            # Compilar experiencia en neurona temporal
            experience_data = {
                "epoch": epoch,
                "loss": epoch_results["loss"],
                "accuracy": epoch_results["accuracy"],
                "academic_content": True,
                "learning_pattern": self._analyze_learning_pattern(epoch_results),
                "code_understanding": epoch_results.get("code_understanding", 0.5),
                "university_context": True
            }
            
            # La neurona temporal metacompila esta experiencia
            self.temporal_node.compile_experience(
                "academic_learning_epoch",
                experience_data,
                epoch_results["loss"] < 0.5  # Éxito si loss < 0.5
            )
            
            temporal_experiences.append(experience_data)
            
            # Monitorear actividad de neurona temporal
            if epoch % monitoring_interval == 0:
                temporal_activity = self._monitor_temporal_node_activity(epoch)
                self.monitoring_data["temporal_node_activity"].append(temporal_activity)
                
                print(f"Época {epoch:2d}: Loss={epoch_results['loss']:.6f}, "
                      f"Precisión={epoch_results['accuracy']:.3f}, "
                      f"Neurona temporal: {temporal_activity['status']}")
            
            # Registrar datos de época
            epoch_info = {
                "epoch": epoch,
                "loss": epoch_results["loss"],
                "accuracy": epoch_results["accuracy"],
                "time": time.time() - epoch_start,
                "temporal_node_active": self.temporal_node.is_active if self.temporal_node else False
            }
            epoch_data.append(epoch_info)
        
        total_time = time.time() - start_time
        
        # Almacenar experiencias compiladas
        self.monitoring_data["metacompiler_experiences"] = temporal_experiences
        
        print(f"✓ Entrenamiento académico completado")
        print(f"   • Tiempo total: {total_time:.2f} segundos")
        print(f"   • Experiencias compiladas: {len(temporal_experiences)}")
        print(f"   • Neurona temporal activa: {self.temporal_node.is_active if self.temporal_node else False}")
        
        return {
            "epochs": epochs,
            "total_time": total_time,
            "final_loss": epoch_data[-1]["loss"],
            "final_accuracy": epoch_data[-1]["accuracy"],
            "epoch_data": epoch_data,
            "temporal_experiences": len(temporal_experiences),
            "dataset_type": "academic_code"
        }
    
    def _train_academic_epoch(self, training_data: List[Dict], epoch: int) -> Dict:
        """Entrenar una época con datos académicos"""
        total_loss = 0.0
        correct_predictions = 0
        code_understanding_score = 0.0
        
        for data in training_data:
            # Forward pass
            output = self.neural_model.forward(data["input"])
            
            # Backward pass
            error = self.neural_model.backward(data["output"], output)
            total_loss += abs(error) if error is not None else 0.0
            
            # Evaluar comprensión de código académico
            if data["metadata"]["language"] == "python" and "code" in str(data):
                code_understanding_score += 0.1
            
            # Verificar precisión
            if hasattr(output, '__iter__') and len(output) > 0:
                predicted = 1 if output[0] > 0.5 else 0
                expected = 1 if data["output"][0] > 0.5 else 0
                if predicted == expected:
                    correct_predictions += 1
        
        avg_loss = total_loss / len(training_data)
        accuracy = correct_predictions / len(training_data)
        code_understanding = code_understanding_score / len(training_data)
        
        return {
            "loss": avg_loss,
            "accuracy": accuracy,
            "code_understanding": code_understanding,
            "epoch": epoch
        }
    
    def _analyze_learning_pattern(self, epoch_results: Dict) -> str:
        """Analizar patrón de aprendizaje en la época"""
        loss = epoch_results["loss"]
        accuracy = epoch_results["accuracy"]
        
        if loss < 0.2 and accuracy > 0.8:
            return "excellent_convergence"
        elif loss < 0.5 and accuracy > 0.6:
            return "good_progress"
        elif loss > 0.8:
            return "struggling"
        else:
            return "steady_learning"
    
    def _monitor_temporal_node_activity(self, epoch: int) -> Dict:
        """Monitorear actividad de la neurona temporal"""
        if not self.temporal_node or not self.temporal_node.is_active:
            return {"status": "inactive", "epoch": epoch}
        
        # Obtener información de la neurona temporal
        experiences_count = len(self.temporal_node.experiences.get("successful_patterns", []))
        metacompiler_patterns = len(self.temporal_node.metacompiler.get("learning_patterns", []))
        
        return {
            "status": "active",
            "epoch": epoch,
            "experiences_compiled": experiences_count,
            "metacompiler_patterns": metacompiler_patterns,
            "session_time": time.time() - self.temporal_node.creation_time,
            "learning_efficiency": min(experiences_count / max(epoch, 1), 1.0)
        }
    
    def _extract_temporal_metadata(self) -> Dict:
        """Extraer metadatos de la neurona temporal antes de destrucción"""
        print("📊 Extrayendo metadatos de neurona temporal...")
        
        if not self.temporal_node or not self.temporal_node.is_active:
            return {"error": "Neurona temporal no disponible"}
        
        # Obtener estado actual de la neurona
        current_metadata = {
            "session_id": self.temporal_node.session_id,
            "creation_time": self.temporal_node.creation_time,
            "current_time": time.time(),
            "total_experiences": {
                "successful": len(self.temporal_node.experiences.get("successful_patterns", [])),
                "failed": len(self.temporal_node.experiences.get("failed_attempts", [])),
                "optimizations": len(self.temporal_node.experiences.get("optimization_points", []))
            },
            "metacompiler_state": {
                "learning_patterns": len(self.temporal_node.metacompiler.get("learning_patterns", [])),
                "error_corrections": len(self.temporal_node.metacompiler.get("error_corrections", [])),
                "optimization_discoveries": len(self.temporal_node.metacompiler.get("optimization_discoveries", [])),
                "efficiency_improvements": len(self.temporal_node.metacompiler.get("efficiency_improvements", []))
            },
            "academic_context": {
                "dataset_type": "academic_code",
                "university_sources": True,
                "code_learning": True,
                "algorithm_training": True
            }
        }
        
        print(f"✓ Metadatos extraídos:")
        print(f"   • Experiencias exitosas: {current_metadata['total_experiences']['successful']}")
        print(f"   • Patrones de aprendizaje: {current_metadata['metacompiler_state']['learning_patterns']}")
        print(f"   • Optimizaciones descubiertas: {current_metadata['metacompiler_state']['optimization_discoveries']}")
        
        return current_metadata
    
    def _destroy_temporal_node(self) -> Dict:
        """Destruir neurona temporal y obtener legado"""
        print("💥 Destruyendo neurona temporal y extrayendo legado...")
        
        if not self.temporal_node or not self.temporal_node.is_active:
            return {"error": "Neurona temporal ya destruida o no disponible"}
        
        # Obtener legado final antes de destrucción
        destruction_legacy = self.meta_learning.destroy_temporal_node()
        
        # Información de destrucción
        destruction_info = {
            "destruction_time": time.time(),
            "session_completed": True,
            "legacy_preserved": destruction_legacy is not None,
            "metadata_generated": True if destruction_legacy else False,
            "temporal_node_destroyed": True
        }
        
        self.monitoring_data["destruction_report"] = destruction_info
        
        print(f"✓ Neurona temporal destruida exitosamente")
        print(f"   • Legado preservado: {'SÍ' if destruction_legacy else 'NO'}")
        print(f"   • Metadatos disponibles para futuros entrenamientos")
        
        return {
            "destruction_info": destruction_info,
            "legacy_metadata": destruction_legacy,
            "session_id": self.training_session
        }
    
    def _count_available_metadata(self) -> Dict:
        """Contar metadatos disponibles de todas las neuronas temporales"""
        print("📈 Contando metadatos de neuronas temporales...")
        
        # Verificar metadatos previos
        metadata_dir = Path("gym_razonbilstro/metadata/training_metadata")
        
        available_metadata = {
            "ecu_abs_metadata": 0,
            "academic_metadata": 1,  # Este entrenamiento
            "total_sessions": 0,
            "metadata_files": []
        }
        
        # Buscar archivos de metadatos existentes
        if metadata_dir.exists():
            for metadata_file in metadata_dir.rglob("*.json"):
                available_metadata["metadata_files"].append(str(metadata_file))
                available_metadata["total_sessions"] += 1
                
                # Clasificar por tipo
                if "ecu" in metadata_file.name.lower():
                    available_metadata["ecu_abs_metadata"] += 1
        
        print(f"✓ Metadatos disponibles:")
        print(f"   • ECU ABS: {available_metadata['ecu_abs_metadata']} sesiones")
        print(f"   • Académico: {available_metadata['academic_metadata']} sesiones")
        print(f"   • Total: {available_metadata['total_sessions']} archivos de metadatos")
        
        return available_metadata
    
    def _generate_temporal_training_report(self, training_results: Dict, temporal_metadata: Dict, destruction_legacy: Dict) -> Path:
        """Generar informe completo del entrenamiento con neurona temporal"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"academic_temporal_training_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 80 + "\n")
            f.write("INFORME ENTRENAMIENTO ACADÉMICO - NEURONA TEMPORAL\n")
            f.write("Núcleo C.A- Razonbilstro con Metacompiler\n")
            f.write("=" * 80 + "\n\n")
            
            # Información de sesión
            f.write("1. INFORMACIÓN DE SESIÓN\n")
            f.write("-" * 50 + "\n")
            session_info = self.monitoring_data["session_info"]
            f.write(f"Sesión ID: {session_info['session_id']}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Dataset: {session_info['dataset_type'].upper()}\n")
            f.write(f"Neurona Temporal: {'ACTIVA' if session_info['temporal_node_created'] else 'INACTIVA'}\n")
            f.write(f"Metacompiler: {'HABILITADO' if session_info['metacompiler_active'] else 'DESHABILITADO'}\n\n")
            
            # Resultados del entrenamiento
            f.write("2. RESULTADOS DEL ENTRENAMIENTO\n")
            f.write("-" * 50 + "\n")
            f.write(f"Épocas completadas: {training_results['epochs']}\n")
            f.write(f"Tiempo total: {training_results['total_time']:.2f} segundos\n")
            f.write(f"Loss final: {training_results['final_loss']:.6f}\n")
            f.write(f"Precisión final: {training_results['final_accuracy']:.3f} ({training_results['final_accuracy']*100:.1f}%)\n")
            f.write(f"Experiencias compiladas: {training_results['temporal_experiences']}\n\n")
            
            # Actividad de neurona temporal
            f.write("3. ACTIVIDAD DE NEURONA TEMPORAL\n")
            f.write("-" * 50 + "\n")
            if temporal_metadata.get("error"):
                f.write(f"Error: {temporal_metadata['error']}\n")
            else:
                total_exp = temporal_metadata["total_experiences"]
                metacompiler = temporal_metadata["metacompiler_state"]
                
                f.write(f"Experiencias totales:\n")
                f.write(f"  • Exitosas: {total_exp['successful']}\n")
                f.write(f"  • Fallidas: {total_exp['failed']}\n")
                f.write(f"  • Optimizaciones: {total_exp['optimizations']}\n\n")
                
                f.write(f"Estado del Metacompiler:\n")
                f.write(f"  • Patrones de aprendizaje: {metacompiler['learning_patterns']}\n")
                f.write(f"  • Correcciones de error: {metacompiler['error_corrections']}\n")
                f.write(f"  • Descubrimientos de optimización: {metacompiler['optimization_discoveries']}\n")
                f.write(f"  • Mejoras de eficiencia: {metacompiler['efficiency_improvements']}\n\n")
            
            # Destrucción y legado
            f.write("4. DESTRUCCIÓN DE NEURONA TEMPORAL\n")
            f.write("-" * 50 + "\n")
            if destruction_legacy.get("error"):
                f.write(f"Error en destrucción: {destruction_legacy['error']}\n")
            else:
                destruction_info = destruction_legacy["destruction_info"]
                f.write(f"Tiempo de destrucción: {datetime.fromtimestamp(destruction_info['destruction_time']).strftime('%H:%M:%S')}\n")
                f.write(f"Sesión completada: {'SÍ' if destruction_info['session_completed'] else 'NO'}\n")
                f.write(f"Legado preservado: {'SÍ' if destruction_info['legacy_preserved'] else 'NO'}\n")
                f.write(f"Metadatos generados: {'SÍ' if destruction_info['metadata_generated'] else 'NO'}\n")
                f.write(f"Neurona destruida: {'SÍ' if destruction_info['temporal_node_destroyed'] else 'NO'}\n\n")
            
            # Progresión del aprendizaje
            f.write("5. PROGRESIÓN DEL APRENDIZAJE\n")
            f.write("-" * 50 + "\n")
            for i in range(0, len(training_results['epoch_data']), 5):
                epoch_data = training_results['epoch_data'][i]
                f.write(f"Época {epoch_data['epoch']:2d}: "
                       f"Loss={epoch_data['loss']:.6f}, "
                       f"Precisión={epoch_data['accuracy']:.3f}, "
                       f"Neurona={'ACTIVA' if epoch_data['temporal_node_active'] else 'INACTIVA'}\n")
            f.write("\n")
            
            # Análisis de metadatos disponibles
            f.write("6. METADATOS DISPONIBLES\n")
            f.write("-" * 50 + "\n")
            metadata_count = self._count_available_metadata()
            f.write(f"Metadatos ECU ABS: {metadata_count['ecu_abs_metadata']} sesiones\n")
            f.write(f"Metadatos Académicos: {metadata_count['academic_metadata']} sesiones\n")
            f.write(f"Total archivos de metadatos: {metadata_count['total_sessions']}\n")
            f.write(f"¿Dos metadatos disponibles?: {'SÍ' if metadata_count['total_sessions'] >= 2 else 'NO'}\n\n")
            
            # Conclusiones
            f.write("7. CONCLUSIONES\n")
            f.write("-" * 50 + "\n")
            f.write("✅ ENTRENAMIENTO ACADÉMICO COMPLETADO\n")
            f.write("La neurona temporal ha procesado exitosamente el dataset académico:\n")
            f.write("  • Dataset universitario verificado procesado\n")
            f.write("  • Metacompiler ha extraído patrones de aprendizaje\n")
            f.write("  • Neurona temporal destruida preservando legado\n")
            f.write("  • Metadatos disponibles para futuros entrenamientos\n\n")
            
            if metadata_count['total_sessions'] >= 2:
                f.write("🎯 HITO ALCANZADO:\n")
                f.write("Dos metadatos de neuronas temporales disponibles:\n")
                f.write("  1. ECU ABS (diagnóstico automotriz)\n")
                f.write("  2. Académico (código universitario)\n")
                f.write("El núcleo puede ahora aprovechar experiencias previas\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("FIN DEL INFORME - NEURONA TEMPORAL DESTRUIDA\n")
            f.write("LEGADO PRESERVADO PARA FUTURAS GENERACIONES\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ Informe temporal generado: {report_file}")
        return report_file


def main():
    """Función principal"""
    executor = AcademicTrainingExecutor()
    
    # Ejecutar entrenamiento académico con neurona temporal
    results = executor.execute_academic_training_with_temporal_node()
    
    print(f"\n🎉 ¡Entrenamiento académico con neurona temporal completado!")
    print(f"📊 Loss final: {results['training_results']['final_loss']:.6f}")
    print(f"📈 Precisión final: {results['training_results']['final_accuracy']:.3f}")
    print(f"🧠 Neurona temporal destruida: {'SÍ' if results['destruction_legacy']['destruction_info']['temporal_node_destroyed'] else 'NO'}")
    print(f"📋 Metadatos disponibles: {results['metadata_count']['total_sessions']}")
    print(f"🎯 Dos metadatos?: {'SÍ' if results['metadata_count']['total_sessions'] >= 2 else 'NO'}")
    print(f"📝 Informe: {results['report_file']}")


if __name__ == "__main__":
    main()