from typing import List

from rich import print as print_rich
from tqdm import tqdm

from src.cache.cache import Cache
from src.config import Config
from src.game.basic import Basic
from src.model.word import Word


class FirstWordScores(Cache):
    file_name = "elimination_scores.csv"
    desc = "Calculating elimination scores"

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self):
        game = self.config.get_game()
        assert isinstance(game, Basic)

        for allowed_word in tqdm(self.get_words_to_process(), desc=self.desc):
            self.add_result(
                {
                    "word": str(allowed_word),
                    "score": game.calculate_score(allowed_word),
                }
            )

        print_rich("[green bold]Finished calculating elimination scores.\n\n")

    def sort_data(self):
        self.results.sort(key=lambda x: -1 * float(x["score"]))

    def get_words_to_process(self) -> List[Word]:
        distributions = self.read_data("distribution_scores.csv")
        allowed_words = [Word.from_string(x["word"]) for x in distributions][:5]
        return [x for x in allowed_words if self.word_should_be_processed(x)]

    def word_should_be_processed(self, word: Word) -> bool:
        return str(word) not in self.processed
