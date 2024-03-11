from oss.utils.command_line_parser import parser
from oss.file_reader.file_name_parser import FileNameParser
from oss.file_reader.read_regex_replacement import ReadRegexReplacement


parser.add_argument('-fp', '--file_path', required=False, type=str, help='name of the library to parse(default: %(default)s)')
parser.add_argument('-fp', '--removal_file_ending', required=False, type=str, help='name of the library to parse(default: %(default)s)' , default= "")
parser.add_argument('-dp', '--destination_path', required=False, type=str, help='name of the folder to collect licenses(default: %(default)s)')
# Add configuration arguments to main
parser.get_options()



# Start of the application
if __name__ == "__main__":
    try:
        print(">>>>> Preparing Document: ", parser["file_path"])
        if parser["file_path"]:
            dictionary_replacement_texts = vars(ReadRegexReplacement())['data']
            file_parser = FileNameParser.create(parser["file_path"], dictionary_replacement_texts)
            print(">>>>> Test Document: ",  file_parser.file_name)
    except KeyboardInterrupt:
        print(f'User Terminate')