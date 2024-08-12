import random
import json
import logging
import torch
import os
from model import NeuralNet
from nltk_utils import tokenize, bag_of_words
from datetime import datetime

from functionality import get_weather, get_coordinates, take_screenshot, save_screenshot, recognize_speech_from_mic, speak, handle_math, perform_calculation, solve_equation
from maths import add, multiply, subtract, divide, extract_numbers_and_operation, calculate_fraction, extract_numbers_for_fraction


# Configure logging
logging.basicConfig(filename='chatbot.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents and model
with open("data/intents.json", 'r') as f:
    intents = json.load(f)

FILE = "data/data.pth"
data = torch.load(FILE, weights_only=True)

model_state = data['model_state']
input_size = data['input_size']
output_size = data['output_size']
hidden_size = data['hidden_size']
all_words = data['all_words']
tags = data['tags']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

textMode = True
ProbMode = True

bot_name = "Ai"

print("Let's start! Type 'quit' to quit.")

while True:

    if textMode == False:
        sentence = recognize_speech_from_mic()
        print(f'You: {sentence}')
        if sentence is None:
            continue
        sentence = sentence.lower()
    else:
        sentence = input("You: ")

    if sentence == 'quit':
        break

    logging.info(f'User input: {sentence}')

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.85:
        for intent in intents['intents']:
            if tag == intent["tag"]:

                logging.info(f'Intent matched: {tag}')

                # Shows date
                if tag == "date":
                    date = datetime.now().strftime('%Y-%m-%d')
                    response = random.choice(intent['responses'])

                    if textMode == True:
                        print(f"{bot_name}: {response} {date}")
                        if ProbMode == True:
                            print(prob.item())
                    else:
                        print(f"{bot_name}: {response} {date}")
                        speak(response + " " + date)
                    
                    logging.info(f'Bot response: {response} {date}')




                # Tells time
                elif tag == "time":
                    time = datetime.now().strftime('%H:%M:%S')
                    response = random.choice(intent['responses'])

                    if textMode == True:
                        print(f"{bot_name}: {response} {time}")
                        if ProbMode == True:
                            print(prob.item())
                    else:
                        print(f"{bot_name}: {response} {time}")
                        speak(response + " " + time)

                    
                    logging.info(f'Bot response: {response} {time}')




                # Shows weather
                elif tag == "weather":
                    print(f"{bot_name}: Please provide the name of the city you want the weather for.")
                    city = input('You: ').strip()
                    lat, lon = get_coordinates(city)
                    if lat and lon:
                        weather_response = get_weather(lat, lon)
                    else:
                        weather_response = "Sorry, I couldn't get the weather information."
                    print(f"{bot_name}: {weather_response}")
                    
                    logging.info(f'Bot response: {weather_response}')




                # Takes a screenshot
                elif tag == "screenshot":

                    if textMode == False:
                        print(f"{bot_name}: What do you want the screenshot to be called?")
                        speak("What do you want the screenshot to be called?")
                    else:
                        print(f"{bot_name}: What do you want the screenshot to be called?")

                    if textMode == False:
                        filename = recognize_speech_from_mic().strip()
                    else:
                        filename = input('You: ').strip()
                    
                    print(f'You: {filename}')

                    screenshot = take_screenshot()

                    save_screenshot(screenshot, filename)
                    response = random.choice(intent['responses'])

                    if textMode == True:
                        print(f"{bot_name}: {response}")
                    else:
                        print(f"{bot_name}: {response}")
                        speak(response)

                    
                    logging.info(f'Bot response: {response}')





                elif tag == "goodbye":
                    response = random.choice(intent['responses'])

                    if textMode == True:
                        print(f"{bot_name}: {response}")
                        if ProbMode == True:
                            print(prob.item())
                    else:
                        print(f"{bot_name}: {response}")
                        speak(response)

                    
                    logging.info(f'Bot response: {response}')
                    
                    logging.info(f'End of conversation')

                    break




                elif tag == "train":
                    response = random.choice(intent['responses'])

                    if textMode == True:
                        print(f"{bot_name}: {response}")
                        if ProbMode == True:
                            print(prob.item())
                    else:
                        print(f"{bot_name}: {response}")
                        speak(response)
                    
                    os.system('python train.py')
                    
                    logging.info(f'Bot response: {response}')




                # Handles math calculations
                elif tag == "calculate":
                    # Extract numbers and operation from the user's input
                    num1, operation, num2 = extract_numbers_and_operation(sentence)
                    
                    if num1 is not None and operation is not None:
                        if operation in ['plus', 'add', '+']:
                            result = add(num1, num2)
                        elif operation in ['minus', 'subtract', '-']:
                            result = subtract(num1, num2)
                        elif operation in ['times', 'multiply', '*']:
                            result = multiply(num1, num2)
                        elif operation in ['divide', 'divided by', '/']:
                            result = divide(num1, num2)
                        else:
                            result = "Operation not recognized."

                        response = f"The result is {result}"
                    else:
                        response = "I couldn't understand the calculation."

                    if textMode == True:
                        print(f"{bot_name}: {response}")
                        if ProbMode == True:
                            print(prob.item())
                            print(tag)
                    else:
                        print(f"{bot_name}: {response}")
                        speak(response)

                    
                    logging.info(f'Bot response: {response}')


                # Fraction
                elif tag == "fraction":
                    # Extract numbers and operation from the user's input
                    num1, operation, num2 = extract_numbers_for_fraction(sentence)
                    
                    if num1 and num2 and operation:
                        response = calculate_fraction(num1, operation, num2)
                    else:
                        response = "I couldn't understand the calculation."

                    if textMode == True:
                        print(f"{bot_name}: {response}")
                        if ProbMode == True:
                            print(prob.item())
                            print(tag)
                    else:
                        print(f"{bot_name}: {response}")
                        speak(response)

                    logging.info(f'Bot response: {response}')


                # Handles default responses
                else:

                    response = random.choice(intent['responses'])

                    if textMode == True:
                        print(f"{bot_name}: {response}")
                        if ProbMode == True:
                            print(prob.item())
                    else:
                        print(f"{bot_name}: {response}")
                        speak(response)

                    
                    logging.info(f'Bot response: {response}')
                break

    else:
        for intent in intents['intents']:
            if intent["tag"] == "noanswer":
                response = random.choice(intent['responses'])
                
                if textMode == True:
                    print(f"{bot_name}: {response}")
                    if ProbMode == True:
                        print(prob.item())
                else:
                    print(f"{bot_name}: {response}")
                    speak(response)

                    
                    logging.info(f'Bot response: {response}')
                break

