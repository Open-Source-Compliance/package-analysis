
from pathlib import Path
from oss.utils.command_line_parser import parser
from oss.file_operation.files_generator import FilesGenerator
from oss.types.operation_boolean import OperationBoolean
from oss.folder_operation.folder_cleaner import FolderCleaner

parser.add_argument('-rmo', '--remove_output',  type=OperationBoolean, choices=list(OperationBoolean), help='Remove the output folder before generations of the files(default value is %(default)s)' , default= "false")


# Add configuration arguments to main
parser.get_options()


input_file_path = str(Path(__file__).parent.parent/ "document-generations/input/")
output_path = str(Path(__file__).parent.parent/ "document-generations/output") + "/"
readme_file = str(Path(__file__).parent.parent/ "README.md")


# Start of the application
if __name__ == "__main__":
    try:
        if parser["remove_output"] == OperationBoolean.true:
            FolderCleaner(output_path)
            
        FilesGenerator.create(input_file_path, output_path, readme_file)

    except KeyboardInterrupt:
        print(f'User Terminate')