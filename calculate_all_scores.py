from random import shuffle

from skye_comlib.utils.file import File
from tqdm import tqdm

from src.model.guess_word import GuessWord
from src.model.word import Word
from src.wordle import Wordle


def primary_scores():
    wordle = Wordle.load_from_file()
    words_with_scores = File.read_json("data/words_with_scores.json")
    shuffle(wordle.allowed_words)
    for allowed_word in tqdm(wordle.allowed_words, desc="Calculating scores"):
        if allowed_word.__str__() in words_with_scores:
            continue
        score = wordle.calculate_score(allowed_word)
        words_with_scores = File.read_json("data/words_with_scores.json")
        words_with_scores[allowed_word.__str__()] = score
        words_with_scores = {
            x[0]: x[1]
            for x in sorted(words_with_scores.items(), key=lambda x: x[1], reverse=True)
        }
        File.write_json(words_with_scores, "data/words_with_scores.json")


def secondary_scores():
    wordle = Wordle.load_from_file()
    guess_words = set()
    for possible_word in wordle.possible_words:
        guess_words.add(
            GuessWord.calculate(correct=possible_word, guess=Word.from_string("raise"))
        )

    words_with_scores = File.read_json("data/words_with_best_next_word.json")
    for guess_word in tqdm(guess_words, desc="Calculating scores"):
        if guess_word.__str__() in words_with_scores:
            continue
        wordle = Wordle.load_from_file()
        wordle.remove_wrong_words(guess_word)
        allowed_words_sorted = wordle.get_allowed_words_sorted()
        words_with_scores[guess_word.__str__()] = str(allowed_words_sorted[0])
        words_with_scores = {
            x[0]: x[1] for x in sorted(words_with_scores.items(), key=lambda x: x[0])
        }
        File.write_json(words_with_scores, "data/words_with_best_next_word.json")


if __name__ == "__main__":
    primary_scores()
    # secondary_scores()
