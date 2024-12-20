class Collection:
    def __init__(self, sort_order="rarity"):
        self.collection = {}
        self.sort_order = sort_order

    def add(self, card):
        if card in self.collection:
            self.collection[card] += 1
        else:
            self.collection[card] = 1

    def items(self):
        listed_items = list(self.collection.items())
        listed_items.sort(key=lambda x: x[0].rarity)
        return listed_items

    def __str__(self):
        string = "{\n"
        tuples = self.items()
        for card, count in tuples:
            string += f"\t\"{str(card)}\": {str(count)},\n"
        if len(tuples) > 0:
            string = string[:-2]
            string += "\n"
        string += "}"
        return string