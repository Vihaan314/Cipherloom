import unittest
from parameterized import parameterized

from .constants import ALPHABET_LOWER_REVERSE
from .cipherloom import *

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


    # VIGENERE CIPHER TESTS
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


    # TRANSPOSITION CIPHER
    @parameterized.expand([
        ("standard case", "Hello World", "key", "eoodHlWll rX"),
        ("repeated key", "Hello welcome to the program", "cheese", "Hwehgllt alcopm mtoXee eroo rX"),
        ("non-alphabetic", "Hello, World! 123", "hello", "e d3H,l2lW!Xlo Xor1X"),
    ])
    def test_columnarTranspositionCipher(self, name, message, key, expected):
        encrypted = columnarTranspositionCipher(message, key)
        self.assertEqual(encrypted, expected)
        decrypted = decryptColumnarTransposition(encrypted, key)
        self.assertIn(message, decrypted)

        
    # AFFINE CIPHER
    @parameterized.expand([
        ("standard case", "Hello World", 5, 8, "Rclla Oaplx"),
        ("non-alphabetic", "Hello, World! 123", 17, 20, "Jkzzy, Eyxzt! 123"),
        ("sample sentence", "Hey man, can you get the lights? Thanks.", 11, 18, "Rkw usf, osf wqe gkt trk jcgrti? Trsfyi."),
        ("invalid a", "Hello World", 13, 8, None),
    ])
    def test_affineCipher(self, name, message, a, b, expected):
        if expected is not None:
            encrypted = affineCipher(message, a, b)
            self.assertEqual(encrypted, expected)
            decrypted = decryptAffine(encrypted, a, b)
            self.assertEqual(decrypted, message)
        else:
            with self.assertWarns(Warning):
                affineCipher(message, a, b)
                
        
    # HILL CIPHER
    @parameterized.expand([
        ("standard case", "Hello World", "CDFH", "X", "Aldcq Qbhfy", False),
        ("uneven non-alphabetical", "Hello, World", "gybnqkurp", "X", "Tfjip, IjsgvNQ", False),
        ("greater key length", "Hello, World!", "gybpmicnotmixmub", "X", "Cveyx, Vizmh!VS", True),
        ("uneven key, filler letter", "Welcome, cheese", "gybnqkurp", "Z", "Fsxwgqb, ylikczAW", True),
        ("greater key, filler letter", "Hello, World!", "gybpmicnotmixmub", "Z", "Cveyx, Vizsl!JI", False),
        ("non-square key", "Hello World", "nonSquareKey", "X", None, False),
    ])
    def test_hillCipher(self, name, message, key, filler_letter, expected_encrypted, remove_filler):
        if expected_encrypted is not None:
            encrypted = hillCipher(message, key, filler_letter = filler_letter)
            self.assertEqual(encrypted, expected_encrypted)
            decrypted = decryptHill(encrypted, key, remove_filler = remove_filler)
            if remove_filler:
                self.assertEqual(message, decrypted)
            else:
                self.assertIn(message, decrypted)
        else:
            with self.assertWarns(Warning):
                hillCipher(message, key)
                
        
    # PLAYFAIR CIPHER
    @parameterized.expand([
        ("standard case unnormalized", "Pictures", "mango", "X", "Hkerqsdt", False, "Pictures"),
        ("non-alphabetical u.n", "Hello, World!", "Diamond", "X", "LbkYpm, ZithaV!", False, "HelXlo, WorldX!"),
        ("uneven message", "Hello man", "APPLE", "X", "GbfLbm ilmY", True, "Hello man"),
        ("duplicates, n.a u.n", "Jazz, dude sirs! What you doing?", "cheese", "X", "OivYw, iqis afuh! Yecy suz ilgofY?", False, "IazXz, dude sirs! What you doingX?"),
        ("duplicates, n.a., u.n", "Jazz, dude sirs! What you doing", "cheese", "X", "OivYw, iqis afuh! Yecy suz ilgofY", True, "Iazz, dude sirs! What you doing"),
        ("custom filler q, n.a", "Jazz, dude sirs! Weelh you doing?", "meeting", "Q", "EcwUn, ozoi qtsq! YaWihl wuz ounmaP?", True, "Iazz, dude sirs! Weelh you doing?"),
        ("duplicates, n.a, custom filler lower u.n", "Jazz, dude sirs! Weelh you doing", "meeting", "q", "Ecwun, ozoi qtsq! Yawihl wuz ounmap", False, "Iazqz, dude sirs! Weqelh you doingq"),
        ("lots of duplicates, n.a u.n", "Jazz, dude sirs Weelh you jazzin?", "Mango", "X", "RcvYx, fsfd trwr XdYltl vfz rcvYwpdN?", False, "IazXz, dude sirs WeXelh you iazXzinX?"),
        ("duplicates with punc, empty key, n.a", "Jazz, dude sirs! Stop, pls jazz? Ab123", "", "X", "FdvYy, etec ugtxC! Tupl, lmt hevv? EcW123", True, "Iazz, dude sirs! Stop, pls iazz? Ab123"),
        ("lots of duplicates with punc, n.a", "Jazz, dude sirs! Stoopp, pls jazz?", "secret", "X", "HbvYx, gpgc elecV! EspWpqxC, qke hgvvY?", True, "Iazz, dude sirs! Stoopp, pls iazz?")
    ])
    def test_playfairCipher(self, name, message, key, filler_letter, expected_encrypted, remove_filler, expected_decrypted):
        encrypted = playfairCipher(message, key, filler_letter = filler_letter)
        self.assertEqual(encrypted, expected_encrypted)
        decrypted = decryptPlayfair(encrypted, key, remove_filler = remove_filler)
        self.assertEqual(decrypted, expected_decrypted)
        

if __name__ == "__main__":
    unittest.main()
