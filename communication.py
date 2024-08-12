import speech_recognition as sr
import serial
import torch
import time
import numpy as np
import json
import random
from nltk_utils import tokenize, bag_of_words
from model import NeuralNet

from functionality import recognize_speech_from_mic

# Initialize serial communication with Arduino
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Adjust 'COM3' to your port

# Load intents and model
with open("data/intents.json", 'r') as f:
    intents = json.load(f)

FILE = "data/data.pth"
data = torch.load(FILE)
model_state = data['model_state']
input_size = data['input_size']
output_size = data['output_size']
hidden_size = data['hidden_size']
all_words = data['all_words']
tags = data['tags']

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# def recognize_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say something...")
#         audio = recognizer.listen(source)
#         try:
#             text = recognizer.recognize_google(audio)
#             print(f"You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("Sorry, I did not understand that.")
#             return None
#         except sr.RequestError:
#             print("Sorry, there was an issue with the speech recognition service.")
#             return None

def send_message_to_arduino(message):
    arduino.write(message.encode())  # Send the message to Arduino
    time.sleep(1)  # Wait for Arduino to process
    response = arduino.readline().decode().strip()  # Read the response
    return response

while True:
    user_input = recognize_speech_from_mic()
    print(user_input)
    if user_input:
        sentence = tokenize(user_input)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:

                    if tag == "move_":
                        res = "Move"
                        send_message_to_arduino(res)
                        print(res)

                    
                    elif tag == "Stop_":
                        res = "Stop"
                        send_message_to_arduino(res)
                        print(res)
        else:
            response = "I'm not sure how to respond to that."
            send_message_to_arduino(response)
