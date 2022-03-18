from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import List, Dict

from rich import print as print_rich
from tqdm import tqdm

from src.game.game import Game
from src.model.guess_word import GuessWord
from src.model.word import Word
from src.model.word_list import WordList


class Quordle(Game):
    def get_allowed_words_sorted(self) -> List[Word]:
        pass

    def print_possibilities(self):
        pass

    def __init__(self, possible_words: WordList, allowed_words: WordList):
        self.possible_words_per_sub_game = [
            deepcopy(possible_words),
            deepcopy(possible_words),
            deepcopy(possible_words),
            deepcopy(possible_words),
        ]
        super().__init__(
            allowed_words,
            WordList(
                [
                    word
                    for word_list in self.possible_words_per_sub_game
                    for word in word_list
                ]
            ),
        )

        print(
            f"Loaded {len(self.possible_words)} possible words and "
            f"{len(self.allowed_words)} allowed words.\n"
        )

    @staticmethod
    def split_guess_word(guess_word: GuessWord) -> List[GuessWord]:
        words = guess_word[0:23]
        colour_codes = guess_word[24:]
        guess_words = []
        for index, word in words.split(" "):
            guess_words.append(GuessWord.from_string(f"{word} {colour_codes[index]}"))
        return guess_words

    def remove_wrong_words(self, guess_word: GuessWord):
        for index, guess_word in self.split_guess_word(guess_word):
            new_possible_words = self.possible_words[index].remove_wrong_words(
                guess_word
            )
            print_rich(
                f"\n[white not bold]Removed words ruled out by {guess_word.get_colour_string()}"
                f"[white]: went from {len(self.possible_words)} to {len(new_possible_words)} words."
                f"\n"
            )
            self.possible_words[index] = new_possible_words

    def get_guess_word_distribution(self, word: Word) -> Dict[GuessWord, int]:
        guess_words = defaultdict(int)
        for possible_words in self.possible_words:
            for possible_word in tqdm(possible_words, leave=False, desc=word.__str__()):
                guess_words[GuessWord.calculate(correct=possible_word, guess=word)] += 1
        return guess_words

    def get_guess_word_distribution_per_list(
        self, word: Word
    ) -> List[Dict[GuessWord, int]]:
        guess_words_per_list = []
        for possible_words in self.possible_words:
            guess_words = defaultdict(int)
            for possible_word in tqdm(possible_words, leave=False, desc=word.__str__()):
                guess_words[GuessWord.calculate(correct=possible_word, guess=word)] += 1
            guess_words_per_list.append(guess_words)
        return guess_words_per_list

    def calculate_score(self, word: Word) -> float:
        total_score = 0
        for index, guess_words in enumerate(
            self.get_guess_word_distribution_per_list(word)
        ):
            for guess_word, count in tqdm(
                guess_words.items(), leave=False, desc=word.__str__()
            ):
                possible_words = self.possible_words[index].remove_wrong_words(
                    guess_word
                )
                guess_word_score = len(self.possible_words[index]) - len(possible_words)
                total_score += guess_word_score * count
        return total_score / sum([len(x) for x in self.possible_words])

    @classmethod
    def load_from_file(cls, data_dir: Path) -> Quordle:
        return cls(
            possible_words=WordList.load_possible_words(data_dir),
            allowed_words=WordList.load_allowed_words(data_dir),
        )
