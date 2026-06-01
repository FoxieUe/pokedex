from flask import Flask, render_template, request
import pandas as pd


app = Flask(__name__)

try:
    df = pd.read_csv('pokemon_data.csv')
    df = df.fillna('')
except Exception as e:
    raise RuntimeError(f"Failed to load dataset: {e}")

ROMAN_MAP = {
    "1": "generation-i",
    "2": "generation-ii",
    "3": "generation-iii",
    "4": "generation-iv",
    "5": "generation-v",
    "6": "generation-vi",
    "7": "generation-vii",
    "8": "generation-viii",
    "9": "generation-ix"
}

STATS = [
    "hp",
    "attack",
    "special_attack",
    "defense",
    "special_defense",
    "speed"
]

@app.route("/")
def index():
    selected_gen = request.args.get("gen", "1")
    selected_type = request.args.get("type", "")

    gen_string = ROMAN_MAP.get(selected_gen, "generation-i")

    gen_mask = df["gen"].str.strip().str.lower() == gen_string.lower()
    filtered_df = df[gen_mask]

    type_list = pd.unique(filtered_df[['type1', 'type2']].values.ravel())
    type_list = [t for t in type_list if t != ""]

    if selected_type:
        type_mask = (filtered_df["type1"] == selected_type) | (filtered_df["type2"] == selected_type)
        filtered_df = filtered_df[type_mask]


    pokemons = filtered_df.to_dict('records')

    return render_template('index.html', pokemons=pokemons,
                           selected_gen=selected_gen, type_list=type_list,
                           selected_type=selected_type)

@app.route("/detail/<name>")
def pokemon_detail(name):
    try:
        current_idx = df[df["name"].str.lower() == name.lower()].index[0]
        selected_pokemon = df.iloc[current_idx].to_dict()
    except (IndexError, ValueError):
        return "Pokemon not found", 404

    prev_name = df.iloc[current_idx - 1]["name"].lower() if current_idx > 0 else None
    prev_sprite = df.iloc[current_idx - 1]["sprite"] if current_idx > 0 else None

    next_name = df.iloc[current_idx + 1]["name"].lower() if current_idx < len(df) - 1 else None
    next_sprite = df.iloc[current_idx + 1]["sprite"] if current_idx < len(df) - 1 else None





    return render_template('detail.html', pokemon=selected_pokemon,
                           stats=STATS, prev_name=prev_name, next_name=next_name,
                           prev_sprite=prev_sprite, next_sprite=next_sprite)

if __name__ == "__main__":
    app.run()
