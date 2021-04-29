

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED

from typing import List

class Logging:
    console = Console()

    @staticmethod
    def print_banner() -> None:
        """ print the ascii banner """
        Logging.console.print(
            '''[cyan]
 __                        ___            
(_ _|_ __ _ __  _  _  __    | |_  o __  _  _ 
__) |_ | (_|| |(_|(/_ |     | | | | | |(_|_> 
               __|                     __|

    [red]simple Web Internet of Things[/red]
    [red]coded by dropskid @ github.com/dropsql[/red]
    [green underline]inspired from dex @ github.com/wybiral/dex[/green underline]

[/cyan]         
            '''
        )


    @staticmethod
    def render_host_table(ip: str, port: int, headers_lines: List[str]) -> Table:
        """ render a table for results """

        table = Table(
            show_header=False,
            border_style='cyan',
            box=ROUNDED
        )

        table.add_row(
            ip, str(port), '\n'.join(headers_lines)
        )

        return table

    @staticmethod
    def print_info(message: str) -> None:
        """ embed a message as a info message """
        panel = Panel(
            message,
            box=ROUNDED,
            border_style='cyan'
        )

        Logging.console.print(panel)

    @staticmethod
    def print_failed(message: str) -> None:
        """ embed a message as a fail message """
        panel = Panel(
            message,
            box=ROUNDED,
            border_style='red'
        )

        Logging.console.print(panel)     

    @staticmethod
    def print_success(message: str) -> None:
        """ embed a message as a success message """
        panel = Panel(
            message,
            box=ROUNDED,
            border_style='green'
        )

        Logging.console.print(panel)