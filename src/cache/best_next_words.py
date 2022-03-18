from copy import deepcopy

from tqdm import tqdm

from src.cache.cache import Cache
from src.config import Config
from src.model.guess_word import GuessWord
from src.model.word import Word


class BestNextWords(Cache):
    file_name = "best_next_words.csv"
    desc = "Calculating best next words"

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self):
        if not self.processed:
            first_word = self.read_data("first_word_scores.csv")[0]
            self.results.append(
                {
                    "round": 0,
                    "word": "",
                    "best_next_word": first_word["word"],
                    "no_of_possibilities": len(self.config.get_game().possible_words),
                }
            )
        for game_round in range(0, 7):
            print(f"GAME ROUND {game_round}")
            for item in [x for x in self.results if int(x["round"]) == game_round - 1]:
                no_of_possibilities = int(item["no_of_possibilities"])
                if no_of_possibilities == 1:
                    continue
                no_of_processed_possibilities = sum(
                    [
                        int(x["no_of_possibilities"])
                        for x in self.results
                        if x["word"].startswith(item["word"])
                        and int(x["round"]) > int(item["round"])
                    ]
                )
                if no_of_possibilities <= no_of_processed_possibilities:
                    continue

                previous_guess_words = []
                if item["word"]:
                    previous_guess_words = [
                        GuessWord.from_string(x) for x in item["word"].split(";")
                    ]
                game = self.config.get_game()
                for guess_word in previous_guess_words:
                    game.remove_wrong_words(guess_word)

                if len(game.possible_words) == 1:
                    continue

                guess_words = set()
                for possible_word in game.possible_words:
                    guess_words.add(
                        GuessWord.calculate(
                            correct=possible_word,
                            guess=Word.from_string(item["best_next_word"]),
                        )
                    )
                guess_words = [
                    x
                    for x in guess_words
                    if ";".join([str(y) for y in previous_guess_words + [x]])
                    not in self.processed
                ]
                for guess_word in tqdm(guess_words, desc=self.desc):
                    guess_word_str = ";".join(
                        [str(x) for x in previous_guess_words + [guess_word]]
                    )
                    if guess_word_str in self.processed:
                        continue

                    game_copy = deepcopy(game)
                    game_copy.remove_wrong_words(guess_word)
                    if len(game_copy.possible_words) <= 2:
                        allowed_words_sorted = game_copy.possible_words
                    else:
                        allowed_words_sorted = game_copy.get_allowed_words_sorted()
                    self.results.append(
                        {
                            "round": game_round,
                            "word": guess_word_str,
                            "best_next_word": str(allowed_words_sorted[0]),
                            "no_of_possibilities": len(game_copy.possible_words),
                        }
                    )
                    self.processed.append(guess_word_str)
                    self.export_data()

    def sort_data(self):
        self.results.sort(key=lambda x: x["word"])
