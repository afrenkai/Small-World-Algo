def find_all_valid_bridges(hand, target_name, deck):
    """
    Find all valid bridges between cards in the hand and the target card in the deck.

    :param hand: List of Card objects in the player's hand.
    :param target_name: Name of the target card the user wants to search for.
    :param deck: List of Card objects in the player's deck.
    :return: A string describing the valid bridges found.
    """
    target_card = None
    valid_bridges = []

    # Locate the target card in the deck
    for card in deck:
        if card.name == target_name:
            target_card = card
            break

    if not target_card:
        return f"Error: The target card '{target_name}' is not in the deck.", []

    # Find valid bridges
    for start_card in hand:
        for bridge_card in deck:
            if bridge_card.name != target_name and bridge_card.is_monster() and is_valid_bridge(start_card, bridge_card,
                                                                                                target_card):
                valid_bridges.append((start_card, bridge_card, target_card))

    if valid_bridges:
        result = "\n".join(
            [f"Bridge: {bridge.name} (from {start.name} to {target_card.name})" for start, bridge, target in
             valid_bridges])
        return result, valid_bridges
    else:
        return f"No valid bridge found between any card in hand and {target_name}.", []


def is_valid_bridge(start_card, bridge_card, target_card):
    """
    Check if the bridge_card is a valid bridge between start_card and target_card.

    :param start_card: The card in the player's hand.
    :param bridge_card: The card in the deck being considered as a bridge.
    :param target_card: The target card that the user wants to reach.
    :return: True if the bridge is valid, False otherwise.
    """
    return (count_matching_attributes(start_card, bridge_card) == 1 and
            count_matching_attributes(bridge_card, target_card) == 1)


def count_matching_attributes(card1, card2):
    """
    Count the number of matching attributes between two Monster cards.

    :param card1: First card object to compare.
    :param card2: Second card object to compare.
    :return: Number of matching attributes.
    """
    match_count = 0
    if card1.card_type == card2.card_type:
        match_count += 1
    if card1.attribute == card2.attribute:
        match_count += 1
    if card1.level == card2.level:
        match_count += 1
    if card1.atk == card2.atk:
        match_count += 1
    if card1.def_ == card2.def_:
        match_count += 1
    return match_count
