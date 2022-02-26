from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from src.model.letter import Letter
from src.model.word_letter import WordLetter


@dataclass
class Word:
    word_letters: List[WordLetter]

    def __str__(self) -> str:
        return "".join([x.letter.value for x in self.word_letters])

    def get_letters(self) -> Set[Letter]:
        return set([x.letter for x in self.word_letters])

    def get_letter_on_index(self, index: int) -> WordLetter:
        for letter in self.word_letters:
            if letter.index == index:
                return letter

    def remove_letter_on_index(self, index: int):
        self.word_letters = [x for x in self.word_letters if x.index != index]

    @classmethod
    def from_string(cls, word_string: str) -> Word:
        return Word(
            [WordLetter(index, Letter(x)) for index, x in enumerate(word_string)]
        )
