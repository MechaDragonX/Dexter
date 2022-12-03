#!/usr/bin/env python

import discord
import pokebase

# Read info file to get any special information
info_file = open('info.txt', 'r').readlines()
# Read the first line to get the client token
token = token=info_file[0].strip()

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced =  False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Logged in as {self.user}')

bot = Client()
tree = discord.app_commands.CommandTree(bot)

@tree.command(name='search_name', description='Search for a Pokémon by its English name')
async def search_name(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokebase.pokemon_species(name.lower()).id}.png')
@tree.command(name='search_id', description='Search for a Pokémon by its National Pokédex entry number')
async def search_id(interaction: discord.Interaction, id: int):
    await interaction.response.send_message(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png')

bot.run(token)
