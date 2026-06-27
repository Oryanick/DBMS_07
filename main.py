#!/usr/bin/env python

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"nachricht": "Bibliotheks-API läuft."}
