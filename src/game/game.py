from __future__ import annotations

from abc import abstractmethod, ABC
from pathlib import Path
from typing import List, Dict

from src.model.guess_word import GuessWord
from src.model.word import Word
from src.model.word_list import WordList


class Game(ABC):
    def __init__(self, allowed_words: WordList, possible_words: WordList):
        self.allowed_words = allowed_words
        self.possible_words = possible_words

    @abstractmethod
    def remove_wrong_words(self, guess_word: GuessWord):
        pass

    @abstractmethod
    def get_allowed_words_sorted(self) -> List[Word]:
        pass

    @abstractmethod
    def get_guess_word_distribution(self, word: Word) -> Dict[GuessWord, int]:
        pass

    @abstractmethod
    def calculate_score(self, word: Word) -> float:
        pass

    @abstractmethod
    def print_possibilities(self):
        pass

    @classmethod
    @abstractmethod
    def load_from_file(cls, data_dir: Path) -> Game:
        pass
