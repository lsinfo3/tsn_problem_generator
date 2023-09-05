import math
import random


def unpack_random(varrange):
    if type(varrange) in (tuple, list):
        if len(varrange) < 2 or len(varrange) > 3:
            raise ValueError("range can either be a number, or a list [min, max], or a list [min, max, 'log']")
        elif len(varrange) == 3 and varrange[2] == "log":
            return exprandom_float_between(varrange[0], varrange[1])
        elif len(varrange) == 3:
            raise ValueError("range[2] can only be 'log' for logarithmically scaled random choice")
        else:
            return urandom_int_between(varrange[0], varrange[1])

    if type(varrange) == set:
        return random.sample(list(varrange), 1)[0]

    return varrange


def urandom_int_between(min: int, max: int) -> int:
    return random.choice(range(min, max+1))

def urandom_float_between(min: float, max: float) -> float:
    return random.random() * (max - min) + min

def exprandom_float_between(min: float, max: float) -> float:
    return math.exp(urandom_float_between(math.log(min), math.log(max)))
