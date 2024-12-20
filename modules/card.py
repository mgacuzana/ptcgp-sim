import re
from consts import parse_rarity_str

class Card:
    def __init__(self, name, rarity, id, card_type="", attack1="", attack2="", weakness="", retreat="", knockout_value=1):
        self.name = name
        self.rarity = rarity
        self.id = id
        self.card_type = card_type
        self.attack1 = attack1
        self.attack2 = attack2
        self.weakness = weakness
        self.retreat = retreat
        self.knockout_value = knockout_value

    def limit_two(self, other):
        """
            Determines if decks have limit 2 of these cards
            @returns true if card name (including ex) match exactly
        """
        if isinstance(other, Card):
            return self.name == other.name
        return False

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        return False

    def __str__(self):
        return f"{self.name} ({self.rarity.value} {self.id})"

    def __repr__(self):
        return f"{self.name} ({self.rarity.value} {self.id})"

    def __hash__(self):
        return hash(self.id)

def parse_card_str(card_str):
    pattern = re.compile(r'([\w ]+) \(([◊☆♕]+) (\w+)\)')
    matches = pattern.match(card_str)
    if not matches:
        raise ValueError(f"{card_str} does not match pattern {pattern}")
    return Card(matches.group(1), parse_rarity_str(matches.group(2)), matches.group(3))