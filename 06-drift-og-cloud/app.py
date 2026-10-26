"""Målinger-API'et fra dag 2, gjort klar til at køre i en container.

Nyt i forhold til dag 2:
  /health  bruges af Docker og Kubernetes til at se, om containeren lever
  /info    viser hvilken container der svarede, og hvilket miljø den kører i
"""

import os
import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Konfiguration kommer fra miljøvariabler, ikke fra koden. Så kan det samme
# image køre i DEV, TEST og PROD med forskellige indstillinger.
MILJOE = os.environ.get("MILJOE", "lokal")
VERSION = os.environ.get("VERSION", "1.0")

app = FastAPI(title="Målinger", description="Mini-API fra dag 2, i en container")


class NyMaaling(BaseModel):
    temperatur: float
    tryk: int


class Maaling(NyMaaling):
    id: int


maalinger = {
    1: Maaling(id=1, temperatur=21.3, tryk=1013),
    2: Maaling(id=2, temperatur=22.1, tryk=1009),
}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/info")
def info() -> dict:
    return {"container": socket.gethostname(), "miljoe": MILJOE, "version": VERSION}


@app.get("/maalinger")
def hent_alle() -> list[Maaling]:
    return list(maalinger.values())


@app.get("/maalinger/{maaling_id}")
def hent_en(maaling_id: int) -> Maaling:
    if maaling_id not in maalinger:
        raise HTTPException(status_code=404, detail=f"måling {maaling_id} findes ikke")
    return maalinger[maaling_id]


@app.post("/maalinger", status_code=201)
def opret(ny: NyMaaling) -> Maaling:
    ny_id = max(maalinger, default=0) + 1
    maaling = Maaling(id=ny_id, **ny.model_dump())
    maalinger[ny_id] = maaling
    return maaling
