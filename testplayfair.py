def playfair(message, key):
    processedMessage, fillerIndices = fillLetters(message.lower().replace("j", "i"), "x")
    messSplit = splitMessage(processedMessage, 2)
    keyAlpha = generateSquare(key)
    decrypted = []
    
    for i in range(0, 5):
        for j in range(0, len(messSplit)):
            if np.where(keyAlpha == messSplit[j][0])[0] == np.where(keyAlpha == messSplit[j][1])[0]:
                
            
    decrypted = "".join(["".join(decrypted[i]) for i in messSplit])
    return decrypted.upper()
