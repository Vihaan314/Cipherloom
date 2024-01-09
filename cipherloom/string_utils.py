from .constants import ALPHABET_LOWER, ALPHABET_UPPER, PUNCTUATION

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

def splitByChunk(message, chunk_size: int) -> list[str]:
    """
    Splits message into sizses of chunk_size
    """
    message = filterAlphabetical(message)
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
"""
End of general string processing
"""
