import unittest

from parameterized import parameterized

from src.model.guess_word import GuessWord
from src.model.word import Word


class TestGuessWord(unittest.TestCase):
    @parameterized.expand(
        [
            ["soare 00000", "wheat", True],
            ["soare 00000", "whelp", True],
            ["there 00200", "speak", False],
            ["utter 01001", "thorn", False],
            ["those 22200", "thorn", False],
            ["fuzzy 00000", "soare", False],
            ["mamma 00002", "theta", False],
            ["mamma 01000", "thank", False],
            ["mamma 00001", "thank", False],
            ["mamma 01002", "tiara", False],
            ["timid 02012", "vivid", True],
            ["timid 01022", "vivid", True],
            ["timid 02022", "vivid", False],
            ["aarti 21000", "abate", True],
            ["geeky 21000", "given", False]
        ]
    )
    def test_rules_out(self, guess_word_str: str, word_str: str, rules_out: bool):
        guess_word = GuessWord.from_string(guess_word_str)
        word = Word.from_string(word_str)
        self.assertEqual(rules_out, guess_word.rules_out(word))

    @parameterized.expand(
        [
            ["soare", "fuzzy", "fuzzy 00000"],
            ["vigil", "clean", "clean 01000"],
            ["thorn", "utter", "utter 01001"],
            ["thorn", "those", "those 22200"],
            ["thorn", "thorn", "thorn 22222"],
            ["trove", "soare", "soare 01012"],
            ["trove", "paint", "paint 00001"],
            ["trove", "tempo", "tempo 21001"],
            ["tiara", "mamma", "mamma 01002"],
            ["vivid", "weary", "weary 00000"],
            ["vivid", "valve", "valve 20010"],
            ["vivid", "river", "river 02200"],
            ["given", "geeky", "geeky 21000"]
        ]
    )
    def test_calculate(self, correct: str, guess: str, guess_word_str: str):
        guess_word = GuessWord.calculate(
            correct=Word.from_string(correct), guess=Word.from_string(guess)
        )
        self.assertEqual(guess_word_str, guess_word.__str__())
