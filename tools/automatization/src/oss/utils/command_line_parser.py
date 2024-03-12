import configargparse
from pathlib import Path


class UnknownArgumentException(Exception):
    pass


def parse_var(s: str):
    """
    Parse a key, value pair, separated by '=' or ":"
    That's the reverse of ShellArgs.

    On the command line a declaration will typically look like:
        user=hello
    """
    if "=" in s:
        items = s.split('=')
    # else:
    #     items = s.split(':')

    value = None
    key = items[0].strip()  # we remove blanks around keys, as is logical
    if len(items) > 1:
        # rejoin the rest:
        value = '='.join(items[1:])
        if value in ["true", "True"]:
            value = True
        elif value in ["false", "False"]:
            value = False
    return (key, value)


class Parser():
    """ This is a simple parser class that we can use the parser instance of this class in all the files to get value of any configuration parameter"""
    def __init__(self):
        self.options = None
        self.parser = configargparse.get_argument_parser(
            default_config_files=[str(Path(__file__).parent.parent / "config.yaml")])
        self.parser.add('-c', '--config_file', required=False,
                        is_config_file=True, help='config file path')

    def add_argument(self, *a, **b):
        """ 
        Adds new configuration parameter to the parser
        """
        self.parser.add(*a, **b)

    def get_options(self):
        if self.options is None:
            self.options = self.parser.parse_known_args()[0]
        return self.options

    def __getitem__(self, key):
        """ 
        Return  a Value of the configuration paramete
        We pass the name of the configuration parameter
        """
        options = self.get_options()
        try:
            return options.__dict__[key]
        except UnknownArgumentException:
            return None

parser = Parser()