from dataclasses import dataclass
from pathlib import Path
from typing import Type

from src.game import Game
from src.quordle import Quordle
from src.wordle import Wordle


@dataclass
class Config:
    data_dir: Path
    game_class: Type[Game]


class Configs:
    WORDLE = Config(data_dir=Path("data/wordle"), game_class=Wordle)
    NERDLE = Config(data_dir=Path("data/nerdle"), game_class=Wordle)
    QUORDLE = Config(data_dir=Path("data/quordle"), game_class=Quordle)
