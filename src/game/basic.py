from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Set

from rich import print as print_rich
from tqdm import tqdm

from src.game.game import Game
from src.model.guess_word import GuessWord
from src.model.word import Word
from src.model.word_list import WordList


class Basic(Game):
    def __init__(self, allowed_words: WordList, possible_words: WordList):
        super().__init__(allowed_words, possible_words)

    def remove_wrong_words(self, guess_word: GuessWord, verbose: bool = True):
        old_possible_words = len(self.possible_words)
        self.possible_words = self.possible_words.remove_wrong_words(guess_word)

        if verbose:
            print_rich(
                f"\n[white not bold]Removed words ruled out by {guess_word.get_colour_string()}"
                f"[white]: went from {old_possible_words} to {len(self.possible_words)} words."
                f"\n"
            )
            self.print_possibilities()

    def get_allowed_words_sorted(self, desc: str = "") -> List[Word]:
        scores = []
        for word in tqdm(
            self.allowed_words,
            desc=f'"{desc}": trying {len(self.possible_words)} possibilities',
            leave=False,
        ):
            scores.append((word, self.calculate_score(word)))
        scores = sorted(
            scores, key=lambda x: (-1 * x[1], x[0] not in self.possible_words)
        )
        return [x[0] for x in scores]

    def get_guess_word_distribution(self, word: Word) -> Dict[GuessWord, int]:
        guess_words = defaultdict(int)
        for possible_word in tqdm(
            self.possible_words, leave=False, desc=word.__str__()
        ):
            guess_words[GuessWord.calculate(correct=possible_word, guess=word)] += 1
        return guess_words

    def get_guess_words(self, word: Word) -> Set[GuessWord]:
        return set(self.get_guess_word_distribution(word).keys())

    def calculate_score(self, word: Word) -> float:
        guess_words = self.get_guess_word_distribution(word)
        total_score = 0
        for guess_word, count in tqdm(
            guess_words.items(), leave=False, desc=word.__str__()
        ):
            possible_words = self.possible_words.remove_wrong_words(guess_word)
            guess_word_score = len(self.possible_words) - len(possible_words)
            total_score += guess_word_score * count
        return total_score / len(self.possible_words)

    def print_possibilities(self):
        print(
            f"Possibilities ({len(self.possible_words)}): "
            f"{', '.join([str(x) for x in self.possible_words])}\n"
        )

    def get_number_of_possibilities(self) -> int:
        return len(self.possible_words)

    @classmethod
    def load_from_file(cls, data_dir: Path) -> Basic:
        return cls(
            possible_words=WordList.load_possible_words(data_dir),
            allowed_words=WordList.load_allowed_words(data_dir),
        )
