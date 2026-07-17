from pyfiglet import Figlet
from rich.console import Console

console = Console()

def show_banner():
    fig = Figlet(font="slant")
    console.print("[bold green]" + fig.renderText("GardeTool") + "[/bold green]")
    console.print("[cyan]==============================================[/cyan]")
    console.print("[yellow]Version : 1.0.0[/yellow]")
    console.print("[yellow]Author  : hama gardi[/yellow]")
    console.print("[cyan]==============================================[/cyan]")