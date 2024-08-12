import requests
import pyautogui
import os
import speech_recognition as sr
import pyttsx3
import math
import sympy as sp



#####################################################################


def take_screenshot():
    """Capture a screenshot."""
    return pyautogui.screenshot()

def save_screenshot(screenshot, filename, directory='screenshots'):
    """Save the screenshot to a specified directory."""
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Save the screenshot with the full path
    filepath = os.path.join(directory, f"{filename}.png")
    screenshot.save(filepath)




##################################################################
    # math logic

def perform_calculation(expression):
    try:
        # Evaluate basic arithmetic expressions
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def solve_equation(equation):
    try:
        # Solve algebraic equations
        x = sp.symbols('x')
        eq = sp.sympify(equation)
        solution = sp.solve(eq, x)
        return f"Solutions: {solution}"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_math(message):
    # Ensure message is a string
    if isinstance(message, list):
        message = ' '.join(message)  # Convert list to a string if necessary
    
    # Extract math expression from the message
    if "solve" in message:
        equation = message.replace("solve", "").strip()
        return solve_equation(equation)
    else:
        return perform_calculation(message)

##########################################################################

def recognize_speech_from_mic():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        
        # Capture audio from the microphone
        audio = recognizer.listen(source)
        
        try:
            # Recognize speech using Google Web Speech API
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, there was an issue with the request.")

def speak(text,):
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', 150)    # Speed percent
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    
    # Add text to be spoken
    engine.say(text)
    
    # Wait for the speech to finish
    engine.runAndWait()

if __name__ == "__main__":
    text = "Hello, how are you today?"
    speak(text)






###########################################################################




# Your OpenWeatherMap API key
api_key = "46f13c584b686a4b67c01bc7d9d97aa0"

def get_coordinates(city):
    """Get latitude and longitude for a given city."""
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    try:
        response = requests.get(geocoding_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
        else:
            return None, None
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def get_weather(lat, lon):
    """Get current weather information based on latitude and longitude."""
    base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        current_weather = data['current']
        weather_desc = current_weather['weather'][0]['description']
        temperature = current_weather['temp']
        humidity = current_weather['humidity']
        wind_speed = current_weather['wind_speed']
        weather_info = (f"Current temperature is {temperature}°C with {weather_desc}. "
                        f"Humidity is {humidity}%. Wind speed is {wind_speed} m/s.")
        return weather_info
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return "I couldn't retrieve the weather information right now. Please try again later."
