#!/usr/bin/env python

import discord
from enum import IntEnum
import pokebase

class Language(IntEnum):
    English = 0,
    JapaneseKana = 1,
    JapaneseKanji = 2

class Commands:
    # Handles the names aren't just one or two English put together with a space
    _game_names = {
        'lets-go-pikachu': 'Let\'s Go, Pikachu!',
        'lets-go-eevee': 'Let\'s Go, Eevee!',
        'legends-arceus': 'Legends: Arceus'
    }
    _lang_codes = [
        'en',
        'ja-Hrkt',
        'ja'
    ]
    # All official artwork is 475*475
    _image_size = 200
    # Embed color
    _color = 0xf4533A

    def search(id: int, language:Language=Language.English) -> discord.Embed:
        species = pokebase.pokemon_species(id)
        pokemon = pokebase.pokemon(id)

        title = ''
        match language:
            case Language.English:
                title = species.names[8].name
            case Language.JapaneseKana:
                title = species.names[0].name
            case Language.JapaneseKanji:
                # Names are in Katakana anyway, and this prevents running into Czech
                # (a language games have never released in) which takes the spot right before Kanji
                title = species.names[0].name
        
        image_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png'

        description = ''
        genus =  ''
        match language:
            case Language.English:
                # Keep in mind while English is still entry 8, Romaji genus names are not stored
                genus = species.genera[7].genus
            case Language.JapaneseKana:
                genus = species.genera[0].genus
            case Language.JapaneseKanji:
                genus = species.genera[0].genus
        
        entry = ''
        game = ''
        entry_list = species.flavor_text_entries
        # current_entry_info = None
        i = len(entry_list) - 1
        while i >= 0:
            # current_entry_info = entry_list[i]
            if entry_list[i].language.name == Commands._lang_codes[language]:
                entry = entry_list[i].flavor_text
                if entry_list[i].version.name in Commands._game_names:
                    game = Commands._game_names[entry_list[i].version.name]
                else:
                    game = entry_list[i].version.name.title().replace('-', ' ')
                break
            i = i - 1
        
        description = f'{genus}\n\n{entry}\n\nFrom {game}'

        embed = discord.Embed(
            title=title,
            color=Commands._color,
            description=description
        )
        embed.set_image(url=image_url)

        return embed
