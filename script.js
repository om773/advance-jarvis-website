const startButton = document.getElementById('startButton');

class VoiceAssistant {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.visualizer = null;
        
        this.initializeElements();
        this.setupSpeechRecognition();
        this.setupVisualizer();
        this.addEventListeners();
    }

    initializeElements() {
        this.startButton = document.getElementById('startButton');
        this.statusText = document.getElementById('status-text');
        this.historyDiv = document.getElementById('history');
        this.visualizerCanvas = document.getElementById('visualizer');
    }

    setupSpeechRecognition() {
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => this.onRecognitionStart();
            this.recognition.onend = () => this.onRecognitionEnd();
            this.recognition.onresult = (event) => this.onRecognitionResult(event);
            this.recognition.onerror = (event) => this.onRecognitionError(event);
        } else {
            this.showError("Speech recognition is not supported in this browser.");
        }
    }

    setupVisualizer() {
        const canvas = this.visualizerCanvas;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        this.visualizer = {
            draw: () => {
                ctx.clearRect(0, 0, width, height);
                if (this.isListening) {
                    ctx.beginPath();
                    ctx.moveTo(0, height/2);
                    for(let i = 0; i < width; i++) {
                        const y = height/2 + Math.sin(i/10 + Date.now()/200) * 20;
                        ctx.lineTo(i, y);
                    }
                    ctx.strokeStyle = '#0d6efd';
                    ctx.stroke();
                } else {
                    ctx.beginPath();
                    ctx.moveTo(0, height/2);
                    ctx.lineTo(width, height/2);
                    ctx.strokeStyle = '#666';
                    ctx.stroke();
                }
                requestAnimationFrame(() => this.visualizer.draw());
            }
        };
        this.visualizer.draw();
    }

    addEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleListening());
    }

    toggleListening() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        try {
            this.recognition.start();
            this.isListening = true;
            this.startButton.innerHTML = '<i class="bi bi-mic-mute"></i> Stop Listening';
            this.startButton.classList.add('btn-danger');
            this.startButton.classList.remove('btn-primary');
            this.statusText.textContent = 'Listening...';
            this.statusText.className = 'badge bg-danger';
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.showError("Failed to start listening");
        }
    }

    stopListening() {
        try {
            this.recognition.stop();
            this.isListening = false;
            this.startButton.innerHTML = '<i class="bi bi-mic"></i> Start Listening';
            this.startButton.classList.add('btn-primary');
            this.startButton.classList.remove('btn-danger');
            this.statusText.textContent = 'Click to Start';
            this.statusText.className = 'badge bg-secondary';
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
    }

    onRecognitionStart() {
        console.log('Recognition started');
    }

    onRecognitionEnd() {
        console.log('Recognition ended');
        if (this.isListening) {
            this.recognition.start();
        }
    }

    async onRecognitionResult(event) {
        const command = event.results[0][0].transcript.toLowerCase();
        console.log('Command recognized:', command);
        
        this.addToHistory('You', command);
        this.statusText.textContent = 'Processing...';
        this.statusText.className = 'badge bg-warning';

        try {
            const response = await fetch('/process_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Response:', data);
            
            if (data.response) {
                this.addToHistory('Jarvis', data.response);
                this.speak(data.response);
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError("Failed to process command");
        } finally {
            this.statusText.textContent = 'Click to Start';
            this.statusText.className = 'badge bg-secondary';
            this.stopListening();
        }
    }

    onRecognitionError(event) {
        console.error('Recognition error:', event.error);
        this.showError(`Recognition error: ${event.error}`);
        this.stopListening();
    }

    addToHistory(speaker, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.innerHTML = `<strong>${speaker}:</strong> ${text}`;
        this.historyDiv.insertBefore(messageDiv, this.historyDiv.firstChild);
    }

    showError(message) {
        this.statusText.textContent = message;
        this.statusText.className = 'badge bg-danger';
        this.addToHistory('System', `Error: ${message}`);
    }

    speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        this.synthesis.speak(utterance);
    }
}

// Initialize the voice assistant when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const assistant = new VoiceAssistant();
});