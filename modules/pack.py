import numpy as np
import time
import sys

import utils.probability
from modules.card import Card

class Pack:
    def __init__(self, name="Dummy Pack", available_cards=[], pull_rates=[], rare_pack_rate=0.00050):
        # Traits shared among ALL packs of this type
        self.name = name
        self.available = np.array(available_cards, dtype=Card)
        self.pull_rates = pull_rates
        self.rare_pack_rate = rare_pack_rate

        # Traits unique to THIS pack
        self.is_rare = None # set to True or False when self.open is called
        self.unopened = True # set to False when self.open is called
        self.cards = [] # cards are generated when pack is opened

        # self.available is a array of cards available in packs of this type. Array indices matter for aligning probabilities for np.random.choice
        # self.probs is a 2D array of length 6
        # self.probs[0] is a array representing each card's probability of being drawn as the FIRST card of a regular pack,
        # self.probs[1] is a array representing each card's probability of being drawn as the SECOND card of a regular pack,
        # etc...
        # self.probs[5] is a array representing each card's probability of being drawn as ANY card in a RARE PACK
        self.probs = np.ndarray((6, len(self.available)))
        for pack_position in range(6):
            for y, card in enumerate(self.available):
                self.probs[pack_position][y] = pull_rates[pack_position][card.rarity]
        # normalize probabilities to sum to 1 (accounts for rounding error summing to 0.99999...)
        self.probs = utils.probability.normalize_probabilities(self.probs, axis=1)

    def open(self, instantaneous):
        if self.unopened:
            sys.stdout.write("Opening pack!\n")
            if not instantaneous:
                time.sleep(0.5)
            rare_pack_check = np.random.rand()
            if rare_pack_check < self.rare_pack_rate: # RARE PACK
                sys.stdout.write(f"WOOWWWWW YOU GOT A RARE PACK!!! This only occurs {self.rare_pack_rate*100}% of the time!!\n")
                self.is_rare = True
                for x in range(5):
                    card = np.random.choice(self.available, 1, replace=True, p=self.probs[5])[0]
                    sys.stdout.write(f"Opened: {card}!\n")
                    if not instantaneous:
                        time.sleep(0.5)
                    self.cards.append(card)
            else: # REGULAR PACK
                self.is_rare = False
                for x in range(5):
                    card = np.random.choice(self.available, 1, replace=True, p=self.probs[x])[0]
                    sys.stdout.write(f"Opened: {card}!\n")
                    if not instantaneous:
                        time.sleep(0.5)
                    self.cards.append(card)
            self.unopened = False

            sys.stdout.write(f"Summary: {str(self.cards)}\n\n")
            return self.cards
        else:
            sys.stderr.write("Can't open pack that has already been unsealed... (mitchell check your code, this shouldn't happen)\n")
            return None

    def __str__(self):
        if self.unopened:
            return f"Pack {self.name} (unopened)"
        else:
            return f"Pack {self.name} containing {[f'{card.name} ({card.id})' for card in self.cards]}"

    def __repr__(self):
        return f"Pack ({self.name}) Unopened: {self.unopened} Available: {self.available} Pull Rates: {self.pull_rates}"
