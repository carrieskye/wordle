import argparse
from typing import List

from rich import print as print_rich
from skye_comlib.utils.file import File

from src.config import Configs, Config
from src.model.guess_word import GuessWord
from src.model.word import Word
from src.wordle import Wordle


def print_try(word: Word):
    print_rich(f"Try [bold cyan]{word}\n")


def get_key(guesses: List[GuessWord]) -> str:
    return ";".join([x.__str__() for x in guesses])


def play(config: Config):
    wordle = Wordle.load_from_file(config.data_dir)
    wordle.print_possibilities()
    guesses = []
    best_next_words = {
        x["guess_word"]: x["best_next_word"]
        for x in File.read_csv(path=config.data_dir / "best_next_words.csv")
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

    FUNCTION_MAP = {"wordle": Configs.WORDLE, "nerdle": Configs.NERDLE, "quordle": Configs.QUORDLE}
    parser.add_argument("task", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    play(FUNCTION_MAP[args.task])
