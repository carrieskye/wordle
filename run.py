import argparse
from typing import List

from rich import print as print_rich

from src.cache.best_next_words import BestNextWords
from src.config import Configs, Config
from src.model.guess_word import GuessWord
from src.model.word import Word


def print_try(word: Word):
    print_rich(f"Try [bold cyan]{word}\n")


def get_key(guesses: List[GuessWord]) -> str:
    return ";".join([str(x) for x in guesses])


def play(config: Config):
    game = config.get_game()
    print(
        f"Loaded {len(game.possible_words)} possible words and "
        f"{len(game.allowed_words)} allowed words."
    )
    game.print_possibilities()
    guesses = []
    best_next_words = BestNextWords(config)
    while game.get_number_of_possibilities() > 1:
        best_next_word = best_next_words.lookup(";".join([str(x) for x in guesses]))
        if not best_next_word:
            number_of_possibilities = game.get_number_of_possibilities()
            best_next_word = game.get_allowed_words_sorted()[0]
            if len(guesses) <= 2:
                best_next_words.add_result(
                    {
                        "round": len(guesses),
                        "word": ";".join([str(x) for x in guesses]),
                        "best_next_word": str(best_next_word),
                        "no_of_possibilities": number_of_possibilities,
                    }
                )
        print_try(best_next_word)
        guess = GuessWord.from_input(best_next_word)
        guesses.append(guess)
        game.remove_wrong_words(guess)


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
