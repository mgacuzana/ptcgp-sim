from datetime import datetime
import getopt
import time
import sys

from modules.collection import Collection
from modules.expansion import Expansion
from modules.pack import Pack
from utils.fileio import load_expansions, save_collection

def main():
    in_batch_mode = handle_opts()
    all_expansions = load_expansions("genetic-apex.json", "mythical-island.json")

    expansion = prompt_expansion_selection(all_expansions)
    pack_type, expansion = prompt_pack_selection(expansion, all_expansions)
    num_packs, pack_type, expansion = prompt_number_of_packs(pack_type, expansion, all_expansions)

    sys.stdout.write(f"Opening {num_packs} packs of {expansion}!\n")
    if not in_batch_mode:
        time.sleep(1.5)
    collection = Collection()
    rare_pack_count = 0
    packs = [Pack(pack_type.name, pack_type.available, pack_type.pull_rates, pack_type.rare_pack_rate) for _ in range(num_packs)]
    for x, pack in enumerate(packs):
        received = pack.open(instantaneous=in_batch_mode)
        if pack.is_rare:
            rare_pack_count += 1
        for card in received:
            collection.add(card)
        if x < len(packs) - 1 and not in_batch_mode:
            input("\nPress any character to continue...")

    sys.stdout.write("Summary of final results:\n")
    sys.stdout.write(str(collection))
    sys.stdout.write(f"\nRare pack count: {rare_pack_count}\n")

    prompt_save_collection(collection)

def handle_opts():
    arguments = sys.argv[1:]
    short_opts = "b"
    long_opts = ["batch-mode"]
    selected_opts, vals = getopt.getopt(arguments, short_opts, long_opts)
    flags = [key for key, val in selected_opts if val == '']
    in_batch_mode = "--batch-mode" in flags or "-b" in flags
    return in_batch_mode

def prompt_expansion_selection(expansions):
    """
        @arg expansions: list of nested objects representing expansion json
        @returns the selected expansion object
    """
    names = [exp.name for exp in expansions]
    selected = None
    while type(selected) is not int:
        try:
            sys.stdout.write("===== AVAILABLE EXPANSIONS =====\n")
            for i in range(len(expansions)):
                sys.stdout.write(f"{i}: {names[i]}\n")
            selected = int(input("\nSelect Expansion: "))
            if selected < 0 or selected > len(expansions) - 1:
                raise ValueError
        except ValueError:
            sys.stderr.write(f"You entered {selected}, please select a valid int value matching an available expansion.\n")
            selected = None
    sys.stdout.write(f"You selected {selected}: {names[selected]}\n")
    return expansions[selected]

def prompt_pack_selection(selected_exp, expansions):
    selected = None
    while type(selected) is not int:
        try:
            names = [pack.name for pack in selected_exp.packs]
            sys.stdout.write(f"===== AVAILABLE PACKS IN {selected_exp.name} =====\n")
            for i in range(len(names)):
                sys.stdout.write(f"{i}: {names[i]}\n")
            sys.stdout.write(f"{i+1}: Back to Expansion Selection\n")
            selected = int(input("\nSelect Pack: "))
            if selected < 0 or selected > len(names):
                raise ValueError
            elif selected == len(names):
                sys.stdout.write("\n")
                selected_exp = prompt_expansion_selection(expansions)
                selected = None
        except ValueError:
            sys.stderr.write(f"You entered {selected}, please select a valid int value matching an available pack within {selected_exp.name}.\n")
            selected = None
    sys.stdout.write(f"You selected {selected}: {names[selected]}\n")
    return selected_exp.packs[selected], selected_exp

def prompt_number_of_packs(pack_type, expansion, all_expansions):
    num_packs = None
    while type(num_packs) is not int:
        try:
            sys.stdout.write(f"===== AVAILABLE CARDS IN {expansion.name} - {pack_type.name} =====\n")
            sys.stdout.write(str(pack_type.available))
            sys.stdout.write("\n")
            num_packs = int(input("How many packs will you open? (0 to return to pack selection)\n"))
            if num_packs < 0:
                raise ValueError
            elif num_packs == 0:
                sys.stdout.write("\n")
                pack_type, expansion = prompt_pack_selection(expansion, all_expansions)
                num_packs = None
        except ValueError:
            sys.stderr.write(f"You entered {num_packs}, please select a valid number of packs to open (positive int).\n")
            num_packs = None
    return num_packs, pack_type, expansion

def prompt_save_collection(collection):
    save_desired = input("\nSave results to file? (y/n, default n) ")
    if len(save_desired) > 0 and save_desired[0] == 'y':
        saved = False
        while not saved:
            save_filename = input("File name (default is collection-{timestamp}.json): ")
            if len(save_filename) == 0:
                save_filename = f"collection-{datetime.now().strftime("%Y-%m-%dT%H%M%S")}.json"
            elif not save_filename.endswith(".json"):
                save_filename += ".json"
            saved = save_collection(save_filename, collection)
            if not saved:
                overwrite = input("File already exists. Would you like to overwrite? (y/n, default n) ")
                if overwrite.startswith('y'):
                    saved = save_collection(save_filename, collection, overwrite=True)

if __name__ == "__main__":
    main()

        
        

    

    

    