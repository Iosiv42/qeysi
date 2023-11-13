import re
from typing import Union

from globals import *


class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, source: str) -> ReturnableTypes:
        source = source.replace(" ", "")
        source = self.evaluate_brackets(source)

        splitted = SPLIT_REGEX.split(source)
        ops_query = sorted(
            splitted[1::2],
            key=lambda op: OPS_PRECEDENCE[op],
            reverse=True
        )

        for op in ops_query:
            idx = splitted.index(op)

            lhs, rhs = splitted[idx - 1:idx + 2:2]
            print(lhs, rhs)

            lhs, rhs, return_type = self.cast_to_max(lhs, rhs)

            splitted[idx - 1:idx + 2] = (
                str(getattr(return_type, OPS_DUNDERS[op])(lhs, rhs)),
            )

        return splitted[0]

    def cast_from_str(self, source: str):
        """ Cast source to numerical type accordingly to CAST_PRECEDENCE. """
        for cast_type in CAST_PRECEDENCE:
            try:
                if cast_type == bool and source not in {"True", "False"}:
                    continue
                return cast_type(source)
            except ValueError:
                pass

        raise ValueError(
            "Cannot cast given str to supported types: "
            f"{CAST_PRECEDENCE.keys()}"
        )

    def cast_to_max(self, lhs: str, rhs: str) -> tuple:
        """ Cast lhs and rhs to one type accordingly to CAST_PRECEDENCE,
            so that return type will be type that has max precedence of 
            casted lhs and rhs.
        """
        type_lhs = type(self.cast_from_str(lhs))
        type_rhs = type(self.cast_from_str(rhs))

        return_type = max(
            type_lhs, type_rhs, key=lambda arg: CAST_PRECEDENCE[arg]
        )

        return (return_type(lhs), return_type(rhs), return_type)

    def evaluate_brackets(self, source: str) -> str:
        """ Evaluate value inside the brackets of source. """
        ret =  BRACKETS_REGEX.sub(lambda m: self.evaluate(m.group(1)), source)
        return ret


evaluator = Evaluator()
print(evaluator.evaluate("2.71 * 2**0.5"))
