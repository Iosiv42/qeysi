import re
from itertools import pairwise

OPERATORS_PRECEDENCE = {
    r"\|\|": 0,
    "&&": 1,
    "!": 2,
    "[<(<=)>(>=)(!=)(==)]": 3,
    r"\|": 4,
    r"\^": 5,
    "&": 6,
    "[(<<)(>>)]": 7,
    "([+-])": 8,
    "([*/(//)%])": 9,
    r"\*\*": 11,

}

OPERATOR_TO_DUNEDER = {
    "+": "__add__",
    "-": "__sub__",
    "*": "__mul__",
}


def evaluate(lhs: str, rhs: str, operator: str) -> int:
    for regex in OPERATORS_PRECEDENCE:
        splitted = re.split(regex, lhs)
        if len(splitted) > 1:
            lhs = splitted[0]
            for op, r in zip(splitted[1::2], splitted[2::2]):
                print(lhs, r, op)
                lhs = evaluate(lhs, r, op)
                print(lhs, type(lhs))

    for regex in OPERATORS_PRECEDENCE:
        splitted = re.split(regex, rhs)
        if len(splitted) > 1:
            rhs = splitted[0]
            for op, r in zip(splitted[1::2], splitted[2::2]):
                print(rhs, r, op)
                rhs = evaluate(rhs, r, op)
                print(rhs, type(rhs))

    print(operator)
    return str(getattr(int, OPERATOR_TO_DUNEDER[operator])(int(lhs), int(rhs)))


queries = ["11", "666 + 11 - 2"]
queries[1] = queries[1].replace(" ", "")

print(evaluate(queries[0], queries[1], "*"))
