import re


class PatternParserException(Exception):
    pass


class MisMatchParenthesisNumber(PatternParserException):
    pass


class UnknownLogicalExpressionsKey(PatternParserException):
    pass


class PatternParser:
    def __init__(self):
        self.parser_result = {}
        self.parsed_keys = []

    def parenthetic_contents(self, string: str):
        """Generate parenthesized contents in string as pairs (level, contents)."""
        stack = []
        cnt_open_pa = 0
        cnt_close_pa = 0
        for i, c in enumerate(string):
            if c == '(':
                cnt_open_pa += 1
                stack.append(i)
            elif c == ')':
                cnt_close_pa += 1
                if stack:
                    start = stack.pop()
                    yield (len(stack), string[start + 1: i])
        if not cnt_close_pa == cnt_open_pa:
            raise MisMatchParenthesisNumber(
                "There is a mistmatch in number of parenthesis")

    def parse_var(self, s: str):
        """
        Parse a key, value pair, separated by '=' or ":"
        That's the reverse of ShellArgs.

        On the command line a declaration will typically look like:
            foo=hello
        """
        if "=" in s:
            items = s.split('=')
        else:
            items = s.split(':')

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

    def compare_with_parsed_expressions(self, expression: str):
        """
        Check if the expression is already parsed in self.parser_result. It is already parsed, remove those parts from expression
        and add its pattern to pattern_list
        """
        reserve_key = []
        expression_parsed = expression
        #If the key exists in self.parser_result, remove the key from expression string and add its value to the pattern_list
        for key, _ in self.parser_result.items():
            if key in expression_parsed:
                reserve_key.append(key)
        if reserve_key:
            for key in reserve_key:
                if not ((key in reserve_key[-1]) and (key is not reserve_key[-1])):
                    expression_parsed = expression_parsed.replace(key, "")
                    expression_parsed = expression_parsed.replace("()", "")
        return expression_parsed

    def parse_expression(self, expression: str):
        expression_parsed = self.compare_with_parsed_expressions(expression)
        #Remove any unnecessary space before or after = or :
        items = re.sub(r"\s*=\s*", "=", expression_parsed)
        items = re.sub(r"\s*:\s*", "=", items)
        #Split the rest of string by space
        items = items.split()
        result = {}
        for item in items:
            key, value = self.parse_var(item)
            result[key] = value
        return result

    def parse_vars(self, items: str):
        """
        Parse a string with series of expressions with parenthesis and return a dictionary pattern
        """
        if items:
            #Add parenthesis in case the user forget to add
            items = "(" + items + ")"
            parenthetic_items = list(self.parenthetic_contents(items))
            final_result = {}
            for el in parenthetic_items:
                final_result = dict(final_result, **self.parse_expression(el[1]))
        return final_result