import pytest

from consts import Rarity
from modules.card import Card, parse_card_str

class TestCard:
    def test_limit_two_same_name(self, kuriboh_ex_common, kuriboh_ex_crown):
        assert kuriboh_ex_common.limit_two(kuriboh_ex_crown)
        assert kuriboh_ex_crown.limit_two(kuriboh_ex_common)
    
    def test_limit_two_different_name(self, kuriboh, kuriboh_ex_common):
        assert not kuriboh.limit_two(kuriboh_ex_common)
        assert not kuriboh_ex_common.limit_two(kuriboh)

    def test_eq_same(self, kuriboh):
        new_kuriboh = Card("Kuriboh", Rarity.DIAMOND_1, "Y1006")
        assert kuriboh == new_kuriboh
        assert new_kuriboh == kuriboh

    def test_eq_different(self, kuriboh, kuriboh_ex_crown):
        assert kuriboh != kuriboh_ex_crown
        assert kuriboh_ex_crown != kuriboh

    def test_hashing(self, kuriboh, kuriboh_ex_common, kuriboh_ex_crown):
        card_set = {kuriboh, kuriboh_ex_common}
        assert kuriboh in card_set
        assert kuriboh_ex_common in card_set
        assert kuriboh_ex_crown not in card_set

    def test_parse_card_str_success(self, kuriboh_ex_common):
        kuriboh_str = "Kuriboh ex (◊◊◊◊ Y1069)"
        parsed_kuriboh = parse_card_str(kuriboh_str)
        assert parsed_kuriboh == kuriboh_ex_common
        assert parsed_kuriboh.name == kuriboh_ex_common.name
        assert parsed_kuriboh.rarity == kuriboh_ex_common.rarity
        assert parsed_kuriboh.id == kuriboh_ex_common.id

    def test_parse_card_str_failure(self):
        malformed = "Kuriboh (◊◊◊◊◊☆◊ - fake id)"
        with pytest.raises(ValueError) as e:
            parse_card_str(malformed)

@pytest.fixture
def kuriboh_ex_common():
    return Card("Kuriboh ex", Rarity.DIAMOND_4, "Y1069")

@pytest.fixture
def kuriboh_ex_crown():
    return Card("Kuriboh ex", Rarity.CROWN, "Y1169")

@pytest.fixture
def kuriboh():
    return Card("Kuriboh", Rarity.DIAMOND_1, "Y1006")