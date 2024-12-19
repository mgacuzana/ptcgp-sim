import json

from consts import rarity_str_to_enum
from modules.expansion import Expansion
from modules.pack import Pack
from modules.card import Card

def load_expansions(*args):
    """
        args: list of expansion filenames
        @returns objects representing all expansion
    """
    expansions = []
    for filename in args:
        file = open(filename)
        exp_json = json.load(file)
        name = exp_json["name"]
        set_code = exp_json["set_code"]
        packs = []
        for pack_json in exp_json["packs"]:
            pack_name = pack_json["name"]
            cards = [
                Card(name=card_json["name"],
                     rarity=rarity_str_to_enum(card_json["rarity"]),
                     id=card_json["id"]
                    )
                for card_json in pack_json["cards"]
            ]
            pull_rates = [
                _handle_rarity_json(pack_json["card_rates"]["card1"]),
                _handle_rarity_json(pack_json["card_rates"]["card2"]),
                _handle_rarity_json(pack_json["card_rates"]["card3"]),
                _handle_rarity_json(pack_json["card_rates"]["card4"]),
                _handle_rarity_json(pack_json["card_rates"]["card5"]),
                _handle_rarity_json(pack_json["card_rates"]["rare"])
            ]
            rare_pack_rate = pack_json["rare_pack_rate"]
            pack = Pack(pack_name, available_cards=cards, pull_rates=pull_rates, rare_pack_rate=rare_pack_rate)
            packs.append(pack)

        expansions.append(Expansion(name, set_code, packs))
    return expansions

def _handle_rarity_json(rarity_json):
    rarity_rate = {}
    for rarity_str, p in rarity_json.items():
        rarity_rate[rarity_str_to_enum(rarity_str)] = p
    return rarity_rate