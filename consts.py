from enum import Enum

class Rarity(Enum):
    DIAMOND_1 = 1
    DIAMOND_2 = 2
    DIAMOND_3 = 3
    DIAMOND_4 = 4
    STAR_1 = 5
    STAR_2 = 6
    STAR_3 = 7
    CROWN = 8

def rarity_str_to_enum(rarity_str):
    match rarity_str:
        case "1diamond":
            rarity = Rarity.DIAMOND_1
        case "2diamond":
            rarity = Rarity.DIAMOND_2
        case "3diamond":
            rarity = Rarity.DIAMOND_3
        case "4diamond":
            rarity = Rarity.DIAMOND_4
        case "1star":
            rarity = Rarity.STAR_1
        case "2star":
            rarity = Rarity.STAR_2
        case "3star":
            rarity = Rarity.STAR_3
        case "crown":
            rarity = Rarity.CROWN
        case _:
            raise ValueError(f"Found an invalid rarity in the expansion json: {rarity_str}")
    return rarity