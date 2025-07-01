import pytest

import utils

@pytest.fixture(scope="module")
def csv_data_fixture() -> utils.CSVData:
    """Return csv-like fixture with list and dictionaries."""
    return [
        {
            'name': 'Alice',
            'age': 28,
            'department': 'Engineering',
            'salary': 85_000,
            'years_of_service': 3
        },
        {
            'name': 'Bob',
            'age': 35,
            'department': 'Marketing',
            'salary': 72_000.05,
            'years_of_service': 5
        },
        {
            'name': 'Charlie',
            'age': 42,
            'department': 'Engineering',
            'salary': 11_0000,
            'years_of_service': 10
        },
        {
            'name': 'Diana',
            'age': 31,
            'department': 'Sales',
            'salary': 68_000,
            'years_of_service': 4
        },
        {
            'name': 'Eve',
            'age': 24,
            'department': 'Engineering',
            'salary': 65_000,
            'years_of_service': 1
        },
    ]