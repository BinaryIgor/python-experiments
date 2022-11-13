import re

INTEGER_PATTERN = re.compile("^-?[0-9]+$")
DOUBLE_PATTERN = re.compile("^-?\\d+[,.]\\d+$")
NAME_PATTERN = re.compile("^[a-zA-z][a-zA-z0-9-_]{2,19}$")


def is_valid_integer(string):
    return bool(string and INTEGER_PATTERN.match(string))


def is_valid_double(string):
    return bool(string and (DOUBLE_PATTERN.match(string) or
                            INTEGER_PATTERN.match(string)))


def is_valid_name(string):
    return bool(string and NAME_PATTERN.match(string))
