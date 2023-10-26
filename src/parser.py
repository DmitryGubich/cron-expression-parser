import sys

from utils import _parse_expression, _parse_string

EXPRESSION_LENGTH = 5


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
