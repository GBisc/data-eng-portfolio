import requests
import pandas as pd


def fetch_pokemon(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch Pokemon #{pokemon_id}: {e}")
        return None


def extract_pokemon_data(pokemon_data):
    if not pokemon_data:
        return None
    
    return {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'type': pokemon_data['types'][0]['type']['name'],
        'hp': pokemon_data['stats'][0]['base_stat'],
        'attack': pokemon_data['stats'][1]['base_stat']
    }


def main():
    print("Fetching Pokemon data...")
    
    pokemon_list = []
    pokemon_ids = range(1, 21)  # First 20 Pokemon
    
    for i, pokemon_id in enumerate(pokemon_ids, 1):
        print(f"Processing {i}/{len(pokemon_ids)}: Pokemon #{pokemon_id}")
        
        raw_data = fetch_pokemon(pokemon_id)
        pokemon_data = extract_pokemon_data(raw_data)
        
        if pokemon_data:
            pokemon_list.append(pokemon_data)
    
    # Save results
    if pokemon_list:
        df = pd.DataFrame(pokemon_list)
        df.to_csv('pokemon_basic.csv', index=False)
        print(f"\nSaved {len(df)} Pokemon to pokemon_basic.csv")
        print("\nFirst few results:")
        print(df[['name', 'type', 'hp', 'attack']].head())


if __name__ == "__main__":
    main()