import numpy as np

from .utils.base_cipher import BaseCipher
from .utils.math_utils import rearrangeRow
from .utils.processing_utils import fillLetters

class TranspositionCipher(BaseCipher):
    def encrypt(self, message, key, decrypt=1):
        transpose = np.transpose if decrypt == -1 else np.array
        order = sorted(range(len(key)), key=lambda x: key[x])
        order = [order.index(i) for i in range(len(key))] if decrypt == -1 else order
        processedMessage = fillLetters(message, "X", chunk_size=len(key), only_alpha=False) if decrypt == 1 else message
        messageMat = transpose(np.array(list(processedMessage)).reshape(*(len(processedMessage) // len(key), len(key))[::decrypt]))
        encrypted = []
        for i in range((len(key) if decrypt == 1 else len(processedMessage) // len(key))):
            chunk = messageMat[:, order[i]] if decrypt == 1 else "".join(rearrangeRow(messageMat, i, order))
            encrypted.append("".join(chunk))
        return "".join(encrypted)
    
    def decrypt(self, message, key):
        return self.encrypt(message, key, decrypt=-1)

