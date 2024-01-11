class BaseCipher:
    def encrypt(self, message):
        raise NotImplementedError

    def decrypt(self, message):
        raise NotImplementedError
