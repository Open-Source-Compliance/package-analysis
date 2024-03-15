import traceback
import re
from oss.utils.command_line_parser import parser, parse_var
from oss.file_reader.replacement_case import ReplacementCase


parser.add_argument('--replacement_regex_txt', metavar="find_text=replace_text another_find_text=another_replace_text",
                    nargs='+',
                    help="Set a number of key-value pairs"
                    "values are always treated as strings.")
parser.add_argument('--replacement_regex_spdx', metavar="find_text=replace_text another_find_text=another_replace_text",
                    nargs='+',
                    help="Set a number of key-value pairs"
                    "values are always treated as strings.")

Default_TXT_Replacements = {"MAIN LICENSES" : "LICENSES",
                            "OTHER LICENSES" : "LICENSES"}

Default_SPDX_Replacements = {"^PackageLicenseConcluded: .*\n$" :"PackageLicenseConcluded: NOASSERTION\n",
                             '^This document was created using license information and a generator from Fossology.' : 'This document was created using license information and a generator from Fossology.\nIt contains the license and copyright analysis of [package].\nPlease check "LicenseComments" for explanations of concluded licenses.'}

class ReplaceTextException(Exception):
    pass


class MissingFindTextException(ReplaceTextException):
    pass


class MissingReplacementTextException(ReplaceTextException):
    pass


class ReadRegexReplacement:
    """
    This class gets username and password for sensor authentication
    """
    def __init__(self, replacement_case):
        self.data = {}
        try:
            config_parameter, default_parameters = self.read_default_configurations(replacement_case)
            self.data = self.get_text_and_replacement_from_cmd(config_parameter, default_parameters)
        except ReplaceTextException as e:
            print(f'{e.__class__.__name__}: {e} : {traceback.format_exc()}')

    def read_default_configurations(self, replacement_case):
        config_parameter = None
        default_parameters = {}
        if replacement_case == ReplacementCase.txt:
            config_parameter = parser["replacement_regex_txt"]
            default_parameters = Default_TXT_Replacements
        if replacement_case == ReplacementCase.spdx:
            config_parameter = parser["replacement_regex_spdx"]
            default_parameters = Default_SPDX_Replacements
        return config_parameter, default_parameters
        
    @staticmethod
    def get_text_and_replacement_from_cmd(config_parameter, default_parameters):
        """
        Get authentication cmd line parameter and parse the text and replacement.
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