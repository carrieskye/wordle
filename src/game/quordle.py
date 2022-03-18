from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import List

from tqdm import tqdm

from src.game.basic import Basic
from src.game.game import Game
from src.model.guess_word import GuessWord
from src.model.word import Word


class Quordle(Game):
    def __init__(self, wordle_list: List[Basic]):
        self.wordle_list = wordle_list
        super().__init__(wordle_list[0].allowed_words, wordle_list[0].possible_words)
        self.correct_words = [None] * len(self.wordle_list)

    def remove_wrong_words(self, guess_word: GuessWord, verbose: bool = True):
        for index, quordle_guess_word in enumerate(guess_word.split_quordle()):
            self.wordle_list[index].remove_wrong_words(quordle_guess_word)

    def get_allowed_words_sorted(self, desc: str = "") -> List[Word]:
        for index, wordle in enumerate(self.wordle_list):
            if len(wordle.possible_words) == 1 and not self.correct_words[index]:
                self.correct_words[index] = wordle.possible_words[0]
                self.wordle_list.pop(index)
                return wordle.possible_words

        scores = []
        for word in tqdm(
            self.allowed_words,
            desc=f'"{desc}": trying {len(self.possible_words)} possibilities',
            leave=False,
        ):
            score = 0
            for wordle in self.wordle_list:
                score += wordle.calculate_score(word)

            scores.append((word, score))
        scores = sorted(
            scores, key=lambda x: (-1 * x[1], x[0] not in self.possible_words)
        )
        return [x[0] for x in scores]

    def print_possibilities(self):
        for wordle in self.wordle_list:
            wordle.print_possibilities()

    def get_number_of_possibilities(self) -> int:
        return sum(
            [wordle.get_number_of_possibilities() for wordle in self.wordle_list]
        )

    def is_final_word(self, word: Word) -> bool:
        for index, wordle in enumerate(self.wordle_list):
            if wordle.is_final_word(word):
                self.wordle_list.pop(index)
                return True
        return False

    @classmethod
    def load_from_file(cls, data_dir: Path) -> Quordle:
        basic = Basic.load_from_file(data_dir)
        return cls(
            wordle_list=[
                deepcopy(basic),
                deepcopy(basic),
                deepcopy(basic),
                deepcopy(basic),
            ]
        )
