import pytest
import numpy as np

from utils.probability import normalize_probabilities

class TestProbability:
    def test_normalize_probabilities(self, arr):
        actual = normalize_probabilities(arr, axis=1)
        expected = np.array(
            [
                [0.5, 0.33333333, 0.166667],
                [0.71428, 0.14286, 0.14286],
                [0.076923, 0.769231, 0.153846]
            ]
        )

        np.testing.assert_allclose(actual, expected, rtol=1e-3, atol=1e-3)

@pytest.fixture
def arr():
    return np.array(
        [
            [3, 2, 1],
            [5, 1, 1],
            [1, 10, 2]
        ]
    )