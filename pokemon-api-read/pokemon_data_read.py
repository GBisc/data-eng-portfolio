import requests

# Get one Pokemon and print it
response = requests.get('https://pokeapi.co/api/v2/pokemon/1')
pokemon_data = response.json()
print(f"Pokemon: {pokemon_data['name']}")
print(f"Height: {pokemon_data['height']}")
print(f"Weight: {pokemon_data['weight']}")
