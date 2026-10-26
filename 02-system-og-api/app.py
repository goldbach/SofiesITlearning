"""Det samme mini-API som server.py, nu med FastAPI.

Start:  fastapi dev app.py
Docs:   http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Målinger", description="Mini-API fra dag 2")


class NyMaaling(BaseModel):
    temperatur: float
    tryk: int


class Maaling(NyMaaling):
    id: int


maalinger = {
    1: Maaling(id=1, temperatur=21.3, tryk=1013),
    2: Maaling(id=2, temperatur=22.1, tryk=1009),
    3: Maaling(id=3, temperatur=19.8, tryk=1017),
}


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
