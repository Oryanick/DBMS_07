#!/usr/bin/env python

import math
from rich.console import Console
from rich.table import Table

def kreisflaeche(r):
    return math.pi * r ** 2


def main():
    console = Console()

    radius = 7
    flaeche = kreisflaeche(radius)

    table = Table(title="Ergebnisse")
    table.add_column("Größe", style="cyan")
    table.add_column("Wert", style="green")

    table.add_row("Radius", str(radius))
    table.add_row("Fläche", f"{flaeche:.4f}")
    table.add_row("Wurzel", f"{math.sqrt(radius):.4f}")

    console.print(table)


if __name__ == "__main__":
    main()
