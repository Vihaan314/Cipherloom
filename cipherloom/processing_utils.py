import math
import numpy as np

from .constants import ALPHABET_LOWER, ALPHABET_UPPER, PUNCTUATION
from .string_utils import getNextLetterIndex, getLastOccurance, filterAlphabetical, replaceChars

"""
Message processing
"""

def getPaddingLength(message, chunk_size: int, only_alpha = True) -> int:
    """
    Returns an integer specifyin the amount of padding in terms of letters a message needs in order to be split into chunks of chunk_size
    """
    modifiedMessage = filterAlphabetical(message) if only_alpha else message
    return -len(modifiedMessage) % chunk_size

def addDuplicates(message: str, filler_letter) -> str:
    """
    Breaks up duplicates with a filler letter to avoid digraphs with the same letter
    """
    i, digraphIndex = 0, 0
    duplicateCount = 0
    while i < len(message) - 1:
        if message[i].isalpha():
            if digraphIndex % 2 == 0 and getNextLetterIndex(message, i) != -1 and message[i].lower() == message[getNextLetterIndex(message, i)].lower():
                message = message[:i + 1] + filler_letter + message[i + 1:]
                i += 1  
                digraphIndex += 1
                duplicateCount += 1
            digraphIndex += 1
        i += 1
    return message

def padMessage(message, chunk_size: int, filler_letter = "X", only_alpha=True, ignore_punc = True) -> str:
    """
    Pads a given message to be a multiple of a specified chunk size. Optionally filters out non-alphabetical characters and handles punctuation.

    :param chunk_size: The size of each chunk after padding.
    :param filler_letter: The letter used for padding. Defaults to "X".
    :param only_alpha: Flag to consider only alphabetical characters. Defaults to True.
    :param ignore_punc: Flag to ignore punctuation when padding. Defaults to True.
    :return: The padded message.
    """
    modifiedMessage = filterAlphabetical(message) if only_alpha else message
    paddingLength = getPaddingLength(modifiedMessage, chunk_size, only_alpha=only_alpha)
    insertPosition = getLastOccurance(message, filterAlphabetical(message)[-1])+1 if not ignore_punc else len(message)
    return message[:insertPosition] + (filler_letter * paddingLength) + message[insertPosition:]

def fillLetters(message: str, filler_letter: str, chunk_size = 2, pad_duplicates = False, filter_result = False, only_alpha = True, ignore_punc = True) -> str:
    """
    Processes a message for classical ciphers by adding fillers and handling duplicates. It can also handle punctuation and split messages into chunks.

    :param filler_letter: The letter used for padding in case of duplicates or for filling.
    :param chunk_size: The chunk size for splitting the message. Defaults to 2.
    :param pad_duplicates: Flag to pad consecutive equal letters. Defaults to False.
    :param filter_result: Flag to filter the message to include or exclude non-alphabetical characters. Defaults to False.
    :param ignore_punc: Flag to decide if padding should ignore punctuation. Defaults to True.
    :return: The modified message ready for encryption or decryption.
    """
    modifiedMessage = (filterAlphabetical if filter_result else lambda x: x)(addDuplicates(message, filler_letter) if pad_duplicates else message)
    return padMessage(modifiedMessage, chunk_size, filler_letter = filler_letter, only_alpha = only_alpha, ignore_punc = ignore_punc)

def applyPunctuation(originalMessage: str, modifiedMessage: str) -> str:
    """
    Adds spacing from original message to modified message
    """
    for i in range(0, len(originalMessage)):
        if not originalMessage[i].isalpha():
            if (i < len(modifiedMessage) and modifiedMessage[i] != originalMessage[i]) or (i <= len(modifiedMessage)):
                modifiedMessage = modifiedMessage[0:i] + originalMessage[i] + modifiedMessage[i:]
                
    return modifiedMessage

def applyCasing(originalMessage: str, modifiedMessage: str, i: int, remove_filler) -> str:
    """
    Applies casing from original message to modified message at specified index
    """
    return (modifiedMessage[i].lower() if originalMessage[i].islower() else modifiedMessage[i].upper() if originalMessage[i].isupper() else originalMessage[i])

def removeFiller(s):
    """
    Detects if there are filler letters and removes them in decryption process
    """
    endIndex = len(s) - len(s.rstrip(s[-1])) if s and s[-1].isupper() else 0
    s = s[:-endIndex] if endIndex > 0 and len(set(s[-endIndex:])) == 1 else s

    normalizedMessage = ""
    for i in range(len(s)):
        if s[i].isupper():
            if (i > 0 and i < len(s) - 1 and s[i-1].isalpha() and s[i-1].islower() and s[i+1].isalpha() and s[i+1].islower()) \
                    or (i == len(s) - 1 and s[i-1].isalpha() and s[i-1].islower()) \
                    or (i < len(s) - 1 and s[i+1] in PUNCTUATION and s[i-1].isalpha() and s[i-1].islower()):
                continue
        normalizedMessage += s[i]
    return normalizedMessage

def formatMessage(originalMessage, modifiedMessage, filledLetters = False, pad_duplicates = False, filler_letter = "X", ignore_punc = False, remove_filler = False) -> str:
    """
    Formats an encrypted or decrypted message by applying case sensitivity and punctuation from the original message, taking into account padding as well.

    :param originalMessage: The original message with capitalization and spacing.
    :param modifiedMessage: The encrypted or decrypted message to format.
    :param filledLetters: Flag indicating if the message has been formatted with padding. Defaults to False.
    :param pad_duplicates: Flag indicating if duplicates have been removed in padding. Defaults to False.
    :param neutralize_case: Flag indicating whether to attempt to normalize the casing of the message (e.g. duplicates removed in padding resulting in random capitalization). Defaults to False.
    :return: The formatted message.
    """
    originalMessage = replaceChars(originalMessage, ["j", "J"], ["i", "I"])
    originalMessage = fillLetters(originalMessage, filler_letter, pad_duplicates = pad_duplicates, ignore_punc = ignore_punc) if filledLetters else originalMessage
    modifiedMessage = applyPunctuation(originalMessage, modifiedMessage)
    removeFillerFunc = removeFiller if remove_filler else lambda x: x
    return removeFillerFunc(("".join([applyCasing(originalMessage, modifiedMessage, i, remove_filler) if i < len(originalMessage) else modifiedMessage[i] if not remove_filler else "" \
                                                                                                        for i in range(0, len(originalMessage))]))) 
"""
End of message / key processing
"""

"""
Key processing
"""

def processRepeatedKey(message, key: str):
    """
    Multiples given key to string length
    """
    key = key.upper()
    mL = len(filterAlphabetical(message))    
    key *= (math.ceil(mL / len(key)))
    return key

def generateKeyMatrix(key: str) -> np.ndarray:
    """
    Generates a 5x5 polybius square with a given key
    """
    key = "".join(dict.fromkeys(key.lower().replace("j", "i")))
    remainingLetters = "".join(filter(lambda x: x not in key, ALPHABET_LOWER.replace("j", "")))
    square = np.array([(i) for i in (key + remainingLetters)]).reshape(5, 5)
    return square

"""
End of key processing
"""
