# Jarvis Voice Assistant

A web-based voice assistant built with Flask that can perform various tasks through voice commands.

## Features

- Voice command recognition
- Task management
- Time and date information
- Music playback
- Wikipedia search
- Web browser control
- WhatsApp messaging
- Beautiful web interface with voice visualization

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Voice Commands

- "Hello" - Greet Jarvis
- "Play music" - Play random music
- "Say time" - Get current time
- "Say date" - Get current date
- "New task [task]" - Add a new task
- "Speak task" - List all tasks
- "Show work" - Display tasks as notification
- "Open YouTube" - Open YouTube in browser
- "Wikipedia [query]" - Search Wikipedia
- "Send WhatsApp" - Send WhatsApp message

## Project Structure

```
jarvis/
├── static/
│   ├── style.css
│   ├── script.js
│   └── images/
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md
```
