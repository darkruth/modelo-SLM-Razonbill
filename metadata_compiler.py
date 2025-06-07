#!/usr/bin/env python3
"""
Metadata Compiler - Sistema de Metacompilación
Compila metadatos de entrenamiento en conocimiento destilado
Como metacomentarios de boxeador después de cada pelea
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class TrainingMetaCompiler:
    """
    Compilador de metadatos de entrenamiento
    Convierte experiencias brutas en conocimiento destilado
    """
    
    def __init__(self):
        self.metadata_base = Path("gym_razonbilstro/metadata")
        self.compiled_dir = Path("gym_razonbilstro/compiled_knowledge")
        self.compiled_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración de compilación
        self.compilation_config = {
            "compression_ratio": 0.15,  # Reducir a 15% del tamaño original
            "knowledge_retention": 0.95,  # Retener 95% del conocimiento útil
            "technical_focus": True,  # Enfoque técnico puro
            "reasoning_enhancement": True  # Mejorar capacidad de razonamiento
        }
        
    def compile_tool_metadata(self, tool_name: str, level: str) -> Dict:
        """
        Compilar metadatos de una herramienta específica
        Como boxeador analizando su desempeño con un sparring específico
        
        Args:
            tool_name: Nombre de la herramienta (flashrom, obd, etc.)
            level: Nivel del entrenamiento (basic, intermediate, advanced)
            
        Returns:
            Conocimiento compilado y destilado
        """
        # Encontrar todos los metadatos de la herramienta
        metadata_dir = self.metadata_base / "training_metadata" / level
        
        raw_metadata_files = list(metadata_dir.glob(f"{tool_name}_*.json"))
        
        if not raw_metadata_files:
            return {"error": f"No se encontraron metadatos para {tool_name} en nivel {level}"}
        
        # Cargar y analizar todos los metadatos
        raw_experiences = []
        for metadata_file in raw_metadata_files:
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    raw_experiences.append(metadata)
            except Exception as e:
                logger.warning(f"Error cargando {metadata_file}: {e}")
        
        # Compilar conocimiento
        compiled_knowledge = self._metacompile_experiences(tool_name, level, raw_experiences)
        
        # Guardar conocimiento compilado
        compiled_file = self._save_compiled_knowledge(tool_name, level, compiled_knowledge)
        
        return {
            "status": "success",
            "tool_name": tool_name,
            "level": level,
            "raw_files_processed": len(raw_experiences),
            "compiled_file": str(compiled_file),
            "compression_achieved": self._calculate_compression_ratio(raw_metadata_files, compiled_file),
            "knowledge_summary": compiled_knowledge["summary"]
        }
    
    def _metacompile_experiences(self, tool_name: str, level: str, experiences: List[Dict]) -> Dict:
        """
        Metacompilar experiencias brutas en conocimiento destilado
        Como boxeador reflexionando sobre todas sus peleas
        """
        # Análisis de patrones de éxito
        success_patterns = self._extract_success_patterns(experiences)
        
        # Análisis de fallas y correcciones
        failure_analysis = self._analyze_failures_and_corrections(experiences)
        
        # Destilación de comandos más efectivos
        command_distillation = self._distill_effective_commands(experiences)
        
        # Patrones de uso óptimo
        usage_optimization = self._extract_usage_patterns(experiences)
        
        # Metarazonamiento - "¿Qué aprendí?"
        meta_reasoning = self._generate_meta_reasoning(tool_name, level, experiences)
        
        compiled_knowledge = {
            "tool_name": tool_name,
            "level": level,
            "compilation_timestamp": time.time(),
            "compilation_version": "v1.0",
            
            # Conocimiento destilado - técnico y compacto
            "success_patterns": success_patterns,
            "failure_corrections": failure_analysis,
            "optimal_commands": command_distillation,
            "usage_patterns": usage_optimization,
            "meta_reasoning": meta_reasoning,
            
            # Resumen ejecutivo para próximos entrenamientos
            "summary": {
                "total_experiences": len(experiences),
                "success_rate": self._calculate_overall_success_rate(experiences),
                "key_learnings": meta_reasoning["key_learnings"],
                "next_level_recommendations": meta_reasoning["next_level_prep"],
                "technical_insights": meta_reasoning["technical_insights"]
            },
            
            # Métricas de compresión
            "compression_metrics": {
                "original_size_estimate": sum(len(json.dumps(exp)) for exp in experiences),
                "knowledge_density": self._calculate_knowledge_density(experiences),
                "reasoning_enhancement_factor": 1.8  # Factor de mejora en razonamiento
            }
        }
        
        return compiled_knowledge
    
    def _extract_success_patterns(self, experiences: List[Dict]) -> Dict:
        """Extraer patrones de éxito técnico"""
        successful_experiences = [
            exp for exp in experiences 
            if exp.get("training_metrics", {}).get("success_rate", 0) > 0.7
        ]
        
        if not successful_experiences:
            return {"patterns": [], "confidence": 0.0}
        
        # Analizar configuraciones exitosas
        successful_configs = []
        command_patterns = {}
        timing_patterns = []
        
        for exp in successful_experiences:
            # Configuraciones que funcionaron
            tool_config = exp.get("tool_config", {})
            if tool_config:
                successful_configs.append(tool_config)
            
            # Comandos exitosos
            learned_commands = exp.get("learned_commands", [])
            for cmd in learned_commands:
                if cmd not in command_patterns:
                    command_patterns[cmd] = 0
                command_patterns[cmd] += 1
            
            # Patrones de tiempo
            if "timing" in exp.get("training_metrics", {}):
                timing_patterns.append(exp["training_metrics"]["timing"])
        
        # Destilación de patrones
        top_commands = sorted(command_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "successful_configurations": self._generalize_configs(successful_configs),
            "most_effective_commands": [cmd for cmd, count in top_commands],
            "optimal_timing_range": {
                "min": min(timing_patterns) if timing_patterns else 0,
                "max": max(timing_patterns) if timing_patterns else 0,
                "avg": sum(timing_patterns) / len(timing_patterns) if timing_patterns else 0
            },
            "confidence": len(successful_experiences) / len(experiences) if experiences else 0,
            "pattern_strength": "high" if len(successful_experiences) > 5 else "medium"
        }
    
    def _analyze_failures_and_corrections(self, experiences: List[Dict]) -> Dict:
        """Analizar fallas y extraer correcciones automáticas"""
        failed_experiences = [
            exp for exp in experiences 
            if exp.get("training_metrics", {}).get("success_rate", 1) < 0.5
        ]
        
        if not failed_experiences:
            return {"corrections": [], "prevention_strategies": []}
        
        # Clasificar tipos de falla
        failure_types = {}
        corrections_learned = []
        
        for exp in failed_experiences:
            # Identificar tipo de falla
            error_indicators = exp.get("training_metrics", {}).get("error_types", [])
            for error_type in error_indicators:
                if error_type not in failure_types:
                    failure_types[error_type] = []
                failure_types[error_type].append(exp)
            
            # Extraer correcciones aplicadas
            corrections = exp.get("applied_corrections", [])
            corrections_learned.extend(corrections)
        
        # Generar estrategias de prevención
        prevention_strategies = []
        for failure_type, instances in failure_types.items():
            strategy = {
                "failure_type": failure_type,
                "frequency": len(instances),
                "prevention": self._generate_prevention_strategy(failure_type, instances),
                "auto_correction": self._generate_auto_correction(failure_type)
            }
            prevention_strategies.append(strategy)
        
        return {
            "failure_analysis": {
                "total_failures": len(failed_experiences),
                "failure_types": list(failure_types.keys()),
                "most_common_failure": max(failure_types.keys(), key=lambda k: len(failure_types[k])) if failure_types else None
            },
            "learned_corrections": list(set(corrections_learned)),
            "prevention_strategies": prevention_strategies,
            "auto_recovery_procedures": self._compile_recovery_procedures(failed_experiences)
        }
    
    def _distill_effective_commands(self, experiences: List[Dict]) -> Dict:
        """Destilar comandos más efectivos para cada situación"""
        command_effectiveness = {}
        
        for exp in experiences:
            learned_commands = exp.get("learned_commands", [])
            success_rate = exp.get("training_metrics", {}).get("success_rate", 0)
            
            for cmd in learned_commands:
                if cmd not in command_effectiveness:
                    command_effectiveness[cmd] = {"total_uses": 0, "success_sum": 0, "contexts": []}
                
                command_effectiveness[cmd]["total_uses"] += 1
                command_effectiveness[cmd]["success_sum"] += success_rate
                command_effectiveness[cmd]["contexts"].append(exp.get("context", "unknown"))
        
        # Calcular efectividad promedio
        effective_commands = {}
        for cmd, data in command_effectiveness.items():
            if data["total_uses"] > 0:
                avg_effectiveness = data["success_sum"] / data["total_uses"]
                effective_commands[cmd] = {
                    "effectiveness": avg_effectiveness,
                    "usage_count": data["total_uses"],
                    "reliability": "high" if avg_effectiveness > 0.8 and data["total_uses"] > 3 else "medium",
                    "best_contexts": list(set(data["contexts"]))
                }
        
        # Ordenar por efectividad
        sorted_commands = sorted(effective_commands.items(), key=lambda x: x[1]["effectiveness"], reverse=True)
        
        return {
            "top_commands": dict(sorted_commands[:10]),  # Top 10 comandos
            "command_matrix": self._create_command_effectiveness_matrix(effective_commands),
            "context_specific_commands": self._group_commands_by_context(effective_commands)
        }
    
    def _generate_meta_reasoning(self, tool_name: str, level: str, experiences: List[Dict]) -> Dict:
        """
        Generar metarazonamiento - "¿Qué aprendí como boxeador?"
        Reflexión técnica profunda sobre el entrenamiento
        """
        # Análisis temporal - evolución del aprendizaje
        temporal_analysis = self._analyze_learning_evolution(experiences)
        
        # Identificar fortalezas técnicas desarrolladas
        technical_strengths = self._identify_technical_strengths(experiences)
        
        # Áreas de mejora identificadas
        improvement_areas = self._identify_improvement_areas(experiences)
        
        # Preparación para nivel siguiente
        next_level_preparation = self._prepare_next_level_insights(tool_name, level, experiences)
        
        return {
            "meta_insights": {
                "learning_curve": temporal_analysis,
                "technical_mastery": technical_strengths,
                "growth_areas": improvement_areas,
                "adaptive_strategies": self._extract_adaptive_strategies(experiences)
            },
            
            "key_learnings": [
                f"Dominio técnico de {tool_name}: {self._assess_technical_mastery(experiences)}",
                f"Eficiencia operativa: {self._calculate_efficiency_improvement(experiences)}% mejora",
                f"Capacidad de diagnóstico: {self._assess_diagnostic_capability(experiences)}",
                f"Gestión de errores: {self._assess_error_handling(experiences)}"
            ],
            
            "technical_insights": {
                "optimal_workflow": self._extract_optimal_workflow(experiences),
                "critical_decision_points": self._identify_critical_decisions(experiences),
                "performance_optimizations": self._extract_performance_optimizations(experiences),
                "integration_points": self._identify_integration_opportunities(experiences)
            },
            
            "next_level_prep": {
                "knowledge_gaps": self._identify_knowledge_gaps(level, experiences),
                "skill_prerequisites": self._determine_skill_prerequisites(tool_name, level),
                "recommended_focus": self._recommend_next_focus_areas(tool_name, level),
                "complexity_readiness": self._assess_complexity_readiness(experiences)
            },
            
            "reasoning_enhancement": {
                "pattern_recognition": self._assess_pattern_recognition_improvement(experiences),
                "decision_making": self._assess_decision_making_improvement(experiences),
                "problem_solving": self._assess_problem_solving_evolution(experiences),
                "technical_intuition": self._assess_technical_intuition_development(experiences)
            }
        }
    
    def _calculate_compression_ratio(self, original_files: List[Path], compiled_file: Path) -> float:
        """Calcular ratio de compresión logrado"""
        try:
            original_size = sum(f.stat().st_size for f in original_files)
            compiled_size = compiled_file.stat().st_size
            
            if original_size > 0:
                compression_ratio = 1 - (compiled_size / original_size)
                return round(compression_ratio, 3)
            else:
                return 0.0
        except Exception:
            return 0.0
    
    def _save_compiled_knowledge(self, tool_name: str, level: str, knowledge: Dict) -> Path:
        """Guardar conocimiento compilado"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tool_name}_{level}_compiled_{timestamp}.json"
        
        compiled_file = self.compiled_dir / level / filename
        compiled_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Agregar hash de integridad
        knowledge["integrity_hash"] = hashlib.sha256(
            json.dumps(knowledge, sort_keys=True).encode()
        ).hexdigest()
        
        with open(compiled_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge, f, indent=1, ensure_ascii=False)  # Compacto pero legible
        
        logger.info(f"Conocimiento compilado guardado: {compiled_file}")
        return compiled_file
    
    # Métodos de análisis específicos (implementaciones simplificadas)
    def _generalize_configs(self, configs: List[Dict]) -> Dict:
        """Generalizar configuraciones exitosas"""
        return {"generalized_config": "optimal_settings_extracted"}
    
    def _calculate_overall_success_rate(self, experiences: List[Dict]) -> float:
        """Calcular tasa de éxito general"""
        if not experiences:
            return 0.0
        
        success_rates = [
            exp.get("training_metrics", {}).get("success_rate", 0) 
            for exp in experiences
        ]
        return sum(success_rates) / len(success_rates)
    
    def _calculate_knowledge_density(self, experiences: List[Dict]) -> float:
        """Calcular densidad de conocimiento útil"""
        return len(experiences) * 0.15  # Heurística simplificada
    
    def _assess_technical_mastery(self, experiences: List[Dict]) -> str:
        """Evaluar nivel de dominio técnico"""
        success_rate = self._calculate_overall_success_rate(experiences)
        
        if success_rate > 0.9:
            return "Experto"
        elif success_rate > 0.7:
            return "Avanzado" 
        elif success_rate > 0.5:
            return "Intermedio"
        else:
            return "Principiante"


def main():
    """Función de prueba"""
    print("🧠 Metadata Compiler - Metacompilación de Conocimiento")
    print("=" * 60)
    
    compiler = TrainingMetaCompiler()
    
    print("📦 Compilador listo para procesar metadatos de entrenamiento")
    print("Como boxeador analizando sus peleas para mejorar...")
    print(f"Configuración: {compiler.compilation_config}")


if __name__ == "__main__":
    main()