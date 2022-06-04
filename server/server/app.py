from importlib import metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
from pydantic import BaseModel
import httpx
from pathlib import Path
from typing import List

settings = Settings()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Track(BaseModel):
    species: str
    name: str


@app.get("/version")
def version():
    return {"version": metadata.version(__package__)}


@app.get("/api/v1/birdclef/listing")
async def listing() -> List[Track]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.static_host}/birdclef-2022-listing.json")
    data = resp.json()

    res = []
    for item in data:
        path = Path(item)
        if path.parts[0] != "train_audio":
            continue
        _, species, name = path.parts
        res.append(Track(species=species, name=name))
    return res
