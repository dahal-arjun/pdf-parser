from typing import List
import pdfplumber

from utils.parser.parser import Parser


class PDFParser(Parser):
    
    def parse(self, file_path: str = None) -> List[List[str]]:
        try:
            with pdfplumber.open(file_path) as pdf:
                results = [page.extract_table() for page in pdf.pages if page is not None]
                return results
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")