import tkinter as tk
from tkinter import messagebox, filedialog
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
from googletrans import Translator
import requests
import pyjokes

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to make Jarvis speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user commands
def listen_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            speak("Listening now. Please speak.")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"
    except sr.WaitTimeoutError:
        return "You didn't say anything. Please try again."

# Function to handle commands
def execute_command(command):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}")
        text_output.insert(tk.END, f"The current time is: {current_time}\n")
    elif 'open google' in command:
        speak("Opening Google")
        text_output.insert(tk.END, "Opening Google...\n")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in command:
        speak("Opening YouTube")
        text_output.insert(tk.END, "Opening YouTube...\n")
        webbrowser.open("https://www.youtube.com")
    elif 'chatgpt' in command:
        speak("Opening ChatGPT")
        text_output.insert(tk.END, "Opening ChatGPT...\n")
        webbrowser.open("https://chat.openai.com")
    elif 'play music' in command:
        speak("Playing music on YouTube")
        text_output.insert(tk.END, "Playing music...\n")
        webbrowser.open("https://youtu.be/Feoea8FQTI0?si=eamxKPwBu2e64VZn")
    elif 'weather' in command:
        location = command.replace("weather in", "").strip()
        if location:
            weather_info = get_weather(location)
            speak(weather_info)
            text_output.insert(tk.END, f"{weather_info}\n")
        else:
            speak("Please specify a location.")
    elif 'calculate' in command:
        calculation = command.replace("calculate", "").strip()
        if calculation:
            try:
                result = eval(calculation)
                speak(f"The result is {result}")
                text_output.insert(tk.END, f"Result: {result}\n")
            except Exception as e:
                speak("Error in calculation.")
                text_output.insert(tk.END, f"Calculation error: {e}\n")
        else:
            speak("Please provide a calculation.")
    elif 'joke' in command:
        joke = pyjokes.get_joke(language="en", category="neutral")
        speak(joke)
        text_output.insert(tk.END, f"Joke: {joke}\n")
    elif 'translate' in command:
        if 'to hindi' in command:
            text_to_translate = command.replace('translate', '').replace('to hindi', '').strip()
            translation = translate_text(text_to_translate, "hi")
            speak(translation)
            text_output.insert(tk.END, f"{translation}\n")
        elif 'to english' in command:
            text_to_translate = command.replace('translate', '').replace('to english', '').strip()
            translation = translate_text(text_to_translate, "en")
            speak(translation)
            text_output.insert(tk.END, f"{translation}\n")
        else:
            speak("Please specify whether to translate to Hindi or English.")
    else:
        speak("Sorry, I can't perform that task.")
        text_output.insert(tk.END, f"Unknown command: {command}\n")

# Function to fetch weather
def get_weather(location):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            city = data["name"]
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return "Sorry, I couldn't find the weather for that location."
    except Exception as e:
        return f"An error occurred while fetching the weather: {e}"

# Function to translate text
def translate_text(text, target_language="en"):
    translator = Translator()
    try:
        result = translator.translate(text, dest=target_language)
        return f"Translation: {result.text}"
    except Exception as e:
        return f"An error occurred while translating: {e}"

# GUI Components and Layout
root = tk.Tk()
root.title("Jarvis Assistant")
root.geometry("700x500")

label = tk.Label(root, text="Jarvis Voice Assistant", font=("Arial", 16))
label.pack(pady=10)

text_output = tk.Text(root, wrap=tk.WORD, height=15, width=80)
text_output.pack(pady=10)

entry_command = tk.Entry(root, width=50, font=("Arial", 12))
entry_command.pack(pady=5)

btn_manual = tk.Button(root, text="Execute Command", command=lambda: execute_command(entry_command.get()), width=20)
btn_manual.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Speak", command=lambda: execute_command(listen_command()), width=15).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Clear Text", command=lambda: text_output.delete(1.0, tk.END), width=15).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Save Log", command=save_log, width=15).grid(row=0, column=2, padx=5)
tk.Button(frame, text="Help", command=lambda: text_output.insert(tk.END, "List of commands goes here...\n"), width=15).grid(row=0, column=3, padx=5)
tk.Button(frame, text="Exit", command=root.quit, width=15).grid(row=0, column=4, padx=5)

root.mainloop()
