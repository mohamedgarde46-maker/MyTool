from rich.console import Console

console = Console()

def show_menu():
    console.print("\n[bold cyan]Main Menu[/bold cyan]")
    console.print("[green]1.[/green] System Information")
    console.print("[green]2.[/green] Network Information")
    console.print("[green]3.[/green] File Manager")
    console.print("[green]4.[/green] Hash Generator")
    console.print("[green]5.[/green] About")
    console.print("[red]0.[/red] Exit")