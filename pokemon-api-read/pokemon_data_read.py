import requests
import pandas as pd
import asyncio
import aiohttp
import time


def extract_pokemon_data(pokemon_data):
    """Extract comprehensive data from Pokemon API response"""
    
    # Basic info
    pokemon = {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'base_experience': pokemon_data.get('base_experience', 0)
    }
    
    # Extract types (Pokemon can have 1 or 2 types)
    types = pokemon_data.get('types', [])
    pokemon['type_1'] = types[0]['type']['name'] if len(types) > 0 else None
    pokemon['type_2'] = types[1]['type']['name'] if len(types) > 1 else None
    
    # Extract base stats
    stats = pokemon_data.get('stats', [])
    for stat in stats:
        stat_name = stat['stat']['name'].replace('-', '_')  # Convert special-attack to special_attack
        pokemon[stat_name] = stat['base_stat']
    
    # Extract abilities
    abilities = pokemon_data.get('abilities', [])
    pokemon['ability_1'] = abilities[0]['ability']['name'] if len(abilities) > 0 else None
    pokemon['ability_2'] = abilities[1]['ability']['name'] if len(abilities) > 1 else None
    
    return pokemon

def get_pokemon_detailed(pokemon_id):
    """Get detailed Pokemon data with error handling"""
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        response.raise_for_status()
        pokemon_data = response.json()
        return extract_pokemon_data(pokemon_data)
    except Exception as e:
        print(f"❌ Failed to get Pokemon #{pokemon_id}: {e}")
        return None

pokemon_list = []

# Get first 25 Pokemon with detailed data
for pokemon_id in range(1, 26):
    print(f"Fetching detailed data for Pokemon #{pokemon_id}...")
    pokemon = get_pokemon_detailed(pokemon_id)
    if pokemon:
        pokemon_list.append(pokemon)

df = pd.DataFrame(pokemon_list)
df.to_csv('pokemon_detailed.csv', index=False)
print(f"✅ Saved {len(df)} Pokemon with detailed stats")
print("\nColumns:", list(df.columns))
print("\nSample data:")
print(df[['name', 'type_1', 'type_2', 'hp', 'attack', 'defense']].head())

async def fetch_pokemon_async(session, pokemon_id):
    """Fetch Pokemon data asynchronously"""
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
        async with session.get(url) as response:
            if response.status == 200:
                pokemon_data = await response.json()
                return extract_pokemon_data(pokemon_data)
            else:
                print(f"❌ HTTP {response.status} for Pokemon #{pokemon_id}")
                return None
    except Exception as e:
        print(f"❌ Error fetching Pokemon #{pokemon_id}: {e}")
        return None

async def get_pokemon_batch_async(pokemon_ids):
    """Get multiple Pokemon concurrently"""
    async with aiohttp.ClientSession() as session:
        # Create tasks for all Pokemon
        tasks = [fetch_pokemon_async(session, pokemon_id) for pokemon_id in pokemon_ids]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        
        # Filter out failed requests
        return [pokemon for pokemon in results if pokemon is not None]

# Compare sync vs async performance
def compare_performance():
    # Test with first 20 Pokemon
    test_ids = list(range(1, 21))
    
    # Synchronous version (from Version 5)
    print("🐌 Testing synchronous version...")
    start_time = time.time()
    sync_results = []
    for pokemon_id in test_ids:
        pokemon = get_pokemon_detailed(pokemon_id)
        if pokemon:
            sync_results.append(pokemon)
    sync_time = time.time() - start_time
    
    # Asynchronous version
    print("🚀 Testing asynchronous version...")
    start_time = time.time()
    async_results = asyncio.run(get_pokemon_batch_async(test_ids))
    async_time = time.time() - start_time
    
    print(f"\n📊 Performance Comparison:")
    print(f"Sync:  {sync_time:.1f} seconds for {len(sync_results)} Pokemon")
    print(f"Async: {async_time:.1f} seconds for {len(async_results)} Pokemon")
    print(f"Speedup: {sync_time/async_time:.1f}x faster!")
    
    return async_results

if __name__ == "__main__":
    pokemon_data = compare_performance()

    # Save the async results
    df = pd.DataFrame(pokemon_data)
    df.to_csv('pokemon_async.csv', index=False)
    print(f"✅ Saved {len(df)} Pokemon using async method")
