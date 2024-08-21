class Card:
    def __init__(self, id, name, card_type, attribute=None, level=None, atk=None, def_=None):
        self.id = id
        self.name = name
        self.card_type = card_type  # This will be "Monster", "Spell", or "Trap"
        self.attribute = attribute
        self.level = level
        self.atk = atk
        self.def_ = def_

    def is_monster(self):
        return self.card_type == "Monster"

    def __repr__(self):
        if self.is_monster():
            return f"{self.name} (Type: {self.card_type}, Attribute: {self.attribute}, Level: {self.level}, ATK: {self.atk}, DEF: {self.def_})"
        else:
            return f"{self.name} (Type: {self.card_type})"
