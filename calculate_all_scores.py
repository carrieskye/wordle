import argparse
from collections import defaultdict
from copy import deepcopy
from itertools import combinations
from pathlib import Path
from typing import List

from skye_comlib.utils.file import File
from tqdm import tqdm

from src.model.game import Game
from src.model.guess_word import GuessWord
from src.model.word import Word
from src.wordle import Wordle


def get_colour_combinations(length: int) -> List[str]:
    colour_combinations = []
    permutation_input = ""
    for digit in range(0, 3):
        permutation_input += "".join([str(digit)] * length)
    for combination in list(combinations(permutation_input, length)):
        colour_combinations.append("".join(combination))
    colour_combinations = list(set(colour_combinations))
    return sorted(colour_combinations, key=lambda x: (-x.count("0"), -x.count("1"), x))


def get_guess_word_distributions(game: Game):
    base_path = Path(f"data/{game.value}")
    try:
        distributions = File.read_csv(base_path / "guess_word_distributions.csv")
    except FileNotFoundError:
        distributions = []

    wordle = Wordle.load_from_file(game)
    colour_combinations = get_colour_combinations(5 if game == Game.WORDLE else 8)
    processed_words = [x["word"] for x in distributions]

    for allowed_word in tqdm(wordle.allowed_words, desc="Preparing"):
        letter_count = len(allowed_word.get_letters())
        if allowed_word.__str__() in processed_words or letter_count < len(
            allowed_word.__str__()
        ):
            continue
        processed_words.append(allowed_word.__str__())
        guess_words = defaultdict(int)
        for k, v in wordle.get_guess_word_distribution(allowed_word).items():
            colour_code = "".join(sorted(list(k.__str__().split(" ")[1])))
            guess_words[colour_code] += v
        distribution = {"word": allowed_word.__str__()}
        score = 0
        for colour_combination in colour_combinations:
            count = guess_words.get(colour_combination, 0)
            distribution[colour_combination] = count
            score += count * colour_combination.count("1")
            score += count * 2 * colour_combination.count("2")
        distribution["score"] = score
        distributions.append(distribution)
        distributions = sorted(distributions, key=lambda x: -1 * x["score"])
        File.write_csv(distributions, base_path / "guess_word_distributions.csv")


def get_first_word_scores(game: Game):
    base_path = Path(f"data/{game.value}")

    try:
        words_with_scores = File.read_csv(base_path / "first_word_scores.csv")
    except FileNotFoundError:
        words_with_scores = []

    wordle = Wordle.load_from_file(game)
    distributions = File.read_csv(base_path / "guess_word_distributions.csv")
    allowed_words = [Word.from_string(x["word"]) for x in distributions][:5]
    processed_words = [x["word"] for x in words_with_scores]

    for allowed_word in tqdm(allowed_words, desc="Calculating scores"):
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
            path=Path(f"data/{game.value}/first_word_scores.csv"),
        )


def get_best_next_words(game: Game):
    base_path = Path(f"data/{game.value}")

    try:
        best_next_words = File.read_csv(base_path / "best_next_words.csv")
    except FileNotFoundError:
        best_next_words = []

    processed_words = [x["guess_word"] for x in best_next_words]
    if not processed_words:
        first_word = File.read_csv(Path(f"data/{game.value}/first_word_scores.csv"))[0]
        best_next_words.append(
            {
                "round": 0,
                "guess_word": "",
                "best_next_word": first_word["word"],
                "no_of_possibilities": len(Wordle.load_from_file(game).possible_words),
            }
        )
    for game_round in range(0, 7):
        print(f"GAME ROUND {game_round}")
        for item in [x for x in best_next_words if int(x["round"]) == game_round - 1]:
            previous_guess_words = []
            if item["guess_word"]:
                previous_guess_words = [
                    GuessWord.from_string(x) for x in item["guess_word"].split(";")
                ]
            wordle = Wordle.load_from_file(game)
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
            guess_words = [
                x
                for x in guess_words
                if ";".join([y.__str__() for y in previous_guess_words + [x]])
                not in processed_words
            ]
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
                    contents=best_next_words,
                    path=Path(f"data/{game.value}/best_next_words.csv"),
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    FUNCTION_MAP = {"wordle": Game.WORDLE, "nerdle": Game.NERDLE}
    parser.add_argument("task", choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    get_guess_word_distributions(FUNCTION_MAP[args.task])
    get_first_word_scores(FUNCTION_MAP[args.task])
    get_best_next_words(FUNCTION_MAP[args.task])

    # TODO: what if you map all the guesses in which you can get the correct word in 6 times?
