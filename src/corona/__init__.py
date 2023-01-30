import asyncclick as click

from corona.history import history_wrapped
from corona.today import today_wrapped


@click.group()
def cli():
    pass


cli.add_command(today_wrapped)
cli.add_command(history_wrapped)

if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
