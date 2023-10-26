from parser import main

import pytest


@pytest.mark.parametrize(
    "command, expected_result",
    [
        (
            "*/15 0 1,15 * 1-5 /usr/bin/find",
            (
                "minute 0 15 30 45\n"
                "hour 0\n"
                "day of month 1 15\n"
                "month 1 2 3 4 5 6 7 8 9 10 11 12\n"
                "day of week 1 2 3 4 5\n"
                "command /usr/bin/find\n"
            ),
        ),
        (
            "5 4 * * * /usr/bin/find",
            (
                "minute 5\n"
                "hour 4\n"
                "day of month 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n"
                "month 1 2 3 4 5 6 7 8 9 10 11 12\n"
                "day of week 0 1 2 3 4 5 6\n"
                "command /usr/bin/find\n"
            ),
        ),
        (
            "0 22 23,24,25 * 1-3 /usr/bin/find",
            (
                "minute 0\n"
                "hour 22\n"
                "day of month 23 24 25\n"
                "month 1 2 3 4 5 6 7 8 9 10 11 12\n"
                "day of week 1 2 3\n"
                "command /usr/bin/find\n"
            ),
        ),
        (
            "2,5,8,9 12-14 25-26 */3 2-5 /usr/bin/find",
            (
                "minute 2 5 8 9\n"
                "hour 12 13 14\n"
                "day of month 25 26\n"
                "month 1 4 7 10\n"
                "day of week 2 3 4 5\n"
                "command /usr/bin/find\n"
            ),
        ),
        (
            "2,5,8,9 12-14 25-26 */3 2-5 /usr/bin/find a*",
            (
                "minute 2 5 8 9\n"
                "hour 12 13 14\n"
                "day of month 25 26\n"
                "month 1 4 7 10\n"
                "day of week 2 3 4 5\n"
                "command /usr/bin/find a*\n"
            ),
        ),
        (
            "2,5,8,9 12-14 25-26 */3 2-5 /usr/bin/find a* grep ls",
            (
                "minute 2 5 8 9\n"
                "hour 12 13 14\n"
                "day of month 25 26\n"
                "month 1 4 7 10\n"
                "day of week 2 3 4 5\n"
                "command /usr/bin/find a* grep ls\n"
            ),
        ),
        (
            "2,5,8,9 12-14 25-26 */3 2-5 2022-2023 /usr/bin/find a* grep ls",
            (
                "minute 2 5 8 9\n"
                "hour 12 13 14\n"
                "day of month 25 26\n"
                "month 1 4 7 10\n"
                "day of week 2 3 4 5\n"
                "year 2022 2023\n"
                "command /usr/bin/find a* grep ls\n"
            ),
        ),
        (
            "2,5,8,9 12-14 25-26 */3 2-5 2022,2025 /usr/bin/find a* grep ls",
            (
                "minute 2 5 8 9\n"
                "hour 12 13 14\n"
                "day of month 25 26\n"
                "month 1 4 7 10\n"
                "day of week 2 3 4 5\n"
                "year 2022 2025\n"
                "command /usr/bin/find a* grep ls\n"
            ),
        ),
        (
            "2,5,8,9 12-14 25-26 */3 2-5 */1000 /usr/bin/find a* grep ls",
            (
                "minute 2 5 8 9\n"
                "hour 12 13 14\n"
                "day of month 25 26\n"
                "month 1 4 7 10\n"
                "day of week 2 3 4 5\n"
                "year 900 1900 2900\n"
                "command /usr/bin/find a* grep ls\n"
            ),
        ),
    ],
)
def test_parser_works_correctly(capfd, command, expected_result):
    # when
    main([command])

    # then
    out, err = capfd.readouterr()
    assert out == expected_result


def test_parser_raises_exception_with_small_amount_of_arguments():
    # given
    five_args_command = "2,5,8,9 12-14 25-26 */3 2-5"

    # when
    with pytest.raises(ValueError) as exc_info:
        main([five_args_command])

    # then
    assert str(exc_info.value) == "Command has incorrect number of components"


def test_parser_raises_exception_for_invalid_number_value():
    # given
    invalid_number_value_command = "66 0 1,15 * 1-5 /usr/bin/find"

    # when
    with pytest.raises(ValueError) as exc_info:
        main([invalid_number_value_command])

    # then
    assert str(exc_info.value) == "66 is greater than 59 or less than 0"


def test_parser_raises_exception_for_invalid_comma_value():
    # given
    invalid_comma_value_command = "15 0 1,35 * 1-5 /usr/bin/find"

    # when
    with pytest.raises(ValueError) as exc_info:
        main([invalid_comma_value_command])

    # then
    assert str(exc_info.value) == "35 is greater than 31 or less than 1"


def test_parser_raises_exception_for_invalid_slash_value():
    # given
    invalid_hyphen_value_command = "15 0 1/100 * 1-5 /usr/bin/find"

    # when
    with pytest.raises(ValueError) as exc_info:
        main([invalid_hyphen_value_command])

    # then
    assert str(exc_info.value) == "100 is greater than 31 or less than 1"


def test_parser_raises_exception_for_invalid_command():
    # when
    with pytest.raises(ValueError) as exc_info:
        main([])

    # then
    assert str(exc_info.value) == "Please, provide cron string"


def test_parser_raises_exception_for_empty_command():
    # given
    empty_value_command = "15 0 1/23  1-5 "
    # when
    with pytest.raises(ValueError) as exc_info:
        main([empty_value_command])

    # then
    assert str(exc_info.value) == "Part of expression can not be an empty string"
