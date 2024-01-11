import unittest
from parameterized import parameterized
from cipherloom import (
    CaesarCipher, ROT13Cipher, TrithemiusCipher, AtbashCipher,
    MonoalphabeticCipher, VigenereCipher, TranspositionCipher,
    AffineCipher, HillCipher, PlayfairCipher,
)
from cipherloom.constants import ALPHABET_LOWER_REVERSE

class TestCipherMethods(unittest.TestCase):
    def _test_encryption_decryption(self, cipher_class, label, message, cipher_args, expected_encrypted, expected_decrypted=None, **kwargs):
        cipher = cipher_class()
        encrypted = cipher.encrypt(message, *cipher_args)
        self.assertEqual(encrypted, expected_encrypted, msg=f"{label} - Encrypt")

        has_decrypt = True
        if expected_decrypted is None:
            has_decrypt = False
            expected_decrypted = message

        decrypted = cipher.decrypt(encrypted, *cipher_args, **kwargs)
        self.assertEqual(decrypted, expected_decrypted, msg=f"{label} - Decrypt") if has_decrypt else self.assertIn(expected_decrypted, message, msg=f"{label} - Decrypt")


    # CAESAR CIPHER TESTS
    @parameterized.expand([
        ("normal text", "Hello World", (3,), "Khoor Zruog"),
        ("upper case", "HELLO WORLD", (3,), "KHOOR ZRUOG"),
        ("wrap around", "xyz", (3,), "abc"),
        ("negative key", "Hello World", (-3,), "Ebiil Tloia"),
        ("zero key", "Hello World", (0,), "Hello World"),
    ])
    def test_caesarCipher(self, label, message, cipher_args, expected):
        self._test_encryption_decryption(CaesarCipher, label, message, cipher_args, expected)


    # ROT13 CIPHER TESTS
    @parameterized.expand([
        ("standard", "Hello World", (), "Uryyb Jbeyq"),
        ("non-alphabetic", "Hello, World!", (), "Uryyb, Jbeyq!"),
    ])
    def test_rot13Cipher(self, label, message, cipher_args, expected):
        self._test_encryption_decryption(ROT13Cipher, label, message, cipher_args, expected)


     # TRITHEMIUS CIPHER TESTS
    @parameterized.expand([
        ("ascending", "Hello, World!", True, 0, "Hfnos, Buytm!"),  
        ("descending", "Hello, World!", False, 0, "Hdjik, Rikdu!"),  
        ("ascending shift", "Hello, World!", True, 12, "Trzae, Ngkfy!"),
        ("descending shift", "Hello, World!", False, 32, "Bxdce, Lcexo!"), 
    ])
    def test_trithemiusCipher(self, label, message, ascending, initial_shift, expected):
        self._test_encryption_decryption(TrithemiusCipher, label, message, (ascending, initial_shift), expected)


    # ATBASH CIPHER TESTS
    @parameterized.expand([
        ("standard", "Hello World", "Svool Dliow"),
        ("non-alphabetic", "Hello, World!", "Svool, Dliow!"),
    ])
    def test_atbashCipher(self, label, message, expected):
        self._test_encryption_decryption(AtbashCipher, label, message, (), expected)


    # MONOALPHABETIC CIPHER TESTS
    @parameterized.expand([
        ("normal text", "Hello World", ALPHABET_LOWER_REVERSE, "Svool Dliow"),
        ("non-alphabetic", "Hello, World!", "QWERTYUIOPASDFGHJKLZXCVBNM", "Itssg, Vgksr!"),
        ("key as rotation", "Hello World", "BCDEFGHIJKLMNOPQRSTUVWXYZA", "Ifmmp Xpsme"),
    ])
    def test_monoalphabeticCipher(self, label, message, alphabet, expected):
        self._test_encryption_decryption(MonoalphabeticCipher, label, message, (alphabet,), expected)


    # VIGENERE CIPHER TESTS
    @parameterized.expand([
        ("standard case", "Hello World", "KEY", "Rijvs Uyvjn"),
        ("non-alphabetic", "Hello, World! Welcome to the cipher.", "Cheese", "Jlppg, Aqyph! Oinjsqw xq ali umroiv."),
        ("sample sentence", "Hello, man! Can you get the lightz?", "lights", "Smrsh, elv! Ihg qzc mlm lsm rpzzeh?"),
    ])
    def test_vigenereCipher(self, label, message, key, expected):
        self._test_encryption_decryption(VigenereCipher, label, message, (key,), expected)
        

    # TRANSPOSITION CIPHER TESTS
    @parameterized.expand([
        ("standard case", "Hello World", ("key",), "eoodHlWll rX"),
        ("repeated key", "Hello welcome to the program", ("cheese",), "Hwehgllt alcopm mtoXee eroo rX"),
        ("non-alphabetic", "Hello, World! 123", ("hello",), "e d3H,l2lW!Xlo Xor1X"),
    ])
    def test_columnarTranspositionCipher(self, label, message, cipher_args, expected):
        self._test_encryption_decryption(TranspositionCipher, label, message, cipher_args, expected)


    # AFFINE CIPHER TESTS
    @parameterized.expand([
        ("standard case", "Hello World", (5, 8), "Rclla Oaplx"),
        ("non-alphabetic", "Hello, World! 123", (17, 20), "Jkzzy, Eyxzt! 123"),
    ])
    def test_affineCipher(self, label, message, cipher_args, expected):
        self._test_encryption_decryption(AffineCipher, label, message, cipher_args, expected)


    # HILL CIPHER TESTS
    @parameterized.expand([
        ("standard case", "Hello World", "CDFH", "X", "Aldcq Qbhfy", False),
        ("uneven non-alphabetical", "Hello, World", "gybnqkurp", "X", "Tfjip, IjsgvNQ", False),
        ("greater key length", "Hello, World!", "gybpmicnotmixmub", "X", "Cveyx, Vizmh!VS", True),
        ("uneven key, filler letter", "Welcome, cheese", "gybnqkurp", "Z", "Fsxwgqb, ylikczAW", True),
        ("greater key, filler letter", "Hello, World!", "gybpmicnotmixmub", "Z", "Cveyx, Vizsl!JI", False),
        ("non-square key", "Hello World", "nonSquareKey", "X", None, False),
    ])
    def test_hillCipher(self, label, message, key, filler_letter, expected_encrypted, remove_filler):
        cipher = HillCipher()
        if expected_encrypted is not None:
            encrypted = cipher.encrypt(message, key, filler_letter=filler_letter)
            self.assertEqual(encrypted, expected_encrypted, msg=f"{label} - Encrypt")
            decrypted = cipher.decrypt(encrypted, key, remove_filler=remove_filler)
            self.assertEqual(decrypted, message, msg=f"{label} - Decrypt") if remove_filler else self.assertIn(message, decrypted, msg=f"{label} - Decrypt")
        else:
            with self.assertWarns(Warning):
                cipher.encrypt(message, key, filler_letter=filler_letter)


    # PLAYFAIR CIPHER TESTS
    @parameterized.expand([
        ("standard case unnormalized", "Pictures", "mango", "Hkerqsdt", False, "Pictures", "X"),
        ("non-alphabetical u.n", "Hello, World!", "Diamond", "LbkYpm, ZithaV!", False, "HelXlo, WorldX!", "X"),
        ("uneven message", "Hello man", "APPLE", "GbfLbm ilmY", True, "Hello man", "X"),
        ("duplicates, n.a u.n", "Jazz, dude sirs! What you doing?", "cheese", "OivYw, iqis afuh! Yecy suz ilgofY?", False, "IazXz, dude sirs! What you doingX?", "X"),
        ("duplicates, n.a., u.n", "Jazz, dude sirs! What you doing", "cheese", "OivYw, iqis afuh! Yecy suz ilgofY", True, "Iazz, dude sirs! What you doing", "X"),
        ("custom filler q, n.a", "Jazz, dude sirs! Weelh you doing?", "meeting", "EcwUn, ozoi qtsq! YaWihl wuz ounmaP?", True, "Iazz, dude sirs! Weelh you doing?", "Q"),
        ("duplicates, n.a, custom filler lower u.n", "Jazz, dude sirs! Weelh you doing", "meeting", "Ecwun, ozoi qtsq! Yawihl wuz ounmap", False, "Iazqz, dude sirs! Weqelh you doingq", "q"),
        ("lots of duplicates, n.a u.n", "Jazz, dude sirs Weelh you jazzin?", "Mango", "RcvYx, fsfd trwr XdYltl vfz rcvYwpdN?", False, "IazXz, dude sirs WeXelh you iazXzinX?", "X"),
        ("duplicates with punc, empty key, n.a", "Jazz, dude sirs! Stop, pls jazz? Ab123", "", "FdvYy, etec ugtxC! Tupl, lmt hevv? EcW123", True, "Iazz, dude sirs! Stop, pls iazz? Ab123", "X"),
        ("lots of duplicates with punc, n.a", "Jazz, dude sirs! Stoopp, pls jazz?", "secret", "HbvYx, gpgc elecV! EspWpqxC, qke hgvvY?", True, "Iazz, dude sirs! Stoopp, pls iazz?", "X"),
    ])
    def test_playfairCipher(self, label, message, key, expected_encrypted, remove_filler, expected_decrypted, filler_letter):
        cipher = PlayfairCipher()
        encrypted = cipher.encrypt(message, key, filler_letter=filler_letter)
        self.assertEqual(encrypted, expected_encrypted, msg=f"{label} - Encrypt")

        decrypted = cipher.decrypt(encrypted, key, remove_filler=remove_filler)
        self.assertEqual(decrypted, expected_decrypted, msg=f"{label} - Decrypt")

if __name__ == "__main__":
    unittest.main()



#python -m unittest discover -s tests
