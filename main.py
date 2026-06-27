#!/usr/bin/env python

import psycopg2
import psycopg2.extras
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Bibliotheks-API")

DB_CONFIG = {
    "dbname":   "bibliothek_oryanick",
    "user":     "oryanick",
    "password": "postgres",
    "host":     "localhost",
    "port":     5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ── Endpoint 1: list all books ──────────────────────────────────────────────

@app.get("/buecher")
def buecher_liste():
    conn   = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT isbn, titel, erscheinungsjahr, verlag, tagesgebuehr FROM buch ORDER BY titel")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── Endpoint 2: open loans with member and book details ─────────────────────

@app.get("/ausleihen/offen")
def offene_ausleihen():
    conn   = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT m.nachname,
               m.vorname,
               b.titel,
               a.ausleihe_datum,
               CURRENT_DATE - a.ausleihe_datum AS tage_ausgeliehen
        FROM   ausleihe  a
        JOIN   exemplar  e ON e.exemplar_id = a.exemplar_id
        JOIN   buch      b ON b.isbn        = e.isbn
        JOIN   mitglied  m ON m.mitglied_id = a.mitglied_id
        WHERE  a.rueckgabe_datum IS NULL
        ORDER BY tage_ausgeliehen DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── Endpoint 3: add a new member ─────────────────────────────────────────────

class NeuesMitglied(BaseModel):
    nachname:       str
    vorname:        str
    geburtsdatum:   str   # expected format: YYYY-MM-DD
    email:          str

@app.post("/mitglieder", status_code=201)
def mitglied_anlegen(mitglied: NeuesMitglied):
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO mitglied (nachname, vorname, geburtsdatum, email)
            VALUES (%s, %s, %s, %s)
            RETURNING mitglied_id
            """,
            (mitglied.nachname, mitglied.vorname, mitglied.geburtsdatum, mitglied.email),
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="E-Mail-Adresse bereits vergeben.")
    finally:
        cursor.close()
        conn.close()
    return {"mitglied_id": new_id}
