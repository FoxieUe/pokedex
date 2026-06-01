import time
import requests
import pandas as pd

MAX_POKEMON_ID = 1025

def get_data(name_or_id):
    response_bd = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name_or_id}")
    response_sd = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name_or_id}")
    if response_bd.status_code != 200:
        print(f"Error in basic data for pokemon number - {name_or_id}")
    if response_sd.status_code != 200:
        print(f"Error in special data for pokemon number - {name_or_id}")
    if response_bd.status_code != 200 or response_sd.status_code != 200:
        return


    b_data = response_bd.json() #  BASIC INFORMATION
    pokemon_id = b_data["id"]
    weight = b_data["weight"]
    height = b_data["height"]
    types = b_data["types"]
    type1 = types[0]["type"]["name"]
    type2 = types[1]["type"]["name"] if len(types) > 1 else None
    sprite = b_data["sprites"]["front_default"]
    artwork = b_data["sprites"]["other"]["official-artwork"]["front_default"]
    artwork_shiny = b_data["sprites"]["other"]["official-artwork"]["front_shiny"]
    stats_list = b_data["stats"]
    stats = {s["stat"]["name"]:s["base_stat"] for s in stats_list}
    hp = stats.get("hp")
    attack = stats.get("attack")
    defense = stats.get("defense")
    special_attack = stats.get("special-attack")
    special_defense = stats.get("special-defense")
    speed = stats.get("speed")

    s_data = response_sd.json() #SPECIAL INFORMATION
    name = s_data["name"]
    species_list = s_data["genera"]
    species = next((s["genus"] for s in species_list if s["language"]["name"] == "en"), "Not Found")
    gen = s_data["generation"]["name"]
    name_list = s_data["names"]
    romanji_name = next((n["name"] for n in name_list if n["language"]["name"] == "ja-roma"),"Not Found")
    jap_name = next((n["name"] for n in name_list if n["language"]["name"] == "ja-hrkt"),"Not Found")
    flavor_text_list = s_data["flavor_text_entries"]
    flavor_text_raw = next((t["flavor_text"] for t in flavor_text_list if t["language"]["name"] == "en" ),"Not Found")
    flavor_text = flavor_text_raw.replace("\n", " ").replace("\f", " ")
    gender_rate = s_data["gender_rate"]
    if gender_rate == -1:
        female_ratio = 0
        male_ratio = 0
        gender_label = "Genderless"
    else:
        female_ratio = (gender_rate / 8) * 100
        male_ratio = 100 - female_ratio
        gender_label = f"Female {female_ratio:.1f}% / Male {male_ratio:.1f}%"
    is_baby = s_data["is_baby"]
    is_legendary = s_data["is_legendary"]
    is_mythical = s_data["is_mythical"]
    if is_mythical:
        special_group = "Mythical"
    elif is_legendary:
        special_group = "Legendary"
    elif is_baby:
        special_group = "Baby"
    else:
        special_group = "Ordinary"
    time.sleep(0.1)
    print(f"Pokemon {name} processed")
    return {
        "pokemon_id": pokemon_id,
        "name": name,
        "species" : species,
        "weight": weight,
        "height": height,
        "type1": type1,
        "type2": type2,
        "sprite": sprite,
        "artwork": artwork,
        "shiny_artwork": artwork_shiny,
        "hp": hp,
        "attack": attack,
        "defense": defense,
        "special_attack": special_attack,
        "special_defense": special_defense,
        "speed": speed,
        "gen": gen,
        "romanji": romanji_name,
        "jap_name": jap_name,
        "flavor_text": flavor_text,
        "female": female_ratio,
        "male": male_ratio,
        "gender_label": gender_label,
        "special_group": special_group
    }

pokemon_data_set = []

for poke in range(1, MAX_POKEMON_ID + 1):
    pokemon = get_data(poke)

    if pokemon:
        pokemon_data_set.append(pokemon)


df = pd.DataFrame(pokemon_data_set)
df.to_csv("pokemon_data.csv", index=False, encoding="utf-8-sig")




