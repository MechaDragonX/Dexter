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
    await interaction.response.defer()
    name = name.lower().replace(' ', '-')
    if not Commands.quick_search(name):
        await interaction.followup.send(
            'That Pokémon does not exist!\n\nDid you spell the name right? The name needs to be spelled exactly right, with some exceptions:\n"ho oh" works for "Ho-oh", \n"mr mime" works for "Mr. Mime", \n"farfetchd" works for "Farfetch\'d", \n"type null" works for "Type: Null", \n"flabebe" works for "Flabébé", \n"nidoran f" works for "Nidoran ♀", \nand "nidoran m" works for "Nidoran ♂"\nNames with dashes, periods, apostrophes, colons, and accents, do not need them.\n\nTry again anytime!'
        )
    else:
        try:
            await interaction.followup.send(
                embed=Commands.search(pokebase.pokemon_species(name).id)
            )
        except:
            await interaction.followup.send(
                'Something went wrong!\n\nTry again anytime!'
            )
@tree.command(name='search_id', description='Search for a Pokémon by its National Pokédex entry number')
async def search_id(interaction: discord.Interaction, id: int):
    await interaction.response.defer()
    if not Commands.quick_search(id):
        await interaction.followup.send(
            'That Pokémon does not exist!'
        )
    else:
        try:
            await interaction.followup.send(
                embed=Commands.search(id)
            )
        except:
            await interaction.followup.send(
                'Something went wrong!\n\nTry again anytime!'
            )

@tree.command(name='namae_kensaku_kana', description='にほんごの　なまえで　ポケモンを　けんさくする（漢字なし）')
async def namae_kensaku_kana(interaction: discord.Integration, name: str):
    await interaction.response.defer()
    id = Commands.get_id(name, 1)
    if id == -1:
        await interaction.followup.send(
            'そのポケモンを見つけられない！もしかして、入力ミス？\n名前を直してまた呼んでね！'
        )
    else:
        try:
            await interaction.followup.send(
                embed=Commands.search(id, 1)
            )
        except:
            await interaction.followup.send(
                '何かのエラーが発生したようだ！\nボクの悪いかもしれないから、また呼んでね！'
            )
@tree.command(name='namae_kensaku_kanji', description='日本語の名前でポケモンを検索する（漢字あり）')
async def namae_kensaku_kanji(interaction: discord.Integration, name: str):
    await interaction.response.defer()
    id = Commands.get_id(name, 2)
    if id == -1:
        await interaction.followup.send(
            'そのポケモンを見つけられない！もしかして、入力ミス？\n名前を直してまた呼んでね！'
        )
    else:
        try:
            await interaction.followup.send(
                embed=Commands.search(id, 2)
            )
        except:
            await interaction.followup.send(
                '何かのエラーが発生したようだ！\nボクの悪いかもしれないから、また呼んでね！'
            )

bot.run(token)
