import traceback
import re
from oss.utils.command_line_parser import parser, parse_var
from oss.types.operation_case import OperationCase
from oss.default_replacement import Default_TXT_Replacements_Single, Default_TXT_Replacements_Multi
from oss.default_replacement import Default_SPDX_Replacements_Single, Default_SPDX_Replacements_Multi

parser.add_argument('--replacement_regex_txt', metavar="find_text=replace_text another_find_text=another_replace_text",
                    nargs='+',
                    help="Set a number of key-value pairs"
                    "values are always treated as strings.")
parser.add_argument('--replacement_regex_spdx', metavar="find_text=replace_text another_find_text=another_replace_text",
                    nargs='+',
                    help="Set a number of key-value pairs"
                    "values are always treated as strings.")


class ReplaceTextException(Exception):
    pass


class MissingFindTextException(ReplaceTextException):
    pass


class MissingReplacementTextException(ReplaceTextException):
    pass


class ReadRegexReplacement:
    """
    This class reads regular expression and replace it with the given value
    """
    def __init__(self, operation_case):
        self.single_data = {}
        self.multi_data = []
        try:
            single_config, default_multi_config= self.read_default_configurations(operation_case)
            self.single_data = self.get_text_and_replacement_from_cmd(single_config[0], single_config[1])
            self.multi_data = default_multi_config
        except ReplaceTextException as e:
            print(f'{e.__class__.__name__}: {e} : {traceback.format_exc()}')

    def read_default_configurations(self, operation_case):
        config_parameter = None
        default_parameters = {}
        if operation_case == OperationCase.txt:
            config_parameter_single = parser["replacement_regex_txt"]
            default_parameters_single = Default_TXT_Replacements_Single
            default_parameters_multi = Default_TXT_Replacements_Multi
        if operation_case == OperationCase.spdx:
            config_parameter_single = parser["replacement_regex_spdx"]
            default_parameters_single = Default_SPDX_Replacements_Single
            default_parameters_multi = Default_SPDX_Replacements_Multi
        return (config_parameter_single, default_parameters_single) , default_parameters_multi
    @staticmethod
    def get_text_and_replacement_from_cmd(config_parameter, default_parameters):
        """
        Get all the key and value lists of items that should be replaced.
        """
        data = {}
        data.update(default_parameters)
        double_quotes = '"'
        if not config_parameter:
            return data
        for element in config_parameter:
            if element:
                key, value = parse_var(element)
                if not key:
                    raise MissingFindTextException("Missing Finding text in configuration parameters")
                if not value:
                    raise MissingReplacementTextException("Missing Replacement Text in configuration parameters")
                if double_quotes in key:
                    key = key.replace(double_quotes, '')
                if double_quotes in value:
                    value = value.replace(double_quotes, '')
                #Remove leading spaces using regex
                value =re.sub(r"^\s+", "", value)
                data[key] = value
        return data