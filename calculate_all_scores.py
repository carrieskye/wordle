from copy import deepcopy
from pathlib import Path

from skye_comlib.utils.file import File
from tqdm import tqdm

from src.model.guess_word import GuessWord
from src.model.word import Word
from src.wordle import Wordle


def get_first_word_scores():
    wordle = Wordle.load_from_file()
    words_with_scores = File.read_csv(path=Path("data/first_word_scores.csv"))
    processed_words = [x["word"] for x in words_with_scores]
    for allowed_word in tqdm(wordle.allowed_words, desc="Calculating scores"):
        if allowed_word.__str__() in processed_words:
            continue
        processed_words.append(allowed_word.__str__())
        words_with_scores.append(
            {
                "word": allowed_word.__str__(),
                "score": wordle.calculate_score(allowed_word),
            }
        )
    File.write_csv(
        contents=sorted(words_with_scores, key=lambda x: -1 * float(x["score"])),
        path=Path("data/first_word_scores.csv"),
    )


def get_best_next_words():
    best_next_words = File.read_csv(path=Path("data/best_next_words.csv"))
    processed_words = [x["guess_word"] for x in best_next_words]
    for game_round in range(0, 7):
        print(f"GAME ROUND {game_round}")
        for item in [x for x in best_next_words if int(x["round"]) == game_round - 1]:
            previous_guess_words = []
            if item["guess_word"]:
                previous_guess_words = [
                    GuessWord.from_string(x) for x in item["guess_word"].split(";")
                ]
            wordle = Wordle.load_from_file()
            for guess_word in previous_guess_words:
                wordle.remove_wrong_words(guess_word)

            if len(wordle.possible_words) == 1:
                continue

            guess_words = set()
            for possible_word in wordle.possible_words:
                guess_words.add(
                    GuessWord.calculate(
                        correct=possible_word,
                        guess=Word.from_string(item["best_next_word"]),
                    )
                )
            for guess_word in tqdm(guess_words, desc="Calculating scores"):
                guess_word_str = ";".join(
                    [x.__str__() for x in previous_guess_words + [guess_word]]
                )
                if guess_word_str in processed_words:
                    continue

                wordle_copy = deepcopy(wordle)
                wordle_copy.remove_wrong_words(guess_word)
                if len(wordle_copy.possible_words) <= 2:
                    allowed_words_sorted = wordle_copy.possible_words
                else:
                    allowed_words_sorted = wordle_copy.get_allowed_words_sorted()
                best_next_words.append(
                    {
                        "round": game_round,
                        "guess_word": guess_word_str,
                        "best_next_word": allowed_words_sorted[0].__str__(),
                        "no_of_possibilities": len(wordle_copy.possible_words),
                    }
                )
                processed_words.append(guess_word_str)
                best_next_words = sorted(best_next_words, key=lambda x: x["guess_word"])
                File.write_csv(
                    contents=best_next_words, path=Path("data/best_next_words.csv")
                )


if __name__ == "__main__":
    get_first_word_scores()
    get_best_next_words()

    # TODO: what if you map all the guesses in which you can get the correct word in 6 times?
