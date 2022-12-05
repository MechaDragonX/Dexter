#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pokebase

def create_dict() -> dict:
    jp_names: dict[int, str] = {}

    i = 1
    species = None
    while True:
        try:
            species = pokebase.pokemon_species(i)
        except:
            break

        jp_names[i] = species.names[0].name
        print(f'{jp_names[i]}　完成')

        i = i + 1
    
    return jp_names

with open('jp_names.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(create_dict()))

print('全記録　完成！')
