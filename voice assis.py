import tkinter as tk
from tkinter import messagebox, filedialog
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
from googletrans import Translator
import pyjokes
import time
import threading
import sympy
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import wikipedia
import PyPDF2

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
            speak("Listening now. Please speak .")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"
    except sr.WaitTimeoutError:
        return "You didn't say anything. Please try again."

# Function to fetch news
def fetch_news():
    api_key = "your_newsapi_key"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        top_news = "\n".join([f"{i+1}. {article['title']}" for i, article in enumerate(articles[:5])])
        speak("Here are the top headlines:")
        return top_news
    except Exception as e:
        return f"Error fetching news: {e}"
# Function to handle PDF reading
def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        try:
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                if text.strip():
                    text_output.insert(tk.END, text + "\n")
                    speak(text)
                else:
                    text_output.insert(tk.END, "No text found in the PDF.\n")
                    speak("No text found in the PDF.")
        except Exception as e:
            text_output.insert(tk.END, f"Error reading PDF: {e}\n")
            speak("An error occurred while reading the PDF.")

# Reminder functionality
reminders = []

def set_reminder(time_str, message):
    reminders.append({"time": time_str, "message": message})
    speak(f"Reminder set for {time_str}")

def check_reminders():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminders:
            if reminder["time"] == now:
                speak(f"Reminder: {reminder['message']}")
                reminders.remove(reminder)
        time.sleep(30)
#convert units
def convert_units(value, from_unit, to_unit):
    try:
        value = float(value)  # Ensure the value is a valid float
    except ValueError:
        return "Invalid number format."
    
    conversions = {
        "km to miles": 0.621371,
        "miles to km": 1.60934,
        "kg to pounds": 2.20462,
        "pounds to kg": 0.453592
    }
    key = f"{from_unit} to {to_unit}"
    if key in conversions:
        return value * conversions[key]
    return "Conversion not supported."

# Math solver
def solve_math(equation):
    try:
        solution = sympy.solve(equation)
        return f"The solution is: {solution}"
    except Exception as e:
        return f"Error solving equation: {e}"

# Alarm
def set_alarm(alarm_time):
    def alarm_thread():
        while True:
            if datetime.datetime.now().strftime("%H:%M") == alarm_time:
                speak("Alarm ringing!")
                break
            time.sleep(10)
    threading.Thread(target=alarm_thread).start()

# Wikipedia search
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        return result
    except Exception as e:
        return f"Error fetching Wikipedia data: {e}"

# Unit conversion
def convert_units(value, from_unit, to_unit):
    conversions = {
        "km to miles": 0.621371,
        "miles to km": 1.60934,
        "kg to pounds": 2.20462,
        "pounds to kg": 0.453592
    }
    key = f"{from_unit} to {to_unit}"
    if key in conversions:
        return value * conversions[key]
    return "Conversion not supported."
#Reminders
reminders = ["Take your medicine", "Meeting at 3 PM"]  # Example reminder list

def execute_command(command):
    if "reminder" in command:
        reminder_message = reminders[0]  # Example to use the first reminder
        speak(reminder_message)
        text_output.insert(tk.END, f"Reminder: {reminder_message}\n")


# Email sending
def send_email(to_email, subject, body):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Error sending email: {e}"

# Dark mode
dark_mode = False

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "black" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"
    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        widget.configure(bg=bg_color, fg=fg_color)

# Function to handle commands
def execute_command(command):
#Time
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}")
        text_output.insert(tk.END, f"The current time is: {current_time}\n")
#Google
    elif 'open google' in command:
        speak("Opening Google")
        text_output.insert(tk.END, "Opening Google...\n")
        webbrowser.open("https://www.google.com")
#YouTube
    elif 'open youtube' in command:
        speak("Opening YouTube")
        text_output.insert(tk.END, "Opening YouTube...\n")
        webbrowser.open("https://www.youtube.com")
#play music
    elif 'play music' in command:
        speak("Playing music on YouTube")
        text_output.insert(tk.END, "Playing music...\n")
        webbrowser.open("https://youtu.be/Feoea8FQTI0?si=eamxKPwBu2e64VZn")
#ChatGPT
    elif 'chatgpt' in command:
        speak("Open ChetGPT on webbrowser")
        text_output.insert(tk.END, "open ChatGPT\n")
        webbrowser.open("https://chatgpt.com")
#calculate
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
#joke            
    elif 'joke' in command:
        joke = pyjokes.get_joke(language="en", category="neutral")
        speak(joke)
        text_output.insert(tk.END, f"Joke: {joke}\n")
#translate        
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
#News            
    if "news" in command:
        news = fetch_news()
        speak(news)
        text_output.insert(tk.END, f"{news}\n")
#Reminder
    elif "reminder" in command:
        time_part = command.split("for")[1].split("to")[0].strip()
        message_part = command.split("to")[1].strip()
        set_reminder(time_part, message_part)
        speak(Reminder)
        text_output.insert(tk.END, f"Command: {command}\n")
#Solve
    elif "solve" in command:
        equation = command.replace("solve", "").strip()
        result = solve_math(equation)
        text_output.insert(tk.END, f"{result}\n")
#Alarm
    elif "alarm" in command:
        alarm_time = command.split("for")[1].strip()
        set_alarm(alarm_time)
        text_output.insert(tk.END, f"Command: {command}\n")
#About
    elif "about" in command:
        query = command.replace("tell me about", "").strip()
        result = search_wikipedia(query)
        text_output.insert(tk.END, f"{result}\n")
#Convert
    elif "convert" in command:
        parts = command.split("to")
        value, from_unit = parts[0].split("convert")[1].strip().split(" ")
        to_unit = parts[1].strip()
        result = convert_units(float(value), from_unit, to_unit)
        text_output.insert(tk.END, f"{result}\n")
#Email
    elif "email" in command:
        to_email = command.split("to")[1].split("about")[0].strip()
        body = command.split("about")[1].strip()
        result = send_email(to_email, "Message from Jarvis", body)
        text.output.insert(tk.END, f"{result}\n")
#ReadFile
    elif 'read pdf' in command:
        open_pdf()

    else:
        speak("Sorry, I can't perform that task.")
        text_output.insert(tk.END, f"Unknown command: {command}\n")

# Function to trigger the "Speak" button
def on_speak():
    command = listen_command()
    text_output.insert(tk.END, f"You said: {command}\n")
    if command:
        execute_command(command)

# Function to handle manual command input
def manual_command():
    command = entry_command.get()
    if command:
        text_output.insert(tk.END, f"You entered: {command}\n")
        execute_command(command)
    else:
        messagebox.showwarning("Input Error", "Please enter a command.")

# Function to clear the text box
def clear_text():
    text_output.delete(1.0, tk.END)

# Function to save conversation to a file
def save_log():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_output.get(1.0, tk.END))
        messagebox.showinfo("Save Log", f"Conversation saved to {file_path}")

# Function to exit the application
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()
# Function to translate text
def translate_text(text, target_language="en"):
    translator = Translator()
    try:
        result = translator.translate(text, dest=target_language)
        return f"Translation: {result.text}"
    except Exception as e:
        return f"An error occurred while translating: {e}"


# Function to display help information
def show_help():
    help_text = """Supported Commands:
    1. "What time is it?" - Tells the current time.
    2. "Open Google" - Opens the Google homepage.
    3. "Open YouTube" - Opens the YouTube homepage.
    4. "Play music" - Plays music on YouTube.
    5. "Chatgpt" - Opens the chatgpt homepage.
    6. "calculate" - The result is {result}.
    7. "joke" - joke.
    8. "translate" - English to Hindi and Hindi To English.
    9. "news" - Fetch top news headlines.
    10. "set a reminder for [time] to [message]."
    11. "solve" [equation].
    12. "set an alarm" for [time].
    13. "tell me about" [topic].
    14. "convert" [value] [unit] to [unit]"km to miles",\
        "miles to km",\
        "kg to pounds",\
        "pounds to kg"\
    15. "send email" to [email] about [message].
    16. "read pdf" - REAd PDF.

    """
    text_output.insert(tk.END, help_text + "\n")
    speak("Displaying supported commands.")

# Create the GUI window
root = tk.Tk()
root.title("Personal Assistant")
root.geometry("700x500")

# Add a label
label = tk.Label(root, text="Personal Voice Assistant", font=("Arial", 16))
label.pack(pady=10)

# Add a text widget for displaying messages
text_output = tk.Text(root, wrap=tk.WORD, height=15, width=80)
text_output.pack(pady=10)

# Entry widget for manual command input
entry_command = tk.Entry(root, width=50, font=("Arial", 12))
entry_command.pack(pady=5)

# Button to execute manual command
btn_manual = tk.Button(root, text="Execute Command", command=manual_command, width=20, bg="lightgray")
btn_manual.pack(pady=5)

# Add buttons
frame = tk.Frame(root)
frame.pack(pady=10)

btn_speak = tk.Button(frame, text="Speak", command=on_speak, width=15, bg="lightblue")
btn_speak.grid(row=0, column=0, padx=5)

btn_clear = tk.Button(frame, text="Clear Text", command=clear_text, width=15, bg="lightgreen")
btn_clear.grid(row=0, column=1, padx=5)

btn_save = tk.Button(frame, text="Save Log", command=save_log, width=15, bg="orange")
btn_save.grid(row=0, column=2, padx=5)

btn_open_pdf = tk.Button(frame, text="Read PDF", command=open_pdf, width=15, bg="orange")
btn_open_pdf.grid(row=0, column=2, padx=5)

btn_help = tk.Button(frame, text="Help", command=show_help, width=15, bg="yellow")
btn_help.grid(row=0, column=3, padx=5)

btn_exit = tk.Button(frame, text="Exit", command=exit_app, width=15, bg="red")
btn_exit.grid(row=0, column=4, padx=5)

# Run the GUI event loop
root.mainloop()
