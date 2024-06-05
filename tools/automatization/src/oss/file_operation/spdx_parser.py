from oss.file_operation.file_parser import FileParser
from oss.utils.command_line_parser import parser


License_Name_Pattern_SPDX = "^LicenseName:.*\n$"


class SpdxParser(FileParser):
    """This is a simple parser class that it parse and replace text in SPDX2TV file"""

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
        file_name = self.packet_name + "-" + self.packet_version + "-SPDX2TV.spdx"
        return file_name

    def post_processing_operation(self, lines):
        new_line_list = []
        for line in lines:
            replacement_line = self.apply_text_replacement(line)
            if replacement_line is not None:
                if "[package]" in replacement_line:
                    replacement_line = replacement_line.replace(
                        "[package]", self.packet_name + " " + self.packet_version
                    )
                if "[CreatorName]" in replacement_line:
                    replacement_line = replacement_line.replace(
                        "[CreatorName]", parser["creator_name"]
                    )
                new_line_list.append(replacement_line)
                continue
            new_line_list.append(line)
        return new_line_list

    def find_license_names(self, line):
        if self.check_regular_expression(line, License_Name_Pattern_SPDX):
            _, license_name = line.split(": ")  # Find License name
            license_name, _ = license_name.split("\n")  # Remove new line
            self.licenses_name = license_name

    def final_processing(self, lines):
        if not self.ml_list_replacement_texts:
            return lines
        lines = self.apply_ml_text_replacement(lines)
        for line in lines:
            self.find_license_names(line)
        print(">>>>> Found license_name: ", self.licenses_name)
        return lines
