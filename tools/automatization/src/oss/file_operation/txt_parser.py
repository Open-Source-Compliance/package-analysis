import textwrap
from oss.file_operation.file_parser import FileParser


class TxtParser(FileParser):
    """This is a simple parser class that it parse and replace text in ReadMe_OSS file"""

    def __init__(
        self,
        file_path=None,
        dictionary_replacement_texts=None,
        ml_list_replacement_texts=None,
    ):
        FileParser.__init__(
            self, file_path, dictionary_replacement_texts, ml_list_replacement_texts
        )

    def new_file_name_provider(self):
        self.packet_name, self.packet_version = self.find_package_name_version(
            self.file_name
        )
        file_name = self.packet_name + "-" + self.packet_version + "-OSS-disclosure.txt"
        return file_name

    def update_filename_in_oss_txt(self, line):
        # It looks for the name of the file in lines and it will replace it with desired format
        if self.packet_name in line:
            if self.packet_version in line:
                print(">>>>>>> Replacing Filename : ", line)
                line = self.packet_name + "-" + self.packet_version + "\n"
                print("        With: ", line)
                return line

    def remove_white_space(self, lines):
        three_element_before = ""
        two_element_before = ""
        one_element_before = ""
        new_list = []
        for i in range(len(lines)):
            if i > 3:
                three_element_before = lines[i - 3]
                two_element_before = lines[i - 2]
                one_element_before = lines[i - 1]
                if (
                    (not three_element_before.strip())
                    and (not two_element_before.strip())
                    and (not one_element_before.strip())
                    and (not lines[i].strip())
                ):
                    continue
            new_list.append(lines[i])
        return new_list

    def post_processing_operation(self, lines):
        new_line_list = []
        for line in lines:
            update_line = self.update_filename_in_oss_txt(line)
            if update_line:
                new_line_list.append(update_line)
                continue
            replacement_line = self.apply_text_replacement(line)
            if replacement_line:
                new_line_list.append(replacement_line)
                continue
            if ("---------" in line) or ("======" in line):
                trimm_line = textwrap.wrap(line, 80, break_long_words=True)
                new_line_list.append(trimm_line[0])
            else:
                new_lines = textwrap.fill(line, width=80)
                new_line_list.append(new_lines)
            new_line_list.append("\n")
        return self.remove_white_space(new_line_list)

    def final_processing(self, lines):
        if not self.ml_list_replacement_texts:
            return lines
        lines = self.apply_ml_text_replacement(lines)
        return lines
