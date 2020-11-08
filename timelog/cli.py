import click
from timelog import parser

@click.command()
@click.option('--file', help='file of the timelog', required=True)
@click.option('-v','--verbose', count=True)
@click.option('--format', help='Output format', default=['log'])
def parse_file(file, verbose: int, format: str):
    parser.parse_file(file,
                       verbose=verbose,
                       format=format)

def main():
    parse_file()
