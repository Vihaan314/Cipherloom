import unittest
from parameterized import parameterized

from Cipherloom import *
from Constants import *

class TestCipherMethods(unittest.TestCase):
    
    # CAESAR CIPHER TESTS
    @parameterized.expand([
        ("normal text", "Hello World", 3, "Khoor Zruog"),
        ("upper case", "HELLO WORLD", 3, "KHOOR ZRUOG"),
        ("wrap around", "xyz", 3, "abc"),
        ("negative key", "Hello World", -3, "Ebiil Tloia"),
        ("zero key", "Hello World", 0, "Hello World"),
    ])
    def test_caesarCipher_variousInputs(self, name, message, key, expected):
        encrypted = caesarCipher(message, key)
        self.assertEqual(encrypted, expected)


    # ROT13 CIPHER TESTS
    @parameterized.expand([
        ("standard", "Hello World", "Uryyb Jbeyq"),
        ("non-alphabetic", "Hello, World!", "Uryyb, Jbeyq!"),
    ])
    def test_rot13Cipher(self, name, message, expected):
        encrypted = rot13Cipher(message)
        self.assertEqual(encrypted, expected)
        decrypted = decryptRot13(encrypted)
        self.assertEqual(decrypted, message)


    # TRITHEMIUS CIPHER TESTS
    @parameterized.expand([
        ("ascending", "Hello, World!", True, 0, "Hfnos, Buytm!"),  
        ("descending", "Hello, World!", False, 0, "Hdjik, Rikdu!"),  
        ("ascending shift", "Hello, World!", True, 12, "Trzae, Ngkfy!"),
        ("descending shift", "Hello, World!", False, 32, "Bxdce, Lcexo!"), 
    ])
    def test_trithemiusCipher(self, name, message, ascending, initial_shift, expected):
        encrypted = trithemiusCipher(message, ascending, initial_shift=initial_shift)
        self.assertEqual(encrypted, expected)
        decrypted = decryptTrithemius(encrypted, ascending, initial_shift=initial_shift)
        self.assertEqual(decrypted, message)


    # ATBASH CIPHER TESTS
    @parameterized.expand([
        ("standard", "Hello World", "Svool Dliow"),
        ("non-alphabetic", "Hello, World!", "Svool, Dliow!"),
    ])
    def test_atbash(self, name, message, expected):
        encrypted = atbashCipher(message)
        self.assertEqual(encrypted, expected)
        decrypted = decryptAtbash(encrypted)
        self.assertEqual(decrypted, message)


    # MONOALPHABETIC CIPHER TESTS
    @parameterized.expand([
        ("normal text", "Hello World", ALPHABET_LOWER_REVERSE, "Svool Dliow"),
        ("non-alphabetic", "Hello, World!", "QWERTYUIOPASDFGHJKLZXCVBNM", "Itssg, Vgksr!"),
        ("key as rotation", "Hello World", "BCDEFGHIJKLMNOPQRSTUVWXYZA", "Ifmmp Xpsme"),
    ])
    def test_monoalphabetic(self, name, message, alphabet, expected):
        encrypted = monoalphabeticCipher(message, alphabet)
        self.assertEqual(encrypted, expected)
        decrypted = decryptMonoalphabetic(encrypted, alphabet)
        self.assertEqual(decrypted, message)


    #VIGENERE CIPHER TESTS
    @parameterized.expand([
        ("standard case", "Hello World", "KEY", "Rijvs Uyvjn"),
        ("non-alphabetic", "Hello, World! Welcome to the cipher.", "Cheese", "Jlppg, Aqyph! Oinjsqw xq ali umroiv."),
        ("sample sentence", "Hello, man! Can you get the lightz?", "lights", "Smrsh, elv! Ihg qzc mlm lsm rpzzeh?"),
    ])
    def test_vigenere(self, name, message, key, expected):
        encrypted = vigenereCipher(message, key)
        self.assertEqual(encrypted, expected)
        decrypted = decryptVigenere(encrypted, key)
        self.assertEqual(decrypted, message)


    #TRANSPOSITION CIPHER
    @parameterized.expand([
        ("standard case", "Hello World", "key", "eoodHlWll rX"),
        ("repeated key", "Hello welcome to the program", "cheese", "Hwehgllt alcopm mtoXee eroo rX"),
        ("non-alphabetic", "Hello, World! 123", "hello", "e d3H,l2lW!Xlo Xor1X"),
    ])
    def test_columnarTranspositionCipher(self, name, input_text, key, expected):
        encrypted = columnarTranspositionCipher(input_text, key)
        self.assertEqual(encrypted, expected)
        decrypted = decryptColumnarTransposition(encrypted, key)
        self.assertIn(input_text, decrypted)

        
    #AFFINE CIPHER
    @parameterized.expand([
        ("standard case", "Hello World", 5, 8, "Rclla Oaplx"),
        ("non-alphabetic", "Hello, World! 123", 17, 20, "Jkzzy, Eyxzt! 123"),
        ("sample sentence", "Hey man, can you get the lights? Thanks.", 11, 18, "Rkw usf, osf wqe gkt trk jcgrti? Trsfyi."),
        ("invalid a", "Hello World", 13, 8, None),
    ])
    def test_affineCipher(self, name, input_text, a, b, expected):
        if expected is not None:
            encrypted = affineCipher(input_text, a, b)
            self.assertEqual(encrypted, expected)
            decrypted = decryptAffine(encrypted, a, b)
            self.assertEqual(decrypted, input_text)
        else:
            with self.assertWarns(Warning):
                affineCipher(input_text, a, b)
                
        
    #HILL CIPHER
    @parameterized.expand([
        ("standard case", "Hello World", "CDFH", "X", "Aldcq Qbhfy"),
        ("uneven non-alphabetical", "Hello, World!", "gybnqkurp", "X", "Tfjip, Ijsgv!NQ"),
        ("greater key length", "Hello, World!", "gybpmicnotmixmub", "X", "Cveyx, Vizmh!VS"),
        ("uneven key, filler letter", "Welcome, cheese.", "gybnqkurp", "Z", "Fsxwgqb, ylikcz.AW"),
        ("greater key, filler letter", "Hello, World!", "gybpmicnotmixmub", "Z", "Cveyx, Vizsl!JI"),
        ("non-square key", "Hello World", "nonSquareKey", "X", None),
    ])
    def test_hillCipher(self, name, input_text, key, fillerLetter, expected):
        if expected is not None:
            encrypted = hillCipher(input_text, key, fillerLetter = fillerLetter)
            self.assertEqual(encrypted, expected)
            decrypted = decryptHill(encrypted, key)
            self.assertIn(input_text, decrypted)
        else:
            with self.assertWarns(Warning):
                hillCipher(input_text, key)
                
        
    #PLAYFAIR CIPHER
    @parameterized.expand([
        ("standard case", "Pictures", "mango", "Hkerqsdt"),
        ("non-alphabetical", "Hello, World!", "diamond", "Lbkyp, Mzith!"),
        ("uneven message", "Hello man", "Apple"),
        ("duplicate letters", ),
        ("duplicate letters, uneven", ),
        ("filler letter", ),
    ])
    def test_playfairCipher(self, name, input_text, key, expected):
        encrypted = playfairCipher(input_text, key)
        self.assertEqual(encrypted, expected)
        decrypted = decryptPlayfair(encrypted, key)
        self.assertEqual(decrypted, input_text)
        

if __name__ == '__main__':
    unittest.main()
