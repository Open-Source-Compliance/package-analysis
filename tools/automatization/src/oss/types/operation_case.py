from enum import Enum


class OperationCase(Enum):
    """ We can decide to use OperationCase or not"""
    txt = 'txt'
    spdx = 'spdx'

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)