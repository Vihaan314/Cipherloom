import numpy as np
import math

from .constants import ALPHABET_UPPER, ALPHABET_LOWER
from .utils.base_cipher import BaseCipher
from .utils.processing_utils import formatMessage, fillLetters
from .utils.string_utils import filterAlphabetical, splitByChunk
from .utils import general_utils, math_utils, processing_utils
from .substitution_ciphers import CaesarCipher

# VIGENERE CIPHER
class VigenereCipher(BaseCipher):
    def encrypt(self, message, key, decrypt=1):
        processedMessage = filterAlphabetical(message).upper()
        keyFormatted = formatMessage(processedMessage, processing_utils.processRepeatedKey(message, key))[:len(message)]
        encrypted = [chr((ALPHABET_UPPER.index(processedMessage[i]) + decrypt * ALPHABET_UPPER.index(keyFormatted[i])) % 26 + 65) 
                     for i in range(len(processedMessage))]
        return formatMessage(message, "".join(encrypted))

    def decrypt(self, message, key):
        return self.encrypt(message, key, decrypt=-1)


# TRITHEMIUS CIPHER
class TrithemiusCipher(BaseCipher):
    def encrypt(self, message, ascending=True, initial_shift=0):
        cipherFunction = CaesarCipher().encrypt if ascending else CaesarCipher().decrypt
        encrypted = "".join([cipherFunction(filterAlphabetical(message)[i], i + initial_shift) 
                             for i in range(len(filterAlphabetical(message)))])
        return formatMessage(message, encrypted)

    def decrypt(self, message, ascending=True, initial_shift=0):
        return self.encrypt(message, not ascending, initial_shift)
