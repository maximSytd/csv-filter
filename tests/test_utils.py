import csv
import pathlib

import pytest

import utils


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        ["just_a_string", "just_a_string"],
        ["99.99", 99.99],
        ["100", 100],
        ["0", 0],
        ["", ""],
    ],
)
def test_parse_str_to_number(value: str, expected: int | float | str):
    """Test parse_str_to_number functionality."""
    assert utils.parse_str_to_number(value) == expected


@pytest.mark.parametrize(
    ["value"],
    [
        [-1],
        [set()],
    ],
)
def test_invalid_parse_str_to_number(value: str):
    """Ensure invalid value raise exception."""
    with pytest.raises(TypeError) as exc_info:
        utils.parse_str_to_number(value)
    assert utils.PARSE_VALUE_TYPE_ERROR_MESSAGE.format(
        value_type=type(value),
    ) in str(exc_info.value)


@pytest.mark.parametrize(
    ["arg_string", "expected"],
    [
        [
            "column=value",
            utils.FilterArgumentsData(
                column="column",
                operator="=",
                value="value",
            ),
        ],
        [
            "column>value",
            utils.FilterArgumentsData(
                column="column",
                operator=">",
                value="value",
            ),
        ],
        [
            "column<value",
            utils.FilterArgumentsData(
                column="column",
                operator="<",
                value="value",
            ),
        ],
        [
            "column=10",
            utils.FilterArgumentsData(
                column="column",
                operator="=",
                value=10,
            ),
        ],
    ],
)
def test_parse_filter_args(
    arg_string: str,
    expected: utils.FilterArgumentsData,
):
    """Test parse_filter_args functionality."""
    assert utils.parse_filter_args(arg_string) == expected


@pytest.mark.parametrize(
    ["sequence", "expected"],
    [
        [[1,2,3], 2],
        [[-1,-2,-3], -2],
        [[0], 0],
    ],
)
def test_avg(sequence: list[int | float], expected: int | float):
    """Test avg functionality."""
    assert utils.avg(sequence) == expected

@pytest.mark.parametrize(
    ["sequence"],
    [
        [[]],
        [["some_string"]],
    ],
)
def test_invalid_avg(sequence: list[None | str]):
    """Ensure avg raise exception with incorrect sequence of numbers."""
    with pytest.raises(ValueError) as exc_info:
        utils.avg(sequence)
    assert utils.AVERAGE_SEQUENCE_ERROR_MESSAGE in str(exc_info.value)


def test_read_csv(csv_data_fixture: utils.CSVData, tmp_path: pathlib.Path):
    """Test read_csv functionality."""
    print(type(tmp_path))
    temp_csv_path = tmp_path / "employee.csv"
    with open(temp_csv_path, 'w', newline='', encoding="UTF-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=csv_data_fixture[0].keys(),
        )
        writer.writeheader()
        writer.writerows(csv_data_fixture)
    assert utils.read_csv(temp_csv_path) == csv_data_fixture


@pytest.mark.parametrize(
    ["column", "operator", "value", "expected"],
    [
        [
            "age",
            ">",
            31,
            [
                {
                    'name': 'Bob',
                    'age': 35,
                    'department': 'Marketing',
                    'salary': 72000.05,
                    'years_of_service': 5
                },
                {
                    'name': 'Charlie',
                    'age': 42,
                    'department': 'Engineering',
                    'salary': 110000,
                    'years_of_service': 10
                },
            ]
        ]
    ]
)
def test_where(
    column: str,
    operator: str,
    value: str | int | float,
    expected: utils.CSVData,
    csv_data_fixture: utils.CSVData,
):
    """Test where filter functionality."""
    assert utils.where(csv_data_fixture, column, value, operator) == expected


@pytest.mark.parametrize(
    ["operator"],
    [
        ["some_text"],
        ["!="],
        ["=="],
        [123],
    ]
)
def test_invalid_where(operator: str):
    """Ensure that invalid operator raise exception."""
    with pytest.raises(ValueError) as exc_info:
        utils.where(
            csv_data=[],
            column="column",
            value="value",
            operator=operator,
        )
    assert utils.OPERATOR_ERROR_MESSAGE.format(
        operator=operator,
        func="Where",
    ) in str(exc_info.value)


@pytest.mark.parametrize(
    ["column", "operator", "value", "expected"],
    [
        [
            "salary",
            "=",
            "avg",
            [
                {"salary": 80_000.01},
            ],
        ],
        [
            "salary",
            "=",
            "max",
            [
                {"salary": 110_000},
            ],
        ],
        [
            "salary",
            "=",
            "min",
            [
                {"salary": 65_000},
            ],
        ],
    ],
)
def test_aggregate(
    column: str,
    operator: str,
    value: str | int | float,
    expected: utils.CSVData,
    csv_data_fixture: utils.CSVData,
):
    """Test aggregate filter functionality."""
    assert utils.aggregate(
        csv_data_fixture,
        column,
        value,
        operator,
    ) == expected


@pytest.mark.parametrize(
    ["operator"],
    [
        ["some_text"],
        ["!="],
        ["=="],
        [123],
    ]
)
def test_invalid_aggregate(operator: str):
    """Ensure that invalid operator raise exception."""
    with pytest.raises(ValueError) as exc_info:
        utils.aggregate(
            csv_data=[],
            column="column",
            value="value",
            operator=operator,
        )
    assert utils.OPERATOR_ERROR_MESSAGE.format(
        operator=operator,
        func="Aggregation",
    ) in str(exc_info.value)