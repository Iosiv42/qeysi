import re
from typing import Union

SPLIT_REGEX = re.compile(
    r"(\*\*|//|[*/%+-]|<<|>>|&&|\|\||&|\||\^|<=|>=|>|<|==|!=)"
)

BRACKETS_REGEX = re.compile(r"\((.*)\)")

OPS_PRECEDENCE = {
    "||": 0,
    "&&": 1,
    "!": 2,
    "<": 3, "<=": 3, ">": 3, ">=": 3, "!=": 3, "==": 3,
    "|": 4,
    "^": 5,
    "&": 6,
    "<<": 7, ">>": 7,
    "+": 8, "-": 8,
    "*": 9, "/": 9, "//": 9, "%": 9,
    "**": 10,
}

OPS_DUNDERS = {
    "+": "__add__",
    "-": "__sub__",
    "*": "__mul__",
    "/": "__truediv__",
    "//": "__floordiv__",
    "**": "__pow__",
    "%": "__mod__",
    "<<": "__lshift__",
    ">>": "__rshift__",
    "&": "__and__",
    "^": "__xor__",
    "|": "__or__",
    "&&": "__and__",
    "||": "__or__",
}

CAST_PRECEDENCE = {
    int: 0,
    float: 1,
    complex: 2,
    bool: 3,
}

ReturnableTypes = Union[bool, int, float, complex]
