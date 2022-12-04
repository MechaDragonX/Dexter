#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
import discord
from enum import IntEnum
import pokebase

class Language(IntEnum):
    English = 0,
    JapaneseKana = 1,
    JapaneseKanji = 2

class Commands:
    _lang_codes = [
        'en',
        'ja-Hrkt',
        'ja'
    ]
    _template_text_en = [
        'Species',
        'Pokédex Entry',
        'Type',
        'Height',
        'Weight',
        'Abilities',
        'From "{0}"'
    ]
    _template_text_ja = [
        '分類',
        'ポケモンずかんの説明文',
        'タイプ',
        '高さ',
        '重さ',
        '特性',
        '『{0}』より'
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
        entry_list = species.flavor_text_entries
        i = len(entry_list) - 1
        while i >= 0:
            if entry_list[i].language.name == Commands._lang_codes[language]:
                entry = entry_list[i].flavor_text
                break
            i = i - 1

        game = ''
        match language:
            case Language.English:
                game = entry_list[i].version.names[7].name
            case Language.JapaneseKana:
                game = entry_list[i].version.names[0].name
            case Language.JapaneseKanji:
                game = entry_list[i].version.names[0].name

        types = ''
        i = 0
        while i  < len(pokemon.types):
            match language:
                case Language.English:
                    if i == 0 and len(pokemon.types) == 2:
                        types += f'{pokemon.types[i].type.names[7].name}, '
                    else:
                        types += pokemon.types[i].type.names[7].name
                case Language.JapaneseKana:
                    if i == 0 and len(pokemon.types) == 2:
                        types += f'{pokemon.types[i].type.names[0].name}　'
                    else:
                        types += pokemon.types[i].type.names[0].name
                case Language.JapaneseKanji:
                    if i == 0 and len(pokemon.types) == 2:
                        types += f'{pokemon.types[i].type.names[0].name}　'
                    else:
                        types += pokemon.types[i].type.names[0].name
            i += 1

        height = ''
        meter = pokemon.height / 10
        match language:
            case Language.English:
                foot = int((meter * 3.281) - float(Decimal(meter * 3.281) % 1))
                inch = round(float(Decimal(meter * 3.281) % 1) *  12)
                height = f'{meter}m / {foot}\'{inch}"'
            case Language.JapaneseKana:
                height = f'{meter}m'
            case Language.JapaneseKanji:
                height = f'{meter}m'

        weight = ''
        match language:
            case Language.English:
                weight = f'{pokemon.weight / 10}kg / {round((pokemon.weight / 10) * 2.205, 1)}lb"'
            case Language.JapaneseKana:
                weight = f'{pokemon.weight / 10}kg'
            case Language.JapaneseKanji:
                weight = f'{pokemon.weight / 10}kg'

        abilities = ''
        i = 0
        while i  < len(pokemon.abilities):
            match language:
                case Language.English:
                    if i == 0 and len(pokemon.abilities) == 2:
                        abilities += f'{pokemon.abilities[i].ability.names[7].name}, '
                    else:
                        abilities += pokemon.abilities[i].ability.names[7].name
                    if i == len(pokemon.abilities) - 1:
                        abilities += ' (Hidden)'
                case Language.JapaneseKana:
                    if i == 0 and len(pokemon.abilities) == 2:
                        abilities += f'{pokemon.abilities[i].ability.names[0].name}　'
                    else:
                        abilities += pokemon.abilities[i].ability.names[0].name
                    if i == len(pokemon.abilities) - 1:
                        abilities += '（かくれ）'
                case Language.JapaneseKanji:
                    if i == 0 and len(pokemon.abilities) == 2:
                        abilities += f'{pokemon.abilities[i].ability.names[0].name}　'
                    else:
                        abilities += pokemon.abilities[i].ability.names[0].name
                    if i == len(pokemon.abilities) - 1:
                        abilities += '（かくれ）'
            i += 1

        embed = discord.Embed(
            title=title,
            color=Commands._color,
        )
        embed.set_image(url=image_url)
        
        match language:
            case Language.English:
                # Add genius field
                embed.add_field(
                    name=Commands._template_text_en[0],
                    value=genus,
                    inline=False
                )
                # Add type field
                embed.add_field(
                    name=Commands._template_text_en[2],
                    value=types,
                    inline=False
                )
                # Add height field
                embed.add_field(
                    name=Commands._template_text_en[3],
                    value=height,
                    inline=True
                )
                # Add weight field
                embed.add_field(
                    name=Commands._template_text_en[4],
                    value=weight,
                    inline=True
                )
                # Add ability field
                embed.add_field(
                    name=Commands._template_text_en[5],
                    value=abilities,
                    inline=False
                )
                # Add entry field
                embed.add_field(
                    name=Commands._template_text_en[1],
                    value=entry,
                    inline=False
                )
                # Add game name as footer
                embed.set_footer(
                    text=Commands._template_text_en[6].format(game),
                )
            case Language.JapaneseKana:
                # Add genius field
                embed.add_field(
                    name=Commands._template_text_ja[0],
                    value=genus,
                    inline=False
                )
                # Add type field
                embed.add_field(
                    name=Commands._template_text_ja[2],
                    value=types,
                    inline=False
                )
                # Add height field
                embed.add_field(
                    name=Commands._template_text_ja[3],
                    value=height,
                    inline=True
                )
                # Add weight field
                embed.add_field(
                    name=Commands._template_text_ja[4],
                    value=weight,
                    inline=True
                )
                # Add ability field
                embed.add_field(
                    name=Commands._template_text_ja[5],
                    value=abilities,
                    inline=False
                )
                # Add entry field
                embed.add_field(
                    name=Commands._template_text_ja[1],
                    value=entry,
                    inline=False
                )
                # Add game name as footer
                embed.set_footer(
                    text=Commands._template_text_ja[6].format(game),
                )
            case Language.JapaneseKanji:
                # Add genius field
                embed.add_field(
                    name=Commands._template_text_ja[0],
                    value=genus,
                    inline=False
                )
                # Add type field
                embed.add_field(
                    name=Commands._template_text_ja[2],
                    value=types,
                    inline=False
                )
                # Add height field
                embed.add_field(
                    name=Commands._template_text_ja[3],
                    value=height,
                    inline=True
                )
                # Add weight field
                embed.add_field(
                    name=Commands._template_text_ja[4],
                    value=weight,
                    inline=True
                )
                # Add ability field
                embed.add_field(
                    name=Commands._template_text_ja[5],
                    value=abilities,
                    inline=False
                )
                # Add entry field
                embed.add_field(
                    name=Commands._template_text_ja[1],
                    value=entry,
                    inline=False
                )
                # Add game name as footer
                embed.set_footer(
                    text=Commands._template_text_ja[6].format(game),
                )

        return embed
