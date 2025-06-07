from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class NucleoMetadata(db.Model):
    """Metadatos del núcleo con información de dominios"""
    __tablename__ = 'nucleo_metadata'
    
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(100), nullable=False)
    temporal_node_id = db.Column(db.String(200), nullable=False)
    training_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    precision_score = db.Column(db.Float, nullable=False)
    loss_final = db.Column(db.Float, nullable=False)
    experiences_count = db.Column(db.Integer, nullable=False)
    metadata_json = db.Column(db.Text)  # JSON con metadatos completos
    
    def __repr__(self):
        return f'<NucleoMetadata {self.domain_name}>'

class KaliDataset(db.Model):
    """Dataset híbrido de herramientas Kali Linux"""
    __tablename__ = 'kali_dataset'
    
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Input data híbrido
    input_raw = db.Column(db.Text, nullable=False)
    input_tokens = db.Column(db.Text, nullable=False)  # JSON array
    input_semantic_type = db.Column(db.String(50))
    input_intent = db.Column(db.String(50))
    
    # Output data binarizado
    output_command = db.Column(db.Text, nullable=False)
    output_explanation = db.Column(db.Text, nullable=False)
    output_tokens = db.Column(db.Text, nullable=False)  # JSON array
    output_binary_int8 = db.Column(db.Text, nullable=False)  # JSON array
    
    # Metadatos Kali
    kali_official = db.Column(db.Boolean, default=True)
    security_category = db.Column(db.String(100))
    complexity_score = db.Column(db.Integer)
    fuzzy_mapping = db.Column(db.Text)  # JSON con mapeo fuzzy
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<KaliDataset {self.tool_name}>'

class QueryHistory(db.Model):
    """Historial de consultas al núcleo"""
    __tablename__ = 'query_history'
    
    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.Text, nullable=False)
    domain_used = db.Column(db.String(100))
    response_generated = db.Column(db.Text)
    confidence_score = db.Column(db.Float)
    execution_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QueryHistory {self.id}>'