from typing import List
import csv

from utils.writer.writer import Writer


class CSVWriter(Writer):
    def write(self, file_path: str, data: List[List[str]]):
        try:
            with open(file_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        except Exception as e:
           raise ValueError(f"Error writing CSV: {str(e)}")