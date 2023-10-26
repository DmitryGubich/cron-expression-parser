import sys

EXPRESSION_LENGTH = 5
OPTIONAL_EXPRESSION_LENGTH = 6


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


def main(args: list) -> None:
    try:
        parts = args[0].split(" ")

    except Exception as e:
        raise ValueError("Please, provide cron string") from e

    if len(parts) <= EXPRESSION_LENGTH:
        raise ValueError(f"Command has incorrect number of components")

    cron_args = parts[:EXPRESSION_LENGTH]
    six_arg = parts[5]
    if six_arg.startswith("*") or (six_arg[:1] and six_arg[0].isnumeric()):
        cron_args.append(six_arg)
    command_args = parts[len(cron_args) :]

    (
        minute_expr,
        hour_expr,
        day_month_expr,
        month_expr,
        day_week_expr,
        *last_args,
    ) = cron_args

    result = [
        f"minute {_parse_expression(minute_expr, max_value=59)}",
        f"hour {_parse_expression(hour_expr, max_value=23)}",
        f"day of month {_parse_expression(day_month_expr, max_value=31, min_value=1)}",
        f"month {_parse_expression(month_expr, max_value=12, min_value=1)}",
        f"day of week {_parse_expression(day_week_expr, max_value=6)}",
    ]
    if last_args:
        result.append(
            f"year {_parse_expression(last_args[0], max_value=3100, min_value=900)}"
        )

    result.append(f"command {_parse_string(' '.join(command_args))}")

    print("\n".join(result))


if __name__ == "__main__":
    main(sys.argv[1:])
