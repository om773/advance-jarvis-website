from flask import Flask, render_template, jsonify, request, send_from_directory
app = Flask(__name__, static_url_path='/static', static_folder='static') 
import os
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk

app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.get_json()
    command_text = data.get('command', '').lower()
    
    response = process_voice_command(command_text)
    return jsonify({'response': response})

def process_voice_command(request):
    if "hello" in request:
        return "Welcome, How can i help you."
    elif "play music" in request:
        song = random.randint(1,3)
        if song == 1:
            webbrowser.open("https://www.youtube.com/watch?v=WzQBAc8i73E")
        elif song == 2:
            webbrowser.open("https://www.youtube.com/watch?v=Vb_3FuiVHBM")
        elif song == 3:
            webbrowser.open("https://www.youtube.com/watch?v=Jx02XQTz2LU")
        return "Playing music"
    elif "say time" in request:
        now_time = datetime.datetime.now().strftime("%H:%M")
        return f"Current time is {now_time}"
    elif "say date" in request:
        now_time = datetime.datetime.now().strftime("%d:%m")
        return f"Current date is {now_time}"
    elif "new task" in request:
        task = request.replace("new task","").strip()
        if task != "":
            with open("todo.txt","a") as file:
                file.write(task + "\n")
            return f"Added task: {task}"
    elif "speak task" in request:
        with open("todo.txt","r") as file:
            tasks = file.read()
            return f"Work we have to do today is: {tasks}"
    elif "show work" in request:
        with open("todo.txt","r") as file:
            tasks = file.read()
            notification.notify(
                title="Today's work",
                message=tasks
            )
            return "Showing today's work"
    elif "open youtube" in request:
        webbrowser.open("www.youtube.com")
        return "Opening YouTube"
    elif "open" in request:
        try:
            app_name = request.replace("open", "").strip().lower()
            
            # Common applications dictionary with their typical paths
            common_apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "word": "winword.exe",
                "excel": "excel.exe",
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
                "explorer": "explorer.exe",
                "control panel": "control.exe",
                "task manager": "taskmgr.exe",
                "settings": "ms-settings:",
            }
            
            if app_name in common_apps:
                # Try to open using the direct command
                os.system(f"start {common_apps[app_name]}")
            else:
                # Use Windows Run dialog for other applications
                pyautogui.press("win")
                pyautogui.sleep(1)
                pyautogui.typewrite(app_name)
                pyautogui.sleep(1)
                pyautogui.press("enter")
            
            return f"Opening {app_name}"
        except Exception as e:
            print(f"Error opening application: {str(e)}")
            return f"Sorry, I couldn't open {app_name}. Please try again."
    elif "wikipedia" in request:
        query = request.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except:
            return "Could not find information on Wikipedia"
    return "I didn't understand that command"

engine = pyttsx3.init()

engine.setProperty("rate", 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command(): 
    content = " "
    while content == " ":  
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)   

        # recognize speech using Google Speech Recognition
        try:
            content = r.recognize_google(audio, language='en-in')
            print("you said........." + content)
        except Exception as e:
            print("please try again...")
        
    return content

def main_process():
    while True:    
        request = command().lower()
        if "hello" in request:
            speak("Welcome, How can i help you.")
        elif "play music" in request:
            speak("playing music")
            song = random.randint(1,3)
            if song == 1:
                webbrowser.open("https://www.youtube.com/watch?v=WzQBAc8i73E&pp=ygUUY29weXJpZ2h0IGZyZWUgbXVzaWM%3D")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=Vb_3FuiVHBM&pp=ygUUY29weXJpZ2h0IGZyZWUgbXVzaWM%3D")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=Jx02XQTz2LU&pp=ygUUY29weXJpZ2h0IGZyZWUgbXVzaWM%3D")
        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("current time is "+str(now_time))
        elif "say date" in request:
            now_time = datetime.datetime.now().strftime("%d:%m")
            speak("current date is "+str(now_time))
        elif "new task" in request:
            task = request.replace("new task","")
            task = task.strip()
            if task != "":
                speak("Adding task: "+task)
                with open ("todo.txt","a") as file:
                    file.write(task + "\n")
        elif "speak task" in request:
            with open ("todo.txt","r") as file:
                speak("work we have to do today is : "+file.read())
        elif "show work" in request:
            with open ("todo.txt","r") as file:
                tasks = file.read()
                notification.notify(
                    title = "Today's work",
                    message = tasks
                )
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")
        elif "open" in request:
            try:
                app_name = request.replace("open", "").strip().lower()
                
                # Common applications dictionary with their typical paths
                common_apps = {
                    "notepad": "notepad.exe",
                    "calculator": "calc.exe",
                    "paint": "mspaint.exe",
                    "word": "winword.exe",
                    "excel": "excel.exe",
                    "chrome": "chrome.exe",
                    "firefox": "firefox.exe",
                    "edge": "msedge.exe",
                    "explorer": "explorer.exe",
                    "control panel": "control.exe",
                    "task manager": "taskmgr.exe",
                    "settings": "ms-settings:",
                }
                
                if app_name in common_apps:
                    # Try to open using the direct command
                    os.system(f"start {common_apps[app_name]}")
                else:
                    # Use Windows Run dialog for other applications
                    pyautogui.press("win")
                    pyautogui.sleep(1)
                    pyautogui.typewrite(app_name)
                    pyautogui.sleep(1)
                    pyautogui.press("enter")
                
                speak(f"Opening {app_name}")
            except Exception as e:
                print(f"Error opening application: {str(e)}")
                speak(f"Sorry, I couldn't open {app_name}. Please try again.")
        elif "wikipedia" in request:
            request = request.replace("Jarvis ", "")
            request = request.replace("search wikipedia ", "")
            print(request)
            result = wikipedia.summary(request, sentences=2)
            print(result)
            speak(result)
            
        elif "search google" in request:
            request = request.replace("Jarvis ", "")
            request = request.replace("search google ", "")
            webbrowser.open("https://www.google.com/search?q="+request)
        elif "send whatsapp" in request:
            pwk.sendwhatmsg("+916355250581", "Hi,How are you ", 11, 8,40)

if __name__ == "__main__":
    import webbrowser
    port = 5000  # Default Flask port
    webbrowser.open(f"http://127.0.0.1:{port}")
    app.run(debug=True, port=port)