import re
from copy import deepcopy
from oss.utils.command_line_parser import parser
from abc import ABC, abstractmethod


Packet_Version_Pattern = "\-[0-9]+.*[0-9]$"


parser.add_argument(
    "-pn",
    "--package_name",
    required=False,
    type=str,
    help="name of the package(default: it will be parsed from the name of the file)",
)
parser.add_argument(
    "-pv",
    "--package_version",
    required=False,
    type=str,
    help="version of the package(default: it will be parsed from the name of the file)",
)
parser.add_argument(
    "-cn",
    "--creator_name",
    required=True,
    type=str,
    help="name of the creator (default value is %(default)s)",
    default="XXXX",
)


class FileParserException(Exception):
    pass


class MissingConfigPackageVersionException(FileParserException):
    pass


class MissingConfigPackageNameException(FileParserException):
    pass


class UnknownVersionException(FileParserException):
    pass


class FileParser(ABC):
    """This is a simple abstract class for all parser objects"""

    def __init__(
        self,
        file_path=None,
        dictionary_replacement_texts=None,
        ml_list_replacement_texts=None,
    ):
        self.file_path = file_path
        self.file_name = self.file_path.split("/")[-1]
        self.dictionary_replacement_texts = dictionary_replacement_texts
        self.ml_list_replacement_texts = ml_list_replacement_texts
        self.packet_name = None
        self.packet_version = None

    @abstractmethod
    def new_file_name_provider(self):
        raise NotImplementedError()

    @abstractmethod
    def post_processing_operation(self, lines):
        raise NotImplementedError()

    @abstractmethod
    def final_processing(self, lines):
        raise NotImplementedError()

    def parse_modify_file(self):
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as file1:
            lines = file1.readlines()
            return self.adjust_file(lines)

    def adjust_file(self, lines):
        final = self.post_processing_operation(lines)
        return self.final_processing(final)

    def get_packet_name(self):
        return self.packet_name

    def get_packet_version(self):
        return self.packet_version

    def remove_fixed_begining(self, file_name, fixed_parts):
        for fixed_part in fixed_parts:
            if fixed_part in file_name:
                _, file_name = file_name.split(fixed_part)
        return file_name

    def find_replace(self, find_pattern, replace_text, input_line):
        return re.sub(find_pattern, replace_text, input_line)

    def check_regular_expression(self, file, given_reg):
        reg_ex_result = re.findall(given_reg, file, re.MULTILINE)
        if reg_ex_result:
            print("Regular expression match: ", reg_ex_result)
            return True

    def apply_text_replacement(self, line):
        new_line = None
        if self.dictionary_replacement_texts:
            for key, value in self.dictionary_replacement_texts.items():
                if self.check_regular_expression(line, key):
                    new_line = self.find_replace(key, value, line)
                    print("Replaced Text: ", new_line)
        return new_line

    def create_substitute_text(
        self, file, given_reg, replacement_part, substitute_part
    ):
        reg_ex_result = re.findall(given_reg, file, re.MULTILINE)
        if reg_ex_result:
            print("Regular expression match: ", reg_ex_result)
            substitute = deepcopy(reg_ex_result[0])
            print("substitute: ", substitute)
            final_substitute = substitute.replace(replacement_part, substitute_part)
            return file.replace(substitute, final_substitute)

    def remove_fixed_ending(self, file_name, fixed_parts):
        for fixed_part in fixed_parts:
            if fixed_part in file_name:
                file_name, _ = file_name.split(fixed_part)
        return file_name

    def check_package_name_version(self):
        if parser["package_name"]:
            if parser["package_version"]:
                return True
            else:
                raise MissingConfigPackageVersionException(
                    "Package name is provided in config. However, package version is missing"
                )
        if parser["package_version"]:
            if not parser["package_name"]:
                raise MissingConfigPackageNameException(
                    "Package version is provided in config. However, package name is missing"
                )

    def find_package_name_version(self, file_name):
        if self.check_package_name_version():
            return parser["package_name"], parser["package_version"]
        file_name = self.remove_fixed_begining(file_name, ["ReadMe_OSS_", "SPDX2TV_"])

        pattern = [".zip", ".tar.xz", ".tar.gz"]
        file_name = self.remove_fixed_ending(file_name, pattern)

        ending = [".txt", ".spdx"]
        file_name = self.remove_fixed_ending(file_name, ending)

        # parse the string to find the version and name
        packet_name_and_version = self.create_substitute_text(
            file_name, Packet_Version_Pattern, "-", " "
        )
        if packet_name_and_version:
            print(packet_name_and_version.split(" "))
            return packet_name_and_version.split(" ")
        raise UnknownVersionException(
            f"can not parse version from {file_name}. Please provide package_name and package_version in configuration"
        )

    def apply_ml_text_replacement(self, lines):
        original_lines = lines
        if self.ml_list_replacement_texts:
            for el in self.ml_list_replacement_texts:
                new_lines = []

                found_start = False
                for line in original_lines:
                    if self.check_regular_expression(line, el["start"]):
                        found_start = True
                        continue
                    if found_start:
                        if self.check_regular_expression(line, el["end"]):
                            new_lines.append(el["replace"])
                            print(">>>>>>>>   Multiple Lines replacement")
                            print("Started Text: ", el["start"])
                            print("Replaced Text: ", el["replace"])
                            print("ended Text: ", el["end"])
                            found_start = False
                        continue
                    new_lines.append(line)
                original_lines = new_lines
        return new_lines
