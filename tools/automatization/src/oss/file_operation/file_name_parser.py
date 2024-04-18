import re
import textwrap
from copy import deepcopy
from oss.utils.command_line_parser import parser
from packageurl.contrib import url2purl


Packet_Version_Pattern = '\-[0-9]+.*[0-9]$'
License_Name_Pattern_SPDX = '^LicenseName:.*\n$'

class FileNameParserException(Exception):
    pass


class MissingConfigPackageVersionException(FileNameParserException):
    pass


class MissingConfigPackageNameException(FileNameParserException):
    pass


class UnknownVersionException(FileNameParserException):
    pass


parser.add_argument('-pn', '--package_name', required=False, type=str, help='name of the package(default: it will be parsed from the name of the file)')
parser.add_argument('-pv', '--package_version', required=False, type=str, help='version of the package(default: it will be parsed from the name of the file)')
parser.add_argument('-cn', '--creator_name', required=True, type=str, help='name of the creator (default value is %(default)s)' , default= "XXXX")
parser.add_argument('-dl', '--download_link', required=False, type=str, help='The download link that it should be written in readme.')
parser.add_argument('-r', '--reviewer', required=False, type=str, help='The reviewer that it should be written in readme.')


class FileNameParser:
    """
    """
    def __init__(self, file_path: str, dictionary_replacement_texts: dict, ml_list_replacement_texts: dict):
        self.file_path = file_path
        self.dictionary_replacement_texts = dictionary_replacement_texts
        self.ml_list_replacement_texts = ml_list_replacement_texts
        self.new_file_name = []
        self.original_file_name = ""
        self.original_packet_name = ""
        self.packet_name = ""
        self.packet_version = ""
        self.final_file = None
        self.license_names =  []

    @classmethod
    def create (cls, file_path: str, dictionary_replacement_texts: dict, ml_list_replacement_texts: dict):
        instance = FileNameParser(file_path, dictionary_replacement_texts, ml_list_replacement_texts)
        new_file_name = instance.new_file_name_provider()
        instance.file_name = new_file_name
        instance.modified_file = instance.read_parse_file()
        return instance

    def get_final_file(self):
        return self.final_file

    def set_final_file(self, final_file: str):
        self.final_file = final_file
    
    def get_license_names(self):
        return self.license_names

    def set_license_names(self, license_name: str):
        self.license_names.append(license_name)

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

    def check_package_name_version(self):
        if parser["package_name"]:
            if parser["package_version"]:
                return True
            else:
                raise MissingConfigPackageVersionException("Package name is provided in config. However, package version is missing")
        if parser["package_version"]:
            if not parser["package_name"]:
                raise MissingConfigPackageNameException("Package version is provided in config. However, package name is missing")

    def remove_fixed_begining(self, file_name, fixed_part):
        if fixed_part in file_name:
            _, file_name = file_name.split(fixed_part)
        return file_name

    def remove_fixed_ending(self, file_name, fixed_part):
        if fixed_part in file_name:
            file_name, _ = file_name.split(fixed_part)
        return file_name

    def find_package_name_version(self, file_name):
        if self.check_package_name_version():
            return parser["package_name"], parser["package_version"]
        file_name = self.remove_fixed_begining(file_name, "ReadMe_OSS_" or "SPDX2TV_")

        pattern = ".zip" or ".tar.xz" or ".tar.gz"
        file_name = self.remove_fixed_ending(file_name, pattern)

        ending = ".txt" or ".spdx"
        file_name = self.remove_fixed_ending(file_name, ending)

        # parse the string to find the version and name
        substitute_text = self.create_substitute_text(file_name, Packet_Version_Pattern, "-", " ")
        if substitute_text:
                return substitute_text.split(" ")
        raise UnknownVersionException(f"can not parse version from {file_name}. Please provide package_name and package_version in configuration")
    
    def parse_txt_file_name(self, file_name):
        self.packet_name, self.packet_version = self.find_package_name_version(file_name)
        file_name = self.packet_name + "-" + self.packet_version + "-OSS-disclosure.txt"
        return file_name
    
    def parse_spdx_file_name(self, file_name):
        self.packet_name, self.packet_version = self.find_package_name_version(file_name)
        file_name = self.packet_name + "-" + self.packet_version + "-SPDX2TV.spdx"
        return file_name

    def remove_white_space(self, lines):
        three_element_before=""
        two_element_before=""
        one_element_before=""
        new_list = []
        for i in range(len(lines)):
            if i > 3:
                three_element_before = lines[i-3]
                two_element_before = lines[i-2]
                one_element_before = lines[i-1]
                if ((not three_element_before.strip()) and  (not two_element_before.strip()) and (not one_element_before.strip()) and ( not lines[i].strip())):
                    continue
            new_list.append(lines[i])
        return new_list

    def check_regular_expression(self, file, given_reg):
        reg_ex_result = re.findall(given_reg, file, re.MULTILINE)
        if reg_ex_result:
            print ("Regular expression match: ", reg_ex_result)
            return True
        
    def create_substitute_text(self, file, given_reg, replacement_part, substitute_part):
        reg_ex_result = re.findall(given_reg, file, re.MULTILINE)
        if reg_ex_result:
            print ("Regular expression match: ", reg_ex_result)
            substitute = deepcopy(reg_ex_result.group(0))
            final_substitute = substitute.replace(replacement_part, substitute_part)
            return file.replace(substitute, final_substitute)
    
    def apply_text_replacement(self, line):
        new_line = None
        if self.dictionary_replacement_texts:
            for key, value in  self.dictionary_replacement_texts.items():
                if self.check_regular_expression(line, key):
                    new_line = self.find_replace(key, value,line)
                    print ("Replaced Text: ", new_line)
        return new_line

    def apply_ml_text_replacement(self, lines):
        original_lines = lines
        if self.ml_list_replacement_texts:
            for el in  self.ml_list_replacement_texts:
                new_lines = []
                print (">>>>>>>>   Multiple Lines replacement")
                print ("Started Text: ", el["start"])
                print ("Replaced Text: ", el["replace"])
                print ("ended Text: ", el["end"])
                found_start = False
                for line in original_lines:
                    if self.check_regular_expression(line, el["start"]):
                        found_start = True
                        continue
                    if found_start:
                        if self.check_regular_expression(line, el["end"]):
                            new_lines.append(el["replace"])
                            found_start = False
                        continue
                    new_lines.append(line)
                original_lines = new_lines
        return new_lines
                   
    def find_replace(self, find_pattern, replace_text, input_line):
        return re.sub(find_pattern, replace_text, input_line)

    def generate_purl(self):
        if parser["download_link"]:
            package_purl = url2purl.get_purl(parser["download_link"])
            print ("PURL Link:   ", package_purl)
            if package_purl:
                return package_purl.to_string()

    def find_license_names(self, line):
        if self.check_regular_expression(line, License_Name_Pattern_SPDX):
            _, license_name = line.split(": ") # Find License name
            license_name, _ = license_name.split("\n") # Remove new line
            self.licenses_name = license_name

    def work_on_spdx_line_by_line(self, lines):
        new_line_list = []
        for line in lines:
            replacement_line = self.apply_text_replacement(line)
            if replacement_line is not None:
                if "[package]" in replacement_line:
                    replacement_line = replacement_line.replace("[package]", self.packet_name + " " + self.packet_version)
                if "[CreatorName]" in replacement_line:
                    replacement_line = replacement_line.replace("[CreatorName]", parser["creator_name"])
                new_line_list.append(replacement_line)
                continue
            new_line_list.append(line)
        return new_line_list

    def work_on_spdx_all_lines(self, lines):
        if not self.ml_list_replacement_texts:
            return lines
        lines = self.apply_ml_text_replacement(lines)
        for line in lines:
            self.find_license_names(line)
        print (">>>>> Found license_name: ", self.licenses_name)
        return lines

    def work_on_txt_line_by_line(self, lines):
        new_line_list = []
        for line in lines:
            replacement_line = self.apply_text_replacement(line)
            if replacement_line:
                new_line_list.append(replacement_line)
                continue
            if ("---------"  in line) or ("======" in line):
                trimm_line = textwrap.wrap(line, 80, break_long_words=True)
                new_line_list.append(trimm_line[0])
            else:
                new_lines = textwrap.fill(line, width=80)
                new_line_list.append(new_lines)
            new_line_list.append('\n')
        return self.remove_white_space(new_line_list)

    def work_on_txt_all_lines(self, lines):
        if not self.ml_list_replacement_texts:
            return lines
        lines = self.apply_ml_text_replacement(lines)
        return lines

    def work_on_readme_file(self, lines):
        new_line_list = []
        package_purl = self.generate_purl()
        for line in lines:
            replacement_line = line
            if "[CreatorName]" in line:
                replacement_line = line.replace("[CreatorName]", parser["creator_name"])
            elif "[DownloadLink]" in line:
                if parser["download_link"]:
                    replacement_line = line.replace("[DownloadLink]", parser["download_link"])
            elif "[PurlLink]" in line:
                if package_purl:
                    replacement_line = line.replace("[PurlLink]", package_purl)
            elif "[Reviewer]" in line:
                if parser["reviewer"]:
                    replacement_line = line.replace("[Reviewer]", parser["reviewer"])
            new_line_list.append(replacement_line)
        return new_line_list

    def read_parse_file(self):
        with open(self.file_path, "r") as file1:
            lines= file1.readlines()
            if ".txt" in self.file_path:
                final = self.work_on_txt_line_by_line(lines)
                final = self.work_on_txt_all_lines(final)
            elif".spdx" in self.file_path:
                final = self.work_on_spdx_line_by_line(lines)
                final = self.work_on_spdx_all_lines(final)
            else:
                final = self.work_on_readme_file(lines)
            return final
    
    def new_file_name_provider(self):
        new_file_name = []
        input_splited = self.file_path.split("/")
        self.original_file_name = input_splited[-1]
        if ".txt" in  self.original_file_name:
            new_file_name = self.parse_txt_file_name(input_splited[-1])
        elif ".spdx" in self.original_file_name:
            new_file_name = self.parse_spdx_file_name(input_splited[-1])
        else:
            new_file_name="README.md"
        return new_file_name
    
    file_name = property(get_new_file_name, set_new_file_name)
    package_name = property(get_packet_name, set_packet_name)
    package_version = property(get_packet_version, set_packet_version)
    modified_file = property(get_final_file, set_final_file)
    licenses_name = property(get_license_names, set_license_names)