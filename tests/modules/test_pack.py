import pytest
import numpy as np
from unittest.mock import patch

from consts import Rarity
from modules.pack import Pack
from modules.card import Card

class TestPack:
    def test_init(self, fake_cards, fake_pull_rates):
        actual = Pack("Omnimon", available_cards=fake_cards, pull_rates=fake_pull_rates)

        expected_name = "Omnimon"
        expected_available = np.array(fake_cards)
        expected_pull_rates = fake_pull_rates
        expected_rare_pack_rate = 0.00050
        expected_probs = np.array([
            [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.2000, 0.4000, 0.2000, 0.1000, 0.0600, 0.0300, 0.0075, 0.0025],
            [0.0000, 0.4000, 0.3000, 0.2000, 0.0600, 0.0300, 0.0075, 0.0025],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.4000, 0.4000, 0.1500, 0.0500]
        ])
        assert actual.unopened == True
        assert actual.is_rare is None
        assert actual.cards == []

        assert actual.name == expected_name
        np.testing.assert_array_equal(actual.available, expected_available)
        assert actual.pull_rates == expected_pull_rates
        assert actual.rare_pack_rate == expected_rare_pack_rate
        np.testing.assert_allclose(actual.probs, expected_probs, rtol=1e-10, atol=1e-10)

    @patch('numpy.random.rand')
    def test_open_regular(self, mock_rand, set_seed, fake_cards, fake_pull_rates):
        mock_rand.return_value = 0.1 # rare_pack_check will force regular pack

        p = Pack("Omnimon", available_cards=fake_cards, pull_rates=fake_pull_rates)
        actual = p.open(instantaneous=True)

        expected = [
            Card("Agumon", Rarity.DIAMOND_1, "X1001"),
            Card("Agumon", Rarity.DIAMOND_1, "X1001"),
            Card("Agumon", Rarity.DIAMOND_1, "X1001"),
            Card("Greymon", Rarity.DIAMOND_2, "X1002"),
            Card("Greymon", Rarity.DIAMOND_2, "X1002")
        ]

        assert p.is_rare == False
        assert p.unopened == False
        assert p.cards == expected
        assert actual == expected

    @patch('numpy.random.rand')
    def test_open_rare(self, mock_rand, set_seed, fake_cards, fake_pull_rates):
        mock_rand.return_value = 1e-10 # rare_pack_check will force rare pack

        p = Pack("Omnimon", available_cards=fake_cards, pull_rates=fake_pull_rates)
        actual = p.open(instantaneous=True)

        expected = [
            Card("Omnimon ex", Rarity.STAR_2, "X1006"),
            Card("Omnimon ex", Rarity.STAR_2, "X1006"),
            Card("Agumon", Rarity.STAR_1, "X1005"),
            Card("Agumon", Rarity.STAR_1, "X1005"),
            Card("Agumon", Rarity.STAR_1, "X1005")
        ]

        assert p.is_rare == True
        assert p.unopened == False
        assert p.cards == expected
        assert actual == expected

@pytest.fixture
def set_seed():
    np.random.seed(1)

@pytest.fixture
def fake_cards():
    return [
        Card("Agumon", Rarity.DIAMOND_1, "X1001"),
        Card("Greymon", Rarity.DIAMOND_2, "X1002"),
        Card("MetalGreymon", Rarity.DIAMOND_3, "X1003"),
        Card("Omnimon", Rarity.DIAMOND_4, "X1004"),
        Card("Agumon", Rarity.STAR_1, "X1005"),
        Card("Omnimon ex", Rarity.STAR_2, "X1006"),
        Card("Omnimon ex", Rarity.STAR_3, "X1007"),
        Card("Omnimon ex", Rarity.CROWN, "X1008")
    ]

@pytest.fixture
def fake_pull_rates():
    return [
        {
            Rarity.DIAMOND_1: 1.0000,
            Rarity.DIAMOND_2: 0,
            Rarity.DIAMOND_3: 0,
            Rarity.DIAMOND_4: 0,
            Rarity.STAR_1: 0,
            Rarity.STAR_2: 0,
            Rarity.STAR_3: 0,
            Rarity.CROWN: 0
        },
        {
            Rarity.DIAMOND_1: 1.0000,
            Rarity.DIAMOND_2: 0,
            Rarity.DIAMOND_3: 0,
            Rarity.DIAMOND_4: 0,
            Rarity.STAR_1: 0,
            Rarity.STAR_2: 0,
            Rarity.STAR_3: 0,
            Rarity.CROWN: 0
        },
        {
            Rarity.DIAMOND_1: 1.0000,
            Rarity.DIAMOND_2: 0,
            Rarity.DIAMOND_3: 0,
            Rarity.DIAMOND_4: 0,
            Rarity.STAR_1: 0,
            Rarity.STAR_2: 0,
            Rarity.STAR_3: 0,
            Rarity.CROWN: 0
        },
        {
            Rarity.DIAMOND_1: 0.2000,
            Rarity.DIAMOND_2: 0.4000,
            Rarity.DIAMOND_3: 0.2000,
            Rarity.DIAMOND_4: 0.1000,
            Rarity.STAR_1: 0.0600,
            Rarity.STAR_2: 0.0300,
            Rarity.STAR_3: 0.0075,
            Rarity.CROWN: 0.0025
        },
        {
            Rarity.DIAMOND_1: 0.0000,
            Rarity.DIAMOND_2: 0.4000,
            Rarity.DIAMOND_3: 0.3000,
            Rarity.DIAMOND_4: 0.2000,
            Rarity.STAR_1: 0.0600,
            Rarity.STAR_2: 0.0300,
            Rarity.STAR_3: 0.0075,
            Rarity.CROWN: 0.0025
        },
        {
            Rarity.DIAMOND_1: 0,
            Rarity.DIAMOND_2: 0,
            Rarity.DIAMOND_3: 0,
            Rarity.DIAMOND_4: 0,
            Rarity.STAR_1: 0.4000,
            Rarity.STAR_2: 0.4000,
            Rarity.STAR_3: 0.1500,
            Rarity.CROWN: 0.0500
        }
    ]