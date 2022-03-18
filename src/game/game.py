from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from src.model.guess_word import GuessWord
from src.model.word import Word
from src.model.word_list import WordList


class Game(ABC):
    def __init__(self, allowed_words: WordList, possible_words: WordList):
        self.allowed_words = allowed_words
        self.possible_words = possible_words

    @abstractmethod
    def remove_wrong_words(self, guess_word: GuessWord, verbose: bool = True):
        pass

    @abstractmethod
    def get_allowed_words_sorted(self, desc: str = "") -> List[Word]:
        pass

    @abstractmethod
    def print_possibilities(self):
        pass

    @abstractmethod
    def get_number_of_possibilities(self) -> int:
        pass

    @abstractmethod
    def is_final_word(self, word: Word) -> bool:
        pass

    @classmethod
    @abstractmethod
    def load_from_file(cls, data_dir: Path) -> Game:
        pass
