#!/usr/bin/env python

import asyncio
import discord
import pokebase

from commands import Commands

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
    name = name.lower().replace(' ', '-')
    await interaction.response.send_message(
        embed=Commands.search(pokebase.pokemon_species(name).id)
    )
@tree.command(name='search_id', description='Search for a Pokémon by its National Pokédex entry number')
async def search_id(interaction: discord.Interaction, id: int):
    await interaction.response.send_message(
        embed=Commands.search(id)
    )
@tree.command(name='namae_kensaku_kana', description='にほんごの　なまえで　ポケモンを　けんさくする（漢字なし）')
async def namae_kensaku_kana(interaction: discord.Integration, name: str):
    await interaction.response.send_message(
        embed=Commands.search(Commands.get_id(name, 1), 1)
    )
@tree.command(name='namae_kensaku_kanji', description='日本語の名前でポケモンを検索する（漢字あり）')
async def namae_kensaku_kanji(interaction: discord.Integration, name: str):
    await interaction.response.defer()
    id = Commands.get_id(name, 2)
    # if id == -1:
    #     await interaction.response.send_message(
    #         'あのポケモンを見つけられない！もしかして、入力ミス？また呼んでね！'
    #     )
    # else:
    await interaction.followup.send(
        embed=Commands.search(id, 2)
    )

bot.run(token)
