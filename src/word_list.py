from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import List

from skye_comlib.utils.file import File
from tqdm import tqdm

from src.model.guess_word import GuessWord
from src.model.word import Word


class WordList(List[Word]):
    def calculate_score(self, word: Word):
        guess_words = defaultdict(int)
        for possible_word in tqdm(self, leave=False, desc=word.__str__()):
            guess_words[GuessWord.calculate(correct=possible_word, guess=word)] += 1
        total_score = 0
        for guess_word, count in tqdm(
            guess_words.items(), leave=False, desc=word.__str__()
        ):
            guess_word_score = len(self) - len(self.remove_wrong_words(guess_word))
            total_score += guess_word_score * count
        return total_score / len(self)

    def remove_wrong_words(self, guess_word: GuessWord) -> WordList:
        correct_words = []
        for word in self:
            if not guess_word.rules_out(word):
                correct_words.append(word)
        return WordList(correct_words)

    @classmethod
    def load(cls, words: List[str]) -> WordList:
        return cls([Word.from_string(word) for word in sorted(words)])

    @classmethod
    def load_possible_words(cls) -> WordList:
        return cls.load(File.read_txt(path=Path("data/possible_words.txt")))

    @classmethod
    def load_allowed_words(cls) -> WordList:
        return cls.load(
            File.read_txt(path=Path("data/allowed_words.txt"))
            + File.read_txt(path=Path("data/possible_words.txt"))
        )
