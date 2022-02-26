from src.model.letter import Letter
from src.model.word import Word


def test_if_word_from_string_then_str_equals_initial_word():
    word = Word.from_string("soare")
    assert word.__str__() == "soare"


def test_if_word_contains_duplicate_letters_then_get_letters_contains_unique_letters():
    word = Word.from_string("there")
    assert word.get_letters() == {Letter.T, Letter.H, Letter.E, Letter.R}
