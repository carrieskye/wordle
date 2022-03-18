from typing import List

from tqdm import tqdm

from src.cache.cache import Cache
from src.config import Config
from src.game.game import Game
from src.model.word import Word


class GuessWordDistribution(Cache):
    file_name = "distribution_scores.csv"
    desc = "Calculating guess word distribution scores"

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self):
        game = self.config.get_game()

        for allowed_word in tqdm(self.get_words_to_process(game), desc=self.desc):
            self.processed.append(str(allowed_word))

            score = 0
            for k, v in game.get_guess_word_distribution(allowed_word).items():
                colour_code = str(k).split()[1]
                score += v * colour_code.count("1")
                score += v * 2 * colour_code.count("2")
            self.results.append({"word": str(allowed_word), "score": score})

            self.export_data()

    def sort_data(self):
        self.results.sort(key=lambda x: -1 * int(x["score"]))

    def get_words_to_process(self, game: Game) -> List[Word]:
        return [x for x in game.allowed_words if self.word_should_be_processed(x)]

    def word_should_be_processed(self, word: Word) -> bool:
        if len(word.get_letters()) < len(str(word)):
            return False
        if str(word) in self.processed:
            return False
        return True
