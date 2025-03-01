#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
import discord
from enum import IntEnum
import json
import pokebase
import requests

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
        'Entry from "{0}"'
    ]
    _template_text_ja = [
        '分類',
        'ずかんの説明文',
        'タイプ',
        '高さ',
        '重さ',
        '特性',
        '説明文　『{0}』より'
    ]
    # All official artwork is 475*475
    # Embed color
    _color = 0xf4533A

    def get_id(name: str, language: Language = Language.JapaneseKana) -> int:
        match language:
            case Language.JapaneseKana:
                return Commands._get_id_ja(name)
            case Language.JapaneseKanji:
                return Commands._get_id_ja(name)
    def _get_id_ja(name: str) -> int:
        with open(f'{__file__.removesuffix("commands.py")}data/jp_names.json') as file:
            jp_names = json.load(file)
            id_set = { i for i in jp_names if jp_names[i] == name }

            if len(id_set) != 0:
                return int(id_set.pop())
            else:
                return -1
            
    # Returns if query exists as a Pokemon
    def quick_search(query: str) -> bool:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{query}/')
        if response.status_code == 200:
            return True
        else:
            return False

    def search(id: int, language: Language = Language.English) -> discord.Embed:
        species = pokebase.pokemon_species(id)
        pokemon = pokebase.pokemon(id)

        title = Commands._get_pokemon_name(name_list=species.names, language=language)
        image_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png'
        genus = Commands._get_pokemon_genus(genus_list=species.genera, language=language)

        entry_game = Commands._get_dex_entry_and_game(entry_list=species.flavor_text_entries, language=language)
        if entry_game == None:
            return None
        entry = entry_game[0]
        game = entry_game[1]

        types = Commands._get_types(type_list=pokemon.types, language=language)
        height = Commands._get_height(api_height=pokemon.height, language=language)
        weight = Commands._get_weight(api_weight=pokemon.weight, language=language)
        abilities = Commands._get_abilities(ability_list=pokemon.abilities, language=language)

        embed = Commands._gen_embed(
            title=title, image_url=image_url,
            genus=genus, entry=entry, game=game, types=types,
            height=height, weight=weight,
            abilities=abilities, language=language
        )

        return embed

    def _get_pokemon_name(name_list: list, language: Language) -> str:
        i = 0
        while i < len(name_list):
            if name_list[i].language.name == Commands._lang_codes[language]:
                return name_list[i].name
            i += 1
    def _get_pokemon_genus(genus_list: list, language: Language) -> str:
        i = 0
        while i < len(genus_list):
            if genus_list[i].language.name == Commands._lang_codes[language]:
                return genus_list[i].genus
            i += 1
    def _get_dex_entry_and_game(entry_list: list, language: Language) -> list:
        result = []
        entry = ''
        version_api = None
        game = ''
        i = 0
        while i < len(entry_list):
            if entry_list[i].language.name == Commands._lang_codes[language]:
                entry = entry_list[i].flavor_text
                # get to look up game name
                version_api = pokebase.version(entry_list[i].version.name)
                break
            i += 1
        if entry == '':
            return None
        j = 0
        while j < len(version_api.names):
            # No name exists for ja, only ja-Hrkt. Likely because all names after GS were katakana only
            if version_api.names[j].language.name == Commands._lang_codes[language] or version_api.names[j].language.name[:2] == Commands._lang_codes[language]:
                game = version_api.names[j].name
                break
            j += 1
        # I noticed leading spaces with ソード (sword), so just in case
        result.append(entry.strip())
        result.append(game.strip())
        return result
    def _get_types(type_list: list, language: Language) -> str:
        types = ''
        i = 0
        j = 0
        while i  < len(type_list):
            while j < len(type_list[i].type.names):
                if type_list[i].type.names[j].language.name == Commands._lang_codes[language]:
                    match language:
                        case Language.English:
                            if i == 0 and len(type_list) >= 2:
                                types += f'{type_list[i].type.names[j].name}, '
                            else:
                                types += type_list[i].type.names[j].name
                            j = 0
                            break
                        case Language.JapaneseKana:
                            if i == 0 and len(type_list) == 2:
                                types += f'{type_list[i].type.names[j].name}　'
                            else:
                                types += type_list[i].type.names[j].name
                            j = 0
                            break
                        case Language.JapaneseKanji:
                            if i == 0 and len(type_list) == 2:
                                types += f'{type_list[i].type.names[j].name}　'
                            else:
                                types += type_list[i].type.names[j].name
                            j = 0
                            break
                j += 1
            i += 1
        return types
    def _get_height(api_height: int, language: Language) -> str:
        meter = api_height / 10
        match language:
            case Language.English:
                foot = int((meter * 3.281) - float(Decimal(meter * 3.281) % 1))
                inch = round(float(Decimal(meter * 3.281) % 1) *  12)
                if inch == 12:
                    foot =  foot + 1
                    inch = 0
                return f'{meter}m / {foot}\'{inch}"'
            case Language.JapaneseKana:
                return f'{meter}m'
            case Language.JapaneseKanji:
                return f'{meter}m'
    def _get_weight(api_weight: int, language: Language) -> str:
        match language:
            case Language.English:
                return f'{api_weight / 10}kg / {round((api_weight / 10) * 2.205, 1)}lb'
            case Language.JapaneseKana:
                return f'{api_weight / 10}kg'
            case Language.JapaneseKanji:
                return f'{api_weight / 10}kg'
    def _get_abilities(ability_list: list, language: Language) -> str:
        abilities = ''
        i = 0
        j = 0
        while i  < len(ability_list):
            while j < len(ability_list[i].ability.names):
                if ability_list[i].ability.names[j].language.name == Commands._lang_codes[language]:
                    match language:
                        case Language.English:
                            if (i < len(ability_list) - 1) and len(ability_list) >= 2:
                                abilities += f'{ability_list[i].ability.names[j].name}, '
                            else:
                                abilities += ability_list[i].ability.names[j].name
                            if (i == len(ability_list) - 1) and ',' in abilities:
                                abilities += ' (Hidden)'
                            j = 0
                            break
                        case Language.JapaneseKana:
                            if (i < len(ability_list) - 1) and len(ability_list) >= 2:
                                abilities += f'{ability_list[i].ability.names[j].name}　'
                            else:
                                abilities += ability_list[i].ability.names[j].name
                            if (i == len(ability_list) - 1) and '　' in abilities:
                                abilities += '（かくれ）'
                            j = 0
                            break
                        case Language.JapaneseKanji:
                            if (i < len(ability_list) - 1) and len(ability_list) >= 2:
                                abilities += f'{ability_list[i].ability.names[j].name}　'
                            else:
                                abilities += ability_list[i].ability.names[j].name
                            if (i == len(ability_list) - 1) and '　' in abilities:
                                abilities += '（かくれ）'
                            j = 0
                            break
                j += 1
            i += 1
        return abilities

    def _gen_embed(title, image_url, genus, entry, game, types, height, weight, abilities, language)  -> discord.Embed:
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
