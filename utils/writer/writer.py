from abc import ABC, abstractmethod
from typing import List

class Writer(ABC):
    @abstractmethod
    def write(self, file_path: str, data: List[List[str]]):
        pass
