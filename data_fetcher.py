import requests

api_key = "MrMUawMRUvQsI/dVxqEXdQ==FMVMuB2VCKdBcIk4"

def fetch_data(animal_name):
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary:
    {
        'name': ...,
        'taxonomy': {
        ...
        },
        'locations': [
        ...
        ],
        'characteristics': {
        ...
        },
    }
    """
    url = "https://api.api-ninjas.com/v1/animals"
    params = {'name': animal_name}
    headers = {'X-Api-Key': api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API error {response.status_code}: {response.text}")
    except requests.RequestException as error_network:
        print(f"❌ Network error: {error_network}")
    return []