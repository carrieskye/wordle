import sys

from rich import print as print_rich
from skye_comlib.utils.file import File

from src.model.guess_word import GuessWord
from src.wordle import Wordle


def print_try(word: str):
    print_rich(f"Try [bold cyan]{word}\n")


def play_wordle():
    wordle = Wordle.load_from_file()
    wordle.print_possibilities()
    words_with_scores = File.read_json("data/words_with_scores.json")
    print_try(list(words_with_scores.keys())[0])

    attempt = 0
    while len(wordle.possible_words) > 0:
        attempt += 1
        guess = GuessWord.from_input()
        wordle.remove_wrong_words(guess)
        wordle.print_possibilities()
        if len(wordle.possible_words) <= 2:
            print_try(str(wordle.possible_words[0]))
            sys.exit()

        if attempt == 1 and guess.__str__().split()[0] in ["soare"]:
            words_with_scores_2 = File.read_json("data/words_with_best_next_word.json")
            print_try(words_with_scores_2[guess.__str__()])
        else:
            print_try(str(wordle.get_allowed_words_sorted()[0]))


if __name__ == "__main__":
    play_wordle()
