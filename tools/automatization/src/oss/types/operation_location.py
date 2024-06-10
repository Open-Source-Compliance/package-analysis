from enum import Enum


class OperationLocation(Enum):
    """ We can decide to use OperationCase or not"""
    output = 'output'
    packages = 'packages'
    user_input = 'user_input'

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)