from abc import ABC, abstractmethod
from typing import List

class Parser(ABC):
    """
    Abstract class for parsing files.
    Right now, it only supports pdf as per the requirement.
    It will support other file types in the future.
    """
    @abstractmethod
    def parse(self, file_path: str = None) -> List[List[str]]:
        """
        Parse the file and return the content as a list of strings.
        """
        pass
