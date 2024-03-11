import re
import textwrap
from oss.utils.command_line_parser import parser

class FileNameParser:
    """
    """
    def __init__(self, file_path: list, dictionary_replacement_texts: dict):
        self.file_path = file_path
        self.dictionary_replacement_texts = dictionary_replacement_texts
        for key, value in  self.dictionary_replacement_texts.items():
            print ("key: ", key)
            print ("value: ", value)
        self.new_file_name = []
        self.original_file_name = ""
        self.packet_name = ""

    @classmethod
    def create (cls, file_path: list, dictionary_replacement_texts: dict):
        instance = FileNameParser(file_path, dictionary_replacement_texts)
        new_file_name = instance.new_file_name_provider()
        instance.file_name = new_file_name
        instance.save_new_file()
        return instance

    def get_new_file_name(self):
        return self.new_file_name

    def set_new_file_name(self, new_file_name: list):
        self.new_file_name = new_file_name
    
    def remove_patter_ending(self, file_name):
        if parser["removal_file_ending"]:
            if parser["removal_file_ending"] in file_name:
                file_name, _= file_name.split(pattern)
        pattern = ".zip" or ".tar.xz" or ".tar.gz"
        if pattern in file_name :
            file_name, _= file_name.split(pattern)
        return file_name
    
    def parse_txt(self, file_name):
        _, file_name = file_name.split("ReadMe_OSS_")
        file_name = self.remove_patter_ending(file_name)
        if ".txt" in file_name:
            file_name, _= file_name.split(".txt")
        self.packet_name = file_name
        file_name = file_name + "-OSS-disclosure.txt"
        return file_name
    
    def parse_spdx(self, file_name):
        _, file_name = file_name.split("SPDX2TV_")
        file_name = self.remove_patter_ending(file_name)
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


    def save_new_file(self):    
        if parser["destination_path"]:
            final_path = parser["destination_path"] + self.file_name
        else:
            final_path = self.filwork_on_txt_filee_path.replace(self.original_file_name, self.file_name)
        with open(parser["file_path"], "r") as file1:
            lines= file1.readlines()
            if ".txt" in parser["file_path"]:
                final = self.work_on_txt_file(lines)
            else:
                final = self.work_on_spdx_file(lines)
            with open(final_path, "w") as file2:
                for line in final:
                    file2.write(line)
    
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