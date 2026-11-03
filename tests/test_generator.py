import os
import string
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator import (SYMBOLS, PasswordParamsError, estimate_strength,
                       generate_password)


class TestGenerator(unittest.TestCase):
    def test_length(self):
        for n in (4, 12, 64):
            self.assertEqual(len(generate_password(n)), n)

    def test_contains_all_selected_types(self):
        for _ in range(200):
            p = generate_password(8, True, True, True, True)
            self.assertTrue(any(c in string.ascii_lowercase for c in p))
            self.assertTrue(any(c in string.ascii_uppercase for c in p))
            self.assertTrue(any(c in string.digits for c in p))
            self.assertTrue(any(c in SYMBOLS for c in p))

    def test_only_digits(self):
        p = generate_password(10, False, False, True, False)
        self.assertTrue(p.isdigit())

    def test_passwords_differ(self):
        self.assertNotEqual(generate_password(20), generate_password(20))

    def test_too_short(self):
        with self.assertRaises(PasswordParamsError):
            generate_password(3)

    def test_too_long(self):
        with self.assertRaises(PasswordParamsError):
            generate_password(65)

    def test_no_sets(self):
        with self.assertRaises(PasswordParamsError):
            generate_password(10, False, False, False, False)

    def test_length_not_int(self):
        with self.assertRaises(PasswordParamsError):
            generate_password("abc")

    def test_strength_levels(self):
        self.assertEqual(estimate_strength("")[1], "Пусто")
        self.assertEqual(estimate_strength("abcd")[1], "Слабый")
        self.assertEqual(estimate_strength("aB3$aB3$aB3$aB3$")[1], "Отличный")


if __name__ == "__main__":
    unittest.main()
