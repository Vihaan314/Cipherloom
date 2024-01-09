import math
import numpy as np
import warnings

from .constants import ALPHABET_UPPER, ALPHABET_LOWER
from .string_utils import filterAlphabetical, splitByChunk, translateTextFromTable
from .processing_utils import formatMessage, fillLetters
from . import processing_utils
from . import general_utils
from . import math_utils

"""
Cipher general class
"""

class BaseCipher:
    def __init__(self, key):
        self.key = key

    def set_key(self, new_key):
        self.key = new_key

    def encrypt(self, message):
        raise NotImplementedError

    def decrypt(self, message):
        raise NotImplementedError

"""
Cipher general class
"""

"""
IMPLEMENTATIONS
"""
#CAESER CIPHER
#ROT13 CIPHER
#TRITHEMIUS CIPHER
#ATBASH CIPHER
#MONOALPHABETIC CIPHER
#VIGENERE CIPHER
#TRANSPOSITION CIPHER
#AFFINE CIPHER
#HILL CIPHER
#PLAYFAIR CIPHER


#CAESER CIPHER ENCRYPTION
def caesarCipher(message, key: int, decrypt = 1):
    encrypted = general_utils.encodeAlphabeticalFunction(message, lambda x: (x+decrypt*key))
    return formatMessage(message, "".join(encrypted))

#CAESER CIPHER DECRYPTION
def decryptCaesar(message, key: int): 
    return caesarCipher(message, key, decrypt= -1)


#ROT13 ENCRYPTION
def rot13Cipher(message): 
    return caesarCipher(message, 13)

#ROT13 DECRYPTION
def decryptRot13(message):
    return decryptCaesar(message, 13)


#TRITHEMIUS CIPHER ENCRYPTION
def trithemiusCipher(message, ascending: bool, initial_shift: int = 0):
    cipherFunction = caesarCipher if ascending else decryptCaesar
    encrypted = "".join([cipherFunction(filterAlphabetical(message)[i], i+initial_shift) for i in range(0, len(filterAlphabetical(message)))])
    return formatMessage(message, encrypted)

#TRITHEMIUS CIPHER DECRYPTION
def decryptTrithemius(message, ascending: bool, initial_shift: int = 0):
    return trithemiusCipher(message, ascending=False, initial_shift=initial_shift) if ascending else trithemiusCipher(message, ascending=True, initial_shift=initial_shift)

    
#ATBASH CIPHER ENCRYPTION  
def atbashCipher(message): 
    return monoalphabeticCipher(message, ALPHABET_LOWER[::-1])

#ATBASH CIPHER DECRYPTION
def decryptAtbash(message): 
    return atbashCipher(message)


#MONOALPHABETIC CIPHER ENCRYPTION
def monoalphabeticCipher(message, key: str, decrypt=1): 
    processedMessage = filterAlphabetical(message).upper()
    key = key.upper()
    alphabet1, alphabet2 = (ALPHABET_UPPER, key)[::decrypt]
    encrypted = translateTextFromTable(processedMessage, general_utils.generateTranslationTable(alphabet1, alphabet2))
    return formatMessage(message, encrypted)

#MONOALPHABETIC CIPHER DECRYPTION
def decryptMonoalphabetic(message, key: str): 
    return monoalphabeticCipher(message, key, decrypt = -1)


#VIGENERE CIPHER ENCRYPTION
def vigenereCipher(message, key: str, decrypt = 1): 
    processedMessage = filterAlphabetical(message).upper()
    key = formatMessage(processedMessage, processing_utils.processRepeatedKey(message, key))[:len(message)]
    encrypted = [chr((ALPHABET_UPPER.index(processedMessage[i]) + decrypt*ALPHABET_UPPER.index(key[i])) % 26 + 65) for i in range(0, len(processedMessage))]
    return formatMessage(message, "".join(encrypted))

#VIGENERE CIPHER DECRYPTION
def decryptVigenere(message, key: str): 
    return vigenereCipher(message, key, decrypt = -1)


#TRANSPOSITION CIPHER ENCRYPTION
def columnarTranspositionCipher(message, key: str, decrypt = 1):
    transpose = np.transpose if decrypt == -1 else np.array
    order = sorted(range(0, len(key)), key=lambda x: key[x])
    order = [order.index(i) for i in range(len(key))] if decrypt == -1 else order
    processedMessage = fillLetters(message, "X", chunk_size = len(key), only_alpha=False) if decrypt == 1 else message
    messageMat = transpose(np.array(list(processedMessage)).reshape(*(len(processedMessage)//len(key), len(key))[::decrypt]))
    encrypted = []
    for i in range(0, (len(key) if decrypt == 1 else len(processedMessage)//len(key))):
        chunk = messageMat[:, order[i]] if decrypt == 1 else "".join(math_utils.rearrangeRow(messageMat, i, order))
        encrypted.append("".join(chunk))
    return "".join(encrypted)
    
#TRANSPOSITION CIPHER DECRYPTION
def decryptColumnarTransposition(message, key: str):
    return columnarTranspositionCipher(message, key, decrypt = -1)


#AFFINE CIPHER ENCRYPTION
def affineCipher(message, a: int, b: int, decrypt = 1):
    gcd, x, y = math_utils.extendedEuclidean(a, 26)
    if gcd != 1:
        return warnings.warn("Modular inverse does not exist!")
    else:
        aInv = x % 26
    operation = lambda i: a*i+b if decrypt == 1 else aInv*(i-b)
    encrypted = general_utils.encodeAlphabeticalFunction(message, operation)
    return formatMessage(message, "".join(encrypted))

#AFFINE CIPHER DECRYPTION
def decryptAffine(message, a: int, b: int):
    return affineCipher(message, a, b, decrypt = -1)


#HILL CIPHER ENCRYPTION (K * P)
def hillCipher(message, key: str, filler_letter = "X", remove_filler = False, decrypt = 1): 
    if not math.sqrt(len(key)).is_integer():
        return warnings.warn("Wrong key. Please enter a key of square length!")
    
    key = key.lower()
    keySize = int(math.sqrt(len(key)))
    padLength = processing_utils.getPaddingLength(message, keySize)
    processedMessage = fillLetters(message, filler_letter.lower(), chunk_size = keySize, filter_result = True)
    messCaps = formatMessage(message, processedMessage)

    messageChunks = splitByChunk(processedMessage, keySize)
    k = math_utils.toSquareMatrix(general_utils.encodeToAlphabetIndices(key), oneDim = True).tolist()
    inverseKey = math_utils.toSquareMatrix(math_utils.matrixInverseModN(k, 26))
    if not math_utils.isMatrixInvertibleModN(k, 26):
        return warnings.warn("Key is not invertible mod 26. Message cannot be decrypted!")
    encryptedChunks = []
    for chunk in messageChunks:
        m = np.array(general_utils.encodeToAlphabetIndices(chunk)).reshape(keySize, 1)
        encryptedChunk = ([0, k, inverseKey][decrypt] @ m) % 26
        encryptedChunks.append("".join(ALPHABET_LOWER[num[0]] for num in encryptedChunk))
        
    message = fillLetters(message, filler_letter, chunk_size = keySize)
    return formatMessage(message, "".join(encryptedChunks), filler_letter=filler_letter, ignore_punc = True, remove_filler = remove_filler)


#HILL CIPHER DECRYPTION (K^(-1) (mod 26) * P)
def decryptHill(message, key: str, remove_filler = True): 
    return hillCipher(message, key, decrypt = -1, remove_filler = remove_filler)


#PLAYFAIR CIPHER ENCRYPTION
def playfairCipher(message, key: str, filler_letter = "X", remove_filler = False, decrypt: int = 1):
    processedMessage = fillLetters(message.lower().replace("j", "i"), filler_letter.lower(), pad_duplicates = True, ignore_punc=False)
    messSplit = splitByChunk(processedMessage, 2)
    keyAlpha = processing_utils.generateKeyMatrix(key)
    decrypted = {}
    
    for i in range(0, 5):
        for j in range(0, len(messSplit)):
            if (np.where(keyAlpha == messSplit[j][0])[0]) == (np.where(keyAlpha == messSplit[j][1])[0]):
                el1Row = (int(np.where(keyAlpha == messSplit[j][0])[0]))
                el1Col = ((int(np.where(keyAlpha == messSplit[j][0])[1]) + decrypt)) % 5
                el2Row = (int(np.where(keyAlpha == messSplit[j][1])[0]))
                el2Col = ((int(np.where(keyAlpha == messSplit[j][1])[1]) + decrypt)) % 5
                decrypted[messSplit[j][0] + messSplit[j][1]] = [keyAlpha[el1Row][el1Col], keyAlpha[el2Row][el2Col]]
            elif (messSplit[j][0] in keyAlpha[ :,i]) and (messSplit[j][1] in keyAlpha[ :,i]):
                decrypted[messSplit[j][0] + messSplit[j][1]] = ([keyAlpha[ :,i][(np.where(keyAlpha[ :,i] == messSplit[j][0])[0][0] + decrypt) % 5],
                                                                 keyAlpha[ :,i][(np.where(keyAlpha[ :,i] == messSplit[j][1])[0][0] + decrypt) % 5]])
            
            elif ((messSplit[j][0] not in keyAlpha[ :,i]) and (messSplit[j][1] not in keyAlpha[ :,i])) and ((messSplit[j][0] not in keyAlpha[i, :]) and (messSplit[j][1] not in keyAlpha[i, :])):
                charWhereOne = np.where(keyAlpha == messSplit[j][0])
                charWhereTwo = np.where(keyAlpha == messSplit[j][1])
                el1 = charWhereOne[0].tolist() + charWhereOne[1].tolist()
                el2 = charWhereTwo[0].tolist() + charWhereTwo[1].tolist()
                
                if el1[1] > el2[1]:  
                    remainingMat = np.transpose(np.array(
                        [keyAlpha[i][j] for j in range(min([el1[1], el2[1]]), max([el1[1], el2[1]])+1) for i in range(min([el1[0], el2[0]]), max([el1[0], el2[0]])+1)]).reshape(
                                                                                                                                    abs(el2[1]-el1[1])+1, abs(el2[0]-el1[0])+1))
                    if remainingMat[0][0] in messSplit[j]:
                        lets = [(remainingMat[0][len(remainingMat[0])-1]), remainingMat[len(remainingMat)-1][0]][::-1]
                    elif remainingMat[0][len(remainingMat[0])-1] == messSplit[j][0]:
                        lets = [remainingMat[0][0], remainingMat[len(remainingMat)-1][len(remainingMat[0])-1]]
                    else:
                        lets = [remainingMat[0][0], remainingMat[len(remainingMat)-1][len(remainingMat[0])-1]][::-1]
                    decrypted[messSplit[j][0] + messSplit[j][1]] = lets
                    
                if el1[1] < el2[1]:                        
                    remainingMat = np.transpose(np.array(
                        [keyAlpha[i][j] for j in range(min([el2[1], el1[1]]), max(el2[1], el1[1])+1) for i in range(min([el2[0], el1[0]]), max(el2[0], el1[0])+1)]).reshape(
                                                                                                                                    abs(el2[1]-el1[1])+1, (abs(el2[0]-el1[0]) + 1)))
                    if remainingMat[0][0] in messSplit[j]:
                        lets = [remainingMat[len(remainingMat)-1][0], (remainingMat[0][len(remainingMat[0])-1])][::-1]
                    elif remainingMat[0][len(remainingMat[0])-1] in messSplit[j]:
                        lets = [remainingMat[0][0], remainingMat[len(remainingMat)-1][len(remainingMat[0])-1]][::-1]
                    else:
                        lets = [remainingMat[0][0], remainingMat[len(remainingMat)-1][len(remainingMat[0])-1]]
                    decrypted[messSplit[j][0] + messSplit[j][1]] = lets
                    
    decrypted = "".join(["".join(decrypted[i]) for i in messSplit])
    return formatMessage(message, decrypted, filledLetters = True, pad_duplicates = True, filler_letter=filler_letter, ignore_punc = False, remove_filler = remove_filler)
            
#PLAYFAIR CIPHER DECRYPTION
def decryptPlayfair(message, key: str, remove_filler = True):
    return playfairCipher(message, key, remove_filler = remove_filler, decrypt = -1)    


"""
IMPLEMENTATIONS
"""
