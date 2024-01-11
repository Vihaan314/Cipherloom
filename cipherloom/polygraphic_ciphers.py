import numpy as np
import math
import warnings

from .constants import ALPHABET_UPPER, ALPHABET_LOWER
from .utils.base_cipher import BaseCipher
from .utils.processing_utils import formatMessage, fillLetters, generateKeyMatrix
from .utils.string_utils import filterAlphabetical, splitByChunk
from .utils import general_utils, math_utils, processing_utils

# HILL CIPHER (K * P)
class HillCipher(BaseCipher):
    def encrypt(self, message, key, filler_letter="X", remove_filler=False, decrypt=1): 
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

    def decrypt(self, message, key, filler_letter="X", remove_filler=True):
        return self.encrypt(message, key, filler_letter=filler_letter, remove_filler=remove_filler, decrypt=-1)


# PLAYFAIR CIPHER
class PlayfairCipher(BaseCipher):
    def encrypt(self, message, key, filler_letter="X", remove_filler=False, decrypt=1):
        processedMessage = fillLetters(message.lower().replace("j", "i"), filler_letter.lower(), pad_duplicates=True, ignore_punc=False)
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
        return formatMessage(message, decrypted, filledLetters=True, pad_duplicates=True, filler_letter=filler_letter, ignore_punc=False, remove_filler=remove_filler)

    def decrypt(self, message, key, remove_filler=True):
        return self.encrypt(message, key, remove_filler=remove_filler, decrypt=-1)

