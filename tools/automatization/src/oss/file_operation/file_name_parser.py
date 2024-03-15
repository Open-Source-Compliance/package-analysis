import re
import os
import textwrap
from copy import deepcopy
from oss.utils.command_line_parser import parser

Packet_Version_Pattern = '\-[0-9]+.*[0-9]$'


parser.add_argument('-pn', '--package_name', required=False, type=str, help='name of the package(default: it will be parsed from the name of the file)')
parser.add_argument('-yn', '--your_name', required=True, type=str, help='name of the author (default value is %(default)s)' , default= "XXXX")


class FileNameParser:
    """
    """
    def __init__(self, file_path: str, dictionary_replacement_texts: dict):
        self.file_path = file_path
        #self.output_path = output_path
        self.dictionary_replacement_texts = dictionary_replacement_texts
        # for key, value in  self.dictionary_replacement_texts.items():
        #     print (">>>  key: ", key)
        #     print (">>>> value: ", value)
        #self.final_file_path = ""
        self.new_file_name = []
        self.original_file_name = ""
        self.original_packet_name = ""
        self.packet_name = ""
        self.final_file = None

    @classmethod
    def create (cls, file_path: str, dictionary_replacement_texts: dict):
        instance = FileNameParser(file_path, dictionary_replacement_texts)
        new_file_name = instance.new_file_name_provider()
        instance.file_name = new_file_name
        instance.modified_file = instance.read_parse_file()
        return instance

    def get_final_file(self):
        return self.final_file

    def set_final_file(self, final_file: str):
        self.final_file = final_file

    def get_packet_name(self):
        return self.packet_name

    def set_packet_name(self, packet_name: str):
        self.new_file_name = packet_name

    def get_new_file_name(self):
        return self.new_file_name

    def set_new_file_name(self, new_file_name: str):
        self.new_file_name = new_file_name
    
    def find_package_name(self, file_name):
        if parser["package_name"]:
            return parser["package_name"]
        pattern = ".zip" or ".tar.xz" or ".tar.gz"
        if pattern in file_name :
            file_name, _= file_name.split(pattern)
        return file_name
    
    def parse_txt(self, file_name):
        _, file_name = file_name.split("ReadMe_OSS_")
        file_name = self.find_package_name(file_name)
        if ".txt" in file_name:
            file_name, _= file_name.split(".txt")
        self.packet_name = file_name
        file_name = file_name + "-OSS-disclosure.txt"
        return file_name
    
    def parse_spdx(self, file_name):
        _, file_name = file_name.split("SPDX2TV_")
        file_name = self.find_package_name(file_name)
        if ".spdx" in file_name:
            file_name, _= file_name.split(".spdx")
        self.packet_name = file_name
        file_name = file_name + "-SPDX2TV.spdx"
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
        reg_ex_result = re.search(given_reg, file)
        if reg_ex_result:
            print ("Regular expression match: ", reg_ex_result)
            return True
        
    def create_substitute_text(self, file, given_reg, replacement_part, substitute_part):
        reg_ex_result = re.search(given_reg, file)
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
                   
    def find_replace(self, find_pattern, replace_text, input_line):
        return re.sub(find_pattern, replace_text, input_line)
    
    def work_on_spdx_file(self, lines):
        new_line_list = []
        for line in lines:
            replacement_line = self.apply_text_replacement(line)
            if replacement_line:
                if "[package]" in replacement_line:
                    package =  deepcopy(self.packet_name)
                    subsctitute_text = self.create_substitute_text(package, Packet_Version_Pattern, "-", " ")
                    if subsctitute_text:
                        package = subsctitute_text
                    replacement_line = replacement_line.replace("[package]", package)
                if "[YourName]" in replacement_line:
                    replacement_line = replacement_line.replace("[YourName]", parser["your_name"])
                new_line_list.append(replacement_line)
                continue
            new_line_list.append(line)
        return new_line_list

    def work_on_txt_file(self, lines):
        new_line_list = []

        for line in lines:
            # if not line.strip():
            #     continue
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


    def read_parse_file(self):
        with open(self.file_path, "r") as file1:
            lines= file1.readlines()
            if ".txt" in self.file_path:
                final = self.work_on_txt_file(lines)
            else:
                final = self.work_on_spdx_file(lines)
            return final
    
    def new_file_name_provider(self):
        new_file_name = []
        input_splited = self.file_path.split("/")
        self.original_file_name = input_splited[-1]
        if ".txt" in  self.original_file_name:
            new_file_name = self.parse_txt(input_splited[-1])
        if ".spdx" in self.original_file_name:
            new_file_name = self.parse_spdx(input_splited[-1])
        return new_file_name
    
    file_name = property(get_new_file_name, set_new_file_name)
    package_name = property(get_packet_name, set_packet_name)
    modified_file = property(get_final_file, set_final_file)