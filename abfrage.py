#!/usr/bin/env python

import psycopg2
from rich.console import Console
from rich.table import Table

DB_CONFIG = {
    "dbname":   "bibliothek_oryanick",
    "user":     "oryanick",
    "password": "postgres",
    "host":     "localhost",
    "port":     5432,
}

def offene_ausleihen(cursor):
    cursor.execute("""
        SELECT m.nachname,
               m.vorname,
               b.titel,
               CURRENT_DATE - a.ausleihe_datum AS tage_ausgeliehen
        FROM   ausleihe  a
        JOIN   exemplar  e ON e.exemplar_id = a.exemplar_id
        JOIN   buch      b ON b.isbn        = e.isbn
        JOIN   mitglied  m ON m.mitglied_id = a.mitglied_id
        WHERE  a.rueckgabe_datum IS NULL
        ORDER BY tage_ausgeliehen DESC
    """)
    return cursor.fetchall()

def main():
    console = Console()

    conn   = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    rows = offene_ausleihen(cursor)

    table = Table(title="Offene Ausleihen")
    table.add_column("Nachname",          style="cyan")
    table.add_column("Vorname",           style="cyan")
    table.add_column("Titel",             style="green")
    table.add_column("Tage ausgeliehen",  style="yellow")

    for row in rows:
        table.add_row(row[0], row[1], row[2], str(row[3]))

    console.print(table)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
