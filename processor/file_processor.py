from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import uuid
import os

"""
FileProcessor is a class that processes files and returns the status of the task.
It uses a ThreadPoolExecutor to process the files in parallel.
"""
class FileProcessor:
    def __init__(self, parser, writer):
        self.parser = parser
        self.writer = writer
        self.executor = ThreadPoolExecutor()
        self.task_status: Dict[str, str] = {}
        self.lock = Lock()

    def __generate_id(self) -> str:
        return str(uuid.uuid4())

    def process_file(self, file_path: str) -> str:
        task_id = self.__generate_id()
        task_folder = os.path.join(os.getenv("TASK_FOLDER"), task_id)
        os.makedirs(task_folder, exist_ok=True)

        self.task_status[task_id] = "in-progress"
        self.executor.submit(self.__process_task, file_path, task_folder, task_id)
        return task_id

    def __process_task(self, file_path: str, task_folder: str, task_id: str):
        try:
            table_data = self.parser.parse(file_path)
            if table_data:
                output_csv = os.path.join(task_folder, "output.csv")
                self.writer.write(output_csv, table_data)
                self.task_status[task_id] = "completed"
            else:
                raise ValueError("No tables found in the PDF.")
        except Exception as e:
            error_file = os.path.join(task_folder, "error.txt")
            with open(error_file, "w") as f:
                f.write(str(e))
            self.task_status[task_id] = "failed"

    def get_status(self, task_id: str) -> Optional[str]:
        with self.lock:
            return self.task_status.get(task_id, None)

    def close(self):
        self.executor.shutdown(wait=True)