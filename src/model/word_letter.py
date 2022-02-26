from dataclasses import dataclass

from src.model.letter import Letter


@dataclass
class WordLetter:
    index: int
    letter: Letter

    def __hash__(self) -> int:
        return hash(self.letter)

    def __eq__(self, other) -> bool:
        if not isinstance(other, WordLetter):
            return False
        return self.__hash__() == other.__hash__()
