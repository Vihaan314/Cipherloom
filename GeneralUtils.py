import numpy as np
from collections.abc import Callable

from Constants import *
from StringUtils import filterAlphabetical

"""
General functions
"""

def generateTranslationTable(alphabet1: str, alphabet2: str) -> dict:
    """
    alphabet1: First string consisting of unique characters
    alphabet2: Second string conssiting of unique characters
    Returns a dictionary mapping each ASCII value from alphabet1 -> alphabet2
    """
    if len(alphabet1) != len(alphabet2):
        raise ValueError("Alphabets must be of the same length")

    translationTable = {ord(a): ord(b) for a, b in zip(alphabet1, alphabet2)}
    return translationTable

def encodeToAlphabetIndices(message: str) -> list[int]:
    """
    Given a message string, it will convert each character to its index in the English alphabet and return a string of those integers
    """
    modifiedMessage = filterAlphabetical(message).lower()
    return [ALPHABET_LOWER.index(char) for char in modifiedMessage if char.isalpha()]

def decodeAlphabetIndices(indices: list[int]) -> list[str]:
    """
    Given a list of integers, they are converted to a list of strings which are the corresponding letters of the index of the integers
    """
    return [ALPHABET_LOWER[i] for i in indices]

def encodeAlphabeticalFunction(message: str, operation: Callable[[int], int]) -> list[str]:
    """
    Applies function to the letters' position in the alphabet of the message (e.g. Caesar cipher -> x+key)
    """
    return decodeAlphabetIndices([(operation(i))%26 for i in encodeToAlphabetIndices(message)])
    
"""
End of general functions
"""
