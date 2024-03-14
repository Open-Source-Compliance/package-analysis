import os
from pathlib import Path
from oss.utils.command_line_parser import parser
from oss.file_reader.file_name_parser import FileNameParser
from oss.file_reader.read_regex_replacement import ReadRegexReplacement
from oss.file_reader.replacement_case import ReplacementCase


parser.add_argument('-fp', '--file_path', required=False, type=str, help='name of the library to parse(default: %(default)s)')
parser.add_argument('-fp', '--package_name', required=False, type=str, help='name of the library to parse(default: %(default)s)' , default= "")
# Add configuration arguments to main
parser.get_options()
input_file_path = str(Path(__file__).parent.parent/ "oss/input/")


class MissingTextFileException(Exception):
    pass


class MissingSpdxException(Exception):
    pass


def read_txt_files():
    txt_files = []
    for file in os.listdir(f"{input_file_path}/"):
        if file.endswith(".txt"):
            print(">>>>> Preparing Document: ",os.path.join(input_file_path, file))
            txt_files.append(os.path.join(input_file_path, file))
    return txt_files

def read_spdx_files():
    spdx_files = []
    for file in os.listdir(f"{input_file_path}/"):
        if file.endswith(".spdx"):
            print(os.path.join(input_file_path, file))
            spdx_files.append(os.path.join(input_file_path, file))
    return spdx_files

def generate_txt_files(output_path):
    txt_files = read_txt_files()
    if not txt_files:
        return False
    dictionary_replacement_texts = vars(ReadRegexReplacement(ReplacementCase.txt))['data']
    for txt_file in txt_files:
        file_parser = FileNameParser.create(txt_file, output_path, dictionary_replacement_texts)
        print(">>>>> Generateed Document name: ",  file_parser.file_name)
    return True

def generate_spdx_files(output_path):
    spdx_files = read_spdx_files()
    if not spdx_files:
        return False
    dictionary_replacement_texts = vars(ReadRegexReplacement(ReplacementCase.spdx))['data']
    for spdx_file in spdx_files:
        file_parser = FileNameParser.create(spdx_file, output_path, dictionary_replacement_texts)
        print(">>>>> Generateed Document name: ",  file_parser.file_name)
    return True

# Start of the application
if __name__ == "__main__":
    try:
        output_path = str(Path(__file__).parent.parent/ "oss/output") + "/"

        result_txt = generate_txt_files(output_path)
        result_spdx = generate_spdx_files(output_path)

        if not result_txt:
            raise MissingTextFileException(f"ReadMe_OSS_XXXXX.txt is missing in {input_file_path} folder")

        if not result_spdx:
            raise MissingSpdxException(f"SPDX2TV_XXXX.spdx is missing in {input_file_path} folder")

    except KeyboardInterrupt:
        print(f'User Terminate')