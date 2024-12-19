from datetime import datetime
import time
import sys

from modules.collection import Collection
from modules.expansion import Expansion
from modules.pack import Pack
from utils.fileio import load_expansions

def main():
    all_expansions = load_expansions('./expansion-files/mythical-island.json')

    expansion = prompt_expansion_selection(all_expansions)
    pack_type = prompt_pack_selection(expansion, all_expansions)
    sys.stdout.write(f"===== AVAILABLE CARDS IN {expansion.name} {[pack_type.name]} =====\n")
    sys.stdout.write(str(pack_type.available))
    sys.stdout.write("\n")
    num_packs = prompt_number_of_packs(expansion, all_expansions)

    sys.stdout.write(f"Opening {num_packs} packs of {expansion}!\n")
    time.sleep(1.5)
    collection = Collection()
    packs = [Pack(pack_type.name, pack_type.available, pack_type.pull_rates, pack_type.rare_pack_rate) for _ in range(num_packs)]
    for x, pack in enumerate(packs):
        received = pack.open()
        for card in received:
            collection.add(card)
        if x < len(packs) - 1:
            input("\nPress any character to continue...")

    sys.stdout.write("Summary of final results:\n")
    sys.stdout.write(str(collection))

    # TODO: Add save collection to file
    #     
    # save_desired = input("\nSave results to file? (y/n, default n)\n")
    # if len(save_desired) > 0 and save_desired[0] == 'y':
    #     save_filename = input("File name (default is collection-{timestamp}.json): ")
    #     if len(save_filename) == 0:
    #         save_filename = f"collection-{datetime.now()}.json"

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
    names = [pack.name for pack in selected_exp.packs]
    selected = None
    while type(selected) is not int:
        try:
            sys.stdout.write(f"===== AVAILABLE PACKS IN {selected_exp.name} =====\n")
            for i in range(len(names)):
                sys.stdout.write(f"{i}: {names[i]}\n")
            sys.stdout.write(f"{i+1}: Back to Expansion Selection\n")
            selected = int(input("\nSelect Pack: "))
            if selected < 0 or selected > len(names):
                raise ValueError
            elif selected == len(names):
                sys.stdout.write("\n")
                prompt_expansion_selection(expansions)
                selected = None
        except ValueError:
            sys.stderr.write(f"You entered {selected}, please select a valid int value matching an available pack within {selected_exp.name}.\n")
            selected = None
    sys.stdout.write(f"You selected {selected}: {names[selected]}\n")
    return selected_exp.packs[selected]

def prompt_number_of_packs(expansion, all_expansions):
    num_packs = None
    while type(num_packs) is not int:
        try:
            num_packs = int(input("How many packs will you open? (0 to return to pack selection)\n"))
            if num_packs < 0:
                raise ValueError
            elif num_packs == 0:
                sys.stdout.write("\n")
                prompt_pack_selection(expansion, all_expansions)
                num_packs = None
        except ValueError:
            sys.stderr.write(f"You entered {num_packs}, please select a valid number of packs to open (positive int).\n")
            num_packs = None
    return num_packs

if __name__ == "__main__":
    main()

        
        

    

    

    