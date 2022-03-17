import argparse
from pathlib import Path
from typing import List

from rich import print as print_rich
from skye_comlib.utils.file import File

from src.model.game import Game
from src.model.guess_word import GuessWord
from src.model.word import Word
from src.wordle import Wordle


def print_try(word: Word):
    print_rich(f"Try [bold cyan]{word}\n")


def get_key(guesses: List[GuessWord]) -> str:
    return ";".join([x.__str__() for x in guesses])


def play(game: Game):
    wordle = Wordle.load_from_file(game)
    wordle.print_possibilities()
    guesses = []
    best_next_words = {
        x["guess_word"]: x["best_next_word"]
        for x in File.read_csv(path=Path(f"data/{game.value}/best_next_words.csv"))
    }
    while len(wordle.possible_words) > 1:
        try:
            best_next_word = best_next_words[get_key(guesses)]
        except KeyError:
            best_next_word = wordle.get_allowed_words_sorted()[0]
        print_try(best_next_word)
        guess = GuessWord.from_input(best_next_word)
        guesses.append(guess)
        wordle.remove_wrong_words(guess)
        wordle.print_possibilities()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    FUNCTION_MAP = {"wordle": Game.WORDLE, "nerdle": Game.NERDLE}
    parser.add_argument("task", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    play(FUNCTION_MAP[args.task])
