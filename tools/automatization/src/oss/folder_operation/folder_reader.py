import os
from oss.types.operation_case import OperationCase


class FolderReaderException(Exception):
    pass


class UnknownOperationCase(FolderReaderException):
    pass


class FolderReader:
    def __init__(self, input_path: str, operation_case):
        self.input_path = input_path
        self.files = []
        self.find_files(operation_case)

    def read_txt_files(self):
        txt_files = []
        for file in os.listdir(f"{self.input_path}/"):
            if file.endswith(".txt"):
                print("---------------------------------------------------------------------------\n")
                print(">>>>> Preparing Document: ", os.path.join(self.input_path, file))
                txt_files.append(os.path.join(self.input_path, file))
        return txt_files

    def read_spdx_files(self):
        spdx_files = []
        for file in os.listdir(f"{self.input_path}/"):
            if file.endswith(".spdx"):
                print("---------------------------------------------------------------------------\n")
                print(">>>>> Preparing Document: ", os.path.join(self.input_path, file))
                spdx_files.append(os.path.join(self.input_path, file))
        return spdx_files

    def find_files(self, operation_case):
        if operation_case == OperationCase.txt:
            self.files = self.read_txt_files()
        elif operation_case == OperationCase.spdx:
            self.files = self.read_spdx_files()
        else:
            raise UnknownOperationCase(f"{operation_case} is not known. Known Operations are either txt or spdx.")
