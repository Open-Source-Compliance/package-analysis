from pathlib import Path
from oss.utils.command_line_parser import parser
from oss.file_reader.file_name_parser import FileNameParser
from oss.file_reader.read_regex_replacement import ReadRegexReplacement


parser.add_argument('-fp', '--file_path', required=False, type=str, help='name of the library to parse(default: %(default)s)')
parser.add_argument('-fp', '--package_name', required=False, type=str, help='name of the library to parse(default: %(default)s)' , default= "")
# Add configuration arguments to main
parser.get_options()


# Start of the application
if __name__ == "__main__":
    try:
        print(">>>>> Preparing Document: ", parser["file_path"])
        if parser["file_path"]:
            file_path = str(Path(__file__).parent.parent/ parser["file_path"])
            output_path = str(Path(__file__).parent.parent/ "oss/output") + "/"
            dictionary_replacement_texts = vars(ReadRegexReplacement())['data']
            file_parser = FileNameParser.create(file_path, output_path, dictionary_replacement_texts)
            print(">>>>> Test Document: ",  file_parser.file_name)
    except KeyboardInterrupt:
        print(f'User Terminate')