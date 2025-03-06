from pathlib import Path
import json
import os
import sys

from consts import parse_rarity_str, default_settings
from modules.expansion import Expansion
from modules.pack import Pack
from modules.card import Card, parse_card_str
from modules.collection import Collection

def load_expansions(*args):
    """
        args: list of expansion filenames
        @returns objects representing all expansion
    """
    expansions = []
    current = Path(".")
    expansions_path = current / "expansion-files"
    for filename in args:
        full_path = expansions_path / filename
        file = open(full_path)
        exp_json = json.load(file)
        name = exp_json["name"]
        set_code = exp_json["set_code"]
        packs = []
        for pack_json in exp_json["packs"]:
            pack_name = pack_json["name"]
            cards = [
                Card(name=card_json["name"],
                     rarity=parse_rarity_str(card_json["rarity"]),
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
    expansions.sort(key=lambda exp: exp.set_code)
    return expansions

def load_collection(filename):
    base_path = get_script_folder() / "collections"
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    full_path = base_path / filename
    if not os.path.exists(full_path):
        raise FileNotFoundError(full_path)
    file = open(full_path, encoding="utf-8")
    collection = Collection()
    collection_json = json.load(file)
    try:
        for card_str in collection_json.keys():
            collection.add(parse_card_str(card_str))
    except (AttributeError, ValueError) as e:
        raise ValueError(f"Could not parse {filename}, please check formatting: {e}", file, 0)

    return collection

def save_collection(filename, collection, overwrite=False):
    base_path = get_script_folder() / "collections"
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    full_path = base_path / filename
    if os.path.exists(full_path) and not overwrite:
        return False
    else:
        with full_path.open('w', encoding="utf-8") as file:
            file.write(str(collection))
            sys.stdout.write(f"Saved collection to {full_path}!")
            return True
        return False

def get_script_folder():
    # path of main .py or .exe when converted with pyinstaller
    if getattr(sys, 'frozen', False):
        script_path = Path(os.path.dirname(sys.executable))
    else:
        script_path = Path(os.path.dirname(
            os.path.abspath(sys.modules['__main__'].__file__)
        ))
    return script_path

def get_settings():
    base_path = get_script_folder() / "settings"
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    full_path = base_path / 'settings.json'

    if not os.path.exists(full_path):
        set_settings(default = True)
        return get_settings()

    else:
        file = open(full_path, encoding="utf-8")
        settings_json = json.load(file)
        return settings_json

def set_settings(show_packs = 'keep current value', save_collection = 'keep current value', collection = 'keep current value', default = False):

    base_path = get_script_folder() / "settings"
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    full_path = base_path / 'settings.json'


    if default:
        settings = default_settings

    elif os.path.exists(full_path):
        settings = get_settings()
    else:
        print('Settings file not found! Restoring default settings.')
        set_settings(default = True)



    if not show_packs == 'keep current value':
        if show_packs:
            settings["Show packs"] = "Yes"
        else:
            settings["Show packs"] = "No"


    if not save_collection == 'keep current value':
        if save_collection:
            settings["Save to collection"] = "Yes"
        else:
            settings["Save to collection"] = "No"

    if not collection == 'keep current value':
        settings["Current Collection"] = collection


    settings_string = "{\n"
    for key, value in settings.items():
        print(key)
        print(value)
        settings_string += f"\t\"{key}\": \"{value}\",\n"
    settings_string = settings_string[0:-2]
    settings_string += "}"

    with full_path.open('w', encoding = "utf-8") as file:
        file.write(str(settings_string))



def _handle_rarity_json(rarity_json):
    rarity_rate = {}
    for rarity_str, p in rarity_json.items():
        rarity_rate[parse_rarity_str(rarity_str)] = p
    return rarity_rate