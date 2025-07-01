import re
import csv
import typing
import pathlib
import dataclasses


OPERATOR_ERROR_MESSAGE = "Operator '{operator}' is unsupported by {func}"
PARSE_VALUE_TYPE_ERROR_MESSAGE = "Value should be 'str', not '{value_type}'"
AVERAGE_SEQUENCE_ERROR_MESSAGE = (
    "Calculating the average is only possible from a sequence of numbers"
)

CSVData: typing.TypeAlias = list[dict[str, str | int | float]]

@dataclasses.dataclass
class FilterArgumentsData:
    """
    Represents a data class for storing arguments to filter functions
    of csv data.
    """

    column: str
    operator: str
    value: str | int | float

def parse_str_to_number(value: str) -> int | float | str:
    """Return and parse string for integer or float numbers."""
    if not isinstance(value, str):
        raise TypeError(PARSE_VALUE_TYPE_ERROR_MESSAGE.format(type(value)))
    try:
        return float(value) if "." in value else int(value)
    except (ValueError, TypeError):
        return value

def parse_filter_args(arg_string: str) -> FilterArgumentsData:
    """Return and parse column, operator and value from string."""
    parsed = re.split(r"([<>!=]=?)", arg_string)
    return FilterArgumentsData(
        column=parsed[0],
        operator=parsed[1],
        value=parse_str_to_number(parsed[2]),
    )

def avg(seq: typing.Sequence[int | float]) -> float:
    """Return average number in sequence."""
    if not all(isinstance(item, (int, float)) for item in seq):
        raise ValueError(AVERAGE_SEQUENCE_ERROR_MESSAGE)
    return round(sum(seq) / len(seq), 2)

def read_csv(path: pathlib.Path) -> CSVData | None:
    """Return csv file data as a list with dictionaries."""
    with open(path, "r", newline="") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read())
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        headers = next(reader)
        parsed_dicts = []
        for row in reader:
            parsed_row = {}
            for key, value in zip(headers, row):
                parsed_row[key] = parse_str_to_number(value)
            parsed_dicts.append(parsed_row)
    return parsed_dicts

def where(
    csv_data: CSVData,
    column: str,
    value: str | int | float,
    operator: str,
) -> CSVData  | None:
    """Return filtered csv date by condition."""
    filter_funcs = {
        "=": lambda row : row[column] == value,
        ">": lambda row : row[column] > value,
        "<": lambda row : row[column] < value,
    }
    if operator not in filter_funcs:
        raise ValueError(
            OPERATOR_ERROR_MESSAGE.format(
                operator,
                "Where",
            ),
        )
    return list(filter(filter_funcs[operator.lower()], csv_data))

def aggregate(
    csv_data: CSVData,
    column: str,
    value: str,
    operator: str = "=",
) -> CSVData | None:
    """Return and aggregate data from csv file."""
    if operator != "=":
        raise ValueError(
            OPERATOR_ERROR_MESSAGE.format(
                operator,
                "Aggregation",
            ),
        )
    agg_funcs = {
        "avg": avg,
        "max": max,
        "min": min,
    }
    numbers_to_aggregate = []
    for row in csv_data:
        numbers_to_aggregate.append(row.get(column))
    return [{column: agg_funcs[value.lower()](numbers_to_aggregate)}]
