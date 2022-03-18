import argparse
from typing import List

from rich import print as print_rich
from skye_comlib.utils.file import File

from src.config import Configs, Config
from src.model.guess_word import GuessWord
from src.model.word import Word


def print_try(word: Word):
    print_rich(f"Try [bold cyan]{word}\n")


def get_key(guesses: List[GuessWord]) -> str:
    return ";".join([x.__str__() for x in guesses])


def play(config: Config):
    game = config.get_game()
    game.print_possibilities()
    guesses = []
    best_next_words = {
        x["guess_word"]: x["best_next_word"]
        for x in File.read_csv(path=config.data_dir / "best_next_words.csv")
    }
    while len(game.possible_words) > 1:
        try:
            best_next_word = best_next_words[get_key(guesses)]
        except KeyError:
            best_next_word = game.get_allowed_words_sorted()[0]
        print_try(best_next_word)
        guess = GuessWord.from_input(best_next_word)
        guesses.append(guess)
        game.remove_wrong_words(guess)
        game.print_possibilities()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    FUNCTION_MAP = {
        "wordle": Configs.WORDLE,
        "nerdle": Configs.NERDLE,
        "quordle": Configs.QUORDLE,
    }
    parser.add_argument("task", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    play(FUNCTION_MAP[args.task])
