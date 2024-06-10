

import os
from pathlib import Path
from oss.utils.command_line_parser import parser
from oss.file_operation.files_generator import FilesGenerator
from oss.types.operation_boolean import OperationBoolean
from oss.types.operation_location import OperationLocation
from oss.folder_operation.folder_cleaner import FolderCleaner

parser.add_argument('-rmo', '--remove_output',  type=OperationBoolean, choices=list(OperationBoolean), help='Remove the output folder before generations of the files(default value is %(default)s)' , default= "false")
parser.add_argument('-lo', '--location',  type=OperationLocation, choices=list(OperationLocation), help='The location that we would like to generate documents %(default)s)' , default= "packages")
parser.add_argument('-gl', '--generation_location',  type=str, help='The location that we would like to generate documents)' )


class GenerationLocationException(Exception):
    pass


class MissingOutputLocationException(GenerationLocationException):
    pass


class BadOutputLocationException(GenerationLocationException):
    pass


# Add configuration arguments to main
parser.get_options()


input_file_path = str(Path(__file__).parent.parent/ "document-generations/input/")
output_path = str(Path(__file__).parent.parent/ "document-generations/output") + "/"
analysed_packages_path = str(Path(__file__).parent.parent.parent.parent.parent/ "analysed-packages") + "/"
readme_file = str(Path(__file__).parent.parent/ "README.md")


# Start of the application
if __name__ == "__main__":
    generation_path = ""
    try:
        if (parser["remove_output"] == OperationBoolean.true and parser["location"] == OperationLocation.output):
            FolderCleaner(output_path)
        #Select generation path based on user desire {output or packages}
        if parser["location"] == OperationLocation.output:
            generation_path = output_path
        elif parser["location"] == OperationLocation.packages:
            generation_path = analysed_packages_path
        else:
            if not parser["generation_location"]:
                raise MissingOutputLocationException("You have selected user_input location. However, you did not provide any input location. Please use generation_location configuration to provide the output location.")
            if not os.path.isabs(parser["generation_location"]):
                raise BadOutputLocationException(f"({ parser['generation_location']}) directory does not exist. Please provide absolute path for generation_location configuration.")
            generation_path = parser["generation_location"]
        FilesGenerator.create(input_file_path, generation_path, readme_file)

    except KeyboardInterrupt:
        print(f'User Terminate')