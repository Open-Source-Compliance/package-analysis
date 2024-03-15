import os
from oss.file_operation.read_regex_replacement import ReadRegexReplacement
from oss.file_operation.operation_case import OperationCase
from oss.file_operation.folder_reader import FolderReader
from oss.file_operation.file_name_parser import FileNameParser


class FilesGeneratorException(Exception):
    pass


class MissingTextFileException(FilesGeneratorException):
    pass


class MissingSpdxException(FilesGeneratorException):
    pass


class MissingOutputPathException(FilesGeneratorException):
    pass


class FilesGenerator:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.final_file_path = ""
    
    def generate_files(self):
        result_txt = self.generate_txt_files()
        result_spdx = self.generate_spdx_files()

        if not result_txt:
            raise MissingTextFileException(f"ReadMe_OSS_XXXXX.txt is missing in {self.input_path} folder")

        if not result_spdx:
            raise MissingSpdxException(f"SPDX2TV_XXXX.spdx is missing in {self.input_path} folder")

    @classmethod
    def create (cls, input_path: str, output_path: str):
        instance = FilesGenerator(input_path, output_path)
        instance.generate_files()
        return instance
    
    def spdx_to_json(self, packet_name):
        generated_spdx_json = self.output_path + packet_name + ".spdx.json"
        command = f"pyspdxtools -i {self.final_file_path} -o {generated_spdx_json}"
        os.system(command)
        print(">>>>> Generateed Document name: ",  generated_spdx_json)

    def spdx_to_yaml(self, packet_name):
        generated_spdx_yaml = self.output_path + packet_name + ".spdx.yaml"
        command = f"pyspdxtools -i {self.final_file_path} -o {generated_spdx_yaml}"
        os.system(command)
        print(">>>>> Generateed Document name: ",  generated_spdx_yaml)

    def spdx_to_rdf_xml(self, packet_name):
        generated_spdx_rdf_xml = self.output_path + packet_name + ".spdx.rdf.xml"
        command = f"pyspdxtools -i {self.final_file_path} -o {generated_spdx_rdf_xml}"
        os.system(command)
        print(">>>>> Generateed Document name: ",  generated_spdx_rdf_xml)
    
    def save_new_file(self, final_file, file_name):
        if self.output_path:
            self.final_file_path = self.output_path + file_name
        if not self.final_file_path:
            raise MissingOutputPathException("Final output path is empty! It can not generate the new file")
        with open(self.final_file_path, "w") as file:
            for line in final_file:
                file.write(line)
    
    def generate_txt_files(self):
        txt_files = vars(FolderReader(self.input_path, OperationCase.txt))['files']
        if not txt_files:
            return False
        dictionary_replacement_texts = vars(ReadRegexReplacement(OperationCase.txt))['data']
        for txt_file in txt_files:
            file_parser = FileNameParser.create(txt_file, dictionary_replacement_texts)
            self.save_new_file(file_parser.modified_file, file_parser.file_name)
            print(">>>>> Generateed Document name: ",  file_parser.file_name)
        return True

    def generate_spdx_files(self):
        spdx_files = vars(FolderReader(self.input_path, OperationCase.spdx))['files']
        if not spdx_files:
            return False
        dictionary_replacement_texts = vars(ReadRegexReplacement(OperationCase.spdx))['data']
        for spdx_file in spdx_files:
            file_parser = FileNameParser.create(spdx_file, dictionary_replacement_texts)
            self.save_new_file(file_parser.modified_file, file_parser.file_name)
            print(">>>>> Generateed Document name: ",  file_parser.file_name)

            self.spdx_to_json(file_parser.package_name)
            self.spdx_to_yaml(file_parser.package_name)
            self.spdx_to_rdf_xml(file_parser.package_name)
        return True