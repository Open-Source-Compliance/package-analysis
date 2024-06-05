from oss.utils.command_line_parser import parser
from oss.file_operation.readme_parser import ReadmeParser
from oss.file_operation.spdx_parser import SpdxParser
from oss.file_operation.txt_parser import TxtParser


class FileAnalyzer:
    """
    """
    def __init__(self):
        self.new_file_name = ""
        self.parser = None
        self.packet_name = ""
        self.packet_version = ""

    @classmethod
    def create (cls, file_path: str, dictionary_replacement_texts: dict, ml_list_replacement_texts: dict):
        instance = FileAnalyzer()
        instance.find_parser(file_path, dictionary_replacement_texts, ml_list_replacement_texts)
        instance.file_name = instance.parser.new_file_name_provider()
        instance.packet_name = instance.parser.get_packet_name()
        instance.packet_version = instance.parser.get_packet_version()
        instance.modified_file = instance.parser.parse_modify_file()
        return instance

    def get_final_file(self):
        return self.final_file

    def set_final_file(self, final_file: str):
        self.final_file = final_file

    def get_packet_version(self):
        return self.packet_version

    def set_packet_version(self, packet_version: str):
        self.packet_version = packet_version

    def get_packet_name(self):
        return self.packet_name

    def set_packet_name(self, packet_name: str):
        self.packet_name = packet_name

    def get_new_file_name(self):
        return self.new_file_name

    def set_new_file_name(self, new_file_name: str):
        self.new_file_name = new_file_name

    def find_parser(self, file_path, dictionary_replacement_texts, ml_list_replacement_texts):
        input_splited = file_path.split("/")
        if ".txt" in  input_splited[-1]:
            self.parser = TxtParser(file_path, dictionary_replacement_texts, ml_list_replacement_texts)
        elif ".spdx" in input_splited[-1]:
            self.parser = SpdxParser(file_path, dictionary_replacement_texts, ml_list_replacement_texts)
        else:
            self.parser = ReadmeParser(file_path, dictionary_replacement_texts, ml_list_replacement_texts)

    file_name = property(get_new_file_name, set_new_file_name)
    package_name = property(get_packet_name, set_packet_name)
    package_version = property(get_packet_version, set_packet_version)
    modified_file = property(get_final_file, set_final_file)
