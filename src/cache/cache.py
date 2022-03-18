from abc import ABC, abstractmethod

from skye_comlib.utils.file import File

from src.config import Config


class Cache(ABC):
    file_name: str

    def __init__(self, config: Config):
        self.config = config
        self.data_dir = config.data_dir
        self.results = self.read_data(self.file_name)
        self.processed = [x["word"] for x in self.results]

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def sort_data(self):
        pass

    def add_result(self, result: dict):
        self.results.append(result)
        self.processed.append(result["word"])
        self.export_data()

    def read_data(self, file_name: str) -> list:
        try:
            return File.read_csv(self.data_dir / file_name)
        except FileNotFoundError:
            return []

    def export_data(self):
        self.sort_data()
        File.write_csv(self.results, self.data_dir / self.file_name)
