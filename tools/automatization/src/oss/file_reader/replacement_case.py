from enum import Enum


class ReplacementCase(Enum):
    """ We can decide to use ReplacementCase or not"""
    txt = 'txt'
    spdx = 'spdx'

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)