import warnings

from .constants import ALPHABET_UPPER, ALPHABET_LOWER_REVERSE
from .utils.base_cipher import BaseCipher
from .utils.processing_utils import formatMessage
from .utils.string_utils import filterAlphabetical, translateTextFromTable
from .utils import general_utils, math_utils

# CAESAR CIPHER
class CaesarCipher(BaseCipher):
    def encrypt(self, message, key, decrypt=1):
        encrypted = general_utils.encodeAlphabeticalFunction(
            message, lambda x: (x + decrypt * key))
        return formatMessage(message, "".join(encrypted))

    def decrypt(self, message, key):
        return self.encrypt(message, key, decrypt=-1)


# ROT13 CIPHER
class ROT13Cipher(CaesarCipher):
    def encrypt(self, message):
        return CaesarCipher().encrypt(message, 13)

    def decrypt(self, message):
        return CaesarCipher().decrypt(message, 13)


# MONOALPHABETIC CIPHER
class MonoalphabeticCipher(BaseCipher):
    def encrypt(self, message, key, decrypt=1):
        processedMessage = filterAlphabetical(message).upper()
        key = key.upper()
        alphabet1, alphabet2 = (ALPHABET_UPPER, key)[::decrypt]
        encrypted = translateTextFromTable(processedMessage, general_utils.generateTranslationTable(alphabet1, alphabet2))
        return formatMessage(message, encrypted)

    def decrypt(self, message, key):
        return self.encrypt(message, key, decrypt=-1)


# ATBASH CIPHER
class AtbashCipher(BaseCipher):
    def encrypt(self, message):
        return MonoalphabeticCipher().encrypt(message, ALPHABET_LOWER_REVERSE)

    def decrypt(self, message):
        return self.encrypt(message)
    

# AFFINE CIPHER
class AffineCipher(BaseCipher):
    def encrypt(self, message, a, b, decrypt=1):
        gcd, x, y = math_utils.extendedEuclidean(a, 26)
        if gcd != 1:
            warnings.warn("Modular inverse does not exist!")
            return None
        aInv = x % 26
        operation = lambda i: a * i + b if decrypt == 1 else aInv * (i - b)
        encrypted = general_utils.encodeAlphabeticalFunction(message, operation)
        return formatMessage(message, "".join(encrypted))

    def decrypt(self, message, a, b):
        return self.encrypt(message, a, b, decrypt=-1)
