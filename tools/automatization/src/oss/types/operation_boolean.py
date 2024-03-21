from enum import Enum


class OperationBoolean(Enum):
    """ We can decide to use OperationBoolean or not"""
    true = 'true'
    false = 'false'

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)