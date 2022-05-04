import argparse
from collections import defaultdict
from typing import List

from rich import print as print_rich

from src.cache.best_next_words import BestNextWords
from src.config import Configs, Config
from src.model.guess_word import GuessWord
from src.model.word import Word


def play(config: Config):
    game = config.get_game()
    best_next_words = BestNextWords(config)
    distribution = defaultdict(int)

    for possible_word in game.possible_words:
        entry = Word.from_string(best_next_words.results[0]["best_next_word"])
        no_of_possibilities = len(game.possible_words)
        guess_word_str = None
        guesses = 1

        while int(no_of_possibilities) > 1:
            guess_word = GuessWord.calculate(possible_word, entry)
            if not guess_word_str:
                guess_word_str = str(guess_word)
            else:
                guess_word_str += f";{guess_word}"
            for result in best_next_words.results:
                if result["word"] == guess_word_str:
                    entry = Word.from_string(result["best_next_word"])
                    no_of_possibilities = result["no_of_possibilities"]
                    break
            if str(guess_word).split()[-1] != "22222":
                guesses += 1
        distribution[guesses] += 1

    distribution_sorted = sorted(distribution.items(), key=lambda x: x[0])
    for k, v in distribution_sorted:
        print(f"{k} guesses: {v}/{len(game.possible_words)} ({100*v/len(game.possible_words):.2f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    FUNCTION_MAP = {
        "wordle": Configs.WORDLE,
        "nerdle": Configs.NERDLE,
    }
    parser.add_argument("task", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    play(FUNCTION_MAP[args.task])
