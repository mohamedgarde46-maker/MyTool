import platform
import socket
import psutil
from rich.console import Console
from rich.table import Table

console = Console()

def system_info():
    table = Table(title="System Information")

    table.add_column("Item", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("OS", platform.system())
    table.add_row("Release", platform.release())
    table.add_row("Machine", platform.machine())
    table.add_row("Hostname", socket.gethostname())
    table.add_row("CPU Cores", str(psutil.cpu_count()))
    table.add_row(
        "RAM",
        f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
    )

    console.print(table)