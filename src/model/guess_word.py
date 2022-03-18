from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Set

from src.model.colour import Colour
from src.model.guess_word_letter import GuessWordLetter
from src.model.letter import Letter
from src.model.word import Word
from src.model.word_letter import WordLetter


@dataclass
class GuessWord:
    guess_word_letters: List[GuessWordLetter]

    def __hash__(self) -> int:
        return hash(
            "".join(
                [f"{x.word_letter.letter}{x.colour}" for x in self.guess_word_letters]
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, GuessWord):
            return False
        return self.__hash__() == other.__hash__()

    def __str__(self) -> str:
        return (
            "".join([x.word_letter.letter.value for x in self.guess_word_letters])
            + " "
            + "".join([str(x.colour.value) for x in self.guess_word_letters])
        )

    def get_colour_string(self) -> str:
        return "".join([x.get_colour_string() for x in self.guess_word_letters])

    def rules_out(self, word: Word) -> bool:
        word_copy = deepcopy(word)
        for green_letter in self.get_letters_for_colour(Colour.GREEN):
            word_letter_on_index = word_copy.get_letter_on_index(green_letter.index)
            if green_letter != word_letter_on_index:
                return True
            else:
                word_copy.remove_letter_on_index(green_letter.index)
        for yellow_letter in self.get_letters_for_colour(Colour.YELLOW):
            if yellow_letter not in word_copy.word_letters:
                return True
            else:
                if yellow_letter == word_copy.get_letter_on_index(yellow_letter.index):
                    return True
                else:
                    word_copy.word_letters.remove(yellow_letter)
        for gray_letter in self.get_letters_for_colour(Colour.GRAY):
            if gray_letter in word_copy.word_letters:
                return True
        return False

    def get_letters(self) -> Set[Letter]:
        return set([x.word_letter.letter for x in self.guess_word_letters])

    def get_letters_for_colour(self, colour: Colour) -> List[WordLetter]:
        return [x.word_letter for x in self.guess_word_letters if x.colour == colour]

    @classmethod
    def calculate(cls, correct: Word, guess: Word) -> GuessWord:
        actual_word_letters = correct.word_letters
        guess_word_letters = [
            GuessWordLetter(word_letter, Colour.GRAY)
            for index, word_letter in enumerate(guess.word_letters)
        ]

        for index, word_letter in enumerate(guess.word_letters):
            if word_letter == actual_word_letters[index]:
                guess_word_letters[index].colour = Colour.GREEN

        remaining_letters = [
            x.letter
            for x in actual_word_letters
            if guess_word_letters[x.index].colour != Colour.GREEN
        ]

        for index, guess_word_letter in enumerate(guess_word_letters):
            if guess_word_letter.colour == Colour.GREEN:
                continue

            if guess_word_letter.word_letter.letter in remaining_letters:
                index_to_remove = remaining_letters.index(
                    guess_word_letter.word_letter.letter
                )
                guess_word_letter.colour = Colour.YELLOW
                remaining_letters.pop(index_to_remove)

        return cls(guess_word_letters)

    @classmethod
    def from_string(cls, guess_word_string: str) -> GuessWord:
        word, scores = guess_word_string.split()

        return cls(
            guess_word_letters=[
                GuessWordLetter(
                    word_letter=WordLetter(index, Letter(letter)),
                    colour=Colour(int(scores[index]))
                    if scores[index] != "."
                    else Colour.WHITE,
                )
                for index, letter in enumerate(list(word))
            ]
        )

    @classmethod
    def from_input(cls, word: Word) -> GuessWord:
        guess_word_string = input(f"Score per letter for {word}: ")
        if re.fullmatch(r"[0-9]{5,8}", guess_word_string):
            return cls.from_string(f"{word} {guess_word_string}")
        if re.fullmatch(r"[a-z0-9+\-*/=]{5,8} [0-9]{5,8}", guess_word_string):
            return cls.from_string(guess_word_string)
        if re.fullmatch(r"([0-9]{5}.?){1,4}", guess_word_string):
            word_string = f"{word}.{word}.{word}.{word}"[: len(guess_word_string)]
            return cls.from_string(f"{word_string} {guess_word_string}")
        if re.fullmatch(r"[a-z]{5} ([0-9]{5}.?){4}", guess_word_string):
            new_word = guess_word_string.split(" ")[0]
            word_string = f"{new_word}.{new_word}.{new_word}.{new_word}"[
                : len(guess_word_string.split()[1])
            ]
            return cls.from_string(f"{word_string} {guess_word_string.split()[1]}")
        raise Exception()

    @classmethod
    def from_quordle_input(cls, word: Word) -> List[GuessWord]:
        guess_word_string = input(f"Score per letter for {word}: ")
        if " " in guess_word_string:
            word = Word.from_string(guess_word_string.split(" ")[0])
            guess_word_string = guess_word_string.split(" ")[1]
        guess_words = []
        for colour_code in guess_word_string.split("-"):
            guess_words.append(GuessWord.from_string(f"{word} {colour_code}"))
        return guess_words

    def split_quordle(self) -> List[GuessWord]:
        word_str, score_str = str(self).split()
        words = word_str.split(".")
        scores = score_str.split(".")

        guess_words = []
        for index, word in enumerate(words):
            guess_words.append(GuessWord.from_string(f"{word} {scores[index]}"))
        return guess_words
