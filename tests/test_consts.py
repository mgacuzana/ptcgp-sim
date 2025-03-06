import pytest

from consts import Rarity, parse_rarity_str

class TestConsts:
    def test_comparison(self):
        rarities = list(Rarity)
        for x in range(len(rarities)):
            if x + 1 < len(rarities):
                assert rarities[x] < rarities[x + 1]

    def test_parse_rarity_str_success(self, rarity_str_symbols, rarity_str_texts):
        for s in rarity_str_symbols:
            rarity = parse_rarity_str(s)
            assert rarity.__class__ == Rarity
        
        for s in rarity_str_texts:
            rarity = parse_rarity_str(s)
            assert rarity.__class__ == Rarity

    def test_parse_rarity_str_failure(self):
        malformed = "◊☆◊"
        with pytest.raises(ValueError):
            parse_rarity_str(malformed)


@pytest.fixture
def rarity_str_symbols():
    return ["◊", "◊◊", "◊◊◊", "◊◊◊◊", "☆", "☆☆", "☆☆☆", "♕"]

@pytest.fixture
def rarity_str_texts():
    return ["1diamond", "1diamond", "1diamond", "1diamond", "1star", "2star", "3star", "crown"]