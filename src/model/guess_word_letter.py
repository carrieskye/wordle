from dataclasses import dataclass

from src.model.colour import Colour
from src.model.word_letter import WordLetter


@dataclass
class GuessWordLetter:
    word_letter: WordLetter
    colour: Colour

    def get_colour_string(self) -> str:
        return (
            f"[bold {self.colour.name.lower().replace('gray', '#727272')}]"
            f"{self.word_letter.letter.value}[not bold]"
        )
