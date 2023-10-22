import sys

EXPRESSION_LENGTH = 6


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
    if "/" in expr:
        left_part, right_part = expr.split("/")
        return _parse_expression(
            expr=left_part,
            max_value=max_value,
            min_value=min_value,
            step=_parse_int(value=right_part, max_value=max_value, min_value=min_value),
        )

    elif expr.isnumeric():
        return expr

    elif "," in expr:
        return " ".join(expr.split(","))

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


def main(expression) -> None:
    parts = expression[0].split(" ")
    if len(parts) != EXPRESSION_LENGTH:
        raise ValueError(f'"{expression}" must have 6 components')

    (
        minute_expr,
        hour_expr,
        day_month_expr,
        month_expr,
        day_week_expr,
        command_expr,
    ) = parts

    minutes = f"minute {_parse_expression(minute_expr, max_value=59)}"
    hours = f"hour {_parse_expression(hour_expr, max_value=23)}"
    day_months = (
        f"day of month {_parse_expression(day_month_expr, max_value=31,min_value=1)}"
    )
    months = f"month {_parse_expression(month_expr,max_value=12, min_value=1)}"
    day_weeks = f"day of week {_parse_expression(day_week_expr,max_value=6)}"
    command = f"command {command_expr}"

    print("\n".join([minutes, hours, day_months, months, day_weeks, command]))


if __name__ == "__main__":
    main(sys.argv[1:])
