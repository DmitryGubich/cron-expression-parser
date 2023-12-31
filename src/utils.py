def _parse_string(value: str) -> str:
    if not value:
        raise ValueError("Part of expression can not be an empty string")
    return value


def _parse_int(value, max_value: int, min_value: int) -> int:
    try:
        result = int(value)
    except Exception as e:
        raise ValueError(f"{value} must be an integer") from e

    if result < 0 or result < min_value or result > max_value:
        raise ValueError(
            f"{result} is greater than {max_value} or less than {min_value}"
        )

    return result


def _parse_expression(
    expr: str, max_value: int, min_value: int = 0, step: int = 1
) -> str:
    _parse_string(expr)

    if "/" in expr:
        left_part, right_part = expr.split("/")
        return _parse_expression(
            expr=left_part,
            max_value=max_value,
            min_value=min_value,
            step=_parse_int(value=right_part, max_value=max_value, min_value=min_value),
        )

    elif expr.isnumeric():
        return str(_parse_int(value=expr, max_value=max_value, min_value=min_value))

    elif "," in expr:
        return " ".join(
            [
                str(_parse_int(value=i, max_value=max_value, min_value=min_value))
                for i in expr.split(",")
            ]
        )

    elif expr == "*":
        return " ".join([f"{i}" for i in range(min_value, max_value + 1, step)])

    elif "-" in expr:
        start, finish = expr.split("-")
        return " ".join(
            [
                f"{i}"
                for i in range(
                    _parse_int(value=start, max_value=max_value, min_value=min_value),
                    _parse_int(value=finish, max_value=max_value, min_value=min_value)
                    + 1,
                    step,
                )
            ]
        )
