from dataclasses import dataclass
from pathlib import Path
from typing import Type

from src.game.game import Game
from src.game.quordle import Quordle
from src.game.basic import Basic


@dataclass
class Config:
    data_dir: Path
    word_length: int
    game_class: Type[Game]

    def get_game(self) -> Game:
        return self.game_class.load_from_file(self.data_dir)


class Configs:
    WORDLE = Config(data_dir=Path("data/wordle"), word_length=5, game_class=Basic)
    NERDLE = Config(data_dir=Path("data/nerdle"), word_length=8, game_class=Basic)
    QUORDLE = Config(data_dir=Path("data/quordle"), word_length=5, game_class=Quordle)
