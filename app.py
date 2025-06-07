"""
Flask application for "Núcleo C.A- Razonbilstro" neural model
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session, flash
from neural_model import default_model

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret-key")

# Global conversation history
conversation_history = []

@app.route('/')
def index():
    """Render the main page with the conversation interface"""
    model_info = {
        "name": default_model.metadata["name"],
        "version": default_model.metadata["version"],
        "description": default_model.metadata["description"],
        "input_size": default_model.input_size,
        "output_size": default_model.output_size,
        "activation": default_model.activation_name,
        "training_epochs": default_model.epoch_count
    }
    
    return render_template('index.html', model_info=model_info)

@app.route('/about')
def about():
    """Render the about page with details about the model"""
    model_info = {
        "name": default_model.metadata["name"],
        "version": default_model.metadata["version"],
        "description": default_model.metadata["description"],
        "created": default_model.metadata["created"],
        "input_size": default_model.input_size,
        "output_size": default_model.output_size,
        "activation": default_model.activation_name,
        "training_epochs": default_model.epoch_count,
        "learning_rate": default_model.learning_rate,
        "memory_size": default_model.memory_size,
        "error_history": default_model.error_history[-10:] if default_model.error_history else []
    }
    
    return render_template('about.html', model_info=model_info)

@app.route('/live-monitoring')
def live_monitoring():
    """Render the live monitoring page for neurona temporal"""
    return render_template('live_monitoring.html')

@app.route('/api/process', methods=['POST'])
def process_input():
    """Process user input and return the model's response"""
    try:
        data = request.get_json()
        user_input = data.get('input', '').strip()
        
        if not user_input:
            return jsonify({
                'success': False,
                'error': 'Input cannot be empty'
            }), 400
        
        # Process input with the model
        response = default_model.process_input(user_input)
        
        # Add to conversation history
        global conversation_history
        conversation_history.append({
            'user': user_input,
            'model': response
        })
        
        # Keep only the last 10 exchanges
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        return jsonify({
            'success': True,
            'response': response,
            'conversation': conversation_history
        })
    
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear the conversation history"""
    try:
        global conversation_history
        conversation_history = []
        
        # Also clear the model's memory
        default_model.memory = []
        
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        })
    
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train the model with user-provided data"""
    try:
        data = request.get_json()
        inputs = data.get('inputs', [])
        targets = data.get('targets', [])
        epochs = data.get('epochs', 100)
        
        if not inputs or not targets:
            return jsonify({
                'success': False,
                'error': 'Inputs and targets are required'
            }), 400
        
        if len(inputs) != len(targets):
            return jsonify({
                'success': False,
                'error': 'Number of inputs must match number of targets'
            }), 400
        
        # Train the model
        error_history = default_model.train(inputs, targets, epochs=epochs)
        
        # Save the trained model
        default_model.save_model()
        
        return jsonify({
            'success': True,
            'message': f'Model trained for {epochs} epochs',
            'final_error': error_history[-1] if error_history else None
        })
    
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
