from pathlib import Path
from typing import List

from rich import print as print_rich
from skye_comlib.utils.file import File

from src.model.guess_word import GuessWord
from src.wordle import Wordle


def print_try(word: str):
    print_rich(f"Try [bold cyan]{word}\n")


def get_key(guesses: List[GuessWord]) -> str:
    return ";".join([x.__str__() for x in guesses])


def play_wordle():
    wordle = Wordle.load_from_file()
    wordle.print_possibilities()
    guesses = []
    best_next_words = {
        x["guess_word"]: x["best_next_word"]
        for x in File.read_csv(path=Path("data/best_next_words.csv"))
    }
    while len(wordle.possible_words) > 1:
        try:
            print_try(best_next_words[get_key(guesses)])
        except KeyError:
            print_try(str(wordle.get_allowed_words_sorted()[0]))
        guess = GuessWord.from_input()
        guesses.append(guess)
        wordle.remove_wrong_words(guess)
        wordle.print_possibilities()


if __name__ == "__main__":
    play_wordle()
