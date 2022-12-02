#!/usr/bin/env python

import discord

# Read info file to get any special information
info_file = open('info.txt', 'r').readlines()
# Read the first line to get the client token
token = token=info_file[0].strip()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('hey dex'):
        await message.channel.send('I am not Rotom')

client.run(token)
