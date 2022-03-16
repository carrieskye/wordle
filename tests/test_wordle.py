from pathlib import Path

import pytest
from skye_comlib.utils.file import File

from src.model.guess_word import GuessWord
from src.word_list import WordList
from src.wordle import Wordle


@pytest.fixture()
def wordle():
    return Wordle(
        possible_words=WordList.load(File.read_txt(Path("../data/wordle/possible_words.txt"))),
        allowed_words=WordList.load(File.read_txt(Path("../data/wordle/allowed_words.txt"))),
    )


def count_words_with_letters(wordle, guess_word: GuessWord) -> int:
    count = 0
    for word in wordle.possible_words:
        if bool([x for x in word.get_letters() if x in guess_word.get_letters()]):
            count += 1
    return count


def test_if_soare_00000_then_all_words_with_s_o_a_r_e_are_removed(wordle):
    guess_word = GuessWord.from_string("soare 00000")
    words_with_letters = count_words_with_letters(wordle, guess_word)
    wordle.remove_wrong_words(guess_word)
    assert len(wordle.possible_words) == 2315 - words_with_letters
