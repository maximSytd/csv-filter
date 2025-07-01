import pathlib

import click
import tabulate

import utils

FILTER_EMPTY_RESULT_MESSAGE = "Filter got empty result"

@click.command()
@click.option(
    "-f",
    "--file",
    type=pathlib.Path,
    required=True,
    help="Path to csv file",
)
@click.option(
    "-w",
    "--where",
    type=str,
    help=(
        "Search row by format '<column><operator(</>/=)><value>', "
        "e.g. --where 'rating>1.8'"
    ),
)
@click.option(
    "-a",
    "--aggregate",
    type=str,
    help=(
        "Aggregation of rows by functions avg, min, max "
        "e.g. --aggregate 'cost=max'"),
)
def filter_csv(
    file: pathlib.Path | None,
    where: str | None,
    aggregate: str | None,
) -> None:
    """Return None and Filter data from CSV file based on passed conditions."""
    if file:
        arguments_data = {"where": where, "aggregate": aggregate}
        operations_map = {
            "where": utils.where,
            "aggregate": utils.aggregate,
        }
        resulted_data = utils.read_csv(file)
        for key, value in arguments_data.items():
            if not value:
                continue
            filter_args_data = utils.parse_filter_args(value)
            resulted_data = operations_map[key](
                csv_data=resulted_data,
                column=filter_args_data.column,
                value=filter_args_data.value,
                operator=filter_args_data.operator,
            )
        if resulted_data:
            click.echo(
                tabulate.tabulate(
                    resulted_data,
                    headers="keys",
                    tablefmt="psql",
                ),
            )
            return
        click.echo(
            tabulate.tabulate(
                (
                    (
                        FILTER_EMPTY_RESULT_MESSAGE,
                    ),
                ),
                tablefmt="psql",
            ),
        )
        return


if __name__ == "__main__":
    filter_csv()