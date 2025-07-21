import requests
import pandas as pd

pokemon_list = []
first_x_pokemon = 10

for pokemon_id in range(1, (first_x_pokemon + 1)):
    print(f"Fetching Pokemon #{pokemon_id}...")
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
    pokemon_data = response.json()
    
    simplified_pokemon = {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'base_experience': pokemon_data['base_experience']
    }
    pokemon_list.append(simplified_pokemon)

df = pd.DataFrame(pokemon_list)
df.to_csv('pokemon_basic.csv', index=False)
print(f"Saved {len(df)} Pokemon to pokemon_basic.csv")
print(df.head())
