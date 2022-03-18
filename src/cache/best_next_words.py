from copy import deepcopy
from typing import List

from tqdm import tqdm

from src.cache.cache import Cache
from src.config import Config
from src.game.basic import Basic
from src.model.guess_word import GuessWord
from src.model.word import Word


class BestNextWords(Cache):
    file_name = "best_next_words.csv"
    desc = "Calculating best next words"

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self):
        self.add_first_result()

        for game_round in tqdm(range(0, 7), desc=self.desc):
            for item in tqdm(
                self.get_words_to_process(game_round),
                desc=f"Game round {game_round}",
                leave=False,
            ):
                previous_guess_words = []
                if item["word"]:
                    previous_guess_words = [
                        GuessWord.from_string(x) for x in item["word"].split(";")
                    ]
                game = self.config.get_game()
                assert isinstance(game, Basic)
                for guess_word in previous_guess_words:
                    game.remove_wrong_words(guess_word)

                guess_words = [
                    x
                    for x in game.get_guess_words(
                        Word.from_string(item["best_next_word"])
                    )
                    if ";".join([str(y) for y in previous_guess_words + [x]])
                    not in self.processed
                ]
                for guess_word in tqdm(
                    guess_words, desc=f'"{item["word"]}"', leave=False
                ):
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
                        allowed_words_sorted = game_copy.get_allowed_words_sorted(
                            desc=str(guess_word)
                        )

                    self.add_result(
                        {
                            "round": game_round,
                            "word": guess_word_str,
                            "best_next_word": str(allowed_words_sorted[0]),
                            "no_of_possibilities": game_copy.get_number_of_possibilities(),
                        }
                    )

    def sort_data(self):
        self.results.sort(key=lambda x: x["word"])

    def add_first_result(self):
        if not self.processed:
            first_word = self.read_data("elimination_scores.csv")[0]
            self.add_result(
                {
                    "round": 0,
                    "word": "",
                    "best_next_word": first_word["word"],
                    "no_of_possibilities": self.config.get_game().get_number_of_possibilities(),
                }
            )

    def get_words_to_process(self, game_round: int) -> List[dict]:
        return [x for x in self.results if self.word_should_be_processed(game_round, x)]

    def word_should_be_processed(self, game_round: int, item: dict) -> bool:
        if int(item["round"]) != game_round - 1:
            return False

        no_of_possibilities = int(item["no_of_possibilities"])
        if no_of_possibilities == 1:
            return False

        no_of_processed_possibilities = sum(
            [int(x["no_of_possibilities"]) for x in self.get_direct_sub_results(item)]
        )
        if no_of_possibilities <= no_of_processed_possibilities:
            return False

        return True

    def get_direct_sub_results(self, item: dict) -> List[dict]:
        return [
            x
            for x in self.results
            if x["word"].startswith(item["word"])
            and int(x["round"]) == int(item["round"]) + 1
        ]

    def lookup(self, word: str) -> Word:
        for result in self.results:
            if result["word"] == word:
                return Word.from_string(result["best_next_word"])
