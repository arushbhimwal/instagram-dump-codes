import requests

# Replace with your access token and Instagram user IDs.
ACCESS_TOKEN = 'your_long_lived_access_token'
INSTAGRAM_USER_IDS = [
    'arush_bhimwal',
    'amextaken',
    'arush.onion',
    'majestical_gaming',
    'horizon_personal_computers',
    'arcanebyte.games'
]

def get_instagram_account_data(user_id):
    """Fetches data for a given Instagram account."""
    url = f'https://graph.facebook.com/v17.0/{user_id}'
    params = {
        'fields': 'username,followers_count,media_count,ig_id',
        'access_token': ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'username': data.get('username'),
            'followers_count': data.get('followers_count'),
            'media_count': data.get('media_count'),
            'ig_id': data.get('ig_id')
        }
    else:
        return {'error': response.json().get('error', {}).get('message', 'Unknown error')}

def main():
    all_accounts_data = {}
    for user_id in INSTAGRAM_USER_IDS:
        data = get_instagram_account_data(user_id)
        all_accounts_data[user_id] = data

    for user_id, data in all_accounts_data.items():
        print(f"Data for Instagram User ID {user_id}:")
        print(data)
        print()

if __name__ == "__main__":
    main()
