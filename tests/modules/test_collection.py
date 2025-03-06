import pytest

from consts import Rarity
from modules.card import Card
from modules.collection import Collection

class TestCollection:
    def test_add_new_card(self, kuriboh):
        c = Collection()
        c.add(kuriboh)
        assert c.collection[kuriboh] == 1

    def test_add_existing_card(self, kuriboh):
        c = Collection()
        c.add(kuriboh)
        c.add(kuriboh)
        assert c.collection[kuriboh] == 2

    def test_iadd(self, kuriboh, kuriboh_ex_common, kuriboh_ex_crown):
        c1 = Collection()
        c1.collection = {
            kuriboh: 2,
            kuriboh_ex_common: 1
        }

        c2 = Collection()
        c2.collection = {
            kuriboh_ex_common: 1,
            kuriboh_ex_crown: 1
        }

        c1 += c2

        expected = {
            kuriboh: 2,
            kuriboh_ex_common: 2,
            kuriboh_ex_crown: 1
        }

        assert c1.collection == expected

    def test_items(self, kuriboh, kuriboh_ex_common, kuriboh_ex_crown):
        c1 = Collection()
        c1.collection = {
            kuriboh_ex_crown: 1,
            kuriboh: 35,
            kuriboh_ex_common: 3
        }

        actual_items = c1.items()
        expected_items = [(kuriboh, 35), (kuriboh_ex_common, 3), (kuriboh_ex_crown, 1)]

        assert actual_items == expected_items


@pytest.fixture
def kuriboh():
    return Card("Kuriboh", Rarity.DIAMOND_1, "Y1006")

@pytest.fixture
def kuriboh_ex_common():
    return Card("Kuriboh ex", Rarity.DIAMOND_4, "Y1069")

@pytest.fixture
def kuriboh_ex_crown():
    return Card("Kuriboh ex", Rarity.CROWN, "Y1169")
