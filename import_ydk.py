from tqdm import tqdm
from getcards import *

def read_ydk_file(filepath):
    main_deck = []
    extra_deck = []
    side_deck = []

    current_section = None

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#main'):
                current_section = 'main'
            elif line.startswith('#extra'):
                current_section = 'extra'
            elif line.startswith('!side'):
                current_section = 'side'
            elif line.isdigit():
                if current_section == 'main':
                    main_deck.append(line)
                elif current_section == 'extra':
                    extra_deck.append(line)
                elif current_section == 'side':
                    side_deck.append(line)

    return main_deck, extra_deck, side_deck


def fetch_deck_from_ydk(filepath):
    main_deck_ids, extra_deck_ids, side_deck_ids = read_ydk_file(filepath)

    main_deck = []
    extra_deck = []
    side_deck = []

    print("Fetching Main Deck cards...")
    for card_id in tqdm(main_deck_ids, desc="Main Deck"):
        card = fetch_card_info(card_id=card_id)
        if card and card.is_monster():  # Only add Monster cards to the deck
            main_deck.append(card)
            print(f"Added {card.name} to Main Deck")

    print("\nFetching Extra Deck cards...")
    for card_id in tqdm(extra_deck_ids, desc="Extra Deck"):
        card = fetch_card_info(card_id=card_id)
        if card and card.is_monster():  # Only add Monster cards to the deck
            extra_deck.append(card)
            print(f"Added {card.name} to Extra Deck")

    print("\nFetching Side Deck cards...")
    for card_id in tqdm(side_deck_ids, desc="Side Deck"):
        card = fetch_card_info(card_id=card_id)
        if card and card.is_monster():  # Only add Monster cards to the deck
            side_deck.append(card)
            print(f"Added {card.name} to Side Deck")

    return main_deck, extra_deck, side_deck
