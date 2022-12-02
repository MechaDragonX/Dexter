#!/usr/bin/env python

import discord

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

client.run("ODg2NjgxNzg4NDk4NDUyNTEx.GdC3i_.tLUq4f_fBQvnHRGOL0LTJmlrq51S9nSn-EZ2xU")
