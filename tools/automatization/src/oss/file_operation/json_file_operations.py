import json
import os
from oss.file_operation.file_operations import FileOperations


class JsonFileOperations(FileOperations):
    """ This is a simple parser class that we can use for json operations"""
    def __init__(self, file_path=None):
        FileOperations.__init__(self, file_path)

    def read_file(self):
        if os.path.exists(self.file_path):
            if os.stat(self.file_path).st_size != 0:
                with open(self.file_path, encoding='utf-8', errors='ignore') as f:
                    data = json.load(f)
                    if data:
                        return data
        return []

    def write_file(self, config):
        # Writing to sample.json
        with open(self.file_path, 'w', encoding='utf-8', errors='ignore') as file:
            file.seek(0)
            json.dump(config, file,  indent=4)
            file.truncate()