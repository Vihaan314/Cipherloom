import numpy as np
import math
from collections.abc import Callable

from Constants import *

"""
General string processing
"""

def getNextLetterIndex(string: str, index: str) -> int:
    """
    Returns the index of the next letter starting from an index in a string
    """
    while index < len(string) - 1:
        index += 1
        if string[index].isalpha():
            return index
    return -1

def replaceChars(string: str, chars: list[str], subs: list[str]) -> str:
    """
    Substitutes multiple characters in string
    """
    for i in range(0, len(chars)):
        string = string.replace(chars[i], subs[i])
    return string

def getLastOccurance(string: str, target: str) -> int:
    """
    Returns the index of the last occurance of a target character in a string
    """
    return len(string) - 1 - string[::-1].index(target)

def filterAlphabetical(string: str, alpha = ALPHABET_LOWER+ALPHABET_UPPER) -> str:
    """
    Removes all non-alphabetical characters from string
    """
    return "".join([char for char in string if char in alpha])

def filterNonAlpha(string: str, nonAlpha = PUNCTUATION) -> str:
    """
    Removes all alphabetical characters from string
    """
    return "".join([char for char in string if char in nonAlpha])

def splitByPunc(string: str) -> list[str]:
    """
    Splits string by punctuation
    """
    string = replaceChars(string, list(PUNCTUATION[1:]), [" "]*len(PUNCTUATION[1:]))
    return string.split()
    
def translateTextFromTable(message, translationTable: dict) -> str:
    """
    Given a dictionary mapping of ASCII values, will apply the keys to the message
    """
    return "".join(chr(translationTable.get(ord(char), ord(char))) for char in message)

"""
End of general string processing
"""


"""
Message / key processing
"""

def splitMessage(message, chunk_size: int) -> list[str]:
    """
    Splits message into sizses of chunk_size
    """
    message = filterAlphabetical(message)
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

def addDuplicates(message: str, fillerLetter) -> str:
    """
    Breaks up duplicates with a filler letter to avoid digraphs with the same letter
    """
    i, digraphIndex = 0, 0
    duplicateCount = 0
    while i < len(message) - 1:
        if message[i].isalpha():
            if digraphIndex % 2 == 0 and getNextLetterIndex(message, i) != -1 and message[i].lower() == message[getNextLetterIndex(message, i)].lower():
                message = message[:i + 1] + fillerLetter + message[i + 1:]
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
    print("MM", modifiedMessage)
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
    endIndex = len(s)
    while endIndex > 0 and s[endIndex - 1].isupper():
        endIndex -= 1
    if endIndex < len(s) and len(set(s[endIndex:])) == 1:
        s = s[:endIndex]

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
    print("OM", originalMessage)
    originalMessage = fillLetters(replaceChars(originalMessage, ["j", "J"], ["i", "I"]), filler_letter=filler_letter, pad_duplicates = pad_duplicates) \
                      if filledLetters else originalMessage
    modifiedMessage = applyPunctuation(originalMessage, modifiedMessage)
    print(originalMessage, modifiedMessage)
    return (removeFiller if remove_filler else lambda x: x)("".join([applyCasing(originalMessage, modifiedMessage, i, remove_filler) \
                                                                           if i < len(originalMessage) else modifiedMessage[i] if not remove_filler else "" \
                                                        for i in range(0, len(originalMessage))]),) \
##                                                            originalMessage = originalMessage if (filledLetters == False and remove_filler == True) else "")

def processRepeatedKey(message, key: str):
    """
    Multiples given key to string length
    """
    key = key.upper()
    mL = len(filterAlphabetical(message))    
    key *= (math.ceil(mL / len(key)))
    return key

"""
End of message / key processing
"""


"""
Misc
"""

def getPaddingLength(message, chunk_size: int, only_alpha = True) -> int:
    """
    Returns an integer specifyin the amount of padding in terms of letters a message needs in order to be split into chunks of chunk_size
    """
    modifiedMessage = filterAlphabetical(message) if only_alpha else message
    return -len(modifiedMessage) % chunk_size

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

def generateSquare(key: str) -> np.ndarray:
    """
    Generates a 5x5 polybius square with a given key
    """
    key = "".join(dict.fromkeys(key.lower().replace("j", "i")))
    remainingLetters = "".join(filter(lambda x: x not in key, ALPHABET_LOWER.replace("j", "")))
    square = np.array([(i) for i in (key + remainingLetters)]).reshape(5, 5)
    return square

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
    
def rearrangeRow(arr: np.ndarray, row: int, key: list[int]) -> np.ndarray:
    """
    Rearranges row of numpy array given order as list of integers
    """
    return [arr[row, i] for i in key]

def rearrangeColumn(arr: np.ndarray, column: int, key: list[int]) -> np.ndarray:
    """
    Rearranges column of numpy array given order as list of integers
    """
    return [arr[i, column] for i in key]

def toSquareMatrix(arr: list[list[int]], oneDim = False) -> np.ndarray:
    """
    Converts default list to numpy square array
    """
    length = int(math.sqrt(len(arr))) if oneDim else len(arr)
    return np.array(arr).reshape(length, length)
    
"""
End of misc
"""
