import argparse

from src.cache.best_next_words import BestNextWords
from src.cache.first_word_scores import FirstWordScores
from src.cache.guess_word_distribution import GuessWordDistribution
from src.config import Configs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    FUNCTION_MAP = {
        "wordle": Configs.WORDLE,
        "nerdle": Configs.NERDLE,
    }
    parser.add_argument("task", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()

    caches = [GuessWordDistribution, FirstWordScores, BestNextWords]
    for cache in caches:
        cache(FUNCTION_MAP[args.task]).run()

    # TODO: what if you map all the guesses in which you can get the correct word in 6 times?
