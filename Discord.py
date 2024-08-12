import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
from datetime import datetime
import asyncio
import typing
from turtle import title
from discord import File
from typing import Optional

import random
import json
import torch
import os
from model import NeuralNet
from nltk_utils import tokenize, bag_of_words
from functionality import get_weather, get_coordinates, take_screenshot, save_screenshot, recognize_speech_from_mic, speak

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents and model
with open("data/intents.json", 'r') as f:
    intents_ = json.load(f)


with open('config.json') as f:
    config = json.load(f)



token = config['DISCORD_TOKEN']

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
bot_name = "Ai"




# ******************************************************************************************************************************************

prf = "."

# ******************************************************************************************************************************************

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prf, intents=intents)
bot.remove_command("help")

###########################################################################################################################################



# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("`You don't have permission to use this command.`")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`Fill the required argument correctly!`")

    elif isinstance(error, commands.MissingRole):
        await ctx.send("`You don't have the required role(s)!`")

    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("`Invalid command`")

    else:
        raise error






# on bot ready
@bot.event
async def on_ready():
    print('{0.user}'.format(bot))
    print("Online")
    print("----------")

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f"Prefix '{prf}'"))



# this is ping
@bot.command()
async def ping(ctx):
    await ctx.send(f"pong! `{round(bot.latency * 1000)} ms`")



# this is hi
@bot.command()
async def r(ctx, str_):
    sentence = str_


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
        for intent in intents_['intents']:
            if tag == intent["tag"]:



                # Shows date
                if tag == "date":
                    date = datetime.now().strftime('%Y-%m-%d')
                    response = random.choice(intent['responses'])

                    print(f"{bot_name}: {response} {date}")
                    await ctx.send(f"{response} {date}")



                # Tells time
                elif tag == "time":
                    time = datetime.now().strftime('%H:%M:%S')
                    response = random.choice(intent['responses'])
                    await ctx.send(f"{response} {time}")


                # Handles default responses
                else:
                    response = random.choice(intent['responses'])
                    await ctx.send(f"{response}")
                    await ctx.send(f"Prob: {prob.item()}")

    else:
        for intent in intents_['intents']:
            if intent["tag"] == "noanswer":
                response = random.choice(intent['responses'])
                
                await ctx.send(f"{response}")











bot.run(token)