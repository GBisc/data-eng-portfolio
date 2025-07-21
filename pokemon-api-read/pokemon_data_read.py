import requests
import pandas as pd

def get_pokemon_safely(pokemon_id):
    """Get Pokemon data with error handling"""
    try:
        print(f"Fetching Pokemon #{pokemon_id}...")
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        
        response.raise_for_status()
        
        pokemon_data = response.json()
        return {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'],
            'height': pokemon_data['height'],
            'weight': pokemon_data['weight'],
            'base_experience': pokemon_data.get('base_experience', 0)  
        }
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get Pokemon #{pokemon_id}: {e}")
        return None

pokemon_list = []

for pokemon_id in range(1, 21):
    pokemon = get_pokemon_safely(pokemon_id)
    if pokemon:  
        pokemon_list.append(pokemon)

df = pd.DataFrame(pokemon_list)
df.to_csv('pokemon_with_errors.csv', index=False)
print(f"✅ Successfully saved {len(df)} Pokemon")
