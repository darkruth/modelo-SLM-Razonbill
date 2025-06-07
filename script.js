/**
 * Script for Núcleo C.A- Razonbilstro Web Interface
 * Handles conversation, neural network visualization, and user interactions
 */

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');
    const conversationContainer = document.getElementById('conversation-container');
    
    // Send message when button is clicked or enter is pressed
    if (sendButton && userInput) {
        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // Clear conversation when clear button is clicked
    if (clearButton) {
        clearButton.addEventListener('click', clearConversation);
    }
    
    // Auto-scroll conversation container to bottom
    if (conversationContainer) {
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
    }
});

/**
 * Initialize the neural network visualization
 * @param {number} inputSize - Number of input neurons
 * @param {number} outputSize - Number of output neurons
 */
function initializeNeuralNetworkVisualization(inputSize, outputSize) {
    const inputLayer = document.getElementById('inputLayer');
    const outputLayer = document.getElementById('outputLayer');
    const connections = document.getElementById('connections');
    
    if (!inputLayer || !outputLayer || !connections) return;
    
    // Clear existing content
    inputLayer.innerHTML = '';
    outputLayer.innerHTML = '';
    connections.innerHTML = '';
    
    // Create input neurons
    const inputNeurons = [];
    for (let i = 0; i < inputSize; i++) {
        const neuron = document.createElement('div');
        neuron.className = 'neuron input-neuron';
        neuron.dataset.index = i;
        inputLayer.appendChild(neuron);
        inputNeurons.push(neuron);
    }
    
    // Create output neurons
    const outputNeurons = [];
    for (let i = 0; i < outputSize; i++) {
        const neuron = document.createElement('div');
        neuron.className = 'neuron output-neuron';
        neuron.dataset.index = i;
        outputLayer.appendChild(neuron);
        outputNeurons.push(neuron);
    }
    
    // Create connections between all input and output neurons
    for (let i = 0; i < inputNeurons.length; i++) {
        for (let j = 0; j < outputNeurons.length; j++) {
            createConnection(inputNeurons[i], outputNeurons[j], connections);
        }
    }
    
    // Add animation to simulate neural activity
    simulateNeuralActivity(inputNeurons, outputNeurons);
}

/**
 * Create a visual connection between two neurons
 * @param {Element} fromNeuron - Source neuron element
 * @param {Element} toNeuron - Target neuron element
 * @param {Element} container - Container for connections
 */
function createConnection(fromNeuron, toNeuron, container) {
    const connection = document.createElement('div');
    connection.className = 'connection';
    connection.dataset.from = fromNeuron.dataset.index;
    connection.dataset.to = toNeuron.dataset.index;
    
    // Position and rotate the connection
    const fromRect = fromNeuron.getBoundingClientRect();
    const toRect = toNeuron.getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();
    
    const fromX = fromRect.left + fromRect.width / 2 - containerRect.left;
    const fromY = fromRect.top + fromRect.height / 2 - containerRect.top;
    const toX = toRect.left + toRect.width / 2 - containerRect.left;
    const toY = toRect.top + toRect.height / 2 - containerRect.top;
    
    // Calculate length and angle
    const length = Math.sqrt(Math.pow(toX - fromX, 2) + Math.pow(toY - fromY, 2));
    const angle = Math.atan2(toY - fromY, toX - fromX) * 180 / Math.PI;
    
    // Apply styles
    connection.style.width = `${length}px`;
    connection.style.left = `${fromX}px`;
    connection.style.top = `${fromY}px`;
    connection.style.transform = `rotate(${angle}deg)`;
    
    container.appendChild(connection);
}

/**
 * Simulate neural activity with animations
 * @param {Array} inputNeurons - Array of input neuron elements
 * @param {Array} outputNeurons - Array of output neuron elements
 */
function simulateNeuralActivity(inputNeurons, outputNeurons) {
    const connections = document.querySelectorAll('.connection');
    
    // Periodically activate random neurons and connections
    setInterval(() => {
        // Reset all neurons and connections
        inputNeurons.forEach(neuron => {
            neuron.style.backgroundColor = 'rgba(13, 202, 240, 0.7)';
        });
        outputNeurons.forEach(neuron => {
            neuron.style.backgroundColor = 'rgba(13, 202, 240, 0.5)';
        });
        connections.forEach(conn => {
            conn.classList.remove('active');
        });
        
        // Activate random input neuron
        const activeInput = Math.floor(Math.random() * inputNeurons.length);
        inputNeurons[activeInput].style.backgroundColor = 'rgba(13, 202, 240, 1)';
        
        // Determine output neurons to activate (1-3 random ones)
        const numActiveOutputs = Math.floor(Math.random() * 3) + 1;
        const activeOutputs = new Set();
        while (activeOutputs.size < numActiveOutputs && activeOutputs.size < outputNeurons.length) {
            activeOutputs.add(Math.floor(Math.random() * outputNeurons.length));
        }
        
        // Activate selected output neurons and their connections
        activeOutputs.forEach(outputIndex => {
            outputNeurons[outputIndex].style.backgroundColor = 'rgba(13, 202, 240, 1)';
            
            // Find and activate the connection
            connections.forEach(conn => {
                if (conn.dataset.from == activeInput && conn.dataset.to == outputIndex) {
                    conn.classList.add('active');
                }
            });
        });
    }, 2000);
}

/**
 * Send a message to the model and display the response
 */
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const conversationContainer = document.getElementById('conversation-container');
    
    if (!userInput || !conversationContainer) return;
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // Clear input field
    userInput.value = '';
    
    // Add user message to conversation
    addMessage('user', message);
    
    // Add thinking indicator
    const thinkingId = addThinkingIndicator();
    
    // Send to backend
    fetch('/api/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove thinking indicator
        removeThinkingIndicator(thinkingId);
        
        if (data.success) {
            // Add model response
            addMessage('model', data.response);
            
            // Activate a random set of neurons to simulate processing
            simulateProcessing();
        } else {
            // Show error
            addMessage('system', `Error: ${data.error}`);
        }
    })
    .catch(error => {
        // Remove thinking indicator
        removeThinkingIndicator(thinkingId);
        
        // Show error
        addMessage('system', `Error: ${error.message}`);
    });
}

/**
 * Add a message to the conversation container
 * @param {string} type - Message type: 'user', 'model', or 'system'
 * @param {string} content - Message content
 */
function addMessage(type, content) {
    const conversationContainer = document.getElementById('conversation-container');
    if (!conversationContainer) return;
    
    // Create message elements
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const paragraph = document.createElement('p');
    paragraph.textContent = content;
    paragraph.className = 'mb-0';
    
    // Assemble message
    contentDiv.appendChild(paragraph);
    messageDiv.appendChild(contentDiv);
    conversationContainer.appendChild(messageDiv);
    
    // Add timestamp for user and model messages
    if (type === 'user' || type === 'model') {
        const timestamp = document.createElement('small');
        timestamp.className = 'text-muted d-block mt-1';
        timestamp.style.fontSize = '0.7rem';
        timestamp.textContent = new Date().toLocaleTimeString();
        
        if (type === 'user') {
            timestamp.style.textAlign = 'right';
        }
        
        messageDiv.appendChild(timestamp);
    }
    
    // Clear existing messages if too many (keep last 50)
    const messages = conversationContainer.querySelectorAll('.message');
    if (messages.length > 50) {
        for (let i = 0; i < messages.length - 50; i++) {
            conversationContainer.removeChild(messages[i]);
        }
    }
    
    // Scroll to bottom
    conversationContainer.scrollTop = conversationContainer.scrollHeight;
}

/**
 * Add a thinking indicator to show the model is processing
 * @returns {string} ID of the thinking indicator
 */
function addThinkingIndicator() {
    const conversationContainer = document.getElementById('conversation-container');
    if (!conversationContainer) return null;
    
    const id = 'thinking-' + Date.now();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message model-message';
    messageDiv.id = id;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content thinking';
    
    // Add the three dots for the thinking animation
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        contentDiv.appendChild(dot);
    }
    
    messageDiv.appendChild(contentDiv);
    conversationContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    conversationContainer.scrollTop = conversationContainer.scrollHeight;
    
    return id;
}

/**
 * Remove the thinking indicator
 * @param {string} id - ID of the thinking indicator to remove
 */
function removeThinkingIndicator(id) {
    if (!id) return;
    
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Clear the conversation history
 */
function clearConversation() {
    const conversationContainer = document.getElementById('conversation-container');
    if (!conversationContainer) return;
    
    // Confirm before clearing
    if (!confirm('¿Estás seguro que deseas limpiar toda la conversación?')) {
        return;
    }
    
    // Send clear request to backend
    fetch('/api/clear', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Clear the conversation container
            conversationContainer.innerHTML = '';
            
            // Add welcome message
            addMessage('system', 'Conversación limpiada. ¿En qué puedo ayudarte?');
        } else {
            // Show error
            addMessage('system', `Error: ${data.error}`);
        }
    })
    .catch(error => {
        // Show error
        addMessage('system', `Error: ${error.message}`);
    });
}

/**
 * Simulate neural processing by activating random neurons and connections
 */
function simulateProcessing() {
    const inputNeurons = document.querySelectorAll('.input-neuron');
    const outputNeurons = document.querySelectorAll('.output-neuron');
    const connections = document.querySelectorAll('.connection');
    
    if (!inputNeurons.length || !outputNeurons.length || !connections.length) return;
    
    // Highlight all nodes briefly
    inputNeurons.forEach(neuron => {
        neuron.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        setTimeout(() => {
            neuron.style.backgroundColor = 'rgba(13, 202, 240, 0.7)';
        }, 500);
    });
    
    // Activate connections in sequence
    const totalDuration = 800;
    const stepDuration = totalDuration / connections.length;
    
    connections.forEach((conn, index) => {
        setTimeout(() => {
            conn.classList.add('active');
            setTimeout(() => {
                conn.classList.remove('active');
            }, 300);
        }, index * stepDuration);
    });
    
    // Highlight output neurons at the end
    setTimeout(() => {
        outputNeurons.forEach(neuron => {
            neuron.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
            setTimeout(() => {
                neuron.style.backgroundColor = 'rgba(13, 202, 240, 0.5)';
            }, 500);
        });
    }, totalDuration);
}
