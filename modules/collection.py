class Collection:
    def __init__(self):
        self.collection = {}

    def add(self, card):
        if card in self.collection:
            self.collection[card] += 1
        else:
            self.collection[card] = 1

    def __str__(self):
        string = "{\n"
        for card, count in self.collection.items():
            string += f"\t{str(card)}: {str(count)}\n"
        string += "}"
        return string