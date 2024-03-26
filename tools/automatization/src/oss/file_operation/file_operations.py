
from abc import ABC, abstractmethod

class FileOperations(ABC):
    """ This is a simple abstract class for file operations"""
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_path.touch(exist_ok=True)

    @abstractmethod
    def read_file(self):
        raise NotImplementedError()

    @abstractmethod
    def write_file(self, config):
        raise NotImplementedError()