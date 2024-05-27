import os
from oss.utils.command_line_parser import parser
from oss.content_analyzer.read_regex_replacement import ReadRegexReplacement
from oss.types.operation_case import OperationCase
from oss.folder_operation.folder_reader import FolderReader
from oss.file_operation.file_name_parser import FileNameParser
from oss.types.operation_boolean import OperationBoolean

parser.add_argument('-v', '--validation',  type=OperationBoolean, choices=list(OperationBoolean), help='Validate all the generated files(default value is %(default)s)' , default= "true")


class FilesGeneratorException(Exception):
    pass


class MissingTextFileException(FilesGeneratorException):
    pass


class MissingSpdxException(FilesGeneratorException):
    pass


class MissingOutputPathException(FilesGeneratorException):
    pass


class MultiplePackageFilesException(FilesGeneratorException):
    pass



class FilesGenerator:
    def __init__(self, input_path: str, output_path: str, readme_file: str):
        self.input_path = input_path
        self.output_path = output_path
        self.generated_folder_path = ""
        self.readme_file = readme_file
        self.package_name =  ""
        self.package_version = ""
        self.final_file_path = ""

    def validate_file(self, input_file):
        command = f"pyspdxtools -i \"{input_file}\""
        os.system(command)
        print(">>>>> Validate Document name: ",  input_file)

    def generate_file(self, input_file):
        generated_file_path = os.path.join(self.generated_folder_path, input_file)
        command = f"pyspdxtools -i \"{self.final_file_path}\" -o \"{generated_file_path}\""
        os.system(command)
        print(">>>>> Generated Document name:",  generated_file_path)
        if parser["validation"] == OperationBoolean.true:
            self.validate_file(generated_file_path)

    def generate_files(self):
        result_txt = self.generate_txt_files()
        result_spdx = self.generate_spdx_files()
        self.generatte_readme()

    @classmethod
    def create (cls, input_path: str, output_path: str, readme_file: str):
        instance = FilesGenerator(input_path, output_path, readme_file)
        instance.generate_files()
        return instance
    
    def spdx_to_json(self, packet_name):
        generated_spdx_json = packet_name + ".spdx.json"
        self.generate_file(generated_spdx_json)

    def spdx_to_yaml(self, packet_name):
        generated_spdx_yaml = packet_name + ".spdx.yaml"
        self.generate_file(generated_spdx_yaml)

    def spdx_to_rdf_xml(self, packet_name):
        generated_spdx_rdf_xml = packet_name + ".spdx.rdf.xml"
        self.generate_file(generated_spdx_rdf_xml)

    def save_new_file(self, final_file, file_name):
        if self.generated_folder_path:
            self.final_file_path = os.path.join(self.generated_folder_path, file_name)
        if not self.final_file_path:
            raise MissingOutputPathException("Final output path is empty! It can not generate the new file")
        with open(self.final_file_path, "w") as file:
            for line in final_file:
                file.write(line)

    def add_folder(self, folder_name):
        self.generated_folder_path  = os.path.join(self.generated_folder_path ,folder_name)
        if not os.path.exists(self.generated_folder_path):
            # Create the directory
            os.makedirs(self.generated_folder_path )
            print("Directory created successfully!")
        else:
            print("Directory already exists!")

    def update_output_path(self, package_name, package_version):
        self.package_name = package_name
        self.package_version = package_version
        self.generated_folder_path = self.output_path
        if self.package_name not in self.generated_folder_path:
            self.add_folder(self.package_name)
            if self.package_version not in self.generated_folder_path:
                self.add_folder("version-" + self.package_version)

    def generate_txt_files(self):
        txt_files = vars(FolderReader(self.input_path, OperationCase.txt))['files']
        if not txt_files:
            raise MissingTextFileException(f"ReadMe_OSS_XXXXX.txt is missing in {self.input_path} folder")
        if len(txt_files) > 1:
            raise MultiplePackageFilesException(f"Multiple ReadMe_OSS_XXXXX.txt in this {self.input_path} folder. Please keep only the ReadMe file for your desired package")
        dictionary_replacement_texts = vars(ReadRegexReplacement(OperationCase.txt))['single_data']
        ml_dictionary_replacement_texts = vars(ReadRegexReplacement(OperationCase.txt))['multi_data']
        for txt_file in txt_files:
            file_parser = FileNameParser.create(txt_file, dictionary_replacement_texts, ml_dictionary_replacement_texts)
            self.update_output_path(file_parser.package_name, file_parser.package_version)

            self.save_new_file(file_parser.modified_file, file_parser.file_name)
            print(">>>>> Generated Document name: ",  file_parser.file_name)
        return True

    def generate_spdx_files(self):
        spdx_files = vars(FolderReader(self.input_path, OperationCase.spdx))['files']
        if not spdx_files:
            raise MissingSpdxException(f"SPDX2TV_XXXX.spdx is missing in {self.input_path} folder")
        if len(spdx_files) > 1:
            raise MultiplePackageFilesException(f"Multiple SPDX2TV_XXXX.spdx in this {self.input_path} folder. Please keep only the SPDX2TV_XXXX.spdx file for your desired package")
        dictionary_replacement_texts = vars(ReadRegexReplacement(OperationCase.spdx))['single_data']
        ml_dictionary_replacement_texts = vars(ReadRegexReplacement(OperationCase.spdx))['multi_data']
        for spdx_file in spdx_files:
            file_parser = FileNameParser.create(spdx_file, dictionary_replacement_texts, ml_dictionary_replacement_texts)
            self.update_output_path(file_parser.package_name, file_parser.package_version)
            self.save_new_file(file_parser.modified_file, file_parser.file_name)
            print(">>>>> Generated Document name: ",  file_parser.file_name)
            fixed_name_part = file_parser.package_name + "-" + file_parser.package_version
            self.spdx_to_json(fixed_name_part)
            self.spdx_to_yaml(fixed_name_part)
            self.spdx_to_rdf_xml(fixed_name_part)
        return True

    def generatte_readme(self):
        file_parser = FileNameParser.create(self.readme_file, {}, {})
        self.save_new_file(file_parser.modified_file, file_parser.file_name)
        print(">>>>> Generated Document name: ",  file_parser.file_name)
        return True
