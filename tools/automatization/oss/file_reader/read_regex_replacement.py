import traceback
import re
from oss.utils.command_line_parser import parser, parse_var


parser.add_argument('--replacement_regex_texts', metavar="find_text=replace_text another_find_text=another_replace_text",
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
    This class gets username and password for sensor authentication
    """
    def __init__(self):
        self.data = {}
        try:
            self.data = self.get_text_and_replacement_from_cmd()
        except ReplaceTextException as e:
            print(f'{e.__class__.__name__}: {e} : {traceback.format_exc()}')

    @staticmethod
    def get_text_and_replacement_from_cmd():
        """
        Get authentication cmd line parameter and parse the text and replacement.
        """
        data ={}
        double_quotes = '"'
        if not parser["replacement_regex_texts"]:
            return data
        for element in parser["replacement_regex_texts"]:
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