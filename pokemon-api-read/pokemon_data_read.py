import requests

pokemon_list = []

for pokemon_id in range(1, 6):
    print(f"Fetching Pokemon #{pokemon_id}...")
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
    pokemon_data = response.json()
    
    simplified_pokemon = {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight']
    }
    pokemon_list.append(simplified_pokemon)

for pokemon in pokemon_list:
    print(pokemon)
