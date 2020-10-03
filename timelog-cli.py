import click
import timelog

@click.command()
@click.option('--file', help='file of the timelog', required=True)
@click.option('-v','--verbose', count=True)
@click.option('--format', help='Output format', default=['log'])
def parse_file(file, verbose: int, format: str):
    timelog.parse_file(file,
                       verbose=verbose,
                       format=format)

if __name__ == "__main__":
    parse_file()
