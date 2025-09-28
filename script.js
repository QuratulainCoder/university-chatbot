const API_BASE = 'http://localhost:5000/api';

// Send message function
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    try {
        // Send to backend
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        addMessage(data.response, 'bot');
        
    } catch (error) {
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    }
}

// Add message to chat
function addMessage(content, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Voice input function
function startVoice() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Voice recognition not supported in this browser');
        return;
    }
    
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function() {
        document.getElementById('messageInput').placeholder = 'Listening...';
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('messageInput').value = transcript;
        document.getElementById('messageInput').placeholder = 'Type your message...';
    };
    
    recognition.onerror = function() {
        document.getElementById('messageInput').placeholder = 'Type your message...';
    };
    
    recognition.start();
}

// PDF upload function
function uploadPDF() {
    document.getElementById('pdfUpload').click();
}

document.getElementById('pdfUpload').addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('pdf', file);
    
    try {
        const response = await fetch(`${API_BASE}/upload_pdf`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        addMessage(data.response, 'bot');
    } catch (error) {
        addMessage('Error uploading PDF', 'bot');
    }
});

// Enter key to send message
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});