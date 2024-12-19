import numpy as np

def normalize_probabilities(arr, axis=None):
    """
        Normalize values from arr so that they sum to 1 for use as a probability distribution

        arr: numpy array
        axis: axis along which the values should sum to 1
        @return numpy array where values along axis sum to 1
    """
    return arr / arr.sum(axis=axis, keepdims=True)
