"""
Neural Model: Núcleo C.A- Razonbilstro
A simple Single Language Model implementation
"""

import numpy as np
import random
import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NeuralModel:
    """
    Núcleo C.A- Razonbilstro: A simple neural network model
    Implements a single language model with customizable activation functions
    """
    
    def __init__(self, input_size=10, output_size=5, learning_rate=0.01, activation='sigmoid'):
        """
        Initialize the neural network
        
        Args:
            input_size: Size of the input layer
            output_size: Size of the output layer
            learning_rate: Learning rate for weight updates
            activation: Activation function ('sigmoid', 'tanh', 'relu')
        """
        self.input_size = input_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.activation_name = activation
        
        # Set activation function
        if activation == 'sigmoid':
            self.activation = self.sigmoid
            self.activation_derivative = self.sigmoid_derivative
        elif activation == 'tanh':
            self.activation = self.tanh
            self.activation_derivative = self.tanh_derivative
        elif activation == 'relu':
            self.activation = self.relu
            self.activation_derivative = self.relu_derivative
        else:
            logger.warning(f"Unknown activation function: {activation}. Using sigmoid instead.")
            self.activation = self.sigmoid
            self.activation_derivative = self.sigmoid_derivative
            self.activation_name = 'sigmoid'
        
        # Initialize weights and biases
        self.weights = np.random.randn(input_size, output_size) * 0.1
        self.bias = np.random.randn(output_size) * 0.1
        
        # Training history
        self.error_history = []
        self.epoch_count = 0
        
        # Memory for conversational context
        self.memory = []
        self.memory_size = 5
        
        # Model metadata
        self.metadata = {
            "name": "Núcleo C.A- Razonbilstro",
            "version": "1.0.0",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Simple SLM Neural Model for text processing"
        }
        
        logger.info(f"Initialized {self.metadata['name']} neural model")
        logger.debug(f"Input size: {input_size}, Output size: {output_size}")
    
    # Activation functions
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x):
        """Derivative of sigmoid function"""
        sig = self.sigmoid(x)
        return sig * (1 - sig)
    
    def tanh(self, x):
        """Hyperbolic tangent activation function"""
        return np.tanh(x)
    
    def tanh_derivative(self, x):
        """Derivative of tanh function"""
        return 1 - np.tanh(x) ** 2
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Derivative of ReLU function"""
        return np.where(x > 0, 1, 0)
    
    def forward(self, inputs):
        """
        Forward pass through the network
        
        Args:
            inputs: Input data (vector)
            
        Returns:
            Output after passing through the network
        """
        # Ensure inputs are in numpy array format
        inputs = np.array(inputs)
        
        # Calculate weighted sum
        self.last_inputs = inputs
        self.weighted_sum = np.dot(inputs, self.weights) + self.bias
        
        # Apply activation function
        self.outputs = self.activation(self.weighted_sum)
        
        return self.outputs
    
    def backward(self, targets, outputs=None):
        """
        Backward pass to update weights
        
        Args:
            targets: Target values
            outputs: Output values (if not provided, uses last outputs)
            
        Returns:
            Error value
        """
        if outputs is None:
            outputs = self.outputs
        
        # Calculate error
        error = targets - outputs
        
        # Calculate delta
        delta = error * self.activation_derivative(self.weighted_sum)
        
        # Update weights and bias
        self.weights += self.learning_rate * np.outer(self.last_inputs, delta)
        self.bias += self.learning_rate * delta
        
        # Return mean squared error
        return np.mean(error ** 2)
    
    def train(self, inputs, targets, epochs=1000, verbose=True):
        """
        Train the neural network
        
        Args:
            inputs: Training inputs
            targets: Target outputs
            epochs: Number of training epochs
            verbose: Whether to print progress
            
        Returns:
            Error history
        """
        self.error_history = []
        
        for epoch in range(epochs):
            total_error = 0
            
            for i in range(len(inputs)):
                # Forward pass
                outputs = self.forward(inputs[i])
                
                # Backward pass
                error = self.backward(targets[i], outputs)
                total_error += error
            
            avg_error = total_error / len(inputs)
            self.error_history.append(avg_error)
            self.epoch_count += 1
            
            if verbose and (epoch % 100 == 0 or epoch == epochs - 1):
                logger.info(f"Epoch {epoch+1}/{epochs}, Error: {avg_error:.6f}")
        
        return self.error_history
    
    def predict(self, inputs):
        """
        Make a prediction
        
        Args:
            inputs: Input data
            
        Returns:
            Prediction
        """
        return self.forward(inputs)
    
    def encode_text(self, text, max_length=10):
        """
        Simple encoding of text to numeric values
        
        Args:
            text: Input text
            max_length: Maximum length to consider
            
        Returns:
            Encoded vector
        """
        # Normalize text
        text = text.lower()
        
        # Simple character frequency encoding
        encoded = np.zeros(self.input_size)
        for i, char in enumerate(text[:self.input_size]):
            encoded[i] = ord(char) / 255.0  # Normalize to 0-1
        
        return encoded
    
    def decode_output(self, output):
        """
        Convert model output to text response
        
        Args:
            output: Model output vector
            
        Returns:
            Decoded text response
        """
        # Map output values to response templates based on highest activations
        templates = [
            "I understand your query about {}.",
            "Let me analyze that {}.",
            "I'm processing your request about {}.",
            "Interesting question about {}.",
            "I'm thinking about {}"
        ]
        
        # Find the highest activation
        max_index = np.argmax(output)
        confidence = output[max_index]
        
        # Get response template
        if max_index < len(templates):
            template = templates[max_index]
        else:
            template = templates[0]
        
        # Generate topic from memory if available
        if self.memory:
            topic = self.memory[-1].split()[0:3]
            topic = " ".join(topic)
        else:
            topic = "your question"
        
        response = template.format(topic)
        
        # Add confidence indicator
        if confidence > 0.8:
            response += " I'm fairly confident in my analysis."
        elif confidence > 0.5:
            response += " I'm moderately certain about this."
        else:
            response += " This is just my preliminary thought."
        
        return response
    
    def process_input(self, text_input):
        """
        Process text input and generate a response
        
        Args:
            text_input: User input text
            
        Returns:
            Model response
        """
        # Add to memory
        self.memory.append(text_input)
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)
        
        # Encode input
        encoded_input = self.encode_text(text_input)
        
        # Get prediction
        output = self.predict(encoded_input)
        
        # Decode output
        response = self.decode_output(output)
        
        return response
    
    def save_model(self, filepath="model_weights.json"):
        """
        Save model weights and configuration
        
        Args:
            filepath: Path to save the model
        """
        model_data = {
            "metadata": self.metadata,
            "config": {
                "input_size": self.input_size,
                "output_size": self.output_size,
                "learning_rate": self.learning_rate,
                "activation": self.activation_name,
                "epoch_count": self.epoch_count
            },
            "weights": self.weights.tolist(),
            "bias": self.bias.tolist(),
            "error_history": self.error_history[-10:] if self.error_history else []
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath="model_weights.json"):
        """
        Load model weights and configuration
        
        Args:
            filepath: Path to load the model from
            
        Returns:
            Success status
        """
        try:
            with open(filepath, 'r') as f:
                model_data = json.load(f)
            
            # Load configuration
            config = model_data["config"]
            self.input_size = config["input_size"]
            self.output_size = config["output_size"]
            self.learning_rate = config["learning_rate"]
            self.activation_name = config["activation"]
            self.epoch_count = config.get("epoch_count", 0)
            
            # Load weights and bias
            self.weights = np.array(model_data["weights"])
            self.bias = np.array(model_data["bias"])
            
            # Load error history if available
            if "error_history" in model_data:
                self.error_history = model_data["error_history"]
            
            # Load metadata
            if "metadata" in model_data:
                self.metadata = model_data["metadata"]
            
            logger.info(f"Model loaded from {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False

# Create a default model instance
default_model = NeuralModel()

# Simple training data for initialization
def initialize_model():
    """Initialize model with some basic training data"""
    try:
        # Simple input-output pairs for training
        inputs = [
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0],
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.9, 0.9, 0.9, 0.9],
            [0.9, 0.9, 0.9, 0.9, 0.9, 0.1, 0.1, 0.1, 0.1, 0.1]
        ]
        
        targets = [
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0]
        ]
        
        # Train the model
        default_model.train(inputs, targets, epochs=500, verbose=True)
        
        # Save the initialized model
        default_model.save_model()
        
        logger.info("Model initialized with basic training data")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        return False

# Initialize or load the model
if not os.path.exists("model_weights.json"):
    initialize_model()
else:
    default_model.load_model()
