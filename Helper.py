import numpy as np
import math
from collections.abc import Callable

from Constants import *


"""
String processing
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

def getLastOccurance(string: str, target: str):
    """
    Returns the index of the last occurance of a target character in a string
    """
    return len(string) - 1 - string[::-1].index(target)

def filterAlphabetical(message: str) -> str:
    """
    Removes all non-alphabetical characters from string
    """
    return "".join([char for char in message if char.isalpha()])

def splitMessage(message, chunk_size: int) -> list[str]:
    """
    Splits message into sizses of chunk_size
    """
    message = filterAlphabetical(message)
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

##def fillLetters(message: str, fillerLetter: str, pad = True) -> str:
##    """
##    Set up message for the playfair cipher
##    """
##    i, digraphIndex = 0, 0
##    while i < len(message) - 1:
##        if message[i] != " ":
##            if digraphIndex % 2 == 0 and message[i] == message[i + 1]:
##                message = message[:i + 1] + "x" + message[i + 1:]
##                i += 1
##                digraphIndex += 1
##            digraphIndex += 1
##        i += 1
##    digraphIndex += 1
##    return message + ((("x" if message[-1] != "x" else fillerLetter) if digraphIndex % 2 else "") if pad else "")

def fillLetters(message: str, fillerLetter: str):
    i, digraphIndex = 0, 0
    fillerIndices = []
    duplicateCount = 0
    while i < len(message) - 1:
        if message[i].isalpha():
            if digraphIndex % 2 == 0 and getNextLetterIndex(message, i) != -1 and message[i].lower() == message[getNextLetterIndex(message, i)].lower():
                message = message[:i + 1] + fillerLetter + message[i + 1:]
                fillerIndices.append(i + 1)
                i += 1  
                digraphIndex += 1
                duplicateCount += 1
            digraphIndex += 1
        i += 1

##        if message[i].isalpha():
##            if digraphIndex % 2 == 0 and message[i] == message[i + 1]:
##                message = message[:i + 1] + fillerLetter + message[i + 1:]
##                fillerIndices.append(i + 1)
##                i += 1  
##                digraphIndex += 1
##                duplicateCount += 1
##            digraphIndex += 1
##        i += 1
    digraphIndex+=1
    puncCount = len(list(filter(lambda x: not x.isalpha(), message)))
    if len(filterAlphabetical(message)) % 2:
        insertPos = getLastOccurance(message, filterAlphabetical(message)[-1])+1
##        insertPos = message[:].index(filterAlphabetical(message)[-1])+1
        fillerIndices.append(insertPos)
        message = message[0:insertPos] + "x" + message[insertPos:]
        
    return message, fillerIndices

    
def applyPunctuation(originalMessage: str, modifiedMessage: str) -> str:
    """
    Adds spacing from original message to modified message
    """
    for i in range(0, len(originalMessage)):
        if not originalMessage[i].isalpha():
            if (i < len(modifiedMessage) and modifiedMessage[i] != originalMessage[i]) or (i <= len(modifiedMessage)):
                modifiedMessage = modifiedMessage[0:i] + originalMessage[i] + modifiedMessage[i:]
                
    return modifiedMessage    

def addFillerIndices(originalMessage, fillerIndices, fillerLetter = "x"):
    print(originalMessage)
    addedFillers = list(originalMessage)
    offset = 0
    for index in sorted(fillerIndices):
        actualIndex = index + offset
        if actualIndex <= len(addedFillers):
            addedFillers.insert(actualIndex, fillerLetter)
            offset += 1
    return "".join(addedFillers)

##def formatMessage(originalMessage, modifiedMessage, pad_length = 0) -> str:
##    """
##    originalMessage: The original message with capitalized and spacing
##    modifiedMessage: Encrypted / decrypted message to be formatted 
##    """
##    modifiedMessage = applyPunctuation(originalMessage, modifiedMessage)
##    return "".join([modifiedMessage[i].lower() if originalMessage[i].islower() else modifiedMessage[i].upper() if originalMessage[i].isupper() else originalMessage[i]
##                    for i in range(0, len(originalMessage))]) + ("" if not pad_length else (modifiedMessage[-1] if pad_length == 1 else (modifiedMessage[-(pad_length):-1]+modifiedMessage[-1])))
def formatMessage(originalMessage, modifiedMessage, fillerIndices = []) -> str:
    """
    originalMessage: The original message with capitalized and spacing
    modifiedMessage: Encrypted / decrypted message to be formatted 
    """
    originalMessage, fillerIndices = fillLetters(replaceChars(originalMessage, ["j", "J"], ["i", "I"]), "x")
    print("OM", originalMessage)
    modifiedMessage = applyPunctuation(originalMessage, modifiedMessage)
    return "".join([modifiedMessage[i].lower() if originalMessage[i].islower() else modifiedMessage[i].upper() if originalMessage[i].isupper() else originalMessage[i]
                    for i in range(0, len(originalMessage))])

def translateTextFromTable(message, translationTable: dict) -> str:
    """
    Given a dictionary mapping of ASCII values, will apply the keys to the message
    """
    return "".join(chr(translationTable.get(ord(char), ord(char))) for char in message)

def processRepeatedKey(message, key: str):
    """
    Multiples given key to string length
    """
    key = key.upper()
    mL = len(filterAlphabetical(message))    
    key *= (math.ceil(mL / len(key)))
    return key

def padMessage(message, chunk_size: int, filler_letter = "X", filter_alpha=True) -> str:
    """
    Given a message that is to be split into chunks of size chunk_size, filler_letters are added to pad the message to be a multiple of the chunk_size
    """
    modifiedMessage = filterAlphabetical(message) if filter_alpha else message
    if len(modifiedMessage) % chunk_size != 0:
        paddingLength = getPaddingLength(message, chunk_size, filter_alpha = filter_alpha)
        modifiedMessage += (filler_letter * paddingLength)
        return formatMessage(message, modifiedMessage, pad_length = paddingLength) if filter_alpha else modifiedMessage
    return message

"""
End of string processing
"""


"""
Misc
"""

def getPaddingLength(message, chunk_size: int, filter_alpha = True) -> int:
    """
    Returns an integer specifyin the amount of padding in terms of letters a message needs in order to be split into chunks of chunk_size
    """
    modifiedMessage = filterAlphabetical(message) if filter_alpha else message
    return (chunk_size - len(modifiedMessage) % chunk_size) % chunk_size

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

def toSquareMatrix(arr: list[list[int]], oneDim = False):
    """
    Converts default list to numpy square array
    """
    length = int(math.sqrt(len(arr))) if oneDim else len(arr)
    return np.array(arr).reshape(length, length)
    
"""
End of misc
"""
