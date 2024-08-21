import requests
import time
from classes import *


def fetch_card_info(card_id=None, name=None, timeout=5):
    base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

    # Adjust parameters depending on whether we're fetching by card_id or name
    params = {}
    if card_id:
        params['id'] = card_id
    elif name:
        params['name'] = name
    else:
        raise ValueError("Either card_id or name must be provided.")

    try:
        response = requests.get(base_url, params=params, timeout=timeout)
        time.sleep(0.05)  # Respect the rate limit

        if response.status_code == 200:
            card_data = response.json()
            if 'data' in card_data and card_data['data']:
                card_info = card_data['data'][0]
                card_type = card_info['type']

                # Ensure the card ID is passed when creating the Card object
                if "Monster" in card_type:
                    card = Card(
                        id=card_info['id'],  # Card ID
                        name=card_info['name'],
                        card_type="Monster",
                        attribute=card_info['attribute'],
                        level=card_info.get('level'),
                        atk=card_info.get('atk'),
                        def_=card_info.get('def')  # Use def_ instead of def
                    )
                else:
                    card = Card(
                        id=card_info['id'],  # Card ID
                        name=card_info['name'],
                        card_type="Spell" if "Spell" in card_type else "Trap"
                    )

                print(f"Card fetched: {card}")  # Debug print
                return card
            else:
                print(f"No card data found for {card_id or name}")  # Debug print
                return None
        else:
            print(f"Failed to fetch data for {card_id or name}, status code: {response.status_code}")  # Debug print
            return None

    except requests.exceptions.Timeout:
        print(f"Request for {card_id or name} timed out")
        return None
